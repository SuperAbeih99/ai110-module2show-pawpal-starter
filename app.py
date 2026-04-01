import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Ahmed")

owner = st.session_state.owner
scheduler = Scheduler(owner)

st.subheader("Owner and Pet Setup")

owner_name = st.text_input("Owner name", value=owner.name)
owner.name = owner_name

pet_name = st.text_input("Pet name")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Pet age", min_value=0, max_value=50, value=1)

if st.button("Add pet"):
    if pet_name.strip():
        if owner.get_pet(pet_name.strip()) is None:
            owner.add_pet(Pet(pet_name.strip(), species, age))
            st.success(f"{pet_name} added.")
        else:
            st.warning("That pet already exists.")
    else:
        st.warning("Enter a pet name first.")

st.divider()

st.subheader("Current Pets")
if owner.pets:
    for pet in owner.pets:
        st.write(f"- {pet.name} ({pet.species}, age {pet.age})")
else:
    st.info("No pets added yet.")

st.divider()

st.subheader("Add a Task")

pet_options = [pet.name for pet in owner.pets]

if pet_options:
    selected_pet = st.selectbox("Choose pet", pet_options)
    task_description = st.text_input("Task description", value="Morning walk")
    task_time = st.text_input("Time (HH:MM)", value="08:00")
    duration_minutes = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    task_frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add task"):
        pet = owner.get_pet(selected_pet)
        if pet is not None:
            pet.add_task(
                Task(
                    task_description,
                    task_time,
                    int(duration_minutes),
                    priority,
                    task_frequency,
                )
            )
            st.success("Task added.")
else:
    st.info("Add a pet before adding tasks.")

st.divider()

st.subheader("Daily Schedule")
schedule = scheduler.build_daily_schedule()

if schedule:
    st.table([task.to_dict() for task in schedule])
else:
    st.info("No tasks scheduled yet.")

st.divider()

st.subheader("Schedule Explanation")
explanations = scheduler.explain_schedule()

if explanations:
    for explanation in explanations:
        st.write(f"- {explanation}")
else:
    st.info("No schedule explanation yet.")

st.divider()

st.subheader("Filter Tasks")

filter_pet = st.selectbox("Filter by pet", ["All"] + pet_options)
filter_status = st.selectbox("Filter by status", ["All", "Pending", "Completed"])
filter_priority = st.selectbox("Filter by priority", ["All", "high", "medium", "low"])

completed_value = None
if filter_status == "Pending":
    completed_value = False
elif filter_status == "Completed":
    completed_value = True

pet_value = None if filter_pet == "All" else filter_pet
priority_value = None if filter_priority == "All" else filter_priority

filtered_tasks = scheduler.filter_tasks(
    completed=completed_value,
    pet_name=pet_value,
    priority=priority_value,
)

if filtered_tasks:
    st.table([task.to_dict() for task in filtered_tasks])
else:
    st.info("No tasks match this filter.")

st.divider()

st.subheader("Conflict Warnings")
conflicts = scheduler.detect_conflicts()

if conflicts:
    for warning in conflicts:
        st.warning(warning)
else:
    st.success("No conflicts found.")

st.divider()

st.subheader("Mark a Task Complete")

pending_tasks = [task for task in scheduler.get_all_tasks() if not task.completed]

if pending_tasks:
    labels = [
        f"{task.pet_name} | {task.time} | {task.description} | {task.priority}"
        for task in pending_tasks
    ]
    chosen = st.selectbox("Choose a task to complete", labels)

    if st.button("Mark complete"):
        task_index = labels.index(chosen)
        scheduler.mark_task_complete(pending_tasks[task_index])
        st.success("Task marked complete.")
else:
    st.info("No pending tasks.")