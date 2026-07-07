# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

    - User Class:
        - Purpose: Store owner's name and list of pets

    - Pet Class:
        - Purpose: Store pet info and list of its tasks

    - Task Class:
        - Purpose: Store task info to be used during schedule generation

    - Schedule Class:
        - Purpose: Contains methods used to create a schedule for the User

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

    - `duration` was added to the Task class during implementation (the initial UML draft only tracked description, time, and frequency). It records how long a task takes and is shown in the schedule output — though the conflict logic itself compares only start times, not durations. The `frequency` field supports recurring tasks: completing a daily/weekly task creates its next occurrence via `Pet.complete_task`.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

    - The schedule only considers time, there is no priority value the schedule uses during schedule generation.
    - It makes sense to only consider time as a constraint since it is intuitive to decide when two tasks overlap.
    - Priority and Preferences as constraints doesn't really make sense since the goal of the scheduler is to create a plan to complete all tasks.  

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

    `Schedule.detect_conflicts()` only flags tasks that share the **exact same** `HH:MM` start time. It does not consider a task's `duration`, so two tasks that overlap without starting at the same minute (e.g. a 09:00 task lasting 45 minutes and a 09:30 task) are not reported as a conflict. This keeps the logic simple and fast — a single grouping pass over the tasks — and exact-time clashes are the most common and most obvious scheduling mistake for a pet owner. Full interval-overlap detection would be more accurate but adds complexity (parsing times into minutes and comparing ranges), which isn't justified for this scenario yet.

    A second tradeoff: recurring tasks use a "clone" model — completing a daily/weekly task creates a fresh incomplete copy rather than tracking a concrete calendar date. This avoids adding date handling to the system while still demonstrating recurrence.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

    - The main purpose of AI use was to implement the actual fields and methods for the backend classes once it knew the purpose and relations of each.
    - AI tools were also used to write test cases to confirm functionality and edge cases of Class methods.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

    - When implementing recurring tasks, the AI recommended adding a `date` field to the Task class so that completing a daily task would schedule its next occurrence for `date + 1 day` using Python's `timedelta`. I declined that suggestion and chose a simpler "clone" model instead: completing a daily/weekly task creates a fresh incomplete copy of the task (same time and frequency) without tracking a concrete calendar date. I verified this decision by running the CLI demo and the test suite to confirm recurrence still worked, and it kept the system from taking on date-handling complexity it didn't yet need.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

    The suite (17 tests across `tests/test_pawpal.py` and `tests/test_schedule.py`) covers the core backend behaviors:
    - **Task completion** — `mark_complete()` flips a task from incomplete to complete.
    - **Task addition** — adding a task to a pet increases that pet's task count.
    - **Sorting correctness** — `Schedule.sort_by_time()` returns tasks in chronological order regardless of insertion order, and does not mutate the input list.
    - **Filtering** — `Schedule.filter_tasks()` narrows tasks by pet name, by completion status, by both, and returns all tasks when given no arguments.
    - **Recurrence logic** — completing a `daily` task creates a new incomplete next occurrence, while a `once` task does not.
    - **Conflict detection** — `Schedule.detect_conflicts()` flags two tasks scheduled at the same time and returns an empty list when all times are unique.

    These tests matter because sorting, recurrence, and conflict detection are the "smart" parts of the scheduler — the logic most likely to break silently and the behavior a pet owner actually relies on. The edge cases (no pets, no tasks, no conflicts, one-off vs. recurring) confirm the system degrades gracefully instead of crashing.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

    Confidence: ★★★★★ for the behaviors covered — all 17 tests pass, and each core method is exercised on both a happy path and at least one edge case.

    With more time I would test: overlapping tasks by *duration* (e.g. a 09:00 task lasting 45 minutes vs. a 09:30 task, which is currently not flagged — see 2b), invalid or malformed time strings (e.g. `"9:00"` or `"25:00"`), weekly recurrence specifically (only daily is directly asserted), and repeatedly completing a recurring task to confirm occurrences keep regenerating without duplication.



---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

    - That it is at least functional, and that the backend classes have a clear purpose in working together to allow the app to function. However in its current build it is very primitive and is lacking many features that would make it desirable to work as a true pet scheduler.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

    - With more time I would expand on functionality on what constraints the scheduler can work with to generate schedules and incorporate duration for the scheduler to detect conflicts besides examining task start time.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

    - AI is generally useful for doing the manual work like implementing class fields, methods, and writing test cases. However, AI generally is not good at creating system design from scratch and may either omit certain components or add superfluous ones depending on the requirements for the project.