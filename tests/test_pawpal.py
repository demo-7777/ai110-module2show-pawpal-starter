"""Quick tests for the PawPal+ backend logic."""

from pawpal_system import Pet, Task


def test_mark_complete_changes_status():
    """Calling mark_complete() flips a task from incomplete to complete."""
    task = Task("Morning walk", "09:00", 30)
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_count():
    """Adding a task to a pet increases that pet's task count."""
    pet = Pet("Mochi", "cat", 3)
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task("Morning feeding", "08:00", 10))
    assert len(pet.get_tasks()) == 1
