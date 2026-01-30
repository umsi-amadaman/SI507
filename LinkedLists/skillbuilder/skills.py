"""
Linked List Skills Assessment
Run with: streamlit run skills.py
"""

import streamlit as st
import random
from typing import List

st.set_page_config(page_title="Linked List Skills", layout="wide")

# ============================================================
# SKILLS
# ============================================================

SKILLS = {
    "basic": ("1", "Basic Chained Notation", "Read head.next.next.data by counting hops"),
    "loop_tracing": ("2", "Loop Tracing", "Track variables through while/for loops"),
    "while_conditions": ("3", "While Conditions", "while current: vs while current.next:"),
    "two_pointers": ("4", "Two-Pointer Tracking", "Track prev and current together"),
    "assignment": ("5", "Assignment vs Comparison", "What CHANGES the list vs READS it"),
    "errors": ("6", "Error Prediction", "Spot code that will crash"),
    "off_by_one": ("7", "Off-by-One", "Why find the node BEFORE the target"),
    "unreachable": ("8", "Unreachable Nodes", "What gets orphaned after surgery"),
}

# ============================================================
# RENDERER
# ============================================================

def render_list(nodes: List[str], var: str = "mylist"):
    if not nodes:
        return f'<div style="font-family:monospace;color:#666;margin:10px 0">{var}.head → <em>None (empty)</em></div>'
    
    boxes = []
    for i, n in enumerate(nodes):
        boxes.append(f'<span style="border:2px solid #333;border-radius:6px;padding:8px 12px;background:white">{n}</span>')
        boxes.append('<span style="margin:0 5px">→</span>')
    boxes.append('<span style="color:#888;font-style:italic">None</span>')
    
    return f'<div style="font-family:monospace;margin:15px 0"><span style="color:#666">{var}.head →</span> {"".join(boxes)}</div>'

# ============================================================
# QUESTION BANKS
# ============================================================

QUESTIONS = {
    "basic": [
        (["Mon","Tue","Wed","Thu","Fri"], "week", None, "week.head.data", "Mon", ["Tue","None","Error"]),
        (["Mon","Tue","Wed","Thu","Fri"], "week", None, "week.head.next.data", "Tue", ["Mon","Wed","Error"]),
        (["Mon","Tue","Wed","Thu","Fri"], "week", None, "week.head.next.next.data", "Wed", ["Tue","Thu","Error"]),
        (["Mon","Tue","Wed","Thu","Fri"], "week", None, "week.head.next.next.next.data", "Thu", ["Wed","Fri","Error"]),
        (["Mon","Tue","Wed","Thu","Fri"], "week", None, "week.head.next.next.next.next.data", "Fri", ["Thu","None","Error"]),
        (["Mon","Tue","Wed","Thu","Fri"], "week", None, "week.head.next.next", "Node(Wed)", ["Wed","Tue","None"]),
        (["A","B","C"], "letters", None, "letters.head.next.next.next", "None", ["C","Error","Node(C)"]),
        (["Cat","Dog","Bird"], "pets", None, "pets.head.next.data", "Dog", ["Cat","Bird","Node(Dog)"]),
        (["Cat","Dog","Bird"], "pets", None, "pets.head.next", "Node(Dog)", ["Dog","Cat","None"]),
        (["Only"], "single", None, "single.head.next", "None", ["Only","Error","Node(Only)"]),
        (["X","Y","Z"], "data", None, "data.head.next.next.data", "Z", ["Y","None","Error"]),
        (["1","2","3","4"], "nums", None, "nums.head.next.next.next.data", "4", ["3","None","Error"]),
    ],
    "loop_tracing": [
        (["A","B","C","D","E"], "lst", "current = lst.head\nwhile current.next:\n    current = current.next", "current.data", "E", ["D","None","A"]),
        (["A","B","C","D","E"], "lst", "current = lst.head\nwhile current:\n    current = current.next", "current", "None", ["E","Node(E)","Error"]),
        (["A","B","C","D"], "lst", "current = lst.head\nfor i in range(2):\n    current = current.next", "current.data", "C", ["B","D","A"]),
        (["A","B","C","D"], "lst", "current = lst.head\nfor i in range(3):\n    current = current.next", "current.data", "D", ["C","None","Error"]),
        (["1","2","3"], "nums", "current = nums.head\ncount = 0\nwhile current:\n    count += 1\n    current = current.next", "count", "3", ["2","4","0"]),
        (["A","B","C","D"], "lst", "current = lst.head\nwhile current.data != 'C':\n    current = current.next", "current.data", "C", ["B","D","Error"]),
        (["A","B","C","D"], "lst", "current = lst.head\nwhile current.data != 'C':\n    current = current.next", "current.next.data", "D", ["C","B","Error"]),
        (["1","2","3","4","5"], "nums", "current = nums.head.next\nwhile current.next:\n    current = current.next", "current.data", "5", ["4","2","None"]),
        (["X","Y","Z"], "data", "current = data.head\nsteps = 0\nwhile current.next:\n    current = current.next\n    steps += 1", "steps", "2", ["3","1","0"]),
        (["A","B","C","D"], "lst", "current = lst.head\nfor i in range(10):\n    if current.next:\n        current = current.next", "current.data", "D", ["Error","None","A"]),
    ],
    "while_conditions": [
        (["A","B","C","D","E"], "lst", "# Loop 1: while current:\n# Loop 2: while current.next:\n# Both start at head", "Iterations: L1 vs L2", "L1:5, L2:4", ["L1:4, L2:5","Both 5","Both 4"]),
        (["X","Y","Z"], "data", "current = data.head\nwhile current.next:\n    current = current.next\n# then:", "current.next.data", "AttributeError", ["Z","None","Y"]),
        ([], "empty", "current = empty.head\nwhile current.next:\n    pass", "What happens?", "AttributeError", ["Runs 0 times","Works fine","Infinite"]),
        ([], "empty", "current = empty.head\nwhile current:\n    current = current.next", "What happens?", "Runs 0 times (safe)", ["AttributeError","Infinite","Runs once"]),
        (["Only"], "single", "current = single.head\nwhile current.next:\n    current = current.next", "Loop body runs?", "0 times", ["1 time","Error","Infinite"]),
        (["Only"], "single", "current = single.head\nwhile current:\n    current = current.next", "Loop body runs?", "1 time", ["0 times","Error","Infinite"]),
        (["A","B"], "short", "current = short.head\nwhile current.next.next:\n    current = current.next", "current.data", "A", ["B","Error","None"]),
        (["A","B","C"], "lst", "current = lst.head\nwhile current.next.next:\n    current = current.next", "current.data", "B", ["A","C","Error"]),
        (["1","2","3","4"], "nums", "# Which finds LAST node?\n# A: while current:\n# B: while current.next:", "Which one?", "B", ["A","Both","Neither"]),
    ],
    "two_pointers": [
        (["A","B","C","D","E"], "lst", "prev = None\ncurrent = lst.head\nwhile current.next:\n    prev = current\n    current = current.next", "prev.data", "D", ["E","C","None"]),
        (["A","B","C","D","E"], "lst", "prev = None\ncurrent = lst.head\nwhile current.next:\n    prev = current\n    current = current.next", "current.data", "E", ["D","None","C"]),
        (["A","B","C","D"], "lst", "prev = None\ncurrent = lst.head\nwhile current.data != 'C':\n    prev = current\n    current = current.next", "prev.data", "B", ["A","C","None"]),
        (["1","2","3"], "nums", "prev = None\ncurrent = nums.head\nprev = current\ncurrent = current.next", "prev.data, current.data", "1, 2", ["None,1","2,3","1,1"]),
        (["X","Y","Z"], "items", "prev = None\ncurrent = items.head\nwhile current:\n    prev = current\n    current = current.next", "prev.data", "Z", ["Y","None","X"]),
        (["A","B","C"], "lst", "prev = None\ncurrent = lst.head\n# before loop starts", "prev", "None", ["A","Node(A)","Error"]),
        (["1","2","3","4","5"], "nums", "prev = None\ncurrent = nums.head\nfor i in range(3):\n    prev = current\n    current = current.next", "prev.data", "3", ["2","4","1"]),
        (["Only"], "single", "prev = None\ncurrent = single.head\nwhile current.next:\n    prev = current\n    current = current.next", "prev", "None", ["Node(Only)","Only","Error"]),
        (["A","B"], "short", "prev = None\ncurrent = short.head\nwhile current.next:\n    prev = current\n    current = current.next", "prev.data", "A", ["B","None","Error"]),
    ],
    "assignment": [
        (["A","B","C"], "nodes", "node_a.next = node_b\nnode_b.next = node_c", "node_a.next.next.data", "C", ["B","A","Error"]),
        (["A","B","C","D"], "lst", "current = lst.head.next  # B\ncurrent.next = lst.head.next.next.next", "List becomes", "A→B→D", ["A→B→C→D","A→D","Error"]),
        (["1","2","3"], "nums", "current = nums.head\ncurrent = current.next", "nums.head.data", "1", ["2","3","None"]),
        (["X","Y","Z"], "data", "# Which CHANGES the list?\n# A: current = data.head\n# B: current = current.next\n# C: current.next = new_node", "Which one?", "C", ["A","B","All"]),
        (["A","B","C"], "lst", "lst.head = lst.head.next", "List becomes", "B→C", ["A→B→C","A→C","Error"]),
        (["1","2","3","4"], "nums", "temp = nums.head\nnums.head = nums.head.next", "temp.data", "1", ["2","None","Error"]),
        (["A","B","C"], "lst", "current = lst.head\ncurrent.data = 'Z'", "lst.head.data", "Z", ["A","Error","current"]),
        (["X","Y"], "short", "a = short.head\nb = short.head\na = a.next", "b.data", "X", ["Y","None","Same as a"]),
        (["1","2","3"], "nums", "nums.head.next.next = nums.head", "What happens?", "Cycle: 1→2→3→1...", ["Error","Deletes 3","Nothing"]),
        (["A","B","C","D"], "lst", "lst.head.next = lst.head.next.next", "Reachable nodes", "3 (A,C,D)", ["4","2","1"]),
    ],
    "errors": [
        (["A","B"], "short", "current = short.head\ncurrent = current.next\ncurrent = current.next\nprint(current.data)", "What happens?", "AttributeError", ["Prints B","Prints None","Prints A"]),
        (["Only"], "single", "if single.head.next.data == 'test':\n    print('found')", "What happens?", "AttributeError", ["Prints found","Nothing","NameError"]),
        (["A","B"], "short", "current = short.head.next.next\nprint(current.data)", "What happens?", "AttributeError", ["Prints B","Prints None","Nothing"]),
        ([], "empty", "print(empty.head.data)", "What happens?", "AttributeError", ["Prints None","Nothing","Prints empty"]),
        (["A","B","C"], "lst", "current = lst.head\nwhile current.next:\n    current = current.next\nprint(current.next.data)", "What happens?", "AttributeError", ["Prints C","Prints None","Nothing"]),
        (["1","2"], "nums", "print(nums.head.data.next)", "What happens?", "AttributeError", ["Prints 2","Prints 1","TypeError"]),
        (["A","B","C"], "lst", "current = lst.head.next.next.next\nif current:\n    print(current.data)", "What happens?", "Nothing (safe)", ["AttributeError","Prints C","Error"]),
        (["X"], "one", "current = one.head\nwhile current:\n    print(current.data)\n    current = current.next\nprint(current.data)", "What happens?", "Prints X, then Error", ["Prints X twice","Just X","Error first"]),
        (["A","B"], "lst", "if lst.head and lst.head.next and lst.head.next.next:\n    print('deep')\nelse:\n    print('safe')", "What prints?", "safe", ["AttributeError","deep","None"]),
    ],
    "off_by_one": [
        (["A","B","C","D"], "lst", "# To DELETE 'C', which node needed?", "Which node?", "B (before C)", ["C","D","A"]),
        (["A","B","C","D"], "lst", "# Deleting 'C':\nwhile current.next.data != 'C':\n    current = current.next", "Why current.next.data?", "Stop at B (before target)", ["Avoid errors","Faster","No reason"]),
        (["1","2","3","4","5"], "nums", "current = nums.head\nwhile current.next:\n    current = current.next\n# Delete last node?", "Can we?", "No - at last, need prev", ["Yes","current=None","Error"]),
        (["1","2","3","4","5"], "nums", "current = nums.head\nwhile current.next.next:\n    current = current.next\ncurrent.next = None", "List becomes", "1→2→3→4", ["1→2→3→4→5","1→2→3","Error"]),
        (["A","B","C"], "lst", "# Insert X between B and C\n# Find which node?", "Which node?", "B (then rewire)", ["C","A","X"]),
        (["1","2","3","4"], "nums", "current = nums.head\nwhile current.data != '3':\n    current = current.next", "Where is current?", "At '3' (for finding)", ["At '2'","At '4'","Error"]),
        (["A","B","C","D","E"], "lst", "# Delete 'C':\nwhile current.next.data != 'C':\n    current = current.next", "current.data", "B", ["C","A","D"]),
        (["X","Y","Z"], "items", "# Wrong approach:\nwhile current.data != 'Y':\n    current = current.next\n# Problem?", "Problem?", "At Y, can't go back", ["No problem","Error","Y deleted"]),
        (["1","2","3"], "nums", "# .next calls from head to last node?", "How many?", "2", ["3","1","0"]),
        (["A","B","C","D"], "lst", "# Replace 'C' with 'X'\n# Which nodes needed?", "Which?", "B and C", ["Just C","Just B","A,B,C"]),
    ],
    "unreachable": [
        (["A","B","C","D"], "lst", "lst.head.next = lst.head.next.next", "What happened to B?", "Orphaned", ["Deleted","At end","Unchanged"]),
        (["A","B","C","D"], "lst", "lst.head = lst.head.next", "List becomes", "B→C→D", ["A→B→C→D","A→C→D","C→D"]),
        (["1","2","3","4"], "nums", "saved = nums.head.next\nnums.head.next = nums.head.next.next", "Is '2' lost?", "No - saved has it", ["Yes","Error","Maybe"]),
        (["A","B","C"], "lst", "current = lst.head.next\nlst.head.next = None", "Reachable from head", "Only A", ["A→B→C","A→B","Nothing"]),
        (["X","Y","Z"], "items", "items.head = items.head.next.next", "Reachable", "Only Z", ["X,Y,Z","Y,Z","Nothing"]),
        (["1","2","3"], "nums", "a = nums.head\nb = nums.head.next\nnums.head = nums.head.next.next", "Nodes in memory?", "All 3", ["Only 3","2 and 3","None"]),
        (["A","B","C","D","E"], "lst", "lst.head.next.next = lst.head.next.next.next.next", "List becomes", "A→B→E", ["A→B→C→D→E","A→B→D→E","A→E"]),
        (["1","2"], "nums", "nums.head.next = None", "Reachable", "Only 1", ["1 and 2","Nothing","Only 2"]),
        (["A","B","C"], "lst", "lst.head = None", "What happened?", "All unreachable", ["Just A gone","Unchanged","Error"]),
        (["W","X","Y","Z"], "items", "items.head.next = items.head.next.next.next", "Orphaned count", "2 (X,Y)", ["0","1","3"]),
    ],
}

# ============================================================
# MAIN APP
# ============================================================

st.title("Linked List Skills Assessment")
st.markdown("*Master these 8 skills to understand linked list operations*")

# Skill selection
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
        nodes, var, code, expr, answer, distractors = qs[idx]
        
        st.progress(idx / len(qs))
        st.markdown(f"**Question {idx+1}/5** | Score: {st.session_state.score}/{idx}")
        
        # Show list
        st.markdown(render_list(nodes, var), unsafe_allow_html=True)
        
        # Show code
        if code:
            st.code(code, language="python")
        
        # Question
        st.markdown(f"### `{expr}`")
        
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
        # Done
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
