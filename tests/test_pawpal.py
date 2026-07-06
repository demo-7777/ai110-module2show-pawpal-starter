"""Quick tests for the PawPal+ backend logic."""

from pawpal_system import User, Pet, Task, Schedule


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


# --- Sorting correctness --------------------------------------------------

def test_sort_by_time_is_chronological():
    """sort_by_time returns tasks in ascending HH:MM order."""
    owner = User("Jordan")
    pet = Pet("Mochi", "cat", 3)
    owner.add_pet(pet)
    pet.add_task(Task("Vet", "15:00", 45))
    pet.add_task(Task("Feed", "08:00", 10))
    pet.add_task(Task("Walk", "12:00", 30))

    schedule = Schedule(owner)
    ordered = schedule.sort_by_time(schedule.get_schedule())
    assert [t.time for t in ordered] == ["08:00", "12:00", "15:00"]


# --- Recurrence logic -----------------------------------------------------

def test_completing_daily_task_creates_next_occurrence():
    """Completing a daily task marks it done and spawns a new incomplete task."""
    pet = Pet("Mochi", "cat", 3)
    daily = Task("Morning feeding", "08:00", 10, frequency="daily")
    pet.add_task(daily)

    next_task = pet.complete_task(daily)

    assert daily.completed is True
    assert len(pet.get_tasks()) == 2
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.frequency == "daily"


def test_completing_once_task_creates_no_new_task():
    """Completing a one-off task does not create a next occurrence."""
    pet = Pet("Mochi", "cat", 3)
    once = Task("Vet appointment", "15:00", 45)  # frequency defaults to "once"
    pet.add_task(once)

    result = pet.complete_task(once)

    assert once.completed is True
    assert result is None
    assert len(pet.get_tasks()) == 1


# --- Conflict detection ---------------------------------------------------

def test_detect_conflicts_flags_duplicate_times():
    """detect_conflicts reports tasks scheduled at the same time."""
    owner = User("Jordan")
    mochi = Pet("Mochi", "cat", 3)
    biscuit = Pet("Biscuit", "dog", 5)
    owner.add_pet(mochi)
    owner.add_pet(biscuit)
    mochi.add_task(Task("Feed", "09:00", 10))
    biscuit.add_task(Task("Walk", "09:00", 30))

    conflicts = Schedule(owner).detect_conflicts()
    assert len(conflicts) == 1
    assert "09:00" in conflicts[0]


def test_detect_conflicts_empty_when_no_overlap():
    """detect_conflicts returns an empty list when all times differ."""
    owner = User("Jordan")
    pet = Pet("Mochi", "cat", 3)
    owner.add_pet(pet)
    pet.add_task(Task("Feed", "08:00", 10))
    pet.add_task(Task("Walk", "09:00", 30))
    assert Schedule(owner).detect_conflicts() == []
