# COEP Attendance Tracker v2.1
**Never miss 75% again.**
Smart Python CLI that **reads your COEP timetable**, groups 2-hour labs, and marks attendance in 10 seconds.

Built by a **COEP CSE '29** first-year who hates manual tracking.

---

## Features
- **Auto "Mark Today"** — no typing subjects
- **2-hour labs = 1 attendance**
- Clean names: `Python Programming`, not `LAB Batch 4-PP-...`
- Color-coded report with **SAFE / DANGER!**
- Persistent `attendance.json`
- Powered by [`rich`](https://github.com/Textualize/rich)

---

## Demo
Today: Tuesday | 5 sessions

08:30-10:30 → DLD Lab (lab)

10:30-11:30 → AEIoT - Applied Electronics And IoT (theory)

11:30-12:30 → FAI - Fundamentals of AI (theory)

01:30-02:30 → DLD - Digital Logic Design (theory)

02:30-03:30 → Linear Algebra (theory)

---

## Setup

```bash
git clone https://github.com/infinite-lo0p/attendance-tracker.git
cd attendance-tracker
pip3 install rich
python3 attendance_tracker.py

File Structure
text
