# Contributing to Elefante

Thank you for your interest in contributing to Elefante! This document provides guidelines and best practices for contributing to this project.

##  Code Quality Standards

### Clean Environment Philosophy

**CRITICAL**: This project maintains an extremely clean and organized codebase. Please adhere to these principles:

-  **NO** leftover test files in the repository
-  **NO** temporary files or artifacts
-  **NO** unnecessary dependencies
-  **YES** to clean, organized code structure
-  **YES** to proper cleanup after testing
-  **YES** to minimal, purposeful files

### Before Committing

1. **Remove test artifacts**: Delete any test data, logs, or temporary files
2. **Clean up imports**: Remove unused imports
3. **Format code**: Use consistent formatting (Black for Python)
4. **Update documentation**: Keep docs in sync with code changes
5. **Test thoroughly**: Run all tests before committing

##  Project Structure

```
Elefante/
├── src/                    # Source code
│   ├── core/              # Core functionality
│   ├── models/            # Data models
│   ├── mcp/               # MCP server
│   ├── dashboard/         # React dashboard
│   └── utils/             # Utilities
├── scripts/               # Utility scripts
├── examples/              # Example usage scripts
├── docs/                  # Documentation
│   ├── technical/         # Production reference docs
│   ├── debug/             # Neural registers & compendiums
│   ├── planning/          # Roadmaps
│   └── archive/           # Historical docs
├── tests/                 # Test files
├── README.md              # Main documentation
├── CHANGELOG.md           # Version history & release notes
└── requirements.txt       # Dependencies
```

##  Development Workflow

### 1. Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/elefante.git
cd elefante

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .  # Install in editable mode
```

### 2. Make Changes

- Create a feature branch: `git checkout -b feature/your-feature-name`
- Make your changes
- Test thoroughly
- **Clean up any test files or artifacts**

### 3. Testing

```bash
# Run health check
python scripts/health_check.py

# Run end-to-end tests
python scripts/test_end_to_end.py

# Run examples (optional)
python examples/test_real_memories.py
```

### 4. Commit Guidelines

```bash
# Stage only necessary files
git add src/ docs/ README.md

# Write clear commit messages
git commit -m "feat: add new memory search feature"
git commit -m "fix: resolve Kuzu relationship bug"
git commit -m "docs: update API documentation"
```

**Commit Message Format**:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Test additions/changes
- `chore:` Maintenance tasks

### 5. Before Pushing

**MANDATORY CHECKLIST**:
- [ ] All tests pass
- [ ] No test data in `data/` directory
- [ ] No logs in `logs/` directory
- [ ] No `__pycache__` directories
- [ ] No `.pyc` files
- [ ] Documentation is updated
- [ ] Code is formatted
- [ ] No unnecessary files

```bash
# Clean up
rm -rf data/ logs/ __pycache__/
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -delete

# Verify clean state
git status

# Push
git push origin feature/your-feature-name
```

##  Code Style

### Python

- Follow PEP 8
- Use type hints
- Write docstrings for all functions/classes
- Keep functions small and focused
- Use meaningful variable names

```python
def search_memories(
    query: str,
    mode: QueryMode = QueryMode.SEMANTIC,
    limit: int = 10
) -> List[SearchResult]:
    """
    Search memories using specified mode.
    
    Args:
        query: Search query string
        mode: Search mode (semantic, graph, or hybrid)
        limit: Maximum number of results
        
    Returns:
        List of search results with scores
    """
    # Implementation
```

### Documentation

- Keep README.md up to date
- Document all public APIs
- Include examples for complex features
- Update CHANGELOG.md for significant changes

##  Reporting Issues

When reporting issues, include:

1. **Description**: Clear description of the problem
2. **Steps to Reproduce**: Exact steps to reproduce the issue
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**: OS, Python version, dependencies
6. **Logs**: Relevant error messages or logs

##  Feature Requests

For feature requests:

1. **Use Case**: Describe the use case
2. **Proposed Solution**: How you envision it working
3. **Alternatives**: Other approaches you've considered
4. **Impact**: Who would benefit from this feature

##  License

By contributing, you agree that your contributions will be licensed under the MIT License.

##  Thank You!

Your contributions help make Elefante better for everyone. We appreciate your effort to maintain code quality and cleanliness!

---

**Remember**: A clean codebase is a happy codebase! 