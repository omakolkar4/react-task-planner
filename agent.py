
from agents.react_agent import ReActAgent


def execute_planning(
    goal,
    days,
    hours_per_day,
    topics,
    simulate_failure=False,
    new_hours=3
):
    agent = ReActAgent()

    result = agent.run(
        goal=goal,
        days=days,
        hours_per_day=hours_per_day,
        topics=topics,
        simulate_failure=simulate_failure,
        new_hours=new_hours
    )

    if "original_plan" not in result:
        raise KeyError(
            "original_plan missing from ReActAgent.run() result"
        )

    return result
