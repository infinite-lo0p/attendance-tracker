# attendance_tracker.py
import json
from datetime import datetime
from rich import print as rprint
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt
from timetable import TIMETABLE

console = Console()
DATA_FILE = "attendance.json"


def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def mark_today(data):
    today = datetime.now().strftime("%A")
    classes = TIMETABLE.get(today, {})
    if not classes:
        rprint("[yellow]No classes today. Chill![/yellow]")
        return

    rprint(f"[bold blue]Today: {today} | {len(classes)} sessions[/bold blue]\n")
    for slot, info in classes.items():
        display_name = info["display_name"]
        type_ = info["type"]

        if display_name not in data:
            data[display_name] = {"present": 0, "total": 0, "type": type_}

        rprint(f"[dim]{slot}[/dim] → [bold]{display_name}[/bold] ({type_})")

        # Ask with y/n/c
        choice = Prompt.ask(
            "  [green]y[/green]=Present  [red]n[/red]=Absent  [yellow]c[/yellow]=Cancelled",
            choices=["y", "n", "c"],
            default="y",
        )

        if choice == "c":
            rprint("    [yellow]Cancelled — not counted[/yellow]")
            continue  # Skip total
        else:
            data[display_name]["total"] += 1
            if choice == "y":
                data[display_name]["present"] += 1
                rprint("    [green]Present ✓[/green]")
            else:
                rprint("    [red]Absent ✗[/red]")

    save_data(data)
    rprint("\n[bold green]All done! Attendance saved.[/bold green]")


def show_report(data):
    table = Table(
        title="COEP Attendance Report", show_header=True, header_style="bold magenta"
    )
    table.add_column("Subject", style="cyan")
    table.add_column("Type", style="dim")
    table.add_column("P/T", justify="center")
    table.add_column("%", justify="right")
    table.add_column("Status", justify="center")

    for name, rec in sorted(data.items(), key=lambda x: x[1]["type"]):
        if rec["total"] == 0:
            continue
        perc = (rec["present"] / rec["total"]) * 100
        status = "[green]SAFE[/green]" if perc >= 75 else "[bold red]DANGER![/bold red]"
        type_emoji = {"theory": "Lecture", "lab": "Lab", "tutorial": "Tutorial"}.get(
            rec["type"], "Unknown"
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
    rprint("[bold underline blue]COEP Attendance Tracker v2.2[/bold underline blue]")
    rprint("[italic]Now with [yellow]Cancelled[/yellow] classes support[/italic]\n")

    while True:
        rprint("[bold]Menu:[/bold]")
        rprint("   [1] Mark Today's Classes")
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
