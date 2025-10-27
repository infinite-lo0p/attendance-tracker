# attendance_tracker.py
import json
from datetime import datetime
from rich import print as rprint
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt, Confirm

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


def add_attendance(data):
    subject = Prompt.ask("[bold cyan]Subject[/bold cyan]").strip().title()
    status = Confirm.ask(f"[bold yellow]Present for {subject}?[/bold yellow]")

    if subject not in data:
        data[subject] = {"present": 0, "total": 0}

    data[subject]["total"] += 1
    if status:
        data[subject]["present"] += 1

    save_data(data)
    rprint(f"[green]Updated[/green] [bold]{subject}[/bold] ✓")


def show_report(data):
    table = Table(
        title="COEP Attendance Report", show_header=True, header_style="bold magenta"
    )
    table.add_column("Subject", style="dim")
    table.add_column("P/T", justify="center")
    table.add_column("Percentage", justify="right")
    table.add_column("Status", justify="center")

    for subj, rec in data.items():
        if rec["total"] == 0:
            continue
        perc = (rec["present"] / rec["total"]) * 100
        status = "[green]SAFE[/green]" if perc >= 75 else "[bold red]DANGER![/bold red]"
        table.add_row(subj, f"{rec['present']}/{rec['total']}", f"{perc:.1f}%", status)

    console.print(table)
    rprint(
        f"\n[italic dim]Report generated on {datetime.now().strftime('%Y-%m-%d')}[/italic dim]"
    )


def main():
    data = load_data()
    rprint("[bold underline blue]COEP Attendance Tracker v1.1[/bold underline blue]")

    while True:
        rprint("\n[bold]Menu:[/bold]")
        rprint("   [1] Mark Attendance")
        rprint("   [2] View Report")
        rprint("   [3] Exit")

        choice = Prompt.ask("Choose", choices=["1", "2", "3"], default="2")

        if choice == "1":
            add_attendance(data)
        elif choice == "2":
            if data:
                show_report(data)
            else:
                rprint("[yellow]No data yet. Mark attendance first![/yellow]")
        elif choice == "3":
            rprint("[bold green]Saved. See you, lo0p![/bold green]")
            break


if __name__ == "__main__":
    main()
