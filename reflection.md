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

    

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

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

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
