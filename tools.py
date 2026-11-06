from datetime import datetime


def calculate_available_time(days, hours_per_day):
    """Calculate the total time available for the goal."""

    total_hours = days * hours_per_day

    return {
        "days": days,
        "hours_per_day": hours_per_day,
        "total_hours": total_hours
    }


def check_task_status(tasks):
    """Count completed and pending tasks."""

    completed = sum(
        1 for task in tasks if task["status"] == "Completed"
    )

    pending = len(tasks) - completed

    return {
        "total_tasks": len(tasks),
        "completed_tasks": completed,
        "pending_tasks": pending
    }


def simulate_time_change(current_hours, new_hours):
    """Simulate a change in available time."""

    return {
        "previous_hours": current_hours,
        "new_hours": new_hours,
        "change_detected": current_hours != new_hours,
        "observation": (
            f"Available time changed from {current_hours} "
            f"to {new_hours} hours per day."
        )
    }


def get_current_date():
    """Return today's date."""

    return datetime.now().strftime("%d-%m-%Y")