"""CLI demo for PawPal+ — verifies the backend logic in the terminal."""

from pawpal_system import User, Pet, Task, Schedule


def print_tasks(title: str, tasks: list[Task]) -> None:
    """Print a titled list of tasks."""
    print(title)
    print("=" * 40)
    for task in tasks:
        status = "✅" if task.completed else "⬜"
        print(
            f"{status} {task.time}  {task.description} "
            f"({task.duration} min, {task.frequency}, {task.priority} priority)"
        )
    print("=" * 40)


def main() -> None:
    # Create an owner and two pets.
    owner = User("Jordan")
    mochi = Pet("Mochi", "cat", 3)
    biscuit = Pet("Biscuit", "dog", 5)
    owner.add_pet(mochi)
    owner.add_pet(biscuit)

    # Add tasks out of chronological order to exercise sorting.
    # Mochi's feeding and Biscuit's walk both at 09:00 -> a conflict.
    mochi.add_task(Task("Vet appointment", "15:00", 45, priority="high"))
    biscuit.add_task(Task("Morning walk", "09:00", 30, priority="medium"))
    mochi.add_task(Task("Morning feeding", "09:00", 10, frequency="daily", priority="high"))
    biscuit.add_task(Task("Evening feeding", "18:00", 10, priority="low"))

    schedule = Schedule(owner)

    # Sorted view: tasks returned chronologically regardless of insert order.
    sorted_tasks = schedule.sort_by_time(schedule.get_schedule())
    print_tasks(f"🐾 Today's Schedule for {owner.owner_name} (sorted by time)", sorted_tasks)

    # Filtered view: just one pet's tasks, still sorted.
    mochi_tasks = schedule.sort_by_time(schedule.filter_tasks(pet_name="Mochi"))
    print_tasks("\n🐱 Mochi's tasks", mochi_tasks)

    # Conflict detection: warn about tasks at the same time.
    print("\n🔎 Conflict check")
    print("=" * 40)
    conflicts = schedule.detect_conflicts()
    for warning in conflicts:
        print(warning)
    if not conflicts:
        print("No conflicts found.")
    print("=" * 40)

    # Recurring tasks: completing a daily task spawns the next occurrence.
    print("\n🔁 Completing Mochi's daily feeding")
    print("=" * 40)
    before = len(mochi.get_tasks())
    mochi.complete_task(mochi.get_tasks()[1])  # the "Morning feeding" daily task
    after = len(mochi.get_tasks())
    print(f"Mochi's task count: {before} -> {after} (next occurrence created)")
    print("=" * 40)


if __name__ == "__main__":
    main()
