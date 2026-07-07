import streamlit as st

from pawpal_system import User, Pet, Task, Schedule

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A pet care planning assistant.")

# --- Application memory ---------------------------------------------------
# Streamlit re-runs this script top-to-bottom on every interaction, so the
# owner (and all their pets/tasks) lives in st.session_state to persist
# across reruns instead of being recreated empty each time.
if "owner" not in st.session_state:
    st.session_state.owner = User("Jordan")

owner: User = st.session_state.owner

# --- Owner ----------------------------------------------------------------
owner.owner_name = st.text_input("Owner name", value=owner.owner_name)

st.divider()

# --- Add a pet ------------------------------------------------------------
st.subheader("Add a pet")
with st.form("add_pet", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        pet_name = st.text_input("Name", value="Mochi")
    with col2:
        species = st.selectbox("Species", ["dog", "cat", "other"])
    with col3:
        age = st.number_input("Age", min_value=0, max_value=40, value=3)
    if st.form_submit_button("Add pet"):
        owner.add_pet(Pet(pet_name, species, int(age)))
        st.success(f"Added {pet_name}.")

if owner.pets:
    st.caption("Current pets: " + ", ".join(p.name for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add a task -----------------------------------------------------------
st.subheader("Add a task")
if owner.pets:
    with st.form("add_task", clear_on_submit=True):
        pet_name = st.selectbox("Pet", [p.name for p in owner.pets])
        description = st.text_input("Description", value="Morning walk")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            time = st.text_input("Time (HH:MM)", value="09:00")
        with col2:
            duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        with col3:
            frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        with col4:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
        if st.form_submit_button("Add task"):
            pet = next(p for p in owner.pets if p.name == pet_name)
            pet.add_task(Task(description, time, int(duration), frequency, priority))
            st.success(f"Added '{description}' for {pet_name}.")
else:
    st.info("Add a pet before scheduling tasks.")

st.divider()

# --- Today's schedule -----------------------------------------------------
st.subheader("Today's Schedule")
if st.button("Generate schedule"):
    schedule = Schedule(owner)
    tasks = schedule.sort_by_time(schedule.get_schedule())
    if tasks:
        # Surface any same-time clashes before showing the plan.
        conflicts = schedule.detect_conflicts()
        for warning in conflicts:
            st.warning(warning)
        if not conflicts:
            st.success("No scheduling conflicts found.")

        rows = [
            {
                "Time": t.time,
                "Task": t.description,
                "Duration (min)": t.duration,
                "Frequency": t.frequency,
                "Priority": t.priority,
                "Done": "✅" if t.completed else "⬜",
            }
            for t in tasks
        ]
        st.table(rows)
    else:
        st.info("No tasks scheduled yet.")
