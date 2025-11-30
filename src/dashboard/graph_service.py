"""
Graph Service for Dashboard
---------------------------
Handles data fetching from KuzuDB for visualization.
"""

import networkx as nx
from typing import Dict, List, Tuple
from pathlib import Path
from datetime import datetime
import kuzu
from src.utils.config import get_config

class GraphService:
    def __init__(self):
        self.config = get_config()
        self.db_path = self.config.elefante.graph_store.database_path
        # Open in READ_ONLY mode to avoid locking conflicts with the main MCP server
        # self.db = kuzu.Database(self.db_path, read_only=True)
        # self.conn = kuzu.Connection(self.db)
        pass

    def get_graph_data(
        self, 
        limit: int = 100, 
        node_types: List[str] = None,
        search_query: str = "",
        date_range: Tuple[datetime, datetime] = None
    ) -> Tuple[List[Dict], List[Dict]]:
        """
        Fetch nodes and edges from snapshot JSON with advanced filtering.
        """
        import json
        from datetime import datetime
        
        snapshot_path = Path("data/dashboard_snapshot.json")
        if not snapshot_path.exists():
            return [], [], ["Snapshot not found"]
            
        debug_log = []
            
        try:
            with open(snapshot_path, "r") as f:
                data = json.load(f)
                
            # 1. Deduplicate Nodes & Build Canonical Map
            canonical_map = {} # (name, type) -> canonical_id
            node_registry = {} # canonical_id -> node_data
            
            for n in data.get("nodes", []):
                key = (n["name"], n["type"])
                if key not in canonical_map:
                    canonical_map[key] = n["id"]
                    node_registry[n["id"]] = n
            
            # 2. Process Edges & Calculate Degree
            processed_edges = []
            node_degrees = {nid: 0 for nid in node_registry}
            
            # Re-build lookup
            id_map = {}
            for n in data.get("nodes", []):
                key = (n["name"], n["type"])
                if key in canonical_map:
                    id_map[n["id"]] = canonical_map[key]
            
            for e in data.get("edges", []):
                src = id_map.get(e["from"])
                dst = id_map.get(e["to"])
                if src and dst and src != dst:
                    processed_edges.append({
                        "from": src,
                        "to": dst,
                        "label": e["label"],
                        "title": e["label"]
                    })
                    node_degrees[src] = node_degrees.get(src, 0) + 1
                    node_degrees[dst] = node_degrees.get(dst, 0) + 1

            # 3. Finalize Nodes with Filters
            nodes = []
            msg = f"Starting node processing. Registry size: {len(node_registry)}"
            debug_log.append(msg)
            with open("rejection.log", "a") as logf: logf.write(msg + "\n")
            
            for nid, n in node_registry.items():
                # Parse properties if string
                if isinstance(n.get("properties"), str):
                    try:
                        n["properties"] = json.loads(n["properties"])
                    except:
                        n["properties"] = {}
                        

                # Type Filter
                if node_types and n["type"] not in node_types:
                    msg = f"Rejected {n.get('name', 'Unknown')} (ID: {nid}) due to type filter: {n['type']} not in {node_types}"
                    debug_log.append(msg)
                    continue
                
                # Search Filter
                if search_query:
                    query = search_query.lower()
                    content = (n["name"] + " " + n.get("description", "")).lower()
                    if query not in content:
                        msg = f"Rejected {n.get('name', 'Unknown')} (ID: {nid}) due to search query: '{search_query}' not in '{content}'"
                        debug_log.append(msg)
                        continue
                        
                # Date Filter
                if date_range:
                    try:
                        created_at = datetime.fromisoformat(n.get("created_at", ""))
                        # Handle naive/aware comparison by ignoring timezone for simplicity in this view
                        if created_at.replace(tzinfo=None) < date_range[0].replace(tzinfo=None) or \
                           created_at.replace(tzinfo=None) > date_range[1].replace(tzinfo=None):
                            msg = f"Rejected {n.get('name', 'Unknown')} (ID: {nid}) due to date filter: {created_at.replace(tzinfo=None)} not in [{date_range[0].replace(tzinfo=None)}, {date_range[1].replace(tzinfo=None)}]"
                            debug_log.append(msg)
                            continue
                    except Exception as e:
                        debug_log.append(f"Date parsing error for node {n.get('name', 'Unknown')} (ID: {nid}): {e}. Keeping node.")
                        pass # Keep if date parsing fails
                
                # Smart Labeling
                label = n["name"]
                if n["type"] == "memory":
                    desc = n.get("description", "")
                    label = (desc[:30] + '...') if len(desc) > 30 else desc
                    if not label: label = "Memory"
                
                # Dynamic Sizing
                degree = node_degrees.get(nid, 0)
                size = min(50, 10 + (degree * 2))
                
                # Color Palette
                color_map = {
                    "person": "#E6E6FA",      # Lavender (User)
                    "company": "#FF8C00",     # DarkOrange (KnownStorm)
                    "project": "#FF6347",     # Tomato (Elefante, AI Tutor)
                    "goal": "#FFD700",        # Gold (High Valuation Exit)
                    "concept": "#BA55D3",     # MediumOrchid
                    "technology": "#00FA9A",  # MediumSpringGreen
                    "memory": "#4682B4",      # SteelBlue
                    "rule": "#DC143C",        # Crimson (Protocols)
                    "protocol": "#DC143C",    # Crimson
                    "metric": "#00FF00",      # Lime (Valuation)
                    "role": "#DA70D6",        # Orchid (Builder)
                    "location": "#20B2AA",    # LightSeaGreen
                    "event": "#F08080"        # LightCoral
                }
                color = color_map.get(n["type"].lower(), "#97C2FC") # Default Blue
                
                # Extract Cognitive Data
                cognitive_data = {
                    "intent": n.get("intent") or n.get("properties", {}).get("cognitive_analysis", {}).get("intent"),
                    "mood": n.get("emotional_context", {}).get("mood") or n.get("properties", {}).get("cognitive_analysis", {}).get("emotional_context", {}).get("mood"),
                    "insight": n.get("strategic_insight") or n.get("properties", {}).get("cognitive_analysis", {}).get("strategic_insight"),
                    "importance": n.get("importance") or n.get("properties", {}).get("importance", 1)
                }

                nodes.append({
                    "id": nid,
                    "label": label,
                    "group": n["type"],
                    "title": f"Type: {n['type']}\nName: {n['name']}\n{n.get('description', '')}",
                    "value": size,
                    "color": color,
                    "full_data": n, # Pass full data for inspector
                    "cognitive": cognitive_data # Pass extracted cognitive data
                })

            # 4. Finalize Edges
            edges = []
            visible_ids = {n["id"] for n in nodes}
            for e in processed_edges:
                if e["from"] in visible_ids and e["to"] in visible_ids:
                    edges.append(e)
                else:
                    # debug_log.append(f"Rejected edge ...")
                    pass
                    
            # DUMMY NODE REMOVED
            
            return nodes, edges, debug_log # Return debug_log
            
        except Exception as e:
            print(f"Error in get_graph_data: {e}")
            msg = f"Critical error in get_graph_data: {e}"
            debug_log.append(msg)
            return [], [], debug_log # Return debug_log even on error

    def get_date_range(self) -> Tuple[datetime, datetime]:
        """Get min and max dates from snapshot"""
        import json
        from datetime import datetime, timedelta
        
        snapshot_path = Path("data/dashboard_snapshot.json")
        if not snapshot_path.exists():
            return datetime.now(), datetime.now()
            
        try:
            with open(snapshot_path, "r") as f:
                data = json.load(f)
            
            dates = []
            for n in data.get("nodes", []):
                if "created_at" in n:
                    try:
                        dates.append(datetime.fromisoformat(n["created_at"]))
                    except:
                        pass
            
            if not dates:
                return datetime.now() - timedelta(days=1), datetime.now()
                
            return min(dates), max(dates)
        except:
            return datetime.now(), datetime.now()
            


    def get_stats(self) -> Dict[str, int]:
        """Get basic graph statistics from snapshot"""
        import json
        snapshot_path = Path("data/dashboard_snapshot.json")
        if not snapshot_path.exists():
            return {"nodes": 0, "edges": 0}
            
        try:
            with open(snapshot_path, "r") as f:
                data = json.load(f)
            return {
                "nodes": len(data.get("nodes", [])),
                "edges": len(data.get("edges", []))
            }
        except:
            return {"nodes": 0, "edges": 0}
