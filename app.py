
import streamlit as st
import pandas as pd

from agent import execute_planning


# PAGE CONFIGURATION
st.set_page_config(
    page_title="ReAct Task Planner AI",
    page_icon="🧠",
    layout="wide"
)


# CUSTOM CSS
st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.main-title {
    font-size: 34px;
    font-weight: 750;
    color: #183153;
}

.subtitle {
    color: #64748b;
    font-size: 15px;
}

.section-title {
    color: #183153;
    font-size: 21px;
    font-weight: 650;
}

.stButton button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    border: none;
    height: 45px;
    font-weight: 600;
}

.stButton button:hover {
    background-color: #1d4ed8;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# HEADER
st.markdown(
    '<div class="main-title">ReAct Task Planner AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Intelligent Goal Decomposition · ReAct Workflow · Dynamic Replanning'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# SIDEBAR SETTINGS
with st.sidebar:

    st.title("⚙️ Planning Settings")

    days = st.number_input(
        "Available days",
        min_value=1,
        max_value=30,
        value=3
    )

    hours_per_day = st.number_input(
        "Available hours per day",
        min_value=1,
        max_value=24,
        value=6
    )

    st.divider()

    simulate_failure = st.checkbox(
        "Enable failure simulation",
        value=False
    )

    new_hours = int(hours_per_day)

    if simulate_failure:

        new_hours = st.number_input(
            "New available hours per day",
            min_value=1,
            max_value=int(hours_per_day),
            value=max(1, int(hours_per_day // 2))
        )


# MAIN INPUT
st.markdown(
    '<div class="section-title">Create Your Task Plan</div>',
    unsafe_allow_html=True
)

goal = st.text_input(
    "Enter your main goal",
    placeholder="Example: Prepare for an examination in 3 days"
)

topics_input = st.text_area(
    "Enter tasks or topics (one per line)",
    placeholder=(
        "Tokenization\n"
        "Stemming\n"
        "POS Tagging\n"
        "Named Entity Recognition\n"
        "TF-IDF"
    ),
    height=150
)


# GENERATE PLAN
if st.button(
    "🚀 Generate Task Plan",
    use_container_width=True
):

    if not goal.strip():

        st.error("Please enter your goal.")

    else:

        topics = [
            topic.strip()
            for topic in topics_input.split("\n")
            if topic.strip()
        ]

        with st.spinner("ReAct Agent is planning..."):

            try:

                result = execute_planning(
                    goal=goal,
                    days=int(days),
                    hours_per_day=int(hours_per_day),
                    topics=topics,
                    simulate_failure=simulate_failure,
                    new_hours=int(new_hours)
                )

                st.session_state["result"] = result

            except Exception as error:

                st.error(f"Execution failed: {error}")


# DISPLAY RESULTS
if "result" in st.session_state:

    result = st.session_state["result"]

    plan = result["plan"]

    original_plan = result["original_plan"]

    st.divider()

    # PLANNING OVERVIEW
    st.markdown(
        '<div class="section-title">Planning Overview</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Days",
        plan["total_days"]
    )

    col2.metric(
        "Hours Per Day",
        plan["hours_per_day"],
        delta=(
            plan["hours_per_day"] - original_plan["hours_per_day"]
            if simulate_failure else None
        )
    )

    col3.metric(
        "Total Available Hours",
        plan["total_available_hours"],
        delta=(
            plan["total_available_hours"]
            - original_plan["total_available_hours"]
            if simulate_failure else None
        )
    )

    # REPLANNING COMPARISON
    if simulate_failure:

        st.divider()

        st.markdown(
            '<div class="section-title">Dynamic Replanning Comparison</div>',
            unsafe_allow_html=True
        )

        before, after = st.columns(2)

        with before:

            st.info("Original Plan")

            st.metric(
                "Available Hours",
                f"{original_plan['total_available_hours']} hrs"
            )

            st.write(
                f"{original_plan['hours_per_day']} hours per day"
            )

        with after:

            st.success("Revised Plan")

            st.metric(
                "Available Hours",
                f"{plan['total_available_hours']} hrs"
            )

            st.write(
                f"{plan['hours_per_day']} hours per day"
            )

        st.success(
            "The agent detected the changed assumption "
            "and successfully generated a revised plan."
        )

        st.info(
            plan.get(
                "reason_for_replanning",
                "Available study time was changed."
            )
        )

    st.divider()

    # TASK PLAN
    st.markdown(
        '<div class="section-title">Final Task Plan</div>',
        unsafe_allow_html=True
    )

    task_df = pd.DataFrame(plan["tasks"])

    task_df = task_df.rename(columns={
        "id": "Task ID",
        "task": "Task Name",
        "day": "Day",
        "estimated_hours": "Estimated Hours",
        "status": "Status"
    })

    st.dataframe(
        task_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # REACT TRACE
    st.markdown(
        '<div class="section-title">ReAct Execution Trace</div>',
        unsafe_allow_html=True
    )

    for index, step in enumerate(result["trace"], start=1):

        # Final summary appears separately below
        if step["step"] == "Final Result":
            continue

        with st.expander(
            f"Step {index}: {step['step']}",
            expanded=True
        ):

            st.write(step["details"])

    st.divider()

    # AI / PLANNING SUMMARY
    st.markdown(
        '<div class="section-title">Final Planning Summary</div>',
        unsafe_allow_html=True
    )

    st.text(result["summary"])

    st.success(
        "Planning workflow completed successfully."
    )

    # CLEAR RESULTS
    if st.button("Clear Results"):

        del st.session_state["result"]

        st.rerun()


# FOOTER
st.divider()

st.caption(
    "ReAct Task Planner AI | Built using Python, "
    "Streamlit, LangChain and Ollama"
)
