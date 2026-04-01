from pawpal_system import Owner, Pet, Task, Scheduler


def print_schedule(tasks, title):
    print(f"\n{title}")
    print("-" * len(title))

    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        print(task)


owner = Owner("Ahmed")

dog = Pet("Milo", "Dog", 4)
cat = Pet("Luna", "Cat", 2)

owner.add_pet(dog)
owner.add_pet(cat)

dog.add_task(Task("Feed breakfast", "07:30", 10, "high", "daily"))
dog.add_task(Task("Morning walk", "08:00", 20, "high", "daily"))
cat.add_task(Task("Vet appointment", "08:00", 30, "medium", "once"))
cat.add_task(Task("Give medicine", "09:00", 5, "high", "daily"))
dog.add_task(Task("Brush fur", "10:00", 15, "low", "weekly"))

scheduler = Scheduler(owner)

print_schedule(scheduler.sort_by_time(), "Sorted by Time")
print_schedule(scheduler.build_daily_schedule(), "Daily Schedule")

print("\nConflict Warnings")
print("-----------------")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(warning)
else:
    print("No conflicts found.")

print("\nSchedule Explanations")
print("---------------------")
for line in scheduler.explain_schedule():
    print(line)

all_tasks = scheduler.get_all_tasks()
if all_tasks:
    scheduler.mark_task_complete(all_tasks[0])

print_schedule(scheduler.build_daily_schedule(), "Schedule After Completing First Task")