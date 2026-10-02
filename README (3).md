# Trip Expense Simplification Engine — Individual Project Assignment

**Problem Statement #37 — Group Travel Expense Simplification Engine**

| | |
|---|---|
| **Student name** | `<your name>` |
| **Roll / ID** | `<your roll number>` |
| **Course / Batch** | `<course and batch>` |
| **GitHub repository** | `<repository link>` |
| **Jira project** | `<Jira project link>` |

## About the project

The Trip Expense Simplification Engine lets a group of travelers record shared expenses (with uneven splits and foreign currencies), see each person's net balance, and get the smallest practical set of peer-to-peer payments that settles everyone to zero.

- **Actors:** Group Traveler (primary), Trip Admin (secondary), Currency Service (external)
- **Use cases:** Add Expense, Convert Currency, Compute Debt Settlement, Notify Travelers, Manage Trip Travelers, View Balance

## Repository structure

```
.
├── README.md
├── 1-RE/
│   ├── FR_NFR_RTM.docx
├── 2-Architecture/
│   └── Architecture_Diagram.png
├── 3-Project-Setup-Screenshots/
│   ├── github/
│   └── jira/
├── 4-SRS-and-WBS/
│   └── SRS_and_WBS.pdf
├── 5-Copilot-Code/
│   ├── screenshots/
│   └── settlement_engine.py
└── 6-Testing-Practice/
    ├── README.md
    └── (game application code and 4 test cases)
```

## Contents

| Folder | Deliverable | What it contains |
|---|---|---|
| [1-RE](./1-RE) | Requirements Engineering | Functional Requirements (FR), Non-Functional Requirements (NFR) and the Requirements Traceability Matrix (RTM) |
| [2-Architecture](./2-Architecture) | Architectural diagram | Layered system architecture: client, API gateway, domain services, data layer, event bus and integration adapters |
| [3-Project-Setup-Screenshots](./3-Project-Setup-Screenshots) | Project creation evidence | Screenshots of the project created in GitHub and in the Jira tool |
| [4-SRS-and-WBS](./4-SRS-and-WBS) | SRS and Work Breakdown | Software Requirements Specification and the Work Breakdown Structure with schedule, milestones and risks |
| [5-Copilot-Code](./5-Copilot-Code) | GitHub Copilot generated code | Screenshots of the Copilot prompt and output, or the repository link, plus the generated code |
| [6-Testing-Practice](./6-Testing-Practice) | Software testing practice | Fixing a bug in the given game application using vibe coding, then retesting |

## 1 — Requirements Engineering (`1-RE`)

- Functional requirements: FR-001 to FR-013
- Non-functional requirements: NFR-001 to NFR-011
- RTM: each requirement traced to its use case, flow step, architecture component and test case

## 2 — Architectural Diagram (`2-Architecture`)

- Layers: presentation, API gateway, application services, data, event bus, integration adapters
- Services: Trip & Member, Expense, Balance, Settlement Engine, Payment Tracking, Currency Conversion, Notification
- External systems: Currency Service (exchange rates) and email / push provider

## 3 — Project Creation Screenshots (`3-Project-Setup-Screenshots`)

- `github/`: repository creation, README, branches and commits
- `jira/`: Jira project, epics, user stories and sprint board

## 4 — SRS and Work Breakdown Steps (`4-SRS-and-WBS`)

- **Part A:** Software Requirements Specification
- **Part B:** Work Breakdown Structure (9 phases, 44 work packages), Gantt chart, milestones, critical path and risks

## 5 — GitHub Copilot Generated Code (`5-Copilot-Code`)

- File generated: `settlement_engine.py`, the Compute Debt Settlement logic (greedy min-flow)
- Evidence: screenshots of the Copilot prompt and the generated output
- Repository link (if hosted separately): `<link>`

Run the file with:

```bash
python settlement_engine.py
```

Expected output: `All checks passed`

## 6 — Software Testing Practice (`6-Testing-Practice`)

The instructor shares a Git repository containing an individual game application and **4 test cases**. The details below are completed from that repository's own README.

### What the game application does

`<describe the game in 2–3 lines>`

### How to test

1. Clone the shared repository and open it in your editor.
2. Install the dependencies listed in its README.
3. Run the 4 test cases and note which pass and which fail.
4. Record the failing test name and the error message.

### How to fix the bug (vibe coding)

1. Paste the failing test, the error message and the relevant code into your AI coding assistant (for example GitHub Copilot).
2. Ask it to explain the cause of the bug and propose a minimal patch.
3. Apply the patch and review the change yourself before keeping it.
4. Re-run all 4 test cases and confirm they pass.
5. Commit with a clear message, for example `fix: <what was fixed>`.

### Test results

| Test case | Before fix | After fix |
|---|---|---|
| Test 1 | `<pass/fail>` | `<pass/fail>` |
| Test 2 | `<pass/fail>` | `<pass/fail>` |
| Test 3 | `<pass/fail>` | `<pass/fail>` |
| Test 4 | `<pass/fail>` | `<pass/fail>` |

**Bug found:** `<short description>`
**Fix applied:** `<short description>`
**Repository link after fixing:** `<link>`

## Submission checklist

- [ ] 1-RE: FR, NFR and RTM uploaded
- [ ] 2-Architecture: diagram uploaded
- [ ] 3-Project-Setup-Screenshots: GitHub and Jira screenshots added
- [ ] 4-SRS-and-WBS: PDF uploaded
- [ ] 5-Copilot-Code: screenshots or repository link added
- [ ] 6-Testing-Practice: bug fixed, tests passing, repository link shared
