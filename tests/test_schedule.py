"""Tests for the Schedule class backend methods."""

import pytest

from pawpal_system import User, Pet, Task, Schedule


@pytest.fixture
def schedule():
    """An owner with two pets and tasks added out of chronological order."""
    owner = User("Jordan")
    mochi = Pet("Mochi", "cat", 3)
    biscuit = Pet("Biscuit", "dog", 5)
    owner.add_pet(mochi)
    owner.add_pet(biscuit)

    mochi.add_task(Task("Vet appointment", "15:00", 45))
    mochi.add_task(Task("Morning feeding", "09:00", 10))
    biscuit.add_task(Task("Morning walk", "09:00", 30))  # same time as feeding
    biscuit.add_task(Task("Evening feeding", "18:00", 10))
    return Schedule(owner)


# --- get_schedule ---------------------------------------------------------

def test_get_schedule_returns_all_tasks(schedule):
    """get_schedule collects tasks from every pet."""
    assert len(schedule.get_schedule()) == 4


def test_get_schedule_empty_when_no_pets():
    """get_schedule returns an empty list for an owner with no pets."""
    assert Schedule(User("Alex")).get_schedule() == []


# --- sort_by_time ---------------------------------------------------------

def test_sort_by_time_orders_chronologically(schedule):
    """sort_by_time returns tasks in ascending HH:MM order."""
    ordered = schedule.sort_by_time(schedule.get_schedule())
    assert [t.time for t in ordered] == ["09:00", "09:00", "15:00", "18:00"]


def test_sort_by_time_does_not_mutate_input(schedule):
    """sort_by_time returns a new list and leaves the original order intact."""
    original = schedule.get_schedule()
    snapshot = list(original)
    schedule.sort_by_time(original)
    assert original == snapshot


# --- filter_tasks ---------------------------------------------------------

def test_filter_by_pet_name(schedule):
    """filter_tasks(pet_name=...) returns only that pet's tasks."""
    mochi_tasks = schedule.filter_tasks(pet_name="Mochi")
    assert len(mochi_tasks) == 2
    assert {t.description for t in mochi_tasks} == {"Vet appointment", "Morning feeding"}


def test_filter_by_status(schedule):
    """filter_tasks(status=...) filters by completion state."""
    all_tasks = schedule.get_schedule()
    all_tasks[0].mark_complete()
    assert len(schedule.filter_tasks(status=True)) == 1
    assert len(schedule.filter_tasks(status=False)) == 3


def test_filter_by_pet_and_status(schedule):
    """filter_tasks combines pet_name and status filters."""
    mochi_tasks = schedule.filter_tasks(pet_name="Mochi")
    mochi_tasks[0].mark_complete()
    completed = schedule.filter_tasks(status=True, pet_name="Mochi")
    assert len(completed) == 1


def test_filter_no_args_returns_all(schedule):
    """filter_tasks with no arguments returns every task."""
    assert len(schedule.filter_tasks()) == 4


# --- detect_conflicts -----------------------------------------------------

def test_detect_conflicts_flags_same_time(schedule):
    """detect_conflicts reports a warning when two tasks share a time."""
    conflicts = schedule.detect_conflicts()
    assert len(conflicts) == 1
    assert "09:00" in conflicts[0]


def test_detect_conflicts_none_when_unique_times():
    """detect_conflicts returns an empty list when all times differ."""
    owner = User("Jordan")
    pet = Pet("Mochi", "cat", 3)
    owner.add_pet(pet)
    pet.add_task(Task("Feed", "08:00", 10))
    pet.add_task(Task("Walk", "09:00", 30))
    assert Schedule(owner).detect_conflicts() == []
