# timetable.py
from collections import defaultdict

# Raw timetable (same as before)
RAW_TIMETABLE = {
    "Monday": {
        "10:30-11:30": {
            "name": "FAI - Fundamentals of AI",
            "room": "NC10",
            "type": "theory",
        },
        "11:30-12:30": {"name": "Engg Physics", "room": "NC04", "type": "theory"},
        "03:30-04:30": {
            "name": "Comp 16-CS- Communication Skills",
            "room": "NC14",
            "type": "lab",
        },
        "04:30-05:30": {
            "name": "Comp 16-CS- Communication Skills",
            "room": "NC14",
            "type": "lab",
        },
        "05:30-06:30": {
            "name": "AEIoT - Applied Electronics And IoT",
            "room": "NC14",
            "type": "theory",
        },
    },
    "Tuesday": {
        "10:30-11:30": {
            "name": "AEIoT - Applied Electronics And IoT",
            "room": "NC14",
            "type": "theory",
        },
        "11:30-12:30": {
            "name": "FAI - Fundamentals of AI",
            "room": "NC10",
            "type": "theory",
        },
        "01:30-02:30": {
            "name": "DLD - Digital Logic Design",
            "room": "NC12",
            "type": "theory",
        },
        "02:30-03:30": {"name": "Linear Algebra", "room": "NC13", "type": "theory"},
        "03:30-04:30": {
            "name": "LAB Batch 4-PP- Python Programming",
            "room": "Advance Software LAB",
            "type": "lab",
        },
        "04:30-05:30": {
            "name": "LAB Batch 4-PP- Python Programming",
            "room": "Advance Software LAB",
            "type": "lab",
        },
    },
    "Wednesday": {
        "10:30-11:30": {"name": "Linear Algebra", "room": "NC13", "type": "theory"},
        "11:30-12:30": {"name": "Engg Physics", "room": "NC04", "type": "theory"},
        "01:30-02:30": {
            "name": "DLD - Digital Logic Design",
            "room": "NC12",
            "type": "theory",
        },
        "02:30-03:30": {
            "name": "Fundamentals Of Quantum Physics",
            "room": "NC09",
            "type": "theory",
        },
        "03:30-04:30": {
            "name": "LAB Batch 2-FAI- Fundamentals of AI",
            "room": "Database Management System LAB",
            "type": "lab",
        },
        "04:30-05:30": {
            "name": "LAB Batch 2-FAI- Fundamentals of AI",
            "room": "Database Management System LAB",
            "type": "lab",
        },
        "05:30-06:30": {
            "name": "Fundamentals Of Quantum Physics",
            "room": "NC09",
            "type": "theory",
        },
    },
    "Thursday": {
        "08:30-09:30": {
            "name": "LAB Batch 1-DLD- Digital Logic Design",
            "room": "Microwave LAB",
            "type": "lab",
        },
        "09:30-10:30": {
            "name": "LAB Batch 1-DLD- Digital Logic Design",
            "room": "Microwave LAB",
            "type": "lab",
        },
        "05:30-06:30": {
            "name": "PP- Python Programming",
            "room": "NC10",
            "type": "theory",
        },
    },
    "Friday": {
        "10:30-11:30": {
            "name": "Tut Batch 2-Linear Algebra",
            "room": "NC13",
            "type": "tutorial",
        },
        "01:30-02:30": {
            "name": "LAB Batch 2-Engg Physics",
            "room": "Physics LAB",
            "type": "lab",
        },
        "02:30-03:30": {
            "name": "LAB Batch 2-Engg Physics",
            "room": "Physics LAB",
            "type": "lab",
        },
        "04:30-05:30": {
            "name": "AEIoT - Applied Electronics And IoT",
            "room": "NC14",
            "type": "theory",
        },
    },
    "Saturday": {},
}


# Group consecutive lab slots
def build_timetable():
    timetable = {}
    for day, slots in RAW_TIMETABLE.items():
        grouped = []
        i = 0
        while i < len(slots):
            current_slot = list(slots.items())[i]
            time, info = current_slot
            name = info["name"]
            type_ = info["type"]

            # If it's a lab and next slot is same lab → merge
            if type_ == "lab" and "LAB" in name:
                j = i + 1
                while j < len(slots):
                    next_time, next_info = list(slots.items())[j]
                    if next_info["type"] == "lab" and next_info["name"] == name:
                        time = f"{time.split('-')[0]}-{next_time.split('-')[1]}"
                        j += 1
                    else:
                        break
                i = j
            else:
                i += 1

            # Clean name
            clean_name = name
            if "LAB" in name:
                clean_name = name.split("-")[1].strip() if "-" in name else name
            elif "Tut" in name:
                clean_name = name.split("-")[1].strip() if "-" in name else name

            grouped.append((time, {**info, "display_name": clean_name}))

        # Convert to dict with time as key
        timetable[day] = {time: info for time, info in grouped}
    return timetable


TIMETABLE = build_timetable()
