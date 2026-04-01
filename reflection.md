# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial UML design used four main classes: `Task`, `Pet`, `Owner`, and `Scheduler`. I used `Task` to represent one pet care activity, including its description, time, duration, priority, frequency, and completion status. I used `Pet` to store a pet’s basic information and the list of tasks assigned to that pet. I used `Owner` to manage multiple pets and act as the main entry point for accessing all pet data. I used `Scheduler` as the main logic class that gathers tasks from all pets, sorts them, filters them, checks for conflicts, and builds the daily schedule.

**b. Design changes**

Yes, my design changed during implementation. At first, my `Task` class was simpler and only stored a description, time, frequency, and completion status. Later, I added `duration_minutes` and `priority` because the project requirements made it clear that the scheduler should consider more than just time. I also added helper methods like `to_dict()` for displaying tasks in the Streamlit UI and `create_next_task()` for recurring task logic. These changes made the system more complete and helped the backend connect more cleanly to the user interface.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler considers task time, task priority, pet name, completion status, and recurrence. When building the daily schedule, I decided that priority should come first and time should be the next sorting factor. I chose those constraints because they seemed the most important for a busy pet owner. For example, feeding or giving medicine should come before lower-priority tasks, but tasks should still appear in an organized time-based order.

**b. Tradeoffs**

One tradeoff my scheduler makes is that conflict detection only checks for exact matching times instead of overlapping task durations. For example, if one task starts at 8:00 and lasts 30 minutes while another starts at 8:15, my current system does not treat that as a conflict. I think this is reasonable for this project because it keeps the logic simple, easy to read, and easy to test while still showing the general idea of conflict detection.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI tools to help brainstorm the class design, think through which methods each class should have, debug mismatches between files, and improve the structure of the project. AI was especially helpful when I needed to connect the backend classes to the Streamlit UI and when I needed help writing and checking the pytest tests. The most useful prompts were the ones that were specific, such as asking how to structure the four classes, how to test recurrence and sorting, and how to connect `st.session_state` to my backend logic.

**b. Judgment and verification**

One moment where I did not accept an AI suggestion as-is was when I had code that was working in a basic way but still did not fully match the assignment requirements. I had to go back and make sure the project included duration, priority, a true daily schedule, and schedule explanations instead of stopping at a simpler version. I verified the final result by running `python3 main.py`, checking the printed output manually, running `python -m pytest` until all tests passed, and launching the Streamlit app to confirm that the interface worked correctly.

---

## 4. Testing and Verification

**a. What you tested**

I tested task completion, adding a task to a pet, sorting tasks by time, building a daily schedule using priority and time, recurrence logic, and conflict detection. These tests were important because they covered both the basic behavior of the objects and the main scheduling features that make the project useful.

**b. Confidence**

I am fairly confident that my scheduler works correctly for the current scope of the project because the demo script runs successfully, the Streamlit app launches, and all of my pytest tests pass. If I had more time, I would test more edge cases such as invalid time formats, duplicate pet names, overlapping task durations, empty schedules, and more realistic recurrence behavior that includes actual dates instead of only time strings.

---

## 5. Reflection

**a. What went well**

The part of this project I am most satisfied with is how the backend classes and the Streamlit UI ended up working together. I also like that the project does more than just store data. It can sort tasks, detect conflicts, handle recurring tasks, and explain why tasks appear in the schedule.

**b. What you would improve**

If I had another iteration, I would improve the scheduling logic so it could detect overlapping tasks based on duration and support more realistic calendar-based recurrence. I would also improve the UI by letting users edit and delete tasks and by making the final schedule display look more polished.

**c. Key takeaway**

One important thing I learned is that designing a system is not just about writing code that runs. It is about making sure the design, implementation, tests, and user interface all match the requirements and work together. I also learned that AI can speed up brainstorming and coding, but I still need to verify whether the result is actually correct and appropriate for the assignment.