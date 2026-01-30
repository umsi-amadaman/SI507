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

def render_snapshot(snap: Snapshot):
    css = """
    <style>
    .ll-container { display: flex; align-items: center; gap: 0; margin: 20px 0; font-family: monospace; }
    .node-box { border: 3px solid #333; border-radius: 8px; padding: 15px 20px; background: white; min-width: 80px; text-align: center; position: relative; font-size: 14px; }
    .node-box.highlight-current { border-color: #e63946; background: #fff0f0; box-shadow: 0 0 10px rgba(230, 57, 70, 0.4); }
    .node-box.highlight-newnode { border-color: #2a9d8f; background: #f0fff0; box-shadow: 0 0 10px rgba(42, 157, 143, 0.4); }
    .arrow { font-size: 24px; color: #333; margin: 0 5px; }
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
    html = [css, '<div class="head-label">week.head</div>', '<div class="ll-container">']
    
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
    
    if not snap.nodes:
        html.append('<span class="none-box">None (empty)</span>')
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


def create_replace_demo():
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
st.markdown("*Step through a replace operation to see pointer chasing in action*")

snapshots = create_replace_demo()
step = st.slider("Step through the operation:", 0, len(snapshots)-1, 0, key="step")

col1, col2, _ = st.columns([1, 1, 6])
with col1:
    if st.button("← Previous") and step > 0:
        st.session_state.step = step - 1
        st.rerun()
with col2:
    if st.button("Next →") and step < len(snapshots)-1:
        st.session_state.step = step + 1
        st.rerun()

st.markdown(f"**Step {step + 1} of {len(snapshots)}**")
st.markdown(render_snapshot(snapshots[step]), unsafe_allow_html=True)

with st.expander("Full replace() method"):
    st.code('''def replace(self, old_data, new_data):
    new_node = Node(new_data)
    
    # Special case: replacing the head
    if self.head.data == old_data:
        new_node.next = self.head.next
        self.head = new_node
        return
    
    # Find the node BEFORE the one we want to replace
    current = self.head
    while current.next and current.next.data != old_data:
        current = current.next
    
    # Rewire the pointers
    new_node.next = current.next.next
    current.next = new_node''', language='python')

st.markdown("---")
st.markdown("*SI 507 - Intermediate Programming*")
