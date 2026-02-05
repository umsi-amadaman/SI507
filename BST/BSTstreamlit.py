"""
BST Visualizer - Step Through Demo + Skills Assessment
Run with: streamlit run streamlit_app.py
"""

import streamlit as st
import random
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple

st.set_page_config(page_title="BST Visualizer", layout="wide")


# ============================================================
# SHARED DATA STRUCTURES
# ============================================================

@dataclass
class TreeNode:
    value: int
    left: Optional['TreeNode'] = None
    right: Optional['TreeNode'] = None


@dataclass
class BSTSnapshot:
    tree: Optional[TreeNode]
    highlighted_nodes: Dict[str, List[int]] = field(default_factory=dict)
    floating_node: Optional[int] = None
    comparison_text: Optional[str] = None
    explanation: str = ""
    code_line: str = ""


# ============================================================
# TREE BUILDING UTILITIES
# ============================================================

def build_tree(values: List[int]) -> Optional[TreeNode]:
    if not values:
        return None
    root = TreeNode(values[0])
    for val in values[1:]:
        insert_into_tree(root, val)
    return root


def insert_into_tree(root: TreeNode, value: int) -> None:
    if value < root.value:
        if root.left is None:
            root.left = TreeNode(value)
        else:
            insert_into_tree(root.left, value)
    else:
        if root.right is None:
            root.right = TreeNode(value)
        else:
            insert_into_tree(root.right, value)


def build_tree_dict(values: List[int]) -> Optional[Dict]:
    if not values:
        return None
    root = {"val": values[0], "left": None, "right": None}
    for val in values[1:]:
        insert_dict(root, val)
    return root


def insert_dict(node: Dict, val: int) -> None:
    if val < node["val"]:
        if node["left"] is None:
            node["left"] = {"val": val, "left": None, "right": None}
        else:
            insert_dict(node["left"], val)
    else:
        if node["right"] is None:
            node["right"] = {"val": val, "left": None, "right": None}
        else:
            insert_dict(node["right"], val)


# ============================================================
# CODE TRACING: GRAPHICAL TREE RENDERING
# ============================================================

def calculate_positions(node, x, y, x_offset, positions):
    if node is None:
        return
    positions[node.value] = (x, y)
    next_offset = x_offset * 0.55
    calculate_positions(node.left, x - x_offset, y + 1, next_offset, positions)
    calculate_positions(node.right, x + x_offset, y + 1, next_offset, positions)


def render_bst_snapshot(snap: BSTSnapshot, tree_var: str = "bst") -> str:
    css = """
    <style>
    .bst-container { position: relative; width: 100%; height: 400px; margin: 20px 0; font-family: monospace; background: #fafafa; border-radius: 8px; overflow: hidden; }
    .bst-node { position: absolute; width: 50px; height: 50px; border: 3px solid #333; border-radius: 50%; background: white; display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: bold; transform: translate(-50%, -50%); z-index: 2; color: #333; }
    .bst-node.highlight-current { border-color: #e63946; background: #fff0f0; box-shadow: 0 0 15px rgba(230, 57, 70, 0.5); }
    .bst-node.highlight-newnode { border-color: #2a9d8f; background: #f0fff0; box-shadow: 0 0 15px rgba(42, 157, 143, 0.5); }
    .bst-node.highlight-found { border-color: #3b82f6; background: #f0f7ff; box-shadow: 0 0 15px rgba(59, 130, 246, 0.5); }
    .bst-node.highlight-path { border-color: #f59e0b; background: #fffbeb; }
    .bst-node.highlight-target { border-color: #8b5cf6; background: #f5f3ff; box-shadow: 0 0 15px rgba(139, 92, 246, 0.5); }
    .bst-edge { position: absolute; background: #666; height: 2px; transform-origin: left center; z-index: 1; }
    .node-label { position: absolute; font-size: 11px; font-weight: bold; transform: translate(-50%, 0); white-space: nowrap; }
    .node-label.current { color: #e63946; top: -20px; }
    .node-label.newnode { color: #2a9d8f; top: -20px; }
    .node-label.found { color: #3b82f6; top: -20px; }
    .floating-node-container { display: flex; align-items: center; gap: 10px; margin: 15px 0; padding: 10px; background: #f0fff0; border-radius: 8px; border: 2px dashed #2a9d8f; }
    .floating-label { color: #2a9d8f; font-weight: bold; font-family: monospace; }
    .floating-node { width: 50px; height: 50px; border: 3px solid #2a9d8f; border-radius: 50%; background: #f0fff0; display: flex; align-items: center; justify-content: center; font-size: 16px; font-weight: bold; font-family: monospace; color: #333; }
    .comparison-box { background: #fef3c7; border: 2px solid #f59e0b; border-radius: 8px; padding: 10px 15px; margin: 10px 0; font-family: monospace; font-size: 16px; text-align: center; }
    .code-line { background: #2d2d2d; color: #f8f8f2; padding: 10px 15px; border-radius: 5px; font-family: monospace; font-size: 14px; margin: 10px 0; }
    .explanation { background: #f0f7ff; border-left: 4px solid #3b82f6; padding: 10px 15px; margin: 10px 0; cursor: pointer; }
    .explanation summary { font-weight: bold; color: #3b82f6; }
    .tree-label { font-size: 12px; color: #666; margin-bottom: 5px; font-family: monospace; }
    .empty-tree { display: flex; align-items: center; justify-content: center; height: 100%; color: #888; font-style: italic; }
    </style>
    """
    
    html = [css, f'<div class="tree-label">{tree_var}.root</div>', '<div class="bst-container">']
    
    if snap.tree is None:
        html.append('<div class="empty-tree">None (empty tree)</div>')
    else:
        positions = {}
        calculate_positions(snap.tree, 0.5, 0, 0.22, positions)
        html.append(draw_edges(snap.tree, positions))
        html.append(draw_nodes(snap.tree, positions, snap.highlighted_nodes))
    
    html.append('</div>')
    
    if snap.floating_node is not None:
        html.append(f'<div class="floating-node-container"><span class="floating-label">new_node =</span><div class="floating-node">{snap.floating_node}</div><span style="color: #666; font-family: monospace;">(not yet in tree)</span></div>')
    
    if snap.comparison_text:
        html.append(f'<div class="comparison-box">{snap.comparison_text}</div>')
    if snap.code_line:
        html.append(f'<div class="code-line">{snap.code_line}</div>')
    if snap.explanation:
        html.append(f'<details class="explanation"><summary>Click to check your interpretation</summary>{snap.explanation}</details>')
    
    return "".join(html)


