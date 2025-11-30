import asyncio
import sys
import os
import json
from datetime import datetime

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.graph_store import GraphStore
from src.utils.config import get_config

async def main():
    print("🐘 Connecting to KuzuDB...")
    config = get_config()
    # Initialize GraphStore directly to avoid Orchestrator overhead
    store = GraphStore(config.elefante.graph_store.database_path)
    
    # Fetch all nodes
    print("Fetching nodes...")
    # Note: Kuzu returns all properties as a dictionary in the result
    nodes_query = "MATCH (n:Entity) RETURN n"
    nodes_result = await store.execute_query(nodes_query)
    
    nodes = []
    for row in nodes_result:
        # row is a dict with column names, e.g. {'n': {...}}
        entity = row.get('n')
        if entity:
            # Handle Kuzu Node object or dict
            props = {}
            if hasattr(entity, 'get'):
                # It's likely a dict or dict-like
                props = dict(entity)
                # Clean up internal Kuzu fields
                props = {k: v for k, v in props.items() if not k.startswith('_')}
            
            # Parse 'properties' JSON string if it exists
            if 'properties' in props and isinstance(props['properties'], str):
                try:
                    extra_props = json.loads(props['properties'])
                    props.update(extra_props)
                except:
                    pass
            
            nodes.append(props)

    print(f"Found {len(nodes)} nodes.")

    # Fetch all edges
    print("Fetching edges...")
    # We need to get source and target IDs. 
    # MATCH (a)-[r]->(b) RETURN a.id, b.id, label(r)
    edges_query = "MATCH (a)-[r]->(b) RETURN a.id, b.id, label(r)"
    edges_result = await store.execute_query(edges_query)
    
    edges = []
    for row in edges_result:
        # row keys depend on the return clause
        # Kuzu python API might return them as 'a.id', 'b.id', 'label(r)' or similar
        # Let's inspect the first row if needed, but usually it matches the return names
        
        # GraphStore.execute_query returns a list of dicts
        # The keys will be the variable names in RETURN
        src = row.get('a.id')
        dst = row.get('b.id')
        lbl = row.get('label(r)')
        
        if src and dst:
            edges.append({
                "from": src,
                "to": dst,
                "label": lbl or "RELATED"
            })

    print(f"Found {len(edges)} edges.")

    # Save to JSON
    snapshot = {
        "generated_at": datetime.utcnow().isoformat(),
        "nodes": nodes,
        "edges": edges
    }
    
    output_path = "data/dashboard_snapshot.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    class DateTimeEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()
            return super().default(o)

    with open(output_path, "w") as f:
        json.dump(snapshot, f, indent=2, cls=DateTimeEncoder)
        
    print(f"✅ Dashboard snapshot saved to {output_path}")

if __name__ == "__main__":
    asyncio.run(main())
