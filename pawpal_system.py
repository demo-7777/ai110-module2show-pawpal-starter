"""PawPal+ backend logic layer.

Class skeletons generated from the UML diagram (diagrams/class_diagram.mmd).
Attributes and method signatures only — bodies are filled in during Phase 2.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class User:
    """The owner; manages one or more pets."""

    owner_name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet with this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return tasks across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


@dataclass
class Pet:
    """A pet and the list of tasks assigned to it."""

    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return this pet's tasks."""
        return self.tasks

    def complete_task(self, task: Task) -> Task | None:
        """Mark a task complete; if recurring, add and return its next occurrence."""
        task.mark_complete()
        if task.frequency in ("daily", "weekly"):
            next_task = Task(
                task.description, task.time, task.duration, task.frequency, task.priority
            )
            self.add_task(next_task)
            return next_task
        return None


@dataclass
class Task:
    """A single pet-care activity (feeding, walk, medication, appointment)."""

    description: str
    time: str  # "HH:MM" 24-hour format
    duration: int  # minutes
    frequency: str = "once"  # "once", "daily", "weekly"
    priority: str = "medium"  # "low", "medium", "high" — display only
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.completed = True


class Schedule:
    """The 'brain': retrieves, organizes, and manages tasks across pets."""

    def __init__(self, user: User):
        self.user = user

    def get_schedule(self) -> list[Task]:
        """Return all tasks for the user's pets."""
        return [task for pet in self.user.pets for task in pet.tasks]

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return the given tasks sorted chronologically by their HH:MM time."""
        return sorted(tasks, key=lambda task: task.time)

    def filter_tasks(
        self,
        status: bool | None = None,
        pet_name: str | None = None,
    ) -> list[Task]:
        """Filter tasks by completion status and/or pet name."""
        return [
            task
            for pet in self.user.pets
            if pet_name is None or pet.name == pet_name
            for task in pet.tasks
            if status is None or task.completed == status
        ]

    def detect_conflicts(self) -> list[str]:
        """Return warnings for tasks sharing the exact same HH:MM time."""
        by_time: dict[str, list[str]] = {}
        for task in self.get_schedule():
            by_time.setdefault(task.time, []).append(task.description)
        return [
            f"⚠️ Conflict at {time}: {', '.join(descriptions)}"
            for time, descriptions in by_time.items()
            if len(descriptions) > 1
        ]
