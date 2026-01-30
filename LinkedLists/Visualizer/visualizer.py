"""
Linked List Visualizer - Step Through Demo
Run with: streamlit run visualizer.py
"""

import streamlit as st
from dataclasses import dataclass
from typing import Optional, List

st.set_page_config(page_title="Linked List Visualizer", layout="wide")

@dataclass
class Snapshot:
    nodes: List[str]
    pointer_positions: dict
    new_node_data: Optional[str]
    explanation: str
    code_line: str

def render_snapshot(snap: Snapshot, list_var: str = "week"):
    css = """
    <style>
    .ll-container { display: flex; align-items: center; gap: 0; margin: 20px 0; font-family: monospace; }
    .node-box { border: 3px solid #333; border-radius: 8px; padding: 15px 20px; background: white; color: #333; min-width: 80px; text-align: center; position: relative; font-size: 14px; }
    .node-box.highlight-current { border-color: #e63946; background: #fff0f0; box-shadow: 0 0 10px rgba(230, 57, 70, 0.4); }
    .node-box.highlight-newnode { border-color: #2a9d8f; background: #f0fff0; box-shadow: 0 0 10px rgba(42, 157, 143, 0.4); }
    .arrow { font-size: 24px; color: #3b82f6; margin: 0 5px; }
    .none-box { color: #888; font-style: italic; padding: 15px 10px; }
    .pointer-label { position: absolute; top: -25px; left: 50%; transform: translateX(-50%); font-size: 12px; font-weight: bold; }
    .pointer-label.current { color: #e63946; }
    .pointer-label.newnode { color: #2a9d8f; }
    .floating-node { display: flex; align-items: center; margin-top: 20px; gap: 10px; }
    .floating-label { color: #2a9d8f; font-weight: bold; font-family: monospace; }
    .code-line { background: #2d2d2d; color: #f8f8f2; padding: 10px 15px; border-radius: 5px; font-family: monospace; font-size: 14px; margin: 10px 0; }
    .explanation { background: #f0f7ff; border-left: 4px solid #3b82f6; padding: 10px 15px; margin: 10px 0; }
    .head-label { font-size: 12px; color: #666; margin-bottom: 5px; font-family: monospace; }
    </style>
    """
    html = [css, f'<div class="head-label">{list_var}.head</div>', '<div class="ll-container">']
    
    if not snap.nodes:
        html.append('<span class="none-box">None (empty list)</span>')
    else:
        for i, data in enumerate(snap.nodes):
            classes = ["node-box"]
            labels = []
            if snap.pointer_positions.get("current") == i:
                classes.append("highlight-current")
                labels.append('<span class="pointer-label current">current ↓</span>')
            if snap.pointer_positions.get("new_node") == i:
                classes.append("highlight-newnode")
                labels.append('<span class="pointer-label newnode">new_node ↓</span>')
            html.append(f'<div class="{" ".join(classes)}">{"".join(labels)}{data}</div>')
            html.append('<span class="arrow">→</span>')
            if i == len(snap.nodes) - 1:
                html.append('<span class="none-box">None</span>')
    
    html.append('</div>')
    
    if snap.new_node_data and snap.pointer_positions.get("new_node") is None:
        html.append(f'<div class="floating-node"><span class="floating-label">new_node →</span>'
                   f'<div class="node-box highlight-newnode">{snap.new_node_data}</div>'
                   f'<span class="arrow">→</span><span class="none-box">None</span></div>')
    
    if snap.code_line:
        html.append(f'<div class="code-line">{snap.code_line}</div>')
    if snap.explanation:
        html.append(f'<div class="explanation">{snap.explanation}</div>')
    
    return "".join(html)


def create_append_demo():
    """Demonstrates append operation, starting from empty list."""
    return [
        # Append "Mon" to empty list
        Snapshot([], {}, None,
                "Starting with an empty linked list. We'll append 'Mon'.",
                "week.append('Mon')"),
        Snapshot([], {}, "Mon",
                "Create a new node containing 'Mon'. It's not connected to anything yet.",
                "new_node = Node('Mon')"),
        Snapshot([], {}, "Mon",
                "Is the list empty? Yes! self.head is None.",
                "if self.head is None:  # True"),
        Snapshot(["Mon"], {"new_node": 0}, None,
                "Since list was empty, the new node becomes the head. Done!",
                "self.head = new_node"),
        
        # Append "Tue" 
        Snapshot(["Mon"], {}, None,
                "Now append 'Tue' to our one-node list.",
                "week.append('Tue')"),
        Snapshot(["Mon"], {}, "Tue",
                "Create a new node containing 'Tue'.",
                "new_node = Node('Tue')"),
        Snapshot(["Mon"], {}, "Tue",
                "Is the list empty? No, head exists.",
                "if self.head is None:  # False"),
        Snapshot(["Mon"], {"current": 0}, "Tue",
                "Start at the head. We need to find the last node.",
                "current = self.head"),
        Snapshot(["Mon"], {"current": 0}, "Tue",
                "Is current.next None? Yes! Mon is the last node. Exit loop immediately.",
                "while current.next:  # False (Mon.next is None)"),
        Snapshot(["Mon", "Tue"], {"current": 0, "new_node": 1}, None,
                "Link the last node to our new node. Mon.next = new_node.",
                "current.next = new_node"),
        
        # Append "Wed"
        Snapshot(["Mon", "Tue"], {}, None,
                "Append 'Wed'. Now we'll see traversal in action.",
                "week.append('Wed')"),
        Snapshot(["Mon", "Tue"], {}, "Wed",
                "Create a new node containing 'Wed'.",
                "new_node = Node('Wed')"),
        Snapshot(["Mon", "Tue"], {"current": 0}, "Wed",
                "Start at head.",
                "current = self.head"),
        Snapshot(["Mon", "Tue"], {"current": 0}, "Wed",
                "Is current.next None? No, it's Tue. Enter the loop.",
                "while current.next:  # True (Mon.next is Tue)"),
        Snapshot(["Mon", "Tue"], {"current": 1}, "Wed",
                "Move current forward. Now pointing at Tue.",
                "current = current.next"),
        Snapshot(["Mon", "Tue"], {"current": 1}, "Wed",
                "Is current.next None? Yes! Tue is the last node. Exit loop.",
                "while current.next:  # False (Tue.next is None)"),
        Snapshot(["Mon", "Tue", "Wed"], {"current": 1, "new_node": 2}, None,
                "Link Tue to Wed. Tue.next = new_node.",
                "current.next = new_node"),
        
        # Append "Thu"
        Snapshot(["Mon", "Tue", "Wed"], {}, None,
                "One more: append 'Thu'. Watch current chase through the list.",
                "week.append('Thu')"),
        Snapshot(["Mon", "Tue", "Wed"], {}, "Thu",
                "Create a new node containing 'Thu'.",
                "new_node = Node('Thu')"),
        Snapshot(["Mon", "Tue", "Wed"], {"current": 0}, "Thu",
                "Start at head (Mon).",
                "current = self.head"),
        Snapshot(["Mon", "Tue", "Wed"], {"current": 0}, "Thu",
                "Mon.next exists (Tue). Continue.",
                "while current.next:  # True"),
        Snapshot(["Mon", "Tue", "Wed"], {"current": 1}, "Thu",
                "Move to Tue.",
                "current = current.next"),
        Snapshot(["Mon", "Tue", "Wed"], {"current": 1}, "Thu",
                "Tue.next exists (Wed). Continue.",
                "while current.next:  # True"),
        Snapshot(["Mon", "Tue", "Wed"], {"current": 2}, "Thu",
                "Move to Wed.",
                "current = current.next"),
        Snapshot(["Mon", "Tue", "Wed"], {"current": 2}, "Thu",
                "Wed.next is None. Exit loop. Found the last node!",
                "while current.next:  # False"),
        Snapshot(["Mon", "Tue", "Wed", "Thu"], {"current": 2, "new_node": 3}, None,
                "Link Wed to Thu. Done! We traversed the entire list to find the end.",
                "current.next = new_node"),
    ]


def create_replace_demo():
    """Demonstrates replace operation."""
    days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    return [
        Snapshot(days.copy(), {}, None, 
                "Starting state: linked list of weekdays. Goal: replace 'Thu' with 'Taco Thu'.", 
                "week.replace('Thu', 'Taco Thu')"),
        Snapshot(days.copy(), {}, "Taco Thu", 
                "Create the new node. It exists in memory but isn't connected yet.", 
                "new_node = Node('Taco Thu')"),
        Snapshot(days.copy(), {}, "Taco Thu", 
                "Is head the target? head.data is 'Mon', not 'Thu'. Go to else branch.", 
                "if self.head.data == old_data:  # False"),
        Snapshot(days.copy(), {"current": 0}, "Taco Thu", 
                "Start 'current' at head. Goal: find the node BEFORE Thu (so we can rewire).", 
                "current = self.head"),
        Snapshot(days.copy(), {"current": 0}, "Taco Thu", 
                "Is current.next our target? current.next.data is 'Tue', not 'Thu'. Keep going.", 
                "while current.next.data != 'Thu':  # True"),
        Snapshot(days.copy(), {"current": 1}, "Taco Thu", 
                "Move current forward by following .next reference. Now pointing at Tue.", 
                "current = current.next"),
        Snapshot(days.copy(), {"current": 1}, "Taco Thu", 
                "Check again: current.next.data is 'Wed', not 'Thu'. Keep going.", 
                "while current.next.data != 'Thu':  # True"),
        Snapshot(days.copy(), {"current": 2}, "Taco Thu", 
                "Move current forward again. Now pointing at Wed.", 
                "current = current.next"),
        Snapshot(days.copy(), {"current": 2}, "Taco Thu", 
                "Check: current.next.data IS 'Thu'! Exit loop. current is now at the node BEFORE our target.", 
                "while current.next.data != 'Thu':  # False - exit"),
        Snapshot(days.copy(), {"current": 2}, "Taco Thu", 
                "Pointer surgery step 1: new_node.next = current.next.next. Taco Thu now points to Fri.", 
                "new_node.next = current.next.next"),
        Snapshot(["Mon", "Tue", "Wed", "Taco Thu", "Fri"], {"current": 2, "new_node": 3}, None, 
                "Pointer surgery step 2: current.next = new_node. Wed now points to Taco Thu. Old Thu is orphaned!", 
                "current.next = new_node"),
        Snapshot(["Mon", "Tue", "Wed", "Taco Thu", "Fri"], {}, None, 
                "Done! Thu has been replaced. The old Thu node will be garbage collected.", 
                "# Replacement complete"),
    ]


# Main app
st.title("Linked List Visualizer")
st.markdown("*Step through linked list operations to see pointer chasing in action*")

tab1, tab2 = st.tabs(["Append Operation", "Replace Operation"])

# ===================== APPEND TAB =====================
with tab1:
    st.subheader("Building a list with append()")
    
    if "append_step" not in st.session_state:
        st.session_state.append_step = 0
    
    snapshots = create_append_demo()
    step = st.session_state.append_step
    
    code_col, viz_col = st.columns([1, 2])
    
    with code_col:
        st.code('''def append(self, data):
    new_node = Node(data)
    
    # Special case: empty list
    if self.head is None:
        self.head = new_node
        return
    
    # Traverse to find last node
    current = self.head
    while current.next:
        current = current.next
    
    # Link last node to new node
    current.next = new_node''', language='python')
    
    with viz_col:
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            if st.button("← Previous", disabled=(step == 0), key="append_prev"):
                st.session_state.append_step -= 1
                st.rerun()
        with col2:
            if st.button("Next →", disabled=(step == len(snapshots)-1), key="append_next"):
                st.session_state.append_step += 1
                st.rerun()
        with col3:
            if st.button("Reset", key="append_reset"):
                st.session_state.append_step = 0
                st.rerun()
        
        st.markdown(f"**Step {step + 1} of {len(snapshots)}**")
        st.markdown(render_snapshot(snapshots[step], "week"), unsafe_allow_html=True)


# ===================== REPLACE TAB =====================
with tab2:
    st.subheader("Replacing a node with replace()")
    
    if "replace_step" not in st.session_state:
        st.session_state.replace_step = 0
    
    snapshots = create_replace_demo()
    step = st.session_state.replace_step
    
    code_col, viz_col = st.columns([1, 2])
    
    with code_col:
        st.code('''def replace(self, old_data, new_data):
    new_node = Node(new_data)
    
    # Special case: replacing head
    if self.head.data == old_data:
        new_node.next = self.head.next
        self.head = new_node
        return
    
    # Find node BEFORE target
    current = self.head
    while current.next and \\
          current.next.data != old_data:
        current = current.next
    
    # Rewire the pointers
    new_node.next = current.next.next
    current.next = new_node''', language='python')
    
    with viz_col:
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            if st.button("← Previous", disabled=(step == 0), key="replace_prev"):
                st.session_state.replace_step -= 1
                st.rerun()
        with col2:
            if st.button("Next →", disabled=(step == len(snapshots)-1), key="replace_next"):
                st.session_state.replace_step += 1
                st.rerun()
        with col3:
            if st.button("Reset", key="replace_reset"):
                st.session_state.replace_step = 0
                st.rerun()
        
        st.markdown(f"**Step {step + 1} of {len(snapshots)}**")
        st.markdown(render_snapshot(snapshots[step], "week"), unsafe_allow_html=True)

st.markdown("---")
st.markdown("*SI 507 - Intermediate Programming*")
