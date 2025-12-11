"""
Elefante Mode Manager (v1.0.1)

Handles multi-IDE safety by providing:
- Lock detection and cleanup
- Graceful resource release
- Mode switching (ON/OFF)
- Database corruption prevention

When ELEFANTE_MODE=N (OFF):
  - Server responds with graceful "disabled" messages
  - All locks are released
  - No database connections held
  - Safe for other IDEs to access the data

When ELEFANTE_MODE=Y (ON):
  - Full memory system active
  - Protocol enforcement enabled
  - Databases locked for exclusive access
"""

import os
import fcntl
import signal
import atexit
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
from contextlib import contextmanager

from src.utils.config import get_config, DATA_DIR, ELEFANTE_HOME
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Lock file paths
LOCK_DIR = ELEFANTE_HOME / "locks"
MASTER_LOCK_FILE = LOCK_DIR / "elefante.lock"
CHROMA_LOCK_FILE = LOCK_DIR / "chroma.lock"
KUZU_LOCK_FILE = LOCK_DIR / "kuzu.lock"


class ElefanteModeManager:
    """
    Singleton manager for Elefante Mode state and lock management.
    
    Ensures only one IDE has active write access to the databases
    while allowing graceful degradation when another IDE needs access.
    """
    
    _instance: Optional['ElefanteModeManager'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self._enabled = False
        self._lock_files: Dict[str, int] = {}  # path -> file descriptor
        self._orchestrator_ref = None
        self._startup_time = datetime.utcnow()
        
        # Ensure lock directory exists
        LOCK_DIR.mkdir(parents=True, exist_ok=True)
        
        # Register cleanup on exit
        atexit.register(self._cleanup_on_exit)
        
        # Handle signals for graceful shutdown
        for sig in (signal.SIGTERM, signal.SIGINT):
            try:
                signal.signal(sig, self._signal_handler)
            except (ValueError, OSError):
                pass  # Signal handling may not work in all contexts
        
        logger.info("ElefanteModeManager initialized", startup_time=self._startup_time.isoformat())
    
    @property
    def is_enabled(self) -> bool:
        """Check if Elefante Mode is currently enabled."""
        return self._enabled
    
    @property
    def status(self) -> Dict[str, Any]:
        """Get current status of Elefante Mode."""
        return {
            "enabled": self._enabled,
            "startup_time": self._startup_time.isoformat(),
            "locks_held": list(self._lock_files.keys()),
            "lock_count": len(self._lock_files),
            "data_dir": str(DATA_DIR),
            "pid": os.getpid()
        }
    
    def _signal_handler(self, signum, frame):
        """Handle termination signals gracefully."""
        logger.info(f"Received signal {signum}, cleaning up...")
        self.disable()
        # Re-raise to allow normal termination
        signal.signal(signum, signal.SIG_DFL)
        os.kill(os.getpid(), signum)
    
    def _cleanup_on_exit(self):
        """Cleanup handler for normal exit."""
        if self._enabled:
            logger.info("Cleaning up on exit...")
            self.disable()
    
    def _acquire_lock(self, lock_path: Path, timeout: int = 5) -> bool:
        """
        Attempt to acquire a file lock.
        
        Args:
            lock_path: Path to lock file
            timeout: Max seconds to wait (not used with non-blocking)
            
        Returns:
            True if lock acquired, False otherwise
        """
        try:
            # Create lock file if it doesn't exist
            lock_path.parent.mkdir(parents=True, exist_ok=True)
            
            fd = os.open(str(lock_path), os.O_RDWR | os.O_CREAT)
            
            # Try non-blocking exclusive lock
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                
                # Write PID and timestamp to lock file
                os.ftruncate(fd, 0)
                os.lseek(fd, 0, os.SEEK_SET)
                lock_info = f"{os.getpid()}|{datetime.utcnow().isoformat()}\n"
                os.write(fd, lock_info.encode())
                
                self._lock_files[str(lock_path)] = fd
                logger.info(f"Lock acquired: {lock_path}")
                return True
                
            except (IOError, OSError) as e:
                # Lock is held by another process
                os.close(fd)
                
                # Try to read who holds the lock
                try:
                    with open(lock_path, 'r') as f:
                        holder_info = f.read().strip()
                    logger.warning(f"Lock held by another process: {lock_path} -> {holder_info}")
                except:
                    logger.warning(f"Lock held by another process: {lock_path}")
                
                return False
                
        except Exception as e:
            logger.error(f"Failed to acquire lock {lock_path}: {e}")
            return False
    
    def _release_lock(self, lock_path: Path) -> bool:
        """
        Release a file lock.
        
        Args:
            lock_path: Path to lock file
            
        Returns:
            True if released, False if not held
        """
        path_str = str(lock_path)
        
        if path_str not in self._lock_files:
            return False
        
        try:
            fd = self._lock_files[path_str]
            fcntl.flock(fd, fcntl.LOCK_UN)
            os.close(fd)
            del self._lock_files[path_str]
            
            # Clear lock file content
            try:
                lock_path.write_text("")
            except:
                pass
            
            logger.info(f"Lock released: {lock_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to release lock {lock_path}: {e}")
            return False
    
    def _release_all_locks(self):
        """Release all held locks."""
        for lock_path in list(self._lock_files.keys()):
            self._release_lock(Path(lock_path))
    
    def check_locks(self) -> Dict[str, Any]:
        """
        Check the status of all lock files.
        
        Returns:
            Dict with lock status for each database
        """
        lock_status = {}
        
        for name, path in [
            ("master", MASTER_LOCK_FILE),
            ("chroma", CHROMA_LOCK_FILE),
            ("kuzu", KUZU_LOCK_FILE)
        ]:
            status = {
                "path": str(path),
                "exists": path.exists(),
                "held_by_us": str(path) in self._lock_files,
                "holder_info": None
            }
            
            if path.exists() and not status["held_by_us"]:
                try:
                    content = path.read_text().strip()
                    if content:
                        parts = content.split("|")
                        status["holder_info"] = {
                            "pid": parts[0] if len(parts) > 0 else "unknown",
                            "timestamp": parts[1] if len(parts) > 1 else "unknown"
                        }
                except:
                    pass
            
            lock_status[name] = status
        
        return lock_status
    
    def enable(self, force: bool = False) -> Dict[str, Any]:
        """
        Enable Elefante Mode.
        
        Acquires all necessary locks and prepares the system for operation.
        
        Args:
            force: If True, attempt to break stale locks
            
        Returns:
            Status dict with success/failure info
        """
        if self._enabled:
            return {
                "success": True,
                "message": "Elefante Mode already enabled",
                "status": self.status
            }
        
        logger.info("Enabling Elefante Mode...")
        
        # Get config
        config = get_config()
        timeout = config.elefante.elefante_mode.lock_timeout_seconds
        
        # Acquire locks in order
        locks_to_acquire = [
            ("master", MASTER_LOCK_FILE),
            ("chroma", CHROMA_LOCK_FILE),
            ("kuzu", KUZU_LOCK_FILE)
        ]
        
        acquired = []
        failed = []
        
        for name, path in locks_to_acquire:
            if self._acquire_lock(path, timeout):
                acquired.append(name)
            else:
                failed.append(name)
        
        if failed:
            # Rollback acquired locks
            for name in acquired:
                for lock_name, lock_path in locks_to_acquire:
                    if lock_name == name:
                        self._release_lock(lock_path)
            
            return {
                "success": False,
                "message": f"Failed to acquire locks: {failed}. Another IDE may be using Elefante.",
                "acquired": acquired,
                "failed": failed,
                "lock_status": self.check_locks()
            }
        
        self._enabled = True
        logger.info("Elefante Mode ENABLED")
        
        return {
            "success": True,
            "message": "Elefante Mode enabled successfully",
            "status": self.status
        }
    
    def disable(self) -> Dict[str, Any]:
        """
        Disable Elefante Mode.
        
        Releases all locks and cleans up resources.
        
        Returns:
            Status dict
        """
        if not self._enabled:
            return {
                "success": True,
                "message": "Elefante Mode already disabled",
                "status": self.status
            }
        
        logger.info("Disabling Elefante Mode...")
        
        config = get_config()
        
        # Cleanup orchestrator if configured
        if config.elefante.elefante_mode.cleanup_on_disable:
            if self._orchestrator_ref is not None:
                try:
                    # Close database connections
                    # The orchestrator doesn't have explicit close methods,
                    # but we can clear references to allow GC
                    self._orchestrator_ref = None
                    logger.info("Orchestrator reference cleared")
                except Exception as e:
                    logger.warning(f"Error cleaning up orchestrator: {e}")
        
        # Release all locks
        self._release_all_locks()
        
        self._enabled = False
        logger.info("Elefante Mode DISABLED")
        
        return {
            "success": True,
            "message": "Elefante Mode disabled. All locks released.",
            "status": self.status
        }
    
    def set_orchestrator_ref(self, orchestrator):
        """Store reference to orchestrator for cleanup."""
        self._orchestrator_ref = orchestrator
    
    def get_disabled_response(self, tool_name: str) -> Dict[str, Any]:
        """
        Generate a graceful disabled response for when mode is OFF.
        
        Args:
            tool_name: Name of the tool that was called
            
        Returns:
            Response dict explaining the disabled state
        """
        return {
            "success": False,
            "elefante_mode": "disabled",
            "message": f"Elefante Mode is OFF. Tool '{tool_name}' is not available.",
            "reason": "Multi-IDE safety mode - another IDE may be using the databases.",
            "action_required": "Call 'enableElefante' tool to activate Elefante Mode.",
            "lock_status": self.check_locks(),
            "help": [
                "1. Ensure no other IDE is using Elefante databases",
                "2. Call enableElefante tool to acquire locks",
                "3. If locks are stale, restart the other IDE or manually delete lock files"
            ]
        }


# Global instance
_mode_manager: Optional[ElefanteModeManager] = None


def get_mode_manager() -> ElefanteModeManager:
    """Get the global ElefanteModeManager instance."""
    global _mode_manager
    if _mode_manager is None:
        _mode_manager = ElefanteModeManager()
    return _mode_manager


def is_elefante_enabled() -> bool:
    """Quick check if Elefante Mode is enabled."""
    return get_mode_manager().is_enabled


def require_elefante_mode(func):
    """
    Decorator that requires Elefante Mode to be enabled.
    
    If mode is disabled, returns a graceful disabled response instead
    of executing the function.
    """
    async def wrapper(*args, **kwargs):
        manager = get_mode_manager()
        if not manager.is_enabled:
            # Extract tool name from function name or kwargs
            tool_name = kwargs.get('tool_name', func.__name__)
            return manager.get_disabled_response(tool_name)
        return await func(*args, **kwargs)
    
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper
