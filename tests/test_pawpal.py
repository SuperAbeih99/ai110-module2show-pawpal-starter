from pawpal_system import Owner, Pet, Task, Scheduler


def test_mark_complete_changes_status():
    task = Task("Feed dog", "08:00", 10, "high")
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Milo", "Dog", 4)
    pet.add_task(Task("Walk", "09:00", 20, "medium"))
    assert len(pet.tasks) == 1


def test_sort_by_time_returns_chronological_order():
    owner = Owner("Ahmed")
    pet = Pet("Milo", "Dog", 4)
    owner.add_pet(pet)

    pet.add_task(Task("Task 1", "10:00", 10, "low"))
    pet.add_task(Task("Task 2", "08:00", 10, "high"))
    pet.add_task(Task("Task 3", "09:00", 10, "medium"))

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()

    assert [task.time for task in sorted_tasks] == ["08:00", "09:00", "10:00"]


def test_build_daily_schedule_sorts_by_priority_then_time():
    owner = Owner("Ahmed")
    pet = Pet("Milo", "Dog", 4)
    owner.add_pet(pet)

    pet.add_task(Task("Low task", "07:00", 10, "low"))
    pet.add_task(Task("High task", "09:00", 10, "high"))
    pet.add_task(Task("Medium task", "08:00", 10, "medium"))

    scheduler = Scheduler(owner)
    scheduled = scheduler.build_daily_schedule()

    assert [task.description for task in scheduled] == [
        "High task",
        "Medium task",
        "Low task",
    ]


def test_conflict_detection_flags_duplicate_times():
    owner = Owner("Ahmed")
    pet1 = Pet("Milo", "Dog", 4)
    pet2 = Pet("Luna", "Cat", 2)

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    pet1.add_task(Task("Walk", "08:00", 20, "high"))
    pet2.add_task(Task("Vet visit", "08:00", 30, "medium"))

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1


def test_daily_recurrence_creates_new_task():
    owner = Owner("Ahmed")
    pet = Pet("Milo", "Dog", 4)
    owner.add_pet(pet)

    task = Task("Feed breakfast", "07:30", 10, "high", "daily")
    pet.add_task(task)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(task)

    assert len(pet.tasks) == 2
    assert pet.tasks[1].description == "Feed breakfast"
    assert pet.tasks[1].completed is False