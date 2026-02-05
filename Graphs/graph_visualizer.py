"""
Graph Traversal Visualizer - BFS & DFS Step Through Demo
Run with: streamlit run graph_visualizer.py
"""

import streamlit as st
from dataclasses import dataclass
from typing import List, Dict, Set, Optional
import random

st.set_page_config(page_title="Graph Traversal Visualizer", layout="wide")

# ============================================================
# DATA STRUCTURES
# ============================================================

@dataclass
class GraphSnapshot:
    """Represents a single step in the algorithm visualization."""
    nodes: Dict[str, tuple]  # node_id -> (x, y) position
    edges: List[tuple]       # list of (from, to) tuples
    visited: Set[str]        # nodes fully processed (blue)
    current: Optional[str]   # node being processed (red)
    frontier: List[str]      # nodes in queue/stack (yellow)
    discovered: Set[str]     # newly discovered nodes (green)
    explanation: str
    code_line: str
    data_structure: List[str]  # current state of queue/stack

# Sample graph for demonstrations
# Layout designed to show BFS level-by-level behavior clearly
#
#     A --- B --- E
#     |     |     
#     C --- D --- F
#           |
#           G
#
DEMO_GRAPH = {
    'nodes': {
        'A': (50, 50),
        'B': (150, 50),
        'E': (250, 50),
        'C': (50, 150),
        'D': (150, 150),
        'F': (250, 150),
        'G': (150, 250),
    },
    'edges': [
        ('A', 'B'), ('B', 'E'),
        ('A', 'C'), ('B', 'D'),
        ('C', 'D'), ('D', 'F'),
        ('D', 'G'),
    ],
    'adjacency': {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'D'],
        'D': ['B', 'C', 'F', 'G'],
        'E': ['B'],
        'F': ['D'],
        'G': ['D'],
    }
}

# ============================================================
# RENDERING
# ============================================================

def render_graph(snap: GraphSnapshot):
    """Render the graph as HTML/SVG with highlighted nodes."""
    
    css = """
    <style>
    .graph-container { position: relative; width: 320px; height: 320px; border: 2px solid #ddd; border-radius: 8px; background: #fafafa; margin: 20px 0; }
    .graph-node { position: absolute; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-family: monospace; font-size: 16px; border: 3px solid #333; background: white; transform: translate(-50%, -50%); z-index: 10; }
    .graph-node.visited { background: #dbeafe; border-color: #3b82f6; }
    .graph-node.current { background: #fee2e2; border-color: #e63946; box-shadow: 0 0 15px rgba(230, 57, 70, 0.5); }
    .graph-node.frontier { background: #fef3c7; border-color: #f59e0b; }
    .graph-node.discovered { background: #d1fae5; border-color: #2a9d8f; box-shadow: 0 0 10px rgba(42, 157, 143, 0.4); }
    .graph-edge { position: absolute; background: #999; height: 3px; transform-origin: left center; z-index: 1; }
    .code-line { background: #2d2d2d; color: #f8f8f2; padding: 10px 15px; border-radius: 5px; font-family: monospace; font-size: 14px; margin: 10px 0; }
    .explanation { background: #f0f7ff; border-left: 4px solid #3b82f6; padding: 10px 15px; margin: 10px 0; cursor: pointer; }
    .explanation summary { font-weight: bold; color: #3b82f6; }
    .data-structure { background: #f5f5f5; border: 2px solid #ddd; border-radius: 5px; padding: 10px 15px; margin: 10px 0; font-family: monospace; }
    .ds-label { font-weight: bold; color: #666; margin-bottom: 5px; }
    .ds-content { display: flex; gap: 5px; flex-wrap: wrap; }
    .ds-item { background: #fef3c7; border: 2px solid #f59e0b; border-radius: 4px; padding: 5px 10px; font-size: 14px; }
    .ds-empty { color: #888; font-style: italic; }
    .legend { display: flex; gap: 15px; margin: 10px 0; flex-wrap: wrap; }
    .legend-item { display: flex; align-items: center; gap: 5px; font-size: 12px; }
    .legend-dot { width: 16px; height: 16px; border-radius: 50%; border: 2px solid; }
    .legend-dot.current { background: #fee2e2; border-color: #e63946; }
    .legend-dot.frontier { background: #fef3c7; border-color: #f59e0b; }
    .legend-dot.visited { background: #dbeafe; border-color: #3b82f6; }
    .legend-dot.discovered { background: #d1fae5; border-color: #2a9d8f; }
    </style>
    """
    
    html = [css]
    
    # Legend
    html.append('''
    <div class="legend">
        <div class="legend-item"><div class="legend-dot current"></div> Current</div>
        <div class="legend-item"><div class="legend-dot frontier"></div> In Queue/Stack</div>
        <div class="legend-item"><div class="legend-dot discovered"></div> Just Discovered</div>
        <div class="legend-item"><div class="legend-dot visited"></div> Visited</div>
    </div>
    ''')
    
    # Graph container
    html.append('<div class="graph-container">')
    
    # Draw edges first (so nodes appear on top)
    for (n1, n2) in snap.edges:
        x1, y1 = snap.nodes[n1]
        x2, y2 = snap.nodes[n2]
        # Calculate edge length and angle
        import math
        length = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        angle = math.atan2(y2-y1, x2-x1) * 180 / math.pi
        html.append(f'<div class="graph-edge" style="left:{x1}px;top:{y1}px;width:{length}px;transform:rotate({angle}deg)"></div>')
    
    # Draw nodes
    for node_id, (x, y) in snap.nodes.items():
        classes = ["graph-node"]
        if node_id == snap.current:
            classes.append("current")
        elif node_id in snap.discovered:
            classes.append("discovered")
        elif node_id in snap.frontier:
            classes.append("frontier")
        elif node_id in snap.visited:
            classes.append("visited")
        html.append(f'<div class="{" ".join(classes)}" style="left:{x}px;top:{y}px">{node_id}</div>')
    
    html.append('</div>')
    
    # Code line
    if snap.code_line:
        html.append(f'<div class="code-line">{snap.code_line}</div>')
    
    # Explanation
    if snap.explanation:
        html.append(f'''<details class="explanation">
            <summary>Click to check your interpretation</summary>
            {snap.explanation}
        </details>''')
    
    return "".join(html)


def render_data_structure(items: List[str], ds_type: str = "queue"):
    """Render the queue or stack state."""
    label = "Queue (FIFO)" if ds_type == "queue" else "Stack (LIFO)"
    pointer = "← front" if ds_type == "queue" else "← top"
    
    html = [f'<div class="data-structure"><div class="ds-label">{label}</div><div class="ds-content">']
    
    if not items:
        html.append('<span class="ds-empty">empty</span>')
    else:
        for i, item in enumerate(items):
            suffix = f' {pointer}' if i == 0 else ''
            html.append(f'<span class="ds-item">{item}{suffix}</span>')
    
    html.append('</div></div>')
    return "".join(html)


# ============================================================
# BFS DEMO
# ============================================================

def create_bfs_demo():
    """Step-by-step BFS starting from node A."""
    g = DEMO_GRAPH
    nodes, edges, adj = g['nodes'], g['edges'], g['adjacency']
    
    snapshots = []
    
    # Initial state
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited=set(), current=None, frontier=[], discovered=set(),
        explanation="Starting BFS from node A. BFS uses a QUEUE (FIFO) to explore nodes level by level.",
        code_line="def bfs(graph, start):",
        data_structure=[]
    ))
    
    # Initialize
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited=set(), current=None, frontier=['A'], discovered={'A'},
        explanation="Initialize: add starting node A to the queue and mark it as discovered.",
        code_line="queue = [start]  # queue = ['A']",
        data_structure=['A']
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited=set(), current=None, frontier=['A'], discovered={'A'},
        explanation="Create an empty set to track visited nodes. 'Visited' means we've fully processed a node.",
        code_line="visited = set()",
        data_structure=['A']
    ))
    
    # Process A
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited=set(), current='A', frontier=[], discovered=set(),
        explanation="Dequeue A (remove from front). A is now the 'current' node being processed.",
        code_line="current = queue.pop(0)  # current = 'A'",
        data_structure=[]
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited=set(), current='A', frontier=[], discovered=set(),
        explanation="Check: have we visited A? No, so we'll process it.",
        code_line="if current not in visited:  # True",
        data_structure=[]
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A'}, current='A', frontier=[], discovered=set(),
        explanation="Mark A as visited. We won't process A again.",
        code_line="visited.add(current)  # visited = {'A'}",
        data_structure=[]
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A'}, current='A', frontier=[], discovered=set(),
        explanation="Get A's neighbors: B and C. We'll add unvisited neighbors to the queue.",
        code_line="for neighbor in graph['A']:  # ['B', 'C']",
        data_structure=[]
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A'}, current='A', frontier=['B'], discovered={'B'},
        explanation="B is not visited. Add B to the queue.",
        code_line="queue.append('B')  # queue = ['B']",
        data_structure=['B']
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A'}, current='A', frontier=['B', 'C'], discovered={'B', 'C'},
        explanation="C is not visited. Add C to the queue. Now queue has both level-1 neighbors.",
        code_line="queue.append('C')  # queue = ['B', 'C']",
        data_structure=['B', 'C']
    ))
    
    # Process B
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A'}, current='B', frontier=['C'], discovered=set(),
        explanation="Dequeue B. Notice: we process ALL level-1 nodes before ANY level-2 nodes. That's the magic of FIFO!",
        code_line="current = queue.pop(0)  # current = 'B'",
        data_structure=['C']
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'B'}, current='B', frontier=['C'], discovered=set(),
        explanation="Mark B as visited.",
        code_line="visited.add(current)  # visited = {'A', 'B'}",
        data_structure=['C']
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'B'}, current='B', frontier=['C'], discovered=set(),
        explanation="Get B's neighbors: A, D, E. A is already visited, so skip it.",
        code_line="for neighbor in graph['B']:  # ['A', 'D', 'E']",
        data_structure=['C']
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'B'}, current='B', frontier=['C', 'D'], discovered={'D'},
        explanation="D is not visited. Add D to queue.",
        code_line="queue.append('D')  # queue = ['C', 'D']",
        data_structure=['C', 'D']
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'B'}, current='B', frontier=['C', 'D', 'E'], discovered={'D', 'E'},
        explanation="E is not visited. Add E to queue. D and E are level-2 nodes - they go AFTER C.",
        code_line="queue.append('E')  # queue = ['C', 'D', 'E']",
        data_structure=['C', 'D', 'E']
    ))
    
    # Process C
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'B'}, current='C', frontier=['D', 'E'], discovered=set(),
        explanation="Dequeue C. C is the last level-1 node.",
        code_line="current = queue.pop(0)  # current = 'C'",
        data_structure=['D', 'E']
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'B', 'C'}, current='C', frontier=['D', 'E'], discovered=set(),
        explanation="Mark C as visited.",
        code_line="visited.add(current)  # visited = {'A', 'B', 'C'}",
        data_structure=['D', 'E']
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'B', 'C'}, current='C', frontier=['D', 'E'], discovered=set(),
        explanation="C's neighbors: A (visited), D (already in queue). Nothing new to add.",
        code_line="for neighbor in graph['C']:  # ['A', 'D'] - both seen",
        data_structure=['D', 'E']
    ))
    
    # Process D
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'B', 'C'}, current='D', frontier=['E'], discovered=set(),
        explanation="Dequeue D. Now processing level-2 nodes.",
        code_line="current = queue.pop(0)  # current = 'D'",
        data_structure=['E']
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'B', 'C', 'D'}, current='D', frontier=['E'], discovered=set(),
        explanation="Mark D as visited.",
        code_line="visited.add(current)  # visited = {'A', 'B', 'C', 'D'}",
        data_structure=['E']
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'B', 'C', 'D'}, current='D', frontier=['E', 'F'], discovered={'F'},
        explanation="D's neighbors: B, C (visited), F, G (new). Add F.",
        code_line="queue.append('F')  # queue = ['E', 'F']",
        data_structure=['E', 'F']
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'B', 'C', 'D'}, current='D', frontier=['E', 'F', 'G'], discovered={'F', 'G'},
        explanation="Add G. F and G are level-3 nodes.",
        code_line="queue.append('G')  # queue = ['E', 'F', 'G']",
        data_structure=['E', 'F', 'G']
    ))
    
    # Process E
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'B', 'C', 'D'}, current='E', frontier=['F', 'G'], discovered=set(),
        explanation="Dequeue E. E's only neighbor is B (visited).",
        code_line="current = queue.pop(0)  # current = 'E'",
        data_structure=['F', 'G']
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'B', 'C', 'D', 'E'}, current='E', frontier=['F', 'G'], discovered=set(),
        explanation="Mark E as visited. No new neighbors to add.",
        code_line="visited.add(current)  # E has no unvisited neighbors",
        data_structure=['F', 'G']
    ))
    
    # Process F
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'B', 'C', 'D', 'E'}, current='F', frontier=['G'], discovered=set(),
        explanation="Dequeue F.",
        code_line="current = queue.pop(0)  # current = 'F'",
        data_structure=['G']
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'B', 'C', 'D', 'E', 'F'}, current='F', frontier=['G'], discovered=set(),
        explanation="Mark F as visited. F's only neighbor D is visited.",
        code_line="visited.add(current)  # F has no unvisited neighbors",
        data_structure=['G']
    ))
    
    # Process G
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'B', 'C', 'D', 'E', 'F'}, current='G', frontier=[], discovered=set(),
        explanation="Dequeue G. Last node!",
        code_line="current = queue.pop(0)  # current = 'G'",
        data_structure=[]
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'B', 'C', 'D', 'E', 'F', 'G'}, current='G', frontier=[], discovered=set(),
        explanation="Mark G as visited. G's only neighbor D is visited.",
        code_line="visited.add(current)  # visited = all nodes",
        data_structure=[]
    ))
    
    # Done
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'B', 'C', 'D', 'E', 'F', 'G'}, current=None, frontier=[], discovered=set(),
        explanation="Queue is empty - BFS complete! Visit order: A, B, C, D, E, F, G. Notice the LEVEL-BY-LEVEL pattern: Level 0 (A) → Level 1 (B,C) → Level 2 (D,E) → Level 3 (F,G)",
        code_line="# while queue: ... loop ends",
        data_structure=[]
    ))
    
    return snapshots


# ============================================================
# DFS DEMO
# ============================================================

def create_dfs_demo():
    """Step-by-step DFS starting from node A."""
    g = DEMO_GRAPH
    nodes, edges, adj = g['nodes'], g['edges'], g['adjacency']
    
    snapshots = []
    
    # Initial state
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited=set(), current=None, frontier=[], discovered=set(),
        explanation="Starting DFS from node A. DFS uses a STACK (LIFO) to explore as deep as possible before backtracking.",
        code_line="def dfs(graph, start):",
        data_structure=[]
    ))
    
    # Initialize
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited=set(), current=None, frontier=['A'], discovered={'A'},
        explanation="Initialize: push starting node A onto the stack.",
        code_line="stack = [start]  # stack = ['A']",
        data_structure=['A']
    ))
    
    # Process A
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited=set(), current='A', frontier=[], discovered=set(),
        explanation="Pop A from stack. A is now current.",
        code_line="current = stack.pop()  # current = 'A'",
        data_structure=[]
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A'}, current='A', frontier=[], discovered=set(),
        explanation="Mark A as visited.",
        code_line="visited.add(current)  # visited = {'A'}",
        data_structure=[]
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A'}, current='A', frontier=['B'], discovered={'B'},
        explanation="A's neighbors: B, C. Push B onto stack.",
        code_line="stack.append('B')  # stack = ['B']",
        data_structure=['B']
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A'}, current='A', frontier=['B', 'C'], discovered={'B', 'C'},
        explanation="Push C onto stack. C is now on TOP (will be processed FIRST - that's LIFO!).",
        code_line="stack.append('C')  # stack = ['B', 'C']",
        data_structure=['B', 'C']
    ))
    
    # Process C (LIFO - C was added last, processed first)
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A'}, current='C', frontier=['B'], discovered=set(),
        explanation="Pop C (it's on top!). This is the key difference from BFS: we go DEEP first, not wide.",
        code_line="current = stack.pop()  # current = 'C'",
        data_structure=['B']
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'C'}, current='C', frontier=['B'], discovered=set(),
        explanation="Mark C as visited.",
        code_line="visited.add(current)  # visited = {'A', 'C'}",
        data_structure=['B']
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'C'}, current='C', frontier=['B', 'D'], discovered={'D'},
        explanation="C's neighbors: A (visited), D (new). Push D. D goes on top of B!",
        code_line="stack.append('D')  # stack = ['B', 'D']",
        data_structure=['B', 'D']
    ))
    
    # Process D
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'C'}, current='D', frontier=['B'], discovered=set(),
        explanation="Pop D. We're going DEEPER into the graph (A→C→D), not exploring B yet.",
        code_line="current = stack.pop()  # current = 'D'",
        data_structure=['B']
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'C', 'D'}, current='D', frontier=['B'], discovered=set(),
        explanation="Mark D as visited.",
        code_line="visited.add(current)  # visited = {'A', 'C', 'D'}",
        data_structure=['B']
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'C', 'D'}, current='D', frontier=['B'], discovered=set(),
        explanation="D's neighbors: B (not visited), C (visited), F, G. Push unvisited ones.",
        code_line="for neighbor in graph['D']:  # ['B', 'C', 'F', 'G']",
        data_structure=['B']
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'C', 'D'}, current='D', frontier=['B', 'F'], discovered={'F'},
        explanation="Push F onto stack.",
        code_line="stack.append('F')  # stack = ['B', 'F']",
        data_structure=['B', 'F']
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'C', 'D'}, current='D', frontier=['B', 'F', 'G'], discovered={'F', 'G'},
        explanation="Push G onto stack. G is now on top.",
        code_line="stack.append('G')  # stack = ['B', 'F', 'G']",
        data_structure=['B', 'F', 'G']
    ))
    
    # Process G
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'C', 'D'}, current='G', frontier=['B', 'F'], discovered=set(),
        explanation="Pop G. We're at the deepest point on this path (A→C→D→G).",
        code_line="current = stack.pop()  # current = 'G'",
        data_structure=['B', 'F']
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'C', 'D', 'G'}, current='G', frontier=['B', 'F'], discovered=set(),
        explanation="Mark G as visited. G's only neighbor D is visited. BACKTRACK time!",
        code_line="visited.add(current)  # G is a dead end",
        data_structure=['B', 'F']
    ))
    
    # Process F (backtracking)
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'C', 'D', 'G'}, current='F', frontier=['B'], discovered=set(),
        explanation="Pop F. We backtracked from G to try another path from D.",
        code_line="current = stack.pop()  # current = 'F' (backtracking)",
        data_structure=['B']
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'C', 'D', 'G', 'F'}, current='F', frontier=['B'], discovered=set(),
        explanation="Mark F as visited. F's only neighbor D is visited. Another dead end!",
        code_line="visited.add(current)  # F is also a dead end",
        data_structure=['B']
    ))
    
    # Process B (more backtracking)
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'C', 'D', 'G', 'F'}, current='B', frontier=[], discovered=set(),
        explanation="Pop B. We've backtracked all the way - now exploring the other branch from A.",
        code_line="current = stack.pop()  # current = 'B'",
        data_structure=[]
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'C', 'D', 'G', 'F', 'B'}, current='B', frontier=[], discovered=set(),
        explanation="Mark B as visited.",
        code_line="visited.add(current)  # visited = {'A', 'C', 'D', 'G', 'F', 'B'}",
        data_structure=[]
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'C', 'D', 'G', 'F', 'B'}, current='B', frontier=['E'], discovered={'E'},
        explanation="B's neighbors: A (visited), D (visited), E (new). Push E.",
        code_line="stack.append('E')  # stack = ['E']",
        data_structure=['E']
    ))
    
    # Process E
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'C', 'D', 'G', 'F', 'B'}, current='E', frontier=[], discovered=set(),
        explanation="Pop E. Last node!",
        code_line="current = stack.pop()  # current = 'E'",
        data_structure=[]
    ))
    
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'C', 'D', 'G', 'F', 'B', 'E'}, current='E', frontier=[], discovered=set(),
        explanation="Mark E as visited. E's only neighbor B is visited.",
        code_line="visited.add(current)  # visited = all nodes",
        data_structure=[]
    ))
    
    # Done
    snapshots.append(GraphSnapshot(
        nodes=nodes, edges=edges,
        visited={'A', 'C', 'D', 'G', 'F', 'B', 'E'}, current=None, frontier=[], discovered=set(),
        explanation="Stack is empty - DFS complete! Visit order: A, C, D, G, F, B, E. Notice: we went DEEP (A→C→D→G) before exploring B's branch. This is NOT level-by-level!",
        code_line="# while stack: ... loop ends",
        data_structure=[]
    ))
    
    return snapshots


# ============================================================
# SKILLS ASSESSMENT
# ============================================================

SKILLS = {
    "adjacency": ("1", "Graph Representation", "Read adjacency lists and find neighbors"),
    "bfs_order": ("2", "BFS Traversal Order", "Predict BFS visit order from a start node"),
    "dfs_order": ("3", "DFS Traversal Order", "Predict DFS visit order (with backtracking)"),
    "queue_vs_stack": ("4", "Queue vs Stack", "Which data structure and why"),
    "reachability": ("5", "Path Finding", "Can you reach node X from node Y?"),
    "levels": ("6", "BFS Levels", "Which level is each node at?"),
    "backtracking": ("7", "DFS Backtracking", "When does DFS backtrack?"),
    "shortest_path": ("8", "Shortest Path", "Why BFS finds shortest paths in unweighted graphs"),
}

# Question format: (graph_adj, start_node, code, question, answer, distractors)
# graph_adj is a simplified adjacency representation for display

QUESTIONS = {
    "adjacency": [
        ({'A': ['B', 'C'], 'B': ['A', 'D'], 'C': ['A'], 'D': ['B']}, 'A', None, "graph['A']", "['B', 'C']", ["['A']", "['B']", "Error"]),
        ({'A': ['B', 'C'], 'B': ['A', 'D'], 'C': ['A'], 'D': ['B']}, 'A', None, "graph['B']", "['A', 'D']", ["['B']", "['A', 'B', 'D']", "['D']"]),
        ({'A': ['B', 'C'], 'B': ['A', 'D'], 'C': ['A'], 'D': ['B']}, 'A', None, "len(graph['A'])", "2", ["3", "1", "4"]),
        ({'X': ['Y'], 'Y': ['X', 'Z'], 'Z': ['Y']}, 'X', None, "'Z' in graph['Y']", "True", ["False", "Error", "None"]),
        ({'A': ['B'], 'B': ['C'], 'C': []}, 'A', None, "graph['C']", "[]", ["['B']", "None", "Error"]),
        ({'A': ['B', 'C', 'D'], 'B': ['A'], 'C': ['A'], 'D': ['A']}, 'A', None, "How many neighbors does A have?", "3", ["1", "4", "0"]),
        ({'A': ['B'], 'B': ['A', 'C'], 'C': ['B']}, 'A', None, "'A' in graph['B']", "True", ["False", "Error", "'B'"]),
        ({'A': ['B'], 'B': ['C'], 'C': ['D'], 'D': []}, 'A', None, "graph['D']", "[]", ["['C']", "None", "Error"]),
    ],
    "bfs_order": [
        ({'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}, 'A', None, "BFS order from A?", "A, B, C, D", ["A, B, D, C", "A, C, B, D", "A, D, B, C"]),
        ({'A': ['B', 'C'], 'B': ['A'], 'C': ['A', 'D'], 'D': ['C']}, 'A', None, "BFS order from A?", "A, B, C, D", ["A, C, D, B", "A, B, D, C", "A, C, B, D"]),
        ({'A': ['B'], 'B': ['C'], 'C': ['D'], 'D': []}, 'A', None, "BFS order from A?", "A, B, C, D", ["A, D, C, B", "D, C, B, A", "A, C, B, D"]),
        ({'A': ['B', 'C', 'D'], 'B': [], 'C': [], 'D': []}, 'A', None, "BFS order from A?", "A, B, C, D", ["A, D, C, B", "B, C, D, A", "A only"]),
        ({'A': ['B'], 'B': ['A', 'C'], 'C': ['B']}, 'C', None, "BFS order from C?", "C, B, A", ["C, A, B", "A, B, C", "C only"]),
        ({'1': ['2', '3'], '2': ['4'], '3': ['4'], '4': []}, '1', None, "BFS order from 1?", "1, 2, 3, 4", ["1, 2, 4, 3", "1, 3, 2, 4", "1, 4, 2, 3"]),
    ],
    "dfs_order": [
        ({'A': ['B', 'C'], 'B': ['D'], 'C': [], 'D': []}, 'A', None, "DFS order from A? (neighbors added B then C)", "A, C, B, D", ["A, B, C, D", "A, B, D, C", "A, D, B, C"]),
        ({'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}, 'A', None, "DFS order from A? (stack: last added = first out)", "A, C, D, B", ["A, B, C, D", "A, B, D, C", "A, D, C, B"]),
        ({'A': ['B'], 'B': ['C'], 'C': ['D'], 'D': []}, 'A', None, "DFS order from A?", "A, B, C, D", ["A, D, C, B", "D, C, B, A", "Same as BFS"]),
        ({'A': ['B', 'C'], 'B': [], 'C': ['D'], 'D': []}, 'A', None, "DFS from A (add B then C to stack)?", "A, C, D, B", ["A, B, C, D", "A, B, D, C", "A, D, C, B"]),
        ({'A': ['B', 'C', 'D'], 'B': [], 'C': [], 'D': []}, 'A', None, "DFS from A (add B, C, D to stack)?", "A, D, C, B", ["A, B, C, D", "A, C, B, D", "Same as BFS"]),
    ],
    "queue_vs_stack": [
        (None, None, "BFS uses which data structure?", "Answer:", "Queue (FIFO)", ["Stack (LIFO)", "List", "Set"]),
        (None, None, "DFS uses which data structure?", "Answer:", "Stack (LIFO)", ["Queue (FIFO)", "List", "Heap"]),
        (None, None, "queue.pop(0) removes from...", "Answer:", "Front (first in)", ["Back (last in)", "Random", "Middle"]),
        (None, None, "stack.pop() removes from...", "Answer:", "Back (last in)", ["Front (first in)", "Random", "Middle"]),
        (None, None, "FIFO means...", "Answer:", "First In First Out", ["First In Last Out", "Last In First Out", "Random"]),
        (None, None, "Which explores level-by-level?", "Answer:", "BFS (queue)", ["DFS (stack)", "Both", "Neither"]),
        (None, None, "Which goes as deep as possible first?", "Answer:", "DFS (stack)", ["BFS (queue)", "Both", "Neither"]),
        (None, None, "If I add A, B, C to a queue and pop, I get:", "Answer:", "A", ["C", "B", "Random"]),
        (None, None, "If I add A, B, C to a stack and pop, I get:", "Answer:", "C", ["A", "B", "Random"]),
    ],
    "reachability": [
        ({'A': ['B'], 'B': ['C'], 'C': [], 'D': []}, 'A', None, "Can you reach D from A?", "No", ["Yes", "Maybe", "Error"]),
        ({'A': ['B'], 'B': ['C'], 'C': ['D'], 'D': []}, 'A', None, "Can you reach D from A?", "Yes", ["No", "Maybe", "Error"]),
        ({'A': ['B'], 'B': ['A'], 'C': ['D'], 'D': ['C']}, 'A', None, "Can you reach C from A?", "No", ["Yes", "Maybe", "Error"]),
        ({'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': ['E'], 'E': []}, 'A', None, "Can you reach E from A?", "Yes", ["No", "Maybe", "Error"]),
        ({'A': [], 'B': ['A'], 'C': ['B']}, 'A', None, "Can you reach C from A?", "No (directed)", ["Yes", "Maybe", "Error"]),
        ({'A': ['B'], 'B': [], 'C': []}, 'C', None, "Can you reach A from C?", "No", ["Yes", "Maybe", "Error"]),
    ],
    "levels": [
        ({'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}, 'A', None, "BFS from A: D is at level?", "2", ["1", "3", "0"]),
        ({'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}, 'A', None, "BFS from A: B is at level?", "1", ["0", "2", "3"]),
        ({'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}, 'A', None, "BFS from A: A is at level?", "0", ["1", "-1", "None"]),
        ({'A': ['B'], 'B': ['C'], 'C': ['D'], 'D': ['E'], 'E': []}, 'A', None, "BFS from A: E is at level?", "4", ["5", "3", "2"]),
        ({'A': ['B', 'C', 'D'], 'B': [], 'C': [], 'D': []}, 'A', None, "BFS from A: All of B,C,D are at level?", "1", ["0", "2", "Different levels"]),
        ({'A': ['B'], 'B': ['C', 'D'], 'C': [], 'D': []}, 'A', None, "BFS from A: C and D are at level?", "2", ["1", "3", "Different levels"]),
    ],
    "backtracking": [
        ({'A': ['B'], 'B': ['C'], 'C': []}, 'A', None, "DFS: After visiting C, what happens?", "Backtrack (C is dead end)", ["Visit A", "Visit B again", "Done"]),
        ({'A': ['B', 'C'], 'B': [], 'C': []}, 'A', "DFS visits A, then C (top of stack)", "After visiting C?", "Pop B from stack", ["Visit A again", "Done", "Push C back"]),
        ({'A': ['B'], 'B': [], 'C': ['D'], 'D': []}, 'A', None, "DFS from A: Will we visit C?", "No (C not reachable)", ["Yes", "Maybe", "Error"]),
        ({'A': ['B', 'C'], 'B': ['D'], 'C': [], 'D': []}, 'A', "Stack after visiting A: [B, C]. Pop C.", "After C (dead end), pop:", "B", ["D", "C again", "A"]),
        ({'A': ['B'], 'B': ['C'], 'C': ['A']}, 'A', None, "DFS: Does A get visited twice?", "No (visited set prevents)", ["Yes", "Error", "Infinite loop"]),
    ],
    "shortest_path": [
        ({'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}, 'A', None, "Shortest path A→D has length?", "2", ["1", "3", "4"]),
        ({'A': ['B'], 'B': ['C'], 'C': ['D'], 'D': []}, 'A', None, "Shortest path A→D has length?", "3", ["4", "2", "1"]),
        ({'A': ['B', 'D'], 'B': ['C'], 'C': ['D'], 'D': []}, 'A', None, "Shortest path A→D has length?", "1", ["2", "3", "0"]),
        (None, None, "Which finds shortest path in unweighted graphs?", "Answer:", "BFS", ["DFS", "Both", "Neither"]),
        (None, None, "Why does BFS find shortest paths?", "Answer:", "Explores level-by-level", ["Goes deep first", "Random", "Uses priority queue"]),
        (None, None, "DFS finds shortest path?", "Answer:", "Not guaranteed", ["Always", "Never", "Only in trees"]),
        ({'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}, 'A', "BFS from A finds D at level 2.", "Is 2 the shortest distance?", "Yes", ["No", "Maybe", "Need Dijkstra"]),
    ],
}


def render_mini_graph(adj: dict):
    """Render a small text representation of the graph."""
    if adj is None:
        return ""
    lines = []
    for node, neighbors in sorted(adj.items()):
        lines.append(f"  {node}: {neighbors}")
    return f'<pre style="background:#f5f5f5;padding:10px;border-radius:5px;font-size:12px">graph = {{\n' + '\n'.join(lines) + '\n}}</pre>'


# ============================================================
# MAIN APP
# ============================================================

st.title("Graph Traversal Visualizer")
st.markdown("*Step through BFS and DFS to see how they explore graphs differently*")

tab1, tab2, tab3 = st.tabs(["BFS (Breadth-First)", "DFS (Depth-First)", "Skills Assessment"])

# ===================== BFS TAB =====================
with tab1:
    st.subheader("Breadth-First Search")
    st.markdown("BFS explores **level by level** using a **queue (FIFO)**. It finds the shortest path in unweighted graphs.")
    
    if "bfs_step" not in st.session_state:
        st.session_state.bfs_step = 0
    
    snapshots = create_bfs_demo()
    step = st.session_state.bfs_step
    
    code_col, viz_col = st.columns([1, 2])
    
    with code_col:
        st.code('''def bfs(graph, start):
    queue = [start]
    visited = set()
    
    while queue:
        current = queue.pop(0)  # FIFO
        
        if current not in visited:
            visited.add(current)
            
            for neighbor in graph[current]:
                if neighbor not in visited:
                    queue.append(neighbor)
    
    return visited''', language='python')
        
        st.markdown("**Key insight:** The queue ensures we process all nodes at distance *d* before any node at distance *d+1*.")
    
    with viz_col:
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            if st.button("← Previous", disabled=(step == 0), key="bfs_prev"):
                st.session_state.bfs_step -= 1
                st.rerun()
        with col2:
            if st.button("Next →", disabled=(step == len(snapshots)-1), key="bfs_next"):
                st.session_state.bfs_step += 1
                st.rerun()
        with col3:
            if st.button("Reset", key="bfs_reset"):
                st.session_state.bfs_step = 0
                st.rerun()
        
        st.markdown(f"**Step {step + 1} of {len(snapshots)}**")
        
        snap = snapshots[step]
        st.markdown(render_graph(snap), unsafe_allow_html=True)
        st.markdown(render_data_structure(snap.data_structure, "queue"), unsafe_allow_html=True)


# ===================== DFS TAB =====================
with tab2:
    st.subheader("Depth-First Search")
    st.markdown("DFS explores **as deep as possible** using a **stack (LIFO)**. It backtracks when hitting dead ends.")
    
    if "dfs_step" not in st.session_state:
        st.session_state.dfs_step = 0
    
    snapshots = create_dfs_demo()
    step = st.session_state.dfs_step
    
    code_col, viz_col = st.columns([1, 2])
    
    with code_col:
        st.code('''def dfs(graph, start):
    stack = [start]
    visited = set()
    
    while stack:
        current = stack.pop()  # LIFO
        
        if current not in visited:
            visited.add(current)
            
            for neighbor in graph[current]:
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return visited''', language='python')
        
        st.markdown("**Key insight:** The stack means the last neighbor added is processed first, causing us to go deep before exploring alternatives.")
    
    with viz_col:
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            if st.button("← Previous", disabled=(step == 0), key="dfs_prev"):
                st.session_state.dfs_step -= 1
                st.rerun()
        with col2:
            if st.button("Next →", disabled=(step == len(snapshots)-1), key="dfs_next"):
                st.session_state.dfs_step += 1
                st.rerun()
        with col3:
            if st.button("Reset", key="dfs_reset"):
                st.session_state.dfs_step = 0
                st.rerun()
        
        st.markdown(f"**Step {step + 1} of {len(snapshots)}**")
        
        snap = snapshots[step]
        st.markdown(render_graph(snap), unsafe_allow_html=True)
        st.markdown(render_data_structure(snap.data_structure, "stack"), unsafe_allow_html=True)


# ===================== SKILLS TAB =====================
with tab3:
    st.subheader("Graph Traversal Skills Assessment")
    st.markdown("*Test your understanding of BFS, DFS, and graph concepts*")
    
    # Skill selection
    st.markdown("### Select a skill to practice:")
    
    cols = st.columns(4)
    for i, (key, (num, name, desc)) in enumerate(SKILLS.items()):
        with cols[i % 4]:
            if st.button(f"{num}. {name}", key=f"skill_btn_{key}", use_container_width=True, help=desc):
                st.session_state.skill = key
                st.session_state.questions = None
                st.session_state.idx = 0
                st.session_state.score = 0
                st.session_state.answered = False
                st.rerun()
    
    st.markdown("---")
    
    # Assessment
    if "skill" in st.session_state and st.session_state.skill:
        skill = st.session_state.skill
        num, name, desc = SKILLS[skill]
        
        st.subheader(f"Skill {num}: {name}")
        st.caption(desc)
        
        # Load questions
        if st.session_state.get("questions") is None:
            qs = QUESTIONS[skill].copy()
            random.shuffle(qs)
            st.session_state.questions = qs[:5]
            st.session_state.idx = 0
            st.session_state.score = 0
            st.session_state.answered = False
        
        qs = st.session_state.questions
        idx = st.session_state.idx
        
        if idx < len(qs):
            q = qs[idx]
            # Unpack based on format
            if len(q) == 6:
                graph_adj, start, code, question, answer, distractors = q
            else:
                graph_adj, start, code, question, answer, distractors = q[0], q[1], q[2], q[3], q[4], q[5]
            
            st.progress(idx / len(qs))
            st.markdown(f"**Question {idx+1}/5** | Score: {st.session_state.score}/{idx}")
            
            # Show graph if present
            if graph_adj:
                st.markdown(render_mini_graph(graph_adj), unsafe_allow_html=True)
                if start:
                    st.markdown(f"*Starting node: {start}*")
            
            # Show code if present
            if code:
                st.code(code, language="python")
            
            # Question
            st.markdown(f"### {question}")
            
            # Choices
            if f"choices_{idx}" not in st.session_state:
                choices = [answer] + distractors
                random.shuffle(choices)
                st.session_state[f"choices_{idx}"] = choices
            
            choices = st.session_state[f"choices_{idx}"]
            
            if not st.session_state.answered:
                cols = st.columns(len(choices))
                for i, c in enumerate(choices):
                    with cols[i]:
                        if st.button(c, key=f"choice_{i}", use_container_width=True):
                            st.session_state.answered = True
                            st.session_state.user_ans = c
                            if c == answer:
                                st.session_state.score += 1
                            st.rerun()
            else:
                if st.session_state.user_ans == answer:
                    st.success("Correct!")
                else:
                    st.error(f"Answer: **{answer}**")
                
                if st.button("Next", type="primary"):
                    st.session_state.idx += 1
                    st.session_state.answered = False
                    st.rerun()
        else:
            # Done
            score = st.session_state.score
            st.success(f"### Round complete! Score: {score}/5")
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Try Again", use_container_width=True):
                    st.session_state.questions = None
                    st.rerun()
            with c2:
                if st.button("Different Skill", use_container_width=True):
                    st.session_state.skill = None
                    st.rerun()
    else:
        st.info("Select a skill above to start practicing")

st.markdown("---")
st.markdown("*SI 507 - Intermediate Programming*")
