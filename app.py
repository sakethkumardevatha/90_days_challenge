import streamlit as st
import json
import os

# Page Config
st.set_page_config(page_title="AI Engineering Roadmap", page_icon="🚀", layout="wide")

# File Path
JSON_FILE = "roadmap.json"

# --- Functions ---
def load_data():
    if not os.path.exists(JSON_FILE):
        return {}
    with open(JSON_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_data(data):
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)

def calculate_progress(data):
    total_tasks = 0
    completed_tasks = 0
    for day_id in data:
        tasks = data[day_id].get("tasks", [])
        for task in tasks:
            total_tasks += 1
            if task.get("status") == "done":
                completed_tasks += 1
    return completed_tasks, total_tasks

# --- Load Data ---
data = load_data()

# --- Sidebar: Navigation ---
st.sidebar.title("📅 Navigator")

completed, total = calculate_progress(data)
if total > 0:
    progress_percent = int((completed / total) * 100)
    st.sidebar.metric("Total Progress", f"{progress_percent}%")
    st.sidebar.progress(progress_percent / 100)
else:
    st.sidebar.warning("No tasks found.")

# Safe sorting for numeric and string keys
sorted_days = sorted(data.keys(), key=lambda x: int(x) if x.isdigit() else x)
selected_day_str = st.sidebar.selectbox("Select Day", sorted_days, index=0 if sorted_days else None)

# --- Main Page ---
if selected_day_str:
    day_data = data[selected_day_str]
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(f"🗓️ {day_data['date']}: {day_data['focus']}")
    with col2:
        day_tasks = day_data['tasks']
        day_done = sum(1 for t in day_tasks if t['status'] == 'done')
        day_total = len(day_tasks)
        st.metric("Day Progress", f"{day_done}/{day_total}")

    st.markdown("---")

    for i, task in enumerate(day_data['tasks']):
        c1, c2, c3 = st.columns([0.5, 3, 1])
        
        with c1:
            is_checked = task['status'] == 'done'
            # Update status based on checkbox
            if st.checkbox("", value=is_checked, key=f"chk_{selected_day_str}_{i}"):
                if task['status'] != "done":
                    task['status'] = "done"
                    save_data(data)
                    st.rerun()
            else:
                if task['status'] != "pending":
                    task['status'] = "pending"
                    save_data(data)
                    st.rerun()
            
        with c2:
            subject_color = {
                "DSA": "🔴", "ML Theory": "🔵", "ML Math": "🟢", 
                "Project": "🟣", "Tools": "🟠"
            }.get(task['subject'], "⚪")
            
            st.markdown(f"**{subject_color} {task['subject']}**: {task['topic']}")
            st.caption(task['action'])
            
        with c3:
            if task['status'] == "done":
                st.success("COMPLETED")
            else:
                st.info("PENDING")

        st.markdown("---")
else:
    st.info("Please ensure 'roadmap.json' is populated.")

st.sidebar.markdown("---")
st.sidebar.caption("Built for the AI Grind 🧠")