
def create_task_plan(goal, days, hours_per_day, topics):
    if days <= 0 or hours_per_day <= 0:
        raise ValueError("Days and hours per day must be positive.")

    topics = [topic.strip() for topic in topics if topic.strip()]

    if not topics:
        topics = [
            "Understand the goal",
            "Complete the main work",
            "Practice and review"
        ]

    # Distribute tasks across the available days.
    tasks = []

    for index, topic in enumerate(topics):
        day_number = min((index * days // len(topics)) + 1, days)

        tasks.append({
            "id": index + 1,
            "task": topic,
            "day": day_number,
            "estimated_hours": 0,
            "status": "Pending"
        })

    return _allocate_daily_hours(
        goal, days, hours_per_day, tasks
    )


def _allocate_daily_hours(goal, days, hours_per_day, tasks):
    """Divide each day's available hours among its assigned tasks."""

    revised_tasks = []

    for task in tasks:
        updated_task = task.copy()
        day = updated_task["day"]

        tasks_on_day = sum(
            1 for item in tasks if item["day"] == day
        )

        updated_task["estimated_hours"] = round(
            hours_per_day / tasks_on_day, 2
        )

        revised_tasks.append(updated_task)

    return {
        "goal": goal,
        "total_days": days,
        "hours_per_day": hours_per_day,
        "total_available_hours": days * hours_per_day,
        "tasks": revised_tasks
    }


def replan_tasks(plan, new_hours_per_day, reason):
    if new_hours_per_day <= 0:
        raise ValueError("Available hours must be positive.")

    # Preserve the existing task order and day assignments.
    revised_plan = _allocate_daily_hours(
        plan["goal"],
        plan["total_days"],
        new_hours_per_day,
        plan["tasks"]
    )

    revised_plan["reason_for_replanning"] = reason

    return revised_plan