def draw_edges(node, positions, parent_pos=None):
    if node is None:
        return ""
    import math
    html = []
    node_pos = positions[node.value]
    if parent_pos is not None:
        px1, py1 = parent_pos[0] * 100, parent_pos[1] * 70 + 40
        px2, py2 = node_pos[0] * 100, node_pos[1] * 70 + 40
        dx, dy = px2 - px1, py2 - py1
        length = math.sqrt(dx*dx + dy*dy)
        angle = math.degrees(math.atan2(dy, dx))
        html.append(f'<div class="bst-edge" style="left: {px1}%; top: {py1}px; width: {length}%; transform: rotate({angle}deg);"></div>')
    html.append(draw_edges(node.left, positions, node_pos))
    html.append(draw_edges(node.right, positions, node_pos))
    return "".join(html)


def draw_nodes(node, positions, highlighted):
    if node is None:
        return ""
    html = []
    x, y = positions[node.value]
    classes = ["bst-node"]
    labels = []
    if node.value in highlighted.get("current", []):
        classes.append("highlight-current")
        labels.append('<span class="node-label current">current ↓</span>')
    if node.value in highlighted.get("new_node", []):
        classes.append("highlight-newnode")
        labels.append('<span class="node-label newnode">new_node ↓</span>')
    if node.value in highlighted.get("found", []):
        classes.append("highlight-found")
        labels.append('<span class="node-label found">found! ↓</span>')
    if node.value in highlighted.get("path", []):
        classes.append("highlight-path")
    if node.value in highlighted.get("target", []):
        classes.append("highlight-target")
    left_pct = x * 100
    top_px = y * 70 + 40
    html.append(f'<div class="{" ".join(classes)}" style="left: {left_pct}%; top: {top_px}px;">{"".join(labels)}{node.value}</div>')
    html.append(draw_nodes(node.left, positions, highlighted))
    html.append(draw_nodes(node.right, positions, highlighted))
    return "".join(html)


# ============================================================
# COMPETENCIES: ASCII TREE RENDERING
# ============================================================

def render_tree_ascii(node, lines, highlight, prefix="", is_left=True, is_root=True):
    if node is None:
        return
    if node["right"]:
        new_prefix = prefix + ("    " if is_root else ("│   " if is_left else "    "))
        render_tree_ascii(node["right"], lines, highlight, new_prefix, False, False)
    connector = "" if is_root else ("└── " if is_left else "┌── ")
    val_str = f"[{node['val']}]" if node["val"] in highlight else str(node["val"])
    lines.append(f"{prefix}{connector}{val_str}")
    if node["left"]:
        new_prefix = prefix + ("    " if is_root else ("    " if is_left else "│   "))
        render_tree_ascii(node["left"], lines, highlight, new_prefix, True, False)


def render_tree(values, var="bst", highlight=None):
    if not values:
        return f'<div style="font-family:monospace;color:#666;margin:10px 0">{var}.root → <em>None (empty)</em></div>'
    tree = build_tree_dict(values)
    lines = []
    render_tree_ascii(tree, lines, highlight or [])
    ascii_art = "\n".join(lines)
    return f'<div style="font-family:monospace;margin:15px 0"><span style="color:#666">{var}.root</span><pre style="background:#f8f8f8;padding:15px;border-radius:8px;overflow-x:auto;font-size:14px">{ascii_art}</pre></div>'


# ============================================================
# CODE TRACING: SNAPSHOT DEMOS
# ============================================================

def create_insert_demo():
    S = BSTSnapshot
    T = build_tree
    return [
        S(tree=None, explanation="Starting with an empty BST. We'll insert 50.", code_line="bst.insert(50)"),
        S(tree=None, floating_node=50, explanation="Create a new node containing 50.", code_line="new_node = Node(50)"),
        S(tree=None, floating_node=50, explanation="Is the tree empty? Yes! root is None.", code_line="if self.root is None:  # True"),
        S(tree=T([50]), highlighted_nodes={"new_node": [50]}, explanation="Since tree was empty, the new node becomes the root. Done!", code_line="self.root = new_node"),
        S(tree=T([50]), explanation="Now insert 30. Where does it go?", code_line="bst.insert(30)"),
        S(tree=T([50]), floating_node=30, explanation="Create a new node containing 30.", code_line="new_node = Node(30)"),
        S(tree=T([50]), highlighted_nodes={"current": [50]}, floating_node=30, explanation="Tree not empty. Start at root.", code_line="current = self.root"),
        S(tree=T([50]), highlighted_nodes={"current": [50]}, floating_node=30, comparison_text="30 < 50? YES → go LEFT", explanation="Compare 30 with current node (50). 30 is less, so we go left.", code_line="if value < current.value:  # 30 < 50 is True"),
        S(tree=T([50]), highlighted_nodes={"current": [50]}, floating_node=30, explanation="Is there a left child? No! current.left is None.", code_line="if current.left is None:  # True"),
        S(tree=T([50, 30]), highlighted_nodes={"current": [50], "new_node": [30]}, explanation="Insert 30 as the left child of 50. Done!", code_line="current.left = new_node"),
        S(tree=T([50, 30]), explanation="Insert 70. Think: where will it go?", code_line="bst.insert(70)"),
        S(tree=T([50, 30]), floating_node=70, explanation="Create a new node containing 70.", code_line="new_node = Node(70)"),
        S(tree=T([50, 30]), highlighted_nodes={"current": [50]}, floating_node=70, explanation="Start at root.", code_line="current = self.root"),
        S(tree=T([50, 30]), highlighted_nodes={"current": [50]}, floating_node=70, comparison_text="70 < 50? NO → go RIGHT", explanation="Compare 70 with current node (50). 70 is greater, so we go right.", code_line="if value < current.value:  # False → else"),
        S(tree=T([50, 30]), highlighted_nodes={"current": [50]}, floating_node=70, explanation="Is there a right child? No!", code_line="if current.right is None:  # True"),
        S(tree=T([50, 30, 70]), highlighted_nodes={"current": [50], "new_node": [70]}, explanation="Insert 70 as the right child of 50. Done!", code_line="current.right = new_node"),
        S(tree=T([50, 30, 70]), explanation="Insert 20. This requires traversing down.", code_line="bst.insert(20)"),
        S(tree=T([50, 30, 70]), floating_node=20, highlighted_nodes={"current": [50]}, comparison_text="20 < 50? YES → go LEFT", explanation="Start at root. 20 < 50, go left.", code_line="current = self.root"),
        S(tree=T([50, 30, 70]), floating_node=20, highlighted_nodes={"current": [30], "path": [50]}, comparison_text="20 < 30? YES → go LEFT", explanation="Now at 30. 20 < 30, go left again.", code_line="current = current.left"),
        S(tree=T([50, 30, 70]), floating_node=20, highlighted_nodes={"current": [30], "path": [50]}, explanation="Is there a left child of 30? No!", code_line="if current.left is None:  # True"),
        S(tree=T([50, 30, 70, 20]), highlighted_nodes={"current": [30], "new_node": [20], "path": [50]}, explanation="Insert 20 as the left child of 30. Done!", code_line="current.left = new_node"),
        S(tree=T([50, 30, 70, 20]), explanation="Insert 40. Where does it belong?", code_line="bst.insert(40)"),
        S(tree=T([50, 30, 70, 20]), floating_node=40, highlighted_nodes={"current": [50]}, comparison_text="40 < 50? YES → go LEFT", explanation="Start at root. 40 < 50, go left.", code_line="current = self.root"),
        S(tree=T([50, 30, 70, 20]), floating_node=40, highlighted_nodes={"current": [30], "path": [50]}, comparison_text="40 < 30? NO → go RIGHT", explanation="At 30. 40 > 30, go RIGHT!", code_line="current = current.left"),
        S(tree=T([50, 30, 70, 20]), floating_node=40, highlighted_nodes={"current": [30], "path": [50]}, explanation="Is there a right child of 30? No!", code_line="if current.right is None:  # True"),
        S(tree=T([50, 30, 70, 20, 40]), highlighted_nodes={"current": [30], "new_node": [40], "path": [50]}, explanation="Insert 40 as right child of 30. BST property maintained!", code_line="current.right = new_node"),
        S(tree=T([50, 30, 70, 20, 40]), explanation="Final tree: [50, 30, 70, 20, 40]. Left < Parent < Right at every node.", code_line="# Tree construction complete!"),
    ]


def create_search_demo():
    S = BSTSnapshot
    T = build_tree([50, 30, 70, 20, 40, 60, 80])
    return [
        S(tree=T, explanation="Starting tree. Let's search for value 40.", code_line="result = bst.search(40)"),
        S(tree=T, highlighted_nodes={"current": [50], "target": [40]}, explanation="Start at root. Looking for 40.", code_line="current = self.root"),
        S(tree=T, highlighted_nodes={"current": [50], "target": [40]}, comparison_text="50 == 40? NO", explanation="50 ≠ 40, keep searching.", code_line="while current and current.value != 40:"),
        S(tree=T, highlighted_nodes={"current": [50], "target": [40]}, comparison_text="40 < 50? YES → go LEFT", explanation="40 < 50, must be in left subtree.", code_line="if 40 < current.value:  # True"),
        S(tree=T, highlighted_nodes={"current": [30], "path": [50], "target": [40]}, explanation="Move to left child (30).", code_line="current = current.left"),
        S(tree=T, highlighted_nodes={"current": [30], "path": [50], "target": [40]}, comparison_text="30 == 40? NO", explanation="30 ≠ 40, keep searching.", code_line="while current and current.value != 40:"),
        S(tree=T, highlighted_nodes={"current": [30], "path": [50], "target": [40]}, comparison_text="40 < 30? NO → go RIGHT", explanation="40 > 30, go right.", code_line="if 40 < current.value:  # False"),
        S(tree=T, highlighted_nodes={"current": [40], "path": [50, 30]}, explanation="Move to right child (40).", code_line="current = current.right"),
        S(tree=T, highlighted_nodes={"current": [40], "path": [50, 30]}, comparison_text="40 == 40? YES!", explanation="Found it! Exit loop.", code_line="while current and current.value != 40:  # Exit"),
        S(tree=T, highlighted_nodes={"found": [40], "path": [50, 30]}, explanation="Return the node. Only visited 3 nodes - O(log n)!", code_line="return current  # Found!"),
        S(tree=T, explanation="Now search for 25 (doesn't exist).", code_line="result = bst.search(25)"),
        S(tree=T, highlighted_nodes={"current": [50]}, comparison_text="25 < 50 → LEFT", explanation="Start at root. 25 < 50, go left.", code_line="current = self.root"),
        S(tree=T, highlighted_nodes={"current": [30], "path": [50]}, comparison_text="25 < 30 → LEFT", explanation="At 30. 25 < 30, go left.", code_line="current = current.left"),
        S(tree=T, highlighted_nodes={"current": [20], "path": [50, 30]}, comparison_text="25 < 20? NO → RIGHT", explanation="At 20. 25 > 20, go right.", code_line="current = current.left"),
        S(tree=T, highlighted_nodes={"path": [50, 30, 20]}, explanation="20 has no right child! current = None.", code_line="current = current.right  # None!"),
        S(tree=T, highlighted_nodes={"path": [50, 30, 20]}, explanation="current is None. Value 25 not in tree.", code_line="return None  # Not found"),
    ]


def create_delete_demo():
    S = BSTSnapshot
    T = build_tree
    return [
        S(tree=T([50, 30, 70, 20, 40, 60, 80]), explanation="Delete 20 (a leaf node - no children).", code_line="bst.delete(20)"),
        S(tree=T([50, 30, 70, 20, 40, 60, 80]), highlighted_nodes={"target": [20], "current": [30]}, explanation="Find 20. Its parent is 30.", code_line="# parent = 30, current = 20"),
        S(tree=T([50, 30, 70, 20, 40, 60, 80]), highlighted_nodes={"found": [20], "current": [30]}, explanation="20 is a leaf (no children). Easiest case!", code_line="if not current.left and not current.right:  # LEAF"),
        S(tree=T([50, 30, 70, 40, 60, 80]), highlighted_nodes={"current": [30]}, explanation="Just set parent.left = None. Done!", code_line="parent.left = None"),
        S(tree=T([50, 30, 70, 20, 40, 80]), explanation="Delete 70 (has one child: 80).", code_line="bst.delete(70)"),
        S(tree=T([50, 30, 70, 20, 40, 80]), highlighted_nodes={"target": [70], "new_node": [80]}, explanation="70 has only right child (80). Bypass 70!", code_line="if current.left is None:  # One child"),
        S(tree=T([50, 30, 80, 20, 40]), highlighted_nodes={"new_node": [80]}, explanation="parent.right = current.right. 80 replaces 70!", code_line="parent.right = current.right"),
        S(tree=T([50, 30, 70, 20, 40, 60, 80]), explanation="Delete 30 (has TWO children: 20 and 40).", code_line="bst.delete(30)"),
        S(tree=T([50, 30, 70, 20, 40, 60, 80]), highlighted_nodes={"target": [30]}, explanation="30 has two children. Need a replacement!", code_line="# current = 30 (left=20, right=40)"),
        S(tree=T([50, 30, 70, 20, 40, 60, 80]), highlighted_nodes={"target": [30], "found": [40]}, explanation="Find IN-ORDER SUCCESSOR: smallest in right subtree = 40", code_line="successor = 40  # (right, then left as far as possible)"),
        S(tree=T([50, 30, 70, 20, 40, 60, 80]), highlighted_nodes={"current": [30], "found": [40]}, explanation="Copy successor's value into target node.", code_line="current.value = successor.value  # 30 → 40"),
        S(tree=T([50, 40, 70, 20, 60, 80]), highlighted_nodes={"new_node": [40]}, explanation="Delete the successor (was leaf). Done! BST property preserved.", code_line="# Delete successor, tree valid!"),
    ]


# ============================================================
# COMPETENCIES: SKILLS DATA
# ============================================================

SKILLS = {
    "navigation": ("1", "Tree Navigation", "Follow .left and .right to find values"),
    "bst_property": ("2", "BST Property", "Left < Parent < Right at every node"),
    "search_path": ("3", "Search Path", "Which nodes are visited when searching?"),
    "insert_position": ("4", "Insert Position", "Where does a new value go?"),
    "height_balance": ("5", "Height & Balance", "How tree shape affects operations"),
    "traversals": ("6", "Traversal Orders", "Inorder, preorder, postorder results"),
    "delete_cases": ("7", "Delete Cases", "Leaf, one child, two children"),
    "successor": ("8", "Successor/Predecessor", "Find in-order next/previous"),
}

QUESTIONS = {
    "navigation": [
        ([50, 30, 70], "bst", None, "bst.root.value", "50", ["30", "70", "None"]),
        ([50, 30, 70], "bst", None, "bst.root.left.value", "30", ["50", "70", "None"]),
        ([50, 30, 70], "bst", None, "bst.root.right.value", "70", ["50", "30", "None"]),
        ([50, 30, 70, 20, 40], "bst", None, "bst.root.left.left.value", "20", ["30", "40", "None"]),
        ([50, 30, 70, 20, 40], "bst", None, "bst.root.left.right.value", "40", ["30", "20", "None"]),
        ([50, 30, 70, 60, 80], "bst", None, "bst.root.right.left.value", "60", ["70", "80", "None"]),
        ([50, 30, 70, 60, 80], "bst", None, "bst.root.right.right.value", "80", ["70", "60", "None"]),
        ([50, 30, 70], "bst", None, "bst.root.left.left", "None", ["20", "Error", "30"]),
        ([50, 30, 70, 20], "bst", None, "bst.root.left.right", "None", ["20", "40", "Error"]),
        ([50, 25, 75, 10, 30], "bst", None, "bst.root.left.left.value", "10", ["25", "30", "None"]),
        ([100, 50, 150, 25, 75], "bst", None, "bst.root.left.right.value", "75", ["50", "25", "None"]),
        ([40, 20, 60, 10, 30, 50, 70], "bst", None, "bst.root.right.left.value", "50", ["60", "70", "None"]),
    ],
    "bst_property": [
        ([50, 30, 70], "bst", "# Is this a valid BST?", "Valid BST?", "Yes", ["No", "Error", "Maybe"]),
        ([50, 30, 70, 20, 40, 60, 80], "bst", "# All left descendants < 50?", "All left < root?", "Yes (20,30,40 < 50)", ["No", "Only direct child", "Error"]),
        ([50, 30, 70], "bst", "# If we insert 45, where?", "45 goes where?", "Right child of 30", ["Left of 30", "Right of 50", "Left of 70"]),
        ([50, 30, 70], "bst", "# If we insert 25, where?", "25 goes where?", "Left child of 30", ["Right of 30", "Left of 50", "Right of 70"]),
        ([50, 30, 70], "bst", "# If we insert 65, where?", "65 goes where?", "Left child of 70", ["Right of 70", "Right of 50", "Left of 30"]),
        ([50, 30, 70, 20, 40], "bst", "# Largest in left subtree?", "Largest left?", "40", ["30", "20", "50"]),
        ([50, 30, 70, 60, 80], "bst", "# Smallest in right subtree?", "Smallest right?", "60", ["70", "80", "50"]),
        ([50, 30, 70], "bst", "# Can 35 be right of 30?", "35 valid there?", "Yes (30 < 35 < 50)", ["No", "Only if < 30", "Error"]),
        ([50, 30, 70], "bst", "# Can 55 be left of 70?", "55 valid there?", "Yes (50 < 55 < 70)", ["No", "Only if > 70", "Error"]),
        ([50, 30, 70], "bst", "# Can 75 be left of 70?", "75 valid there?", "No (75 > 70)", ["Yes", "Maybe", "Error"]),
        ([50, 30, 70, 20, 40], "bst", "# Which must be true?", "BST rule?", "20 < 30 < 40 < 50", ["20 < 40 < 30", "30 < 20 < 40", "None"]),
        ([100], "bst", "# Insert 50, then 150", "Valid result?", "Yes - 50 left, 150 right", ["No", "50 right, 150 left", "Error"]),
    ],
    "search_path": [
        ([50, 30, 70, 20, 40, 60, 80], "bst", "# Search for 40", "Path to 40?", "50 → 30 → 40", ["50 → 70 → 40", "50 → 40", "30 → 40"]),
        ([50, 30, 70, 20, 40, 60, 80], "bst", "# Search for 60", "Path to 60?", "50 → 70 → 60", ["50 → 60", "50 → 30 → 60", "70 → 60"]),
        ([50, 30, 70, 20, 40, 60, 80], "bst", "# Search for 20", "Path to 20?", "50 → 30 → 20", ["50 → 20", "30 → 20", "50 → 70 → 20"]),
        ([50, 30, 70, 20, 40, 60, 80], "bst", "# Search for 80", "Path to 80?", "50 → 70 → 80", ["50 → 80", "70 → 80", "50 → 30 → 80"]),
        ([50, 30, 70, 20, 40, 60, 80], "bst", "# Search for 50", "Path to 50?", "50 (found at root)", ["None", "30 → 50", "70 → 50"]),
        ([50, 30, 70, 20, 40, 60, 80], "bst", "# Search for 35", "Path for 35?", "50 → 30 → 40 → None", ["50 → 30 → None", "50 → 35", "Not found"]),
        ([50, 30, 70, 20, 40, 60, 80], "bst", "# Search for 55", "Path for 55?", "50 → 70 → 60 → None", ["50 → 70 → None", "50 → 55", "Found"]),
        ([50, 30, 70, 20, 40, 60, 80], "bst", "# Nodes visited for 40?", "Count visited?", "3 (50, 30, 40)", ["2", "4", "1"]),
        ([50, 25, 75, 10, 30, 60, 90], "bst", "# Search for 10", "Path to 10?", "50 → 25 → 10", ["50 → 10", "25 → 10", "50 → 75 → 10"]),
        ([50, 25, 75, 10, 30, 60, 90], "bst", "# Search for 90", "Path to 90?", "50 → 75 → 90", ["50 → 90", "75 → 90", "50 → 25 → 90"]),
        ([50, 25, 75, 10, 30, 60, 90], "bst", "# Search for 45", "Path for 45?", "50 → 25 → 30 → None", ["50 → 45", "Found", "50 → 25 → None"]),
        ([100, 50, 150, 25, 75, 125, 175], "bst", "# Search for 75", "Path to 75?", "100 → 50 → 75", ["100 → 75", "50 → 75", "100 → 150 → 75"]),
    ],
    "insert_position": [
        ([50], "bst", "# Insert 30", "30 becomes?", "Left child of 50", ["Right of 50", "New root", "Error"]),
        ([50], "bst", "# Insert 70", "70 becomes?", "Right child of 50", ["Left of 50", "New root", "Error"]),
        ([50, 30], "bst", "# Insert 20", "20 becomes?", "Left child of 30", ["Right of 30", "Left of 50", "Error"]),
        ([50, 30], "bst", "# Insert 40", "40 becomes?", "Right child of 30", ["Left of 30", "Right of 50", "Error"]),
        ([50, 30, 70], "bst", "# Insert 60", "60 becomes?", "Left child of 70", ["Right of 70", "Right of 50", "Left of 30"]),
        ([50, 30, 70], "bst", "# Insert 80", "80 becomes?", "Right child of 70", ["Left of 70", "Right of 50", "Error"]),
        ([50, 30, 70, 20, 40], "bst", "# Insert 35", "35 becomes?", "Left child of 40", ["Right of 30", "Left of 30", "Right of 40"]),
        ([50, 30, 70, 20, 40], "bst", "# Insert 25", "25 becomes?", "Right child of 20", ["Left of 20", "Left of 30", "Right of 30"]),
        ([50, 30, 70, 60, 80], "bst", "# Insert 65", "65 becomes?", "Right child of 60", ["Left of 60", "Left of 70", "Right of 70"]),
        ([50, 30, 70, 60, 80], "bst", "# Insert 55", "55 becomes?", "Left child of 60", ["Right of 60", "Right of 50", "Left of 70"]),
        ([100, 50, 150], "bst", "# Insert 25", "25 becomes?", "Left child of 50", ["Right of 50", "Left of 100", "Error"]),
        ([100, 50, 150], "bst", "# Insert 175", "175 becomes?", "Right child of 150", ["Left of 150", "Right of 100", "Error"]),
    ],
    "height_balance": [
        ([50, 30, 70], "bst", "# Tree height?", "Height?", "2", ["1", "3", "0"]),
        ([50, 30, 70, 20, 40, 60, 80], "bst", "# Tree height?", "Height?", "3", ["2", "4", "7"]),
        ([50], "bst", "# Tree height?", "Height?", "1", ["0", "2", "None"]),
        ([10, 20, 30, 40, 50], "bst", "# Insert order matters!", "Height?", "5 (degenerate)", ["3", "2", "1"]),
        ([30, 20, 40, 10, 50], "bst", "# More balanced insert", "Height?", "3", ["5", "2", "4"]),
        ([50, 30, 70, 20, 40, 60, 80], "bst", "# Max nodes at height 3?", "Max possible?", "7", ["8", "6", "3"]),
        ([10, 20, 30, 40], "bst", "# Shape of this tree?", "Shape?", "Right-leaning chain", ["Balanced", "Left-leaning", "Full"]),
        ([40, 30, 20, 10], "bst", "# Shape of this tree?", "Shape?", "Left-leaning chain", ["Balanced", "Right-leaning", "Full"]),
        ([50, 25, 75, 10, 30, 60, 90], "bst", "# Is this balanced?", "Balanced?", "Yes (roughly)", ["No", "Error", "Can't tell"]),
        ([50, 30, 70, 20, 40, 60, 80], "bst", "# Search worst case?", "Worst case?", "O(log n) = ~3 steps", ["O(n)", "O(1)", "O(n²)"]),
        ([10, 20, 30, 40, 50, 60, 70], "bst", "# Search worst case?", "Worst case?", "O(n) = 7 steps", ["O(log n)", "O(1)", "O(n²)"]),
        ([50, 30, 70], "bst", "# Left subtree height?", "Left height?", "1", ["2", "0", "3"]),
    ],
    "traversals": [
        ([50, 30, 70], "bst", "# Inorder traversal", "Inorder?", "30, 50, 70", ["50, 30, 70", "70, 50, 30", "30, 70, 50"]),
        ([50, 30, 70], "bst", "# Preorder traversal", "Preorder?", "50, 30, 70", ["30, 50, 70", "30, 70, 50", "70, 30, 50"]),
        ([50, 30, 70], "bst", "# Postorder traversal", "Postorder?", "30, 70, 50", ["50, 30, 70", "30, 50, 70", "70, 50, 30"]),
        ([50, 30, 70, 20, 40], "bst", "# Inorder traversal", "Inorder?", "20, 30, 40, 50, 70", ["50, 30, 20, 40, 70", "30, 20, 40, 50, 70", "20, 40, 30, 70, 50"]),
        ([50, 30, 70, 60, 80], "bst", "# Inorder traversal", "Inorder?", "30, 50, 60, 70, 80", ["50, 30, 70, 60, 80", "30, 60, 50, 80, 70", "80, 70, 60, 50, 30"]),
        ([50, 30, 70, 20, 40], "bst", "# Preorder traversal", "Preorder?", "50, 30, 20, 40, 70", ["20, 30, 40, 50, 70", "50, 70, 30, 40, 20", "30, 50, 70, 20, 40"]),
        ([50, 30, 70, 20, 40], "bst", "# Postorder traversal", "Postorder?", "20, 40, 30, 70, 50", ["50, 30, 70, 20, 40", "20, 30, 40, 50, 70", "70, 40, 20, 30, 50"]),
        ([50, 30, 70, 20, 40, 60, 80], "bst", "# Inorder = sorted?", "Inorder sorted?", "Yes, always!", ["No", "Sometimes", "Only if balanced"]),
        ([100, 50, 150, 25, 75], "bst", "# Inorder traversal", "Inorder?", "25, 50, 75, 100, 150", ["100, 50, 25, 75, 150", "50, 25, 75, 100, 150", "25, 75, 50, 150, 100"]),
        ([40, 20, 60, 10, 30], "bst", "# Preorder first 3?", "First 3 preorder?", "40, 20, 10", ["10, 20, 30", "40, 60, 20", "20, 40, 60"]),
        ([40, 20, 60, 10, 30], "bst", "# Postorder last?", "Last postorder?", "40 (root)", ["60", "30", "10"]),
        ([50, 30, 70], "bst", "# Which visits root first?", "Root first?", "Preorder", ["Inorder", "Postorder", "All of them"]),
    ],
    "delete_cases": [
        ([50, 30, 70, 20, 40], "bst", "# Delete 20 (leaf)", "Case type?", "Leaf - just remove", ["One child", "Two children", "Error"]),
        ([50, 30, 70, 20, 40], "bst", "# Delete 40 (leaf)", "Case type?", "Leaf - just remove", ["One child", "Two children", "Error"]),
        ([50, 30, 70, 20], "bst", "# Delete 30 (one child)", "Case type?", "One child - bypass", ["Leaf", "Two children", "Error"]),
        ([50, 30, 70, 80], "bst", "# Delete 70 (one child)", "Case type?", "One child - bypass", ["Leaf", "Two children", "Error"]),
        ([50, 30, 70, 20, 40], "bst", "# Delete 30 (two children)", "Case type?", "Two children - successor", ["Leaf", "One child", "Error"]),
        ([50, 30, 70, 60, 80], "bst", "# Delete 70 (two children)", "Case type?", "Two children - successor", ["Leaf", "One child", "Error"]),
        ([50, 30, 70, 20, 40], "bst", "# After deleting 20?", "30's left?", "None", ["40", "50", "Error"]),
        ([50, 30, 70, 20], "bst", "# After deleting 30?", "50's left?", "20", ["None", "70", "Error"]),
        ([50, 30, 70, 20, 40], "bst", "# Delete 30, successor?", "Successor of 30?", "40", ["20", "50", "70"]),
        ([50, 30, 70, 60, 80], "bst", "# Delete 70, successor?", "Successor of 70?", "80", ["60", "50", "None"]),
        ([50, 30, 70, 20, 40, 35], "bst", "# Delete 30, successor?", "Successor of 30?", "35", ["40", "20", "50"]),
        ([50, 30, 70, 20, 40], "bst", "# After delete 30 with 40", "Tree valid?", "Yes - 40 replaces 30", ["No", "Error", "Maybe"]),
    ],
    "successor": [
        ([50, 30, 70, 20, 40, 60, 80], "bst", "# In-order successor of 30?", "Successor?", "40", ["20", "50", "None"]),
        ([50, 30, 70, 20, 40, 60, 80], "bst", "# In-order successor of 50?", "Successor?", "60", ["70", "40", "None"]),
        ([50, 30, 70, 20, 40, 60, 80], "bst", "# In-order successor of 70?", "Successor?", "80", ["60", "None", "50"]),
        ([50, 30, 70, 20, 40, 60, 80], "bst", "# In-order successor of 80?", "Successor?", "None (largest)", ["70", "50", "Error"]),
        ([50, 30, 70, 20, 40, 60, 80], "bst", "# In-order predecessor of 50?", "Predecessor?", "40", ["30", "20", "None"]),
        ([50, 30, 70, 20, 40, 60, 80], "bst", "# In-order predecessor of 70?", "Predecessor?", "60", ["50", "80", "None"]),
        ([50, 30, 70, 20, 40, 60, 80], "bst", "# In-order predecessor of 20?", "Predecessor?", "None (smallest)", ["30", "10", "Error"]),
        ([50, 30, 70, 20, 40, 60, 80], "bst", "# Successor = ?", "Successor rule?", "Smallest in right subtree", ["Largest in left", "Parent", "Right child"]),
        ([50, 30, 70, 20, 40, 60, 80], "bst", "# Predecessor = ?", "Predecessor rule?", "Largest in left subtree", ["Smallest in right", "Parent", "Left child"]),
        ([50, 30, 70, 40, 35, 45], "bst", "# Successor of 35?", "Successor?", "40", ["45", "30", "50"]),
        ([50, 30, 70, 20, 40, 35], "bst", "# Successor of 30?", "Successor?", "35", ["40", "20", "50"]),
        ([50, 25, 75, 10, 30, 27], "bst", "# Successor of 25?", "Successor?", "27", ["30", "10", "50"]),
    ],
}


# ============================================================
# MAIN APP
# ============================================================

st.title("BST Visualizer")
st.markdown("*Step through Binary Search Tree operations to understand the recursive structure*")

# Top-level tabs
main_tab1, main_tab2 = st.tabs(["Code Tracing", "Competencies"])

# ============================================================
# CODE TRACING TAB
# ============================================================
with main_tab1:
    op_tab1, op_tab2, op_tab3 = st.tabs(["Insert", "Search", "Delete"])
    
    with op_tab1:
        st.subheader("Building a BST with insert()")
        if "insert_step" not in st.session_state:
            st.session_state.insert_step = 0
        snapshots = create_insert_demo()
        step = st.session_state.insert_step
        code_col, viz_col = st.columns([1, 2])
        with code_col:
            st.code('''def insert(self, value):
    new_node = Node(value)
    if self.root is None:
        self.root = new_node
        return
    current = self.root
    while True:
        if value < current.value:
            if current.left is None:
                current.left = new_node
                return
            current = current.left
        else:
            if current.right is None:
                current.right = new_node
                return
            current = current.right''', language='python')
        with viz_col:
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                if st.button("← Previous", disabled=(step == 0), key="insert_prev"):
                    st.session_state.insert_step -= 1
                    st.rerun()
            with col2:
                if st.button("Next →", disabled=(step >= len(snapshots)-1), key="insert_next"):
                    st.session_state.insert_step += 1
                    st.rerun()
            with col3:
                if st.button("Reset", key="insert_reset"):
                    st.session_state.insert_step = 0
                    st.rerun()
            st.markdown(f"**Step {step + 1} of {len(snapshots)}**")
            st.markdown(render_bst_snapshot(snapshots[step], "bst"), unsafe_allow_html=True)
    
    with op_tab2:
        st.subheader("Finding values with search()")
        if "search_step" not in st.session_state:
            st.session_state.search_step = 0
        snapshots = create_search_demo()
        step = st.session_state.search_step
        code_col, viz_col = st.columns([1, 2])
        with code_col:
            st.code('''def search(self, value):
    current = self.root
    while current is not None:
        if current.value == value:
            return current  # Found!
        elif value < current.value:
            current = current.left
        else:
            current = current.right
    return None  # Not found''', language='python')
        with viz_col:
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                if st.button("← Previous", disabled=(step == 0), key="search_prev"):
                    st.session_state.search_step -= 1
                    st.rerun()
            with col2:
                if st.button("Next →", disabled=(step >= len(snapshots)-1), key="search_next"):
                    st.session_state.search_step += 1
                    st.rerun()
            with col3:
                if st.button("Reset", key="search_reset"):
                    st.session_state.search_step = 0
                    st.rerun()
            st.markdown(f"**Step {step + 1} of {len(snapshots)}**")
            st.markdown(render_bst_snapshot(snapshots[step], "bst"), unsafe_allow_html=True)
    
    with op_tab3:
        st.subheader("Removing nodes with delete()")
        if "delete_step" not in st.session_state:
            st.session_state.delete_step = 0
        snapshots = create_delete_demo()
        step = st.session_state.delete_step
        code_col, viz_col = st.columns([1, 2])
        with code_col:
            st.code('''def delete(self, value):
    # Find node and parent
    parent, current = None, self.root
    while current and current.value != value:
        parent = current
        if value < current.value:
            current = current.left
        else:
            current = current.right
    
    # CASE 1: Leaf node
    if not current.left and not current.right:
        parent.left/right = None
    
    # CASE 2: One child
    elif not current.left or not current.right:
        child = current.left or current.right
        parent.left/right = child
    
    # CASE 3: Two children
    else:
        successor = current.right
        while successor.left:
            successor = successor.left
        current.value = successor.value
        # delete successor''', language='python')
        with viz_col:
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                if st.button("← Previous", disabled=(step == 0), key="delete_prev"):
                    st.session_state.delete_step -= 1
                    st.rerun()
            with col2:
                if st.button("Next →", disabled=(step >= len(snapshots)-1), key="delete_next"):
                    st.session_state.delete_step += 1
                    st.rerun()
            with col3:
                if st.button("Reset", key="delete_reset"):
                    st.session_state.delete_step = 0
                    st.rerun()
            st.markdown(f"**Step {step + 1} of {len(snapshots)}**")
            st.markdown(render_bst_snapshot(snapshots[step], "bst"), unsafe_allow_html=True)


# ============================================================
# COMPETENCIES TAB
# ============================================================
with main_tab2:
    st.markdown("### Select a skill to practice:")
    
    cols = st.columns(4)
    for i, (key, (num, name, desc)) in enumerate(SKILLS.items()):
        with cols[i % 4]:
            if st.button(f"{num}. {name}", key=f"btn_{key}", use_container_width=True, help=desc):
                st.session_state.skill = key
                st.session_state.questions = None
                st.session_state.idx = 0
                st.session_state.score = 0
                st.session_state.answered = False
                st.rerun()
    
    st.markdown("---")
    
    if "skill" in st.session_state and st.session_state.skill:
        skill = st.session_state.skill
        num, name, desc = SKILLS[skill]
        st.subheader(f"Skill {num}: {name}")
        st.caption(desc)
        
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
            values, var, code, expr, answer, distractors = qs[idx]
            st.progress(idx / len(qs))
            st.markdown(f"**Question {idx+1}/5** | Score: {st.session_state.score}/{idx}")
            st.markdown(render_tree(values, var), unsafe_allow_html=True)
            if code:
                st.code(code, language="python")
            st.markdown(f"### `{expr}`")
            
            if f"choices_{idx}" not in st.session_state:
                choices = [answer] + distractors
                random.shuffle(choices)
                st.session_state[f"choices_{idx}"] = choices
            choices = st.session_state[f"choices_{idx}"]
            
            if not st.session_state.answered:
                choice_cols = st.columns(len(choices))
                for i, c in enumerate(choices):
                    with choice_cols[i]:
                        if st.button(c, key=f"c_{i}", use_container_width=True):
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
            score = st.session_state.score
            st.success(f"### Round complete. Score: {score}/5")
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
