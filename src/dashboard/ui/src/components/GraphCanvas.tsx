import { useRef, useEffect, useState } from 'react';


interface Node {
  id: string;
  label: string;
  type: 'memory' | 'entity' | 'session';
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
}

interface Edge {
  source: string;
  target: string;
  type: string;
}

interface GraphData {
  nodes: any[];
  edges: any[];
}

interface GraphCanvasProps {
  space: string;
}

const GraphCanvas: React.FC<GraphCanvasProps> = ({ space }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [data, setData] = useState<GraphData>({ nodes: [], edges: [] });
  const nodesRef = useRef<Node[]>([]);
  const edgesRef = useRef<Edge[]>([]);
  const requestRef = useRef<number>();
  
  // Interaction state
  const [hoveredNode, setHoveredNode] = useState<Node | null>(null);
  const draggingNode = useRef<Node | null>(null);
  const offset = useRef({ x: 0, y: 0 }); // Pan offset
  const scale = useRef(1); // Zoom scale
  const isDraggingCanvas = useRef(false);
  const lastMousePos = useRef({ x: 0, y: 0 });

  // Fetch Data
  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch(`/api/graph?limit=500&space=${space === 'all' ? '' : space}`);
        const json = await res.json();
        
        // Initialize positions randomly
        const width = window.innerWidth;
        const height = window.innerHeight;
        
        const newNodes = json.nodes.map((n: any) => ({
          ...n,
          x: Math.random() * width,
          y: Math.random() * height,
          vx: 0,
          vy: 0,
          radius: n.type === 'session' ? 20 : n.type === 'entity' ? 15 : 8
        }));
        
        nodesRef.current = newNodes;
        edgesRef.current = json.edges;
        setData(json);
      } catch (err) {
        console.error("Failed to fetch graph", err);
      }
    };
    
    fetchData();
  }, [space]);

  // Simulation & Render Loop
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const animate = () => {
      const width = canvas.width;
      const height = canvas.height;
      
      // 1. Physics Step
      const nodes = nodesRef.current;
      const edges = edgesRef.current;
      
      // Repulsion
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const dx = nodes[i].x - nodes[j].x;
          const dy = nodes[i].y - nodes[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy) || 1;
          
          if (dist < 200) {
            const force = 100 / (dist * dist);
            const fx = (dx / dist) * force;
            const fy = (dy / dist) * force;
            
            nodes[i].vx += fx;
            nodes[i].vy += fy;
            nodes[j].vx -= fx;
            nodes[j].vy -= fy;
          }
        }
      }
      
      // Attraction (Edges)
      edges.forEach(edge => {
        const source = nodes.find(n => n.id === edge.source);
        const target = nodes.find(n => n.id === edge.target);
        
        if (source && target) {
          const dx = target.x - source.x;
          const dy = target.y - source.y;
          const dist = Math.sqrt(dx * dx + dy * dy) || 1;
          
          const force = (dist - 100) * 0.005; // Spring constant
          const fx = (dx / dist) * force;
          const fy = (dy / dist) * force;
          
          source.vx += fx;
          source.vy += fy;
          target.vx -= fx;
          target.vy -= fy;
        }
      });
      
      // Center Gravity
      const cx = width / 2;
      const cy = height / 2;
      nodes.forEach(node => {
        const dx = cx - node.x;
        const dy = cy - node.y;
        node.vx += dx * 0.0005;
        node.vy += dy * 0.0005;
        
        // Velocity dampening
        node.vx *= 0.9;
        node.vy *= 0.9;
        
        // Update position (unless dragging)
        if (draggingNode.current?.id !== node.id) {
          node.x += node.vx;
          node.y += node.vy;
        }
      });

      // 2. Render Step
      ctx.clearRect(0, 0, width, height);
      ctx.save();
      ctx.translate(offset.current.x, offset.current.y);
      ctx.scale(scale.current, scale.current);
      
      // Draw Edges
      ctx.strokeStyle = 'rgba(148, 163, 184, 0.2)'; // Slate 400, low opacity
      ctx.lineWidth = 1;
      edges.forEach(edge => {
        const source = nodes.find(n => n.id === edge.source);
        const target = nodes.find(n => n.id === edge.target);
        if (source && target) {
          ctx.beginPath();
          ctx.moveTo(source.x, source.y);
          ctx.lineTo(target.x, target.y);
          ctx.stroke();
        }
      });
      
      // Draw Nodes
      nodes.forEach(node => {
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
        
        // Color based on type
        if (node.type === 'session') {
          ctx.fillStyle = '#8b5cf6'; // Violet
          ctx.shadowColor = '#8b5cf6';
        } else if (node.type === 'entity') {
          ctx.fillStyle = '#3b82f6'; // Blue
          ctx.shadowColor = '#3b82f6';
        } else {
          ctx.fillStyle = '#10b981'; // Emerald (Memory)
          ctx.shadowColor = '#10b981';
        }
        
        // Glow effect
        ctx.shadowBlur = 15;
        ctx.fill();
        ctx.shadowBlur = 0; // Reset shadow
        
        // Hover effect
        if (hoveredNode?.id === node.id) {
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 2;
            ctx.stroke();
            
            // Draw Label
            ctx.fillStyle = '#fff';
            ctx.font = '12px Inter';
            ctx.fillText(node.label, node.x + 15, node.y + 4);
        }
      });
      
      ctx.restore();
      requestRef.current = requestAnimationFrame(animate);
    };
    
    requestRef.current = requestAnimationFrame(animate);
    
    return () => {
      if (requestRef.current) cancelAnimationFrame(requestRef.current);
    };
  }, [data]); // Re-bind when data changes (positions are ref-stable)

  // Resize Handler
  useEffect(() => {
    const handleResize = () => {
      if (canvasRef.current) {
        canvasRef.current.width = window.innerWidth;
        canvasRef.current.height = window.innerHeight;
      }
    };
    window.addEventListener('resize', handleResize);
    handleResize();
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Mouse Handlers
  const handleMouseDown = (e: React.MouseEvent) => {
    const rect = canvasRef.current!.getBoundingClientRect();
    const x = (e.clientX - rect.left - offset.current.x) / scale.current;
    const y = (e.clientY - rect.top - offset.current.y) / scale.current;
    
    // Check node hit
    const hitNode = nodesRef.current.find(n => {
      const dx = n.x - x;
      const dy = n.y - y;
      return Math.sqrt(dx*dx + dy*dy) < n.radius + 5;
    });
    
    if (hitNode) {
      draggingNode.current = hitNode;
    } else {
      isDraggingCanvas.current = true;
      lastMousePos.current = { x: e.clientX, y: e.clientY };
    }
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    const rect = canvasRef.current!.getBoundingClientRect();
    const x = (e.clientX - rect.left - offset.current.x) / scale.current;
    const y = (e.clientY - rect.top - offset.current.y) / scale.current;
    
    // Hover check
    const hitNode = nodesRef.current.find(n => {
        const dx = n.x - x;
        const dy = n.y - y;
        return Math.sqrt(dx*dx + dy*dy) < n.radius + 5;
    });
    setHoveredNode(hitNode || null);
    
    if (draggingNode.current) {
      draggingNode.current.x = x;
      draggingNode.current.y = y;
      draggingNode.current.vx = 0;
      draggingNode.current.vy = 0;
    } else if (isDraggingCanvas.current) {
      const dx = e.clientX - lastMousePos.current.x;
      const dy = e.clientY - lastMousePos.current.y;
      offset.current.x += dx;
      offset.current.y += dy;
      lastMousePos.current = { x: e.clientX, y: e.clientY };
    }
  };

  const handleMouseUp = () => {
    draggingNode.current = null;
    isDraggingCanvas.current = false;
  };
  
  const handleWheel = (e: React.WheelEvent) => {
      const zoomSensitivity = 0.001;
      const newScale = scale.current - e.deltaY * zoomSensitivity;
      scale.current = Math.max(0.1, Math.min(5, newScale));
  };

  return (
    <canvas
      ref={canvasRef}
      className="absolute top-0 left-0 w-full h-full cursor-crosshair"
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
      onWheel={handleWheel}
    />
  );
};

export default GraphCanvas;
