# attendance_tracker.py
import json
from datetime import datetime

DATA_FILE = "attendance.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # {subject: {"present": 0, "total": 0}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_attendance(data):
    subject = input("Subject name: ").strip().title()
    status = input("Present? (y/n): ").strip().lower()
    
    if subject not in data:
        data[subject] = {"present": 0, "total": 0}
    
    data[subject]["total"] += 1
    if status == "y":
        data[subject]["present"] += 1
    
    save_data(data)
    print(f"Updated {subject} ✓")

def show_report(data):
    print("\n" + "="*40)
    print("ATTENDANCE REPORT")
    print("="*40)
    for subj, rec in data.items():
        if rec["total"] == 0:
            continue
        perc = (rec["present"] / rec["total"]) * 100
        status = "SAFE" if perc >= 75 else "DANGER!"
        print(f"{subj:15} | {rec['present']}/{rec['total']} | {perc:5.1f}% | {status}")
    print("="*40)

def main():
    data = load_data()
    while True:
        print("\n1. Mark Attendance")
        print("2. View Report")
        print("3. Exit")
        choice = input("Choose: ").strip()
        
        if choice == "1":
            add_attendance(data)
        elif choice == "2":
            show_report(data)
        elif choice == "3":
            print("Saved. See you!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()