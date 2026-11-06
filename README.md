# 🤖 ReAct Task Planner AI

### Intelligent Goal Decomposition · ReAct Workflow · Dynamic Replanning

An AI-powered task planning application that converts user-defined goals into structured schedules using a ReAct-based workflow. The application integrates **Python, Streamlit, LangChain, Ollama and Qwen 2.5 3B** to demonstrate reasoning explanations, tool execution, observations and dynamic replanning.

---

## 📌 Project Overview

The **ReAct Task Planner AI** is developed as part of the Unit 2 Experiential Learning activity for the Agentic Artificial Intelligence course.

The application helps users organize complex goals into smaller, manageable tasks and allocate available working hours across multiple days.

It follows the ReAct (Reasoning and Acting) approach:

- **Reason:** Understand the goal and generate a planning explanation.
- **Action:** Execute Python planning functions and tools.
- **Observation:** Examine the results of tool execution.
- **Replanning:** Adjust the schedule when the original assumptions change.

The application also includes a failure simulation feature that demonstrates how an agent can respond to changes in available working hours.

## ✨ Key Features

- **Goal Decomposition:** Divide a main goal into smaller tasks.
- **AI Reasoning:** Use Qwen 2.5 3B to generate planning explanations.
- **Automated Task Scheduling:** Distribute tasks across available days.
- **ReAct Execution Trace:** Display Reason, Action and Observation steps.
- **Tool Execution:** Perform time calculations and task-status checks.
- **Failure Simulation:** Simulate changes in available working hours.
- **Dynamic Replanning:** Generate a revised schedule when conditions change.
- **Workload Verification:** Ensure daily scheduled hours do not exceed available hours.
- **Interactive Dashboard:** View planning results through a Streamlit interface.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web interface |
| LangChain | Language model integration |
| Ollama | Local LLM execution |
| Qwen 2.5 3B | Planning explanations |
| Pandas | Data handling |

## 🏗️ Project Structure

```text
react-task-planner/
│
├── app.py
├── agent.py
├── planner.py
├── tools.py
├── requirements.txt
├── README.md
│
├── agents/
│   └── react_agent.py
│
└── utils/
    └── prompt_templates.py
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/react-task-planner.git
```

### 2. Navigate to the Project Directory

```bash
cd react-task-planner
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Install and Start Ollama

Download Ollama:

https://ollama.com/

Pull the Qwen 2.5 3B model:

```bash
ollama pull qwen2.5:3b
```

Start the model:

```bash
ollama run qwen2.5:3b
```

### 7. Run the Application

Open another terminal in the activated virtual environment and execute:

```bash
streamlit run app.py
```

The application will open in your browser:

```text
http://localhost:8501
```

## 🔄 ReAct Workflow

The application follows a structured execution process.

```text
         User Goal and Task Input
                   |
                   v
             Reasoning
                   |
                   v
            Initial Planning
                   |
                   v
              Observation
                   |
                   v
          Task Status Checking
                   |
                   v
          Failure Simulation
                   |
                   v
          Change Detection
                   |
                   v
          Dynamic Replanning
                   |
                   v
          Workload Verification
                   |
                   v
             Final Schedule
```

## 🧪 Experimental Testing

The application was evaluated using three test scenarios.

### Test Case 1: NLP Exam Preparation

**Goal:** Prepare for my NLP final assessment.

**Input:**
- Available days: 3
- Hours per day: 6
- Total available hours: 18

**Tasks:**
1. Tokenization and Text Preprocessing
2. Stemming and Lemmatization
3. POS Tagging
4. Named Entity Recognition
5. TF-IDF and Word Embeddings

**Result:** Successfully generated a five-task schedule with daily workload verification.

### Test Case 2: Dynamic Replanning

**Initial Conditions:**
- Available days: 3
- Hours per day: 6
- Total available hours: 18

**Changed Conditions:**
- Hours per day: 3
- Revised total available hours: 9

**Result:** The system detected the changed availability and generated a revised schedule while retaining all five tasks.

### Test Case 3: Portfolio Website Planning

**Goal:** Develop a personal portfolio website within one week.

**Input:**
- Available days: 7
- Hours per day: 4
- Total available hours: 28

**Tasks:**
1. Requirement Analysis
2. UI and UX Design
3. Frontend Development
4. Backend Development
5. Database Integration
6. Testing and Debugging
7. Deployment and Documentation

**Result:** Successfully generated a seven-day task schedule with daily workload verification.

## 📊 Results

| Test Scenario | Result |
|---|---|
| NLP Task Planning | ✅ Passed |
| Dynamic Replanning | ✅ Passed |
| Portfolio Website Planning | ✅ Passed |
| Daily Workload Verification | ✅ Passed |

## 🔮 Future Enhancements

- Automatic task generation from user goals.
- Priority-based task scheduling.
- Deadline and reminder management.
- Task completion tracking.
- Additional failure simulation scenarios.
- Advanced autonomous tool selection.
- Calendar integration.
- Progress tracking and visualization.

## 🎯 Learning Outcomes

Through this project, the following concepts were explored:

- Goal decomposition and task planning.
- Reasoning and Acting (ReAct) workflow.
- Integration of local language models.
- Python-based tool execution.
- Observation and failure simulation.
- Dynamic replanning.
- Development of interactive AI applications.

## 👨‍💻 Author

**Om Akolkar**

B.Tech – Computer Science and Engineering  
Specialization: Artificial Intelligence and Analytics  
MIT ADT University, Pune

## 📚 References

- [LangChain Documentation](https://python.langchain.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Ollama Documentation](https://docs.ollama.com/)
- [Python Documentation](https://docs.python.org/3/)
- [Qwen Documentation](https://qwenlm.github.io/)

---

⭐ If you find this project interesting, consider giving the repository a star!

**Developed as part of Unit 2 Experiential Learning – Agentic Artificial Intelligence.**