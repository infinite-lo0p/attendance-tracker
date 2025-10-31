# attendance_tracker.py
import json
from datetime import datetime
from rich import print as rprint
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt, Confirm
from timetable import TIMETABLE

console = Console()
DATA_FILE = "attendance.json"
WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def get_today_classes():
    today = datetime.now().strftime("%A")
    time_now = datetime.now().strftime("%H:%M")
    classes = TIMETABLE.get(today, {})
    return [
        (slot, info)
        for slot, info in classes.items()
        if slot.split("-")[0] <= time_now <= slot.split("-")[1][:-3]
    ]


def mark_today(data):
    today = datetime.now().strftime("%A")
    classes = TIMETABLE.get(today, {})
    if not classes:
        rprint("[yellow]No classes today. Chill![/yellow]")
        return

    rprint(f"[bold blue]Today: {today} | {len(classes)} classes[/bold blue]\n")
    for slot, info in classes.items():
        name = info["name"]
        if "LAB" in name or "Tut" in name:
            name = name.split("-")[1].strip() if "LAB" in name else name
        if name not in data:
            data[name] = {"present": 0, "total": 0, "type": info["type"]}

        rprint(f"[dim]{slot}[/dim] → [bold]{name}[/bold] ({info['type']})")
        present = Confirm.ask("  Present?")
        data[name]["total"] += 1
        if present:
            data[name]["present"] += 1
    save_data(data)
    rprint("\n[green]All classes marked![/green]")


def show_report(data):
    table = Table(
        title="COEP Attendance Report", show_header=True, header_style="bold magenta"
    )
    table.add_column("Subject", style="cyan")
    table.add_column("Type", style="dim")
    table.add_column("P/T", justify="center")
    table.add_column("%", justify="right")
    table.add_column("Status", justify="center")

    for name, rec in data.items():
        if rec["total"] == 0:
            continue
        perc = (rec["present"] / rec["total"]) * 100
        status = "[green]SAFE[/green]" if perc >= 75 else "[bold red]DANGER![/bold red]"
        type_emoji = (
            "Theory"
            if rec["type"] == "theory"
            else "Lab"
            if rec["type"] == "lab"
            else "Tut"
        )
        table.add_row(
            name, type_emoji, f"{rec['present']}/{rec['total']}", f"{perc:.1f}", status
        )
    console.print(table)
    rprint(
        f"\n[italic dim]Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}[/italic dim]"
    )


def main():
    data = load_data()
    rprint("[bold underline blue]COEP Attendance Tracker v2.0[/bold underline blue]")
    rprint("[italic]Smart. Fast. Built for COEP.[/italic]\n")

    while True:
        rprint("[bold]Menu:[/bold]")
        rprint("   [1] Mark Today's Classes (Auto)")
        rprint("   [2] View Full Report")
        rprint("   [3] Exit")
        choice = Prompt.ask("Choose", choices=["1", "2", "3"], default="1")

        if choice == "1":
            mark_today(data)
        elif choice == "2":
            if data:
                show_report(data)
            else:
                rprint("[yellow]No attendance marked yet![/yellow]")
        elif choice == "3":
            rprint("[bold green]Saved. See you, lo0p![/bold green]")
            break


if __name__ == "__main__":
    main()
