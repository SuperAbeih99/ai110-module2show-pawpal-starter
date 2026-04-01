from datetime import datetime, timedelta


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


class Task:
    """Represents one pet care task."""

    def __init__(
        self,
        description,
        time,
        duration_minutes,
        priority,
        frequency="once",
        completed=False,
        pet_name=None,
    ):
        self.description = description
        self.time = time
        self.duration_minutes = duration_minutes
        self.priority = priority.lower()
        self.frequency = frequency.lower()
        self.completed = completed
        self.pet_name = pet_name

    def mark_complete(self):
        """Marks the task complete."""
        self.completed = True

    def create_next_task(self):
        """Creates the next recurring version of the task if needed."""
        if self.frequency == "daily":
            next_time = datetime.strptime(self.time, "%H:%M") + timedelta(days=1)
            return Task(
                self.description,
                next_time.strftime("%H:%M"),
                self.duration_minutes,
                self.priority,
                self.frequency,
                False,
                self.pet_name,
            )

        if self.frequency == "weekly":
            next_time = datetime.strptime(self.time, "%H:%M") + timedelta(weeks=1)
            return Task(
                self.description,
                next_time.strftime("%H:%M"),
                self.duration_minutes,
                self.priority,
                self.frequency,
                False,
                self.pet_name,
            )

        return None

    def to_dict(self):
        """Converts the task to a dictionary for table display."""
        return {
            "pet": self.pet_name,
            "description": self.description,
            "time": self.time,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "frequency": self.frequency,
            "completed": self.completed,
        }

    def __repr__(self):
        status = "Done" if self.completed else "Pending"
        return (
            f"{self.time} | {self.pet_name} | {self.description} | "
            f"{self.duration_minutes} min | {self.priority} | {self.frequency} | {status}"
        )


class Pet:
    """Stores pet information and tasks."""

    def __init__(self, name, species, age):
        self.name = name
        self.species = species
        self.age = age
        self.tasks = []

    def add_task(self, task):
        """Adds a task to this pet."""
        task.pet_name = self.name
        self.tasks.append(task)

    def get_tasks(self):
        """Returns all tasks for this pet."""
        return self.tasks


class Owner:
    """Stores owner information and pets."""

    def __init__(self, name):
        self.name = name
        self.pets = []

    def add_pet(self, pet):
        """Adds a pet to the owner."""
        self.pets.append(pet)

    def get_pet(self, pet_name):
        """Finds a pet by name."""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet
        return None

    def get_all_tasks(self):
        """Returns all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """Handles scheduling logic across all pets."""

    def __init__(self, owner):
        self.owner = owner

    def get_all_tasks(self):
        """Returns all tasks for the owner."""
        return self.owner.get_all_tasks()

    def sort_by_time(self):
        """Sorts tasks by time only."""
        return sorted(self.get_all_tasks(), key=lambda task: task.time)

    def build_daily_schedule(self):
        """Builds a schedule using priority first, then time."""
        return sorted(
            self.get_all_tasks(),
            key=lambda task: (PRIORITY_ORDER.get(task.priority, 3), task.time),
        )

    def filter_tasks(self, completed=None, pet_name=None, priority=None):
        """Filters tasks by completion, pet, and/or priority."""
        tasks = self.get_all_tasks()

        if completed is not None:
            tasks = [task for task in tasks if task.completed == completed]

        if pet_name is not None:
            tasks = [task for task in tasks if task.pet_name == pet_name]

        if priority is not None:
            tasks = [task for task in tasks if task.priority == priority.lower()]

        return tasks

    def detect_conflicts(self):
        """Detects exact-time conflicts."""
        tasks = self.sort_by_time()
        warnings = []

        for i in range(len(tasks)):
            for j in range(i + 1, len(tasks)):
                if tasks[i].time == tasks[j].time:
                    warnings.append(
                        f"Conflict: '{tasks[i].description}' for {tasks[i].pet_name} "
                        f"and '{tasks[j].description}' for {tasks[j].pet_name} "
                        f"are both scheduled at {tasks[i].time}."
                    )

        return warnings

    def explain_schedule(self):
        """Returns simple human-readable explanations for scheduled tasks."""
        explanations = []
        for task in self.build_daily_schedule():
            explanations.append(
                f"{task.description} for {task.pet_name} is scheduled at {task.time} "
                f"because it has {task.priority} priority and lasts {task.duration_minutes} minutes."
            )
        return explanations

    def mark_task_complete(self, task):
        """Marks a task complete and creates a recurring replacement if needed."""
        task.mark_complete()
        new_task = task.create_next_task()

        if new_task is not None:
            pet = self.owner.get_pet(task.pet_name)
            if pet is not None:
                pet.add_task(new_task)