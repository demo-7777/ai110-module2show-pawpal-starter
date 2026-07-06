# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## ✨ Features

- **Owner & pet management** — add an owner and multiple pets, each with its own task list (`User.add_pet`, `Pet.add_task`).
- **Task tracking** — every task records a description, time (`HH:MM`), duration, frequency, and completion status.
- **Sorting by time** — the daily schedule is returned in chronological order (`Schedule.sort_by_time`).
- **Filtering** — narrow tasks by pet and/or completion status (`Schedule.filter_tasks`).
- **Conflict warnings** — flags any tasks scheduled at the same time (`Schedule.detect_conflicts`).
- **Recurring tasks** — completing a `daily`/`weekly` task automatically creates its next occurrence (`Pet.complete_task`).
- **Streamlit UI** — add pets and tasks, then generate a sorted schedule with conflict warnings.

## 🖥️ Sample Output

Running the CLI demo (`python main.py`) verifies the backend logic in the terminal:

```
🐾 Today's Schedule for Jordan (sorted by time)
========================================
⬜ 09:00  Morning feeding (10 min)
⬜ 09:00  Morning walk (30 min)
⬜ 15:00  Vet appointment (45 min)
⬜ 18:00  Evening feeding (10 min)
========================================

🐱 Mochi's tasks
========================================
⬜ 09:00  Morning feeding (10 min)
⬜ 15:00  Vet appointment (45 min)
========================================

🔎 Conflict check
========================================
⚠️ Conflict at 09:00: Morning feeding, Morning walk
========================================

🔁 Completing Mochi's daily feeding
========================================
Mochi's task count: 2 -> 3 (next occurrence created)
========================================
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov

# Run my own tests:
# Tests cover Schedule's sorting correctness, recurrence logic, and conflict detection
python -m pytest
```

Sample test output:

```
========================================================= test session starts ==========================================================
platform linux -- Python 3.13.0, pytest-9.0.3, pluggy-1.6.0
rootdir: /mnt/c/vs/ai110/week4/ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 17 items                                                                                                                     

tests/test_pawpal.py .......                                                                                                     [ 41%]
tests/test_schedule.py ..........                                                                                                [100%]

========================================================== 17 passed in 0.29s ==========================================================
```

**Confidence Level:** ★★★★★

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Schedule.sort_by_time(tasks)` | Sorts tasks chronologically via `sorted()` with a key on the `HH:MM` time string. |
| Filtering | `Schedule.filter_tasks(status, pet_name)` | Returns tasks filtered by completion status and/or pet name; composes with sorting. |
| Conflict handling | `Schedule.detect_conflicts()` | Groups tasks by exact start time and returns a warning string for any time shared by 2+ tasks (exact-match only — see reflection §2b). |
| Recurring tasks | `Pet.complete_task(task)` | Marking a `daily`/`weekly` task complete creates a fresh incomplete copy as the next occurrence. |

## 📸 Demo Walkthrough

Run the UI with `streamlit run app.py`. The app lets a pet owner:

- Set the **owner name** and add one or more **pets** (name, species, age).
- Add **tasks** to a chosen pet (description, time, duration, frequency).
- Click **Generate schedule** to see today's plan, sorted by time, with conflict warnings.

**Example workflow**

1. Enter the owner name (e.g. *Jordan*).
2. Add a pet — *Mochi*, cat, age 3 — then add a second pet, *Biscuit*.
3. Add tasks: Mochi's *Morning feeding* at 09:00 (daily) and *Vet appointment* at 15:00; Biscuit's *Morning walk* at 09:00 and *Evening feeding* at 18:00.
4. Click **Generate schedule**. Tasks appear **sorted by time** in a table.
5. Because Mochi's feeding and Biscuit's walk are both at 09:00, the app shows a **conflict warning** (`st.warning`); with no clashes it shows a success message instead.

**Key `Schedule` behaviors shown:** chronological sorting (`sort_by_time`) and same-time conflict warnings (`detect_conflicts`). Recurring tasks (`Pet.complete_task`) regenerate the next occurrence when a daily/weekly task is completed.

**Sample CLI output** (`python main.py`):

```
🐾 Today's Schedule for Jordan (sorted by time)
========================================
⬜ 09:00  Morning feeding (10 min)
⬜ 09:00  Morning walk (30 min)
⬜ 15:00  Vet appointment (45 min)
⬜ 18:00  Evening feeding (10 min)
========================================

🔎 Conflict check
========================================
⚠️ Conflict at 09:00: Morning feeding, Morning walk
========================================
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
