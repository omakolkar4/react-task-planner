
from langchain_ollama import ChatOllama

from planner import create_task_plan, replan_tasks

from tools import (
    calculate_available_time,
    check_task_status,
    simulate_time_change
)


class ReActAgent:

    def __init__(self):
        self.llm = ChatOllama(
            model="qwen2.5:3b",
            temperature=0.3
        )

        self.trace = []

    def record(self, step, details):
        self.trace.append({
            "step": step,
            "details": details
        })

    def ask_qwen(self, prompt):
        """Get a concise explanation from the local Qwen model."""

        try:
            response = self.llm.invoke(prompt)
            return str(response.content).strip()

        except Exception as error:
            return (
                "Qwen was unavailable. The Python planning tools "
                f"will continue the workflow. Details: {error}"
            )

    def run(
        self,
        goal,
        days,
        hours_per_day,
        topics,
        simulate_failure=False,
        new_hours=3
    ):

        self.trace = []

        # STEP 1: REASON - QWEN
        reasoning = self.ask_qwen(
            f"""
            You are assisting with a task-planning application.

            User goal: {goal}
            Available days: {days}
            Available hours per day: {hours_per_day}
            Tasks: {topics}

            Give a short planning rationale in 2 sentences.
            Explain what should be prioritized.
            Do not calculate or invent a schedule.
            """
        )

        self.record("Reason", reasoning)

        # STEP 2: ACTION - INITIAL PLAN
        plan = create_task_plan(
            goal,
            days,
            hours_per_day,
            topics
        )

        original_plan = {
            "goal": plan["goal"],
            "total_days": plan["total_days"],
            "hours_per_day": plan["hours_per_day"],
            "total_available_hours": plan["total_available_hours"],
            "tasks": [task.copy() for task in plan["tasks"]]
        }

        self.record(
            "Action",
            "Python planning function generated the initial task schedule."
        )

        # STEP 3: OBSERVATION - TIME CHECK
        time_info = calculate_available_time(
            days,
            hours_per_day
        )

        self.record(
            "Observation",
            f"Initial available time: {time_info['total_hours']} hours."
        )

        # STEP 4: REASON - TASK ANALYSIS
        self.record(
            "Reason",
            "The agent will inspect the task list and verify task status."
        )

        # STEP 5: ACTION - STATUS CHECK
        status = check_task_status(plan["tasks"])

        self.record(
            "Action",
            "Executed the task status checking tool."
        )

        # STEP 6: OBSERVATION
        self.record(
            "Observation",
            f"Total tasks: {status['total_tasks']}. "
            f"Completed: {status['completed_tasks']}. "
            f"Pending: {status['pending_tasks']}."
        )

        # STEP 7: FAILURE SIMULATION
        if simulate_failure:

            self.record(
                "Reason",
                "The original assumption about available study time "
                "may have changed."
            )

            change = simulate_time_change(
                hours_per_day,
                new_hours
            )

            self.record(
                "Action",
                "Executed the time-change simulation tool."
            )

            self.record(
                "Observation",
                change["observation"]
            )

            if change["change_detected"]:

                # Ask Qwen for a short replanning rationale.
                revised_reasoning = self.ask_qwen(
                    f"""
                    The user's goal is: {goal}

                    Original availability: {hours_per_day} hours per day.
                    New availability: {new_hours} hours per day.
                    Number of days: {days}.
                    Tasks: {topics}

                    Explain briefly why the task schedule needs
                    to be adjusted. Do not calculate task hours.
                    Use 2 concise sentences.
                    """
                )

                self.record(
                    "Reason",
                    revised_reasoning
                )

                # Python performs the actual replanning.
                plan = replan_tasks(
                    plan,
                    new_hours,
                    change["observation"]
                )

                self.record(
                    "Action",
                    "Python replanning function generated the revised schedule."
                )

                self.record(
                    "Observation",
                    f"Revised total available time: "
                    f"{plan['total_available_hours']} hours."
                )

            else:
                self.record(
                    "Observation",
                    "No change detected. The original plan remains valid."
                )

        # STEP 8: VERIFY DAILY WORKLOAD
        daily_totals = {}

        for task in plan["tasks"]:
            day = task["day"]

            daily_totals[day] = (
                daily_totals.get(day, 0)
                + task["estimated_hours"]
            )

        schedule_valid = all(
            total <= plan["hours_per_day"] + 0.01
            for total in daily_totals.values()
        )

        self.record(
            "Observation",
            "Daily workload verification: "
            + ("Passed." if schedule_valid else "Failed.")
        )

        if not schedule_valid:
            raise ValueError(
                "The generated schedule exceeds daily availability."
            )

        # STEP 9: FINAL SUMMARY
        summary = (
            f"Goal: {plan['goal']}\n\n"
            f"Total duration: {plan['total_days']} days\n"
            f"Available hours per day: {plan['hours_per_day']}\n"
            f"Total available hours: {plan['total_available_hours']}\n\n"
            f"Total tasks: {len(plan['tasks'])}\n\n"
        )

        if simulate_failure and (
            plan["hours_per_day"] != original_plan["hours_per_day"]
        ):
            summary += (
                "Dynamic Replanning: Successfully triggered.\n"
                f"Original availability: "
                f"{original_plan['hours_per_day']} hours/day.\n"
                f"Revised availability: "
                f"{plan['hours_per_day']} hours/day.\n\n"
            )

        summary += "Final Task Schedule:\n"

        for task in plan["tasks"]:
            summary += (
                f"Day {task['day']} - {task['task']} "
                f"({task['estimated_hours']} hours)\n"
            )

        summary += "\nDaily Workload Verification:\n"

        for day in sorted(daily_totals):
            summary += (
                f"Day {day}: {round(daily_totals[day], 2)} / "
                f"{plan['hours_per_day']} hours\n"
            )

        summary += (
            "\nThe schedule was calculated and verified "
            "using Python planning functions."
        )

        self.record("Final Result", summary)

        return {
            "plan": plan,
            "original_plan": original_plan,
            "trace": self.trace,
            "summary": summary
        }
