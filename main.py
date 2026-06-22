"""CLI demo for PawPal+ — verifies the backend logic in the terminal."""

from pawpal_system import User, Pet, Task, Schedule


def main() -> None:
    # Create an owner and two pets.
    owner = User("Jordan")
    mochi = Pet("Mochi", "cat", 3)
    biscuit = Pet("Biscuit", "dog", 5)
    owner.add_pet(mochi)
    owner.add_pet(biscuit)

    # Add tasks with different times across both pets.
    mochi.add_task(Task("Morning feeding", "08:00", 10))
    biscuit.add_task(Task("Morning walk", "09:00", 30))
    mochi.add_task(Task("Vet appointment", "15:00", 45))
    biscuit.add_task(Task("Evening feeding", "18:00", 10))

    # Build the schedule and print today's tasks.
    schedule = Schedule(owner)

    print(f"🐾 Today's Schedule for {owner.owner_name}")
    print("=" * 40)
    for pet in owner.pets:
        for task in pet.get_tasks():
            status = "✅" if task.completed else "⬜"
            print(
                f"{status} {task.time}  {task.description} "
                f"({pet.name}, {task.duration} min)"
            )
    print("=" * 40)
    print(f"{len(schedule.get_schedule())} task(s) scheduled today.")


if __name__ == "__main__":
    main()
