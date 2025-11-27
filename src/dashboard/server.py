import os
import threading
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Dict, Any, List, Optional

from src.core.graph_store import get_graph_store
from src.utils.logger import get_logger
from src.utils.config import get_config

logger = get_logger(__name__)

app = FastAPI(title="Elefante Knowledge Garden")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Endpoints
@app.get("/api/graph")
async def get_graph(limit: int = 1000, space: Optional[str] = None):
    """
    Fetch graph data (nodes and edges) for visualization.
    """
    try:
        graph_store = get_graph_store()
        
        # Base query for nodes
        # We fetch entities and memories
        # TODO: Implement space filtering when 'space' property is added to schema
        
        # Fetch Nodes
        nodes_cypher = f"""
        MATCH (n:Entity)
        RETURN n
        LIMIT {limit}
        """
        node_results = await graph_store.execute_query(nodes_cypher)
        
        nodes = []
        node_ids = set()
        
        for row in node_results:
            entity = row.get("n")
            if entity:
                node_id = str(entity.id)
                node_ids.add(node_id)
                
                # Determine visual type
                visual_type = "memory" if entity.type.value == "memory" else "entity"
                if entity.type.value == "session":
                    visual_type = "session"
                
                nodes.append({
                    "id": node_id,
                    "label": entity.name,
                    "type": visual_type,
                    "entityType": entity.type.value,
                    "properties": entity.properties
                })
        
        # Fetch Relationships
        # Only fetch relationships where both nodes are in our node set
        edges_cypher = f"""
        MATCH (a:Entity)-[r]->(b:Entity)
        RETURN a.id, b.id, type(r), r
        LIMIT {limit * 2}
        """
        edge_results = await graph_store.execute_query(edges_cypher)
        
        edges = []
        for row in edge_results:
            source_id = row.get("a.id")
            target_id = row.get("b.id")
            rel_type = row.get("type(r)")
            
            # Kuzu might return IDs as strings or other types, ensure consistency
            if str(source_id) in node_ids and str(target_id) in node_ids:
                edges.append({
                    "source": str(source_id),
                    "target": str(target_id),
                    "type": rel_type,
                    "properties": row.get("r", {})
                })
                
        return {
            "nodes": nodes,
            "edges": edges,
            "stats": {
                "node_count": len(nodes),
                "edge_count": len(edges)
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to fetch graph data: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats():
    """Get system statistics"""
    try:
        from src.core.orchestrator import get_orchestrator
        orchestrator = get_orchestrator()
        return await orchestrator.get_stats()
    except Exception as e:
        logger.error(f"Failed to fetch stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Serve Frontend
# We assume the frontend is built to src/dashboard/ui/dist
frontend_path = os.path.join(os.path.dirname(__file__), "ui", "dist")

if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")
else:
    @app.get("/")
    def index():
        return {"message": "Elefante Dashboard API is running. Frontend not found (run 'npm run build' in src/dashboard/ui)."}

def start_server(host: str = "127.0.0.1", port: int = 8000):
    """Start the dashboard server"""
    uvicorn.run(app, host=host, port=port, log_level="info")

def serve_dashboard_in_thread(host: str = "127.0.0.1", port: int = 8000):
    """Start the dashboard server in a background thread"""
    thread = threading.Thread(target=start_server, args=(host, port), daemon=True)
    thread.start()
    return thread

if __name__ == "__main__":
    start_server()
