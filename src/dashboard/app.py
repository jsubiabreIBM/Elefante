"""
Elefante Dashboard ("The Chart")
--------------------------------
Visual control plane for the memory graph.
Run with: streamlit run src/dashboard/app.py
"""

import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import networkx as nx
from pathlib import Path
import sys
import os

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.dashboard.graph_service import GraphService
from src.models.entity import EntityType

# Page Config
st.set_page_config(
    page_title="Elefante Brain",
    page_icon="🐘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Premium" feel
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stSidebar {
        background-color: #262730;
    }
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

def init_service():
    if 'graph_service' not in st.session_state:
        st.session_state.graph_service = GraphService()
    return st.session_state.graph_service

def render_graph(nodes, edges):
    """Render PyVis graph"""
    net = Network(height="750px", width="100%", bgcolor="#0E1117", font_color="white")
    
    # Add nodes
    for node in nodes:
        net.add_node(
            node["id"], 
            label=node["label"], 
            title=node["title"],
            group=node["group"],
            value=node["value"],
            color=node.get("color", "#97C2FC")
        )
        
    # Add edges
    for edge in edges:
        net.add_edge(
            edge["from"], 
            edge["to"], 
            title=edge["label"],
            label=edge["label"]
        )
        
    # Physics options for "Organic" feel
    net.set_options("""
    var options = {
      "nodes": {
        "font": {
          "size": 16,
          "face": "Inter"
        },
        "borderWidth": 2
      },
      "edges": {
        "color": {
          "inherit": true
        },
        "smooth": false
      },
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 100,
          "springConstant": 0.08
        },
        "minVelocity": 0.75,
        "solver": "forceAtlas2Based"
      }
    }
    """)
    
    # Save to temporary HTML file
    path = Path("tmp_graph.html")
    net.save_graph(str(path))
    
    # Read HTML file
    try:
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        return html
    finally:
        # Cleanup
        if path.exists():
            path.unlink()

def main():
    service = init_service()
    
    # Sidebar - Filters
    st.sidebar.title("🐘 Elefante Brain")
    st.sidebar.markdown("---")
    
    # 1. Search
    st.sidebar.subheader("🔍 Search")
    search_query = st.sidebar.text_input("Find nodes...", placeholder="e.g., 'python' or 'memory'")
    
    # 2. Timeline
    st.sidebar.subheader("⏳ Timeline")
    min_date, max_date = service.get_date_range()
    # Ensure distinct range for slider
    if min_date.date() >= max_date.date():
        from datetime import timedelta
        min_date = min_date - timedelta(days=1)
        
    date_range = st.sidebar.slider(
        "Created At",
        min_value=min_date.date(),
        max_value=max_date.date(),
        value=(min_date.date(), max_date.date())
    )
    
    # 3. Angle Selector
    st.sidebar.subheader("📐 Angle Selector")
    all_types = [t.value for t in EntityType]
    selected_types = st.sidebar.multiselect(
        "Filter Entity Types",
        options=all_types,
        default=["person", "project", "company", "goal", "concept", "technology", "rule", "protocol", "metric", "role", "memory"]
    )
    
    st.sidebar.markdown("---")
    
    # Stats
    stats = service.get_stats()
    c1, c2 = st.sidebar.columns(2)
    c1.metric("Nodes", stats.get("nodes", 0))
    c2.metric("Edges", stats.get("edges", 0))
    
    # Main Area
    st.title("Visual Control Plane")
    
    # Fetch Data with Filters
    # Convert date_range (date) to datetime for service
    from datetime import datetime, time
    start_dt = datetime.combine(date_range[0], time.min)
    end_dt = datetime.combine(date_range[1], time.max)
    
    nodes, edges, debug_log = service.get_graph_data(
        node_types=selected_types,
        search_query=search_query,
        date_range=(start_dt, end_dt)
    )
    
    # DEBUG INFO
    with st.sidebar.expander("🐞 Debug Info", expanded=False):
        st.write(f"Nodes Found: {len(nodes)}")
        st.write(f"Raw Min/Max: {min_date} / {max_date}")
        st.write(f"Filter Range: {start_dt} - {end_dt}")
        st.write(f"Selected Types: {len(selected_types)}")
        if debug_log:
            st.write("### Rejection Log")
            for log in debug_log[:10]: # Show first 10
                st.text(log)
        if nodes:
            st.write(f"Sample Node: {nodes[0]['label']} ({nodes[0]['group']})")
    
    # Node Inspector (Workaround for limited interactivity)
    st.sidebar.markdown("---")
    st.sidebar.subheader("🧐 Inspector")
    
    if nodes:
        node_options = {n["label"]: n for n in nodes}
        selected_label = st.sidebar.selectbox("Select Node to Inspect", options=node_options.keys())
        
        if selected_label:
            selected_node = node_options[selected_label]
            full_data = selected_node.get("full_data", {})
            
            # Cognitive Card UI
            with st.sidebar.container():
                # Header
                st.sidebar.markdown(f"## {selected_node['label']}")
                st.sidebar.caption(f"**Type**: {selected_node['group'].title()} | **ID**: `{selected_node['id'][:8]}...`")
                
                # Cognitive Badges
                cog = selected_node.get("cognitive", {})
                cols = st.sidebar.columns(2)
                if cog.get("intent"):
                    cols[0].markdown(f"**Intent**: `{cog['intent']}`")
                if cog.get("mood"):
                    cols[1].markdown(f"**Mood**: `{cog['mood']}`")
                
                st.sidebar.markdown("---")
                
                # Strategic Insight (The "So What")
                if cog.get("insight"):
                    st.sidebar.info(f"**💡 Strategic Insight**\n\n{cog['insight']}")
                
                # Description / Summary
                desc = full_data.get("description") or full_data.get("properties", {}).get("content")
                if desc:
                    st.sidebar.markdown("### 📝 Summary")
                    st.sidebar.markdown(desc)
                
                # Raw Metadata (Collapsible)
                with st.sidebar.expander("🔍 Raw Data"):
                    st.json(full_data)
    
    if not nodes:
        st.warning("No nodes found. Try adjusting filters or adding memories.")
    else:
        # Render Graph
        html_data = render_graph(nodes, edges)
        components.html(html_data, height=800)
        
    # Data Panel (Simple Table for now)
    st.markdown("### 🧠 Memory Stream")
    if nodes:
        # Flatten data for table
        table_data = []
        for n in nodes:
            d = n.get("full_data", {})
            table_data.append({
                "Name": n["label"],
                "Type": n["group"],
                "Description": d.get("description", ""),
                "Created": d.get("created_at", "")
            })
        st.dataframe(table_data, use_container_width=True)

if __name__ == "__main__":
    main()
