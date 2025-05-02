# Duke University Chatbot


## Project Overview: Dual Agentic Chatbot Approaches

This repository contains two implementations of a Duke-focused agentic chatbot:

### 1. Custom Agentic Chatbot (from Scratch)
- **Backend:** Flask, LangGraph, Gemini API, custom tools for Duke info/events/AI MEng (Google Custom Search)
- **Frontend:** React + Tailwind
- **Agentic Workflow:**
  1. **Planning:** Decides which tools to use for a query
  2. **Tool Execution:** Fetches info from APIs/search
  3. **Thinking:** Synthesizes info into a response
  4. **Evaluation:** Rates response quality (quantitative metrics: relevance, completeness, etc.)
- **Data Sources & Tools:**
  - **Duke Events API:** Streams event data from [Duke Calendar API](http://urlbuilder.calendar.duke.edu/)
  - **Google Programmable Search Engine:** For AI MEng program and general Duke info
    - Searches across:
      - https://masters.pratt.duke.edu/life/students/*
      - https://masters.pratt.duke.edu/people?s=&department=artificial-intelligence&group=faculty&submit=Filter*
      - https://masters.pratt.duke.edu/ai/*
  - **Duke General Info Tool:** Scrapes/queries public Duke websites
- **Evaluation:** Automated metrics for response quality
- **Deployment:** Cloud-hosted (GCP/Azure/AWS)
- **Demo URLs:**
  - [Frontend Demo](https://frontend-623186457718.us-central1.run.app)
  - [Backend API](https://backend-623186457718.us-central1.run.app)

---

### 2. Google Cloud Conversational Agents Version
- **Platform:** [Google Cloud Conversational Agents](https://cloud.google.com/products/conversational-agents)
- **Features:**
  - No-code/low-code agent builder
  - Gemini models
  - Built-in connectors
  - Multimodal (text/voice/image)
  - Rapid deployment
- **Use Case:** Fast prototyping, scalable, easy integration with Google ecosystem
- **Demo:** [Google Cloud Agent Demo](https://aipi-590-llm-website.vercel.app/)

---

## Architecture

![System Architecture](architecture.png)

*Figure: System architecture showing data sources, Cloud Run functions, modular tools, agent workflow, and user interaction. This illustrates the agentic, modular, and cloud-native design of the chatbot.*

---

## Scope
- Answers about Duke, the AI MEng program, campus events, and general info for prospective students.

## Agentic Workflow (Both Versions)
- Planning → Tool Use → Synthesis → Evaluation (modular, extensible, and agentic)

## Evaluation
- Quantitative metrics on response quality (relevance, completeness, etc.)

## Deployment
- Both versions deployed to the cloud (GCP/Azure/AWS)
- UI is cloud-hosted, demo URLs above

## For More Details
- See `Explanation.pdf` (project rationale, design choices, evaluation, etc)

---

This project implements an AI-powered chatbot designed to answer questions about Duke University. It utilizes LangGraph for building an agentic search workflow, a Flask backend, a React frontend, and integrates with Google Gemini and various Duke-specific information sources.

## Features

*   **Natural Language Queries:** Ask questions about Duke in plain English.
*   **Multi-Source Information:** Retrieves information about:
    *   General Duke topics
    *   The AI for Product Innovation Master of Engineering (AI MEng) program
    *   Current Duke events
    *   Future Duke events
*   **Agentic Workflow:** Employs a structured process for handling queries:
    *   **Planning:** Determines which information sources (tools) are needed.
    *   **Tool Execution:** Queries the relevant Duke APIs or search engines.
    *   **Thinking:** Synthesizes information from tools and conversation history.
    *   **Evaluation:** Assesses the relevance and completeness of the generated response.
*   **Conversation Context:** Maintains basic conversation history within a session.
*   **Interactive Frontend:** Clean web interface displaying the chat history, user input, and optional agent "thinking" steps.
*   **Response Quality Evaluation:** Provides metrics on the generated response (e.g., relevance, completeness).

## Architecture

The application follows a standard client-server architecture:

1.  **Frontend (Client):**
    *   Built with **React** (using **Vite**) and styled with **Tailwind CSS**.
    *   Handles user interaction through the `ChatInterface.jsx` component.
    *   Manages application state (messages, loading status) in `App.jsx`.
    *   Communicates with the backend API using `axios` (defined in `services/api.js`).
    *   Displays messages (`Message.jsx`), thinking processes (`ThinkingProcess.jsx`), and response stats (`ResponseStats.jsx`).

2.  **Backend (Server):**
    *   Built with **Python** and the **Flask** web framework.
    *   Exposes a primary API endpoint (`/api/chat`) to receive user messages.
    *   Orchestrates the core logic using **LangGraph**.
    *   Integrates with **Google Gemini** via `utils/gemini_client.py` for language understanding and generation.
    *   Manages the agent workflow (`graph/agent_workflow.py`) and state (`graph/state_management.py`).

3.  **Agent Workflow (LangGraph):**
    *   The core of the backend logic, defined in `graph/agent_workflow.py`.
    *   **State:** A dictionary holding the current message, conversation history, plan, tool results, thinking steps, and final response.
    *   **Nodes:**
        *   `PlanningAgent` (`agents/planning_agent.py`): Uses Gemini to analyze the user query and decide which tools (if any) are required.
        *   `execute_tools`: A function that runs the selected tool(s).
        *   `ThinkingAgent` (`agents/thinking_agent.py`): Uses Gemini to synthesize the results from the tools and the conversation context into a user-friendly response.
        *   `EvaluationAgent` (`agents/evaluation_agent.py`): Uses Gemini to evaluate the final response based on criteria like relevance and completeness.
    *   **Edges:** Define the flow between the nodes (Planning -> Execute Tools -> Thinking -> Evaluation -> End).
    *   **Tools:** Defined in the `tools/` directory:
        *   `DukeGeneralInfoTool`: Searches general Duke information.
        *   `DukeAIMEngTool`: Uses Google Custom Search for AI MEng program details.
        *   `DukeEventsSearchTool`: Queries an API for current Duke events.
        *   `DukeFutureEventsSearchTool`: Queries an API for future Duke events.

## Agent Workflow Explained

The chatbot uses a structured workflow orchestrated by LangGraph to process user queries and generate responses. This workflow ensures that the appropriate information sources are consulted and the final answer is synthesized coherently.

1.  **Planning (`PlanningAgent`):**
    *   Receives the user's message and conversation context.
    *   Uses the Gemini LLM to analyze the query.
    *   Determines the user's intent and identifies which specific tools (Duke General Info, AI MEng Search, Events Search, Future Events Search) are best suited to answer the question.
    *   If the query is out of scope or doesn't require specific Duke information, it may decide no tools are needed.
    *   Outputs a plan, including the list of tools to execute and their parameters (e.g., the search query for a tool).

2.  **Tool Execution (`execute_tools`):**
    *   Receives the plan from the Planning Agent.
    *   Iterates through the list of tools specified in the plan.
    *   Invokes each required tool with the appropriate parameters.
        *   `DukeGeneralInfoTool`, `DukeEventsSearchTool`, `DukeFutureEventsSearchTool` call their respective backend APIs.
        *   `DukeAIMEngTool` uses the Google Custom Search API.
    *   Collects the results (or errors) from each tool execution.

3.  **Thinking (`ThinkingAgent`):**
    *   Receives the original user query, conversation context, and the results from the executed tools.
    *   Uses the Gemini LLM to synthesize all the gathered information.
    *   Generates a concise, user-friendly response based on the tool outputs and the context.
    *   Also generates a brief explanation of its "thinking process" (how it arrived at the answer).

4.  **Evaluation (`EvaluationAgent`):**
    *   Receives the generated response and the thinking explanation.
    *   Uses the Gemini LLM to evaluate the quality of the response based on criteria like relevance, completeness, and clarity.
    *   Outputs an evaluation score or assessment.

5.  **Final Output:**
    *   The final response, thinking explanation, tool results (for potential display), and evaluation are sent back to the frontend.

This multi-step, agentic approach allows the chatbot to handle complex queries more effectively than a single LLM call by breaking down the problem, gathering specific information, and then reasoning over that information.

## Technology Stack

*   **Backend:** Python 3.x, Flask, Langchain, LangGraph, Google Gemini API (`google-generativeai`), python-dotenv
*   **Frontend:** React, Vite, Tailwind CSS, Axios
*   **Environment:** Node.js, npm, Python Virtual Environment (`venv`)
*   **HTTPS:** Use HTTPS for secure communication in production.

## Project Structure

```
Duke_chatbot/
├── backend/
│   ├── .env              # Backend environment variables (GITIGNORED)
│   ├── .env.example      # Example environment variables
│   ├── app.py            # Main Flask application, API endpoints
│   ├── requirements.txt  # Python dependencies
│   ├── agents/           # Agent logic
│   │   ├── planning_agent.py
│   │   ├── thinking_agent.py
│   │   └── evaluation_agent.py
│   ├── graph/            # LangGraph workflow and state
│   │   ├── agent_workflow.py
│   │   └── state_management.py
│   ├── tools/            # Tools for information retrieval
│   │   ├── duke_general_tool.py
│   │   ├── duke_ai_meng_tool.py
│   │   ├── duke_events_tool.py
│   │   └── duke_future_events_tool.py
│   └── utils/            # Utility functions (e.g., Gemini client)
│       └── gemini_client.py
└── frontend/
    ├── .env              # Frontend environment variables (GITIGNORED)
    ├── .env.example      # Example environment variable
    ├── index.html        # Main HTML entry point
    ├── package.json      # Node.js dependencies and scripts
    ├── tailwind.config.cjs # Tailwind CSS configuration
    ├── vite.config.js    # Vite configuration
    ├── node_modules/     # Node.js dependencies (GITIGNORED)
    ├── public/           # Static assets
    └── src/
        ├── main.jsx          # Main React entry point
        ├── App.jsx           # Root React component, state management
        ├── components/       # UI Components
        │   ├── ChatInterface.jsx
        │   ├── Message.jsx
        │   ├── Header.jsx
        │   ├── ThinkingProcess.jsx
        │   ├── EvaluationBadge.jsx
        │   └── ResponseStats.jsx
        ├── services/         # API communication
        │   └── api.js
        ├── styles/           # CSS styles
        │   └── index.css
        └── utils/            # Frontend utility functions
            └── formatters.js # (Currently empty)
```

## Environment Variables

Create `.env` files in both the `backend` and `frontend` directories. You can copy the `.env.example` files as a starting point.

**`Duke_chatbot/backend/.env`:**

```ini
# Required: Your Google Gemini API Key
GEMINI_API_KEY=YOUR_GEMINI_API_KEY

# Required: Authentication token for Duke APIs (Events, General Info)
DUKE_API_AUTH_TOKEN=YOUR_DUKE_AUTH_TOKEN

# Required for AI MEng Tool (often the same as GEMINI_API_KEY if using GCP API Key)
# Alternatively, a specific Google Cloud API Key with Custom Search API enabled
GOOGLE_API_KEY=YOUR_GOOGLE_CLOUD_OR_GEMINI_API_KEY

# Optional: Override default Duke API URLs if necessary
# DUKE_EVENTS_API_URL=https://your-custom-events-api.run.app
# DUKE_FUTURE_EVENTS_API_URL=https://your-custom-future-events-api.run.app
# DUKE_GENERAL_API_URL=https://your-custom-general-api.run.app
```

**`Duke_chatbot/frontend/.env`:**

```ini
# Required: URL where the Flask backend is running
VITE_API_URL=http://127.0.0.1:5000
```

*(Note: The AI MEng tool currently has a hardcoded Google Custom Search Engine ID (`cx`). You might need to replace `"40ad5871d1ccf4b4e"` in `backend/tools/duke_ai_meng_tool.py` and `backend/graph/agent_workflow.py` with your own if you set up a custom search engine).*

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>/Duke_chatbot
    ```

2.  **Backend Setup:**
    *   Navigate to the backend directory: `cd backend`
    *   Create and activate a Python virtual environment:
        ```bash
        python -m venv venv
        source venv/bin/activate  # On Windows: venv\\Scripts\\activate
        ```
    *   Install Python dependencies:
        ```bash
        pip install -r requirements.txt
        ```
    *   Create the `.env` file: `cp .env.example .env`
    *   Edit `.env` and add your API keys and tokens (see Environment Variables section).

3.  **Frontend Setup:**
    *   Navigate to the frontend directory: `cd ../frontend` (if in `backend`) or `cd frontend` (if in `Duke_chatbot`)
    *   Install Node.js dependencies:
        ```bash
        npm install
        ```
    *   Create the `.env` file: `cp .env.example .env`
    *   Edit `.env` and set `VITE_API_URL` to your backend address (default is usually correct).

## Running the Application

1.  **Run the Backend:**
    *   Navigate to `Duke_chatbot/backend`.
    *   Activate the virtual environment: `source venv/bin/activate` (or `venv\Scripts\activate`).
    *   Start the Flask server:
        ```bash
        flask run --port 5000 # Or your preferred port
        ```
    *   The backend should be running on `http://127.0.0.1:5000`.

2.  **Run the Frontend:**
    *   Open a **new terminal window/tab**.
    *   Navigate to `Duke_chatbot/frontend`.
    *   Start the Vite development server:
        ```bash
        npm run dev
        ```
    *   The frontend should be accessible in your browser, typically at `http://localhost:5173` or `http://localhost:5174`.

## API Endpoints

*   `POST /api/chat`:
    *   **Request Body:** `{"message": "User's query", "conversationId": "unique-id-for-session"}`
    *   **Response Body (Success):** JSON object containing `response`, `thinking_explanation`, `tool_results`, `evaluation`, `processing_time`, etc.
    *   **Response Body (Error):** `{"error": "...", "details": "..."}` with status code 400 or 500.
*   `GET /api/health`:
    *   **Response Body:** `{"status": "healthy"}`

## Deployment

Deploying this application involves deploying the Flask backend and the React frontend separately, or packaging them together.

**Common Strategies:**

1.  **Containerization (Docker):**
    *   Create a `Dockerfile` for the backend (Flask application).
    *   Create a `Dockerfile` for the frontend (React build using a multi-stage build with a static server like Nginx).
    *   Use `docker-compose` to manage both services locally or deploy them to container orchestration platforms (e.g., Kubernetes, Google Cloud Run, AWS ECS/Fargate).

2.  **Separate Deployment:**
    *   **Backend (Flask):**
        *   Deploy to Platform-as-a-Service (PaaS) like Google Cloud Run,.
        *   Requires a production-ready WSGI server (like `gunicorn` or `waitress`) instead of Flask's development server.
        *   Ensure all environment variables (`GEMINI_API_KEY`, `DUKE_API_AUTH_TOKEN`, etc.) are configured in the deployment environment.
    *   **Frontend (React):**
        *   Build the static assets: `npm run build` in the `frontend` directory.
        *   Deploy the contents of the `frontend/dist` folder to a static hosting service like Netlify, Vercel, AWS S3 + CloudFront, Google Cloud Storage, Firebase Hosting, or GitHub Pages.
        *   Ensure the `VITE_API_URL` environment variable in the frontend build points to the deployed backend URL.

3.  **Serving Frontend from Backend (Simpler for Single Server):**
    *   Build the frontend: `npm run build`.
    *   Configure Flask to serve the static files from the `frontend/dist` directory.
    *   Configure Flask to serve `index.html` for any routes not handled by the API.
    *   Deploy the combined Flask application using a WSGI server.

**Important Considerations:**

*   **Environment Variables:** Securely manage and provide API keys and other secrets to your deployed application environment. Do not commit them directly to your repository.
*   **Production WSGI Server:** Use `gunicorn` or `waitress` for the Flask backend in production instead of `flask run`.
*   **CORS:** Ensure Cross-Origin Resource Sharing (CORS) is configured correctly on the backend to allow requests from your deployed frontend domain.
*   **HTTPS:** Use HTTPS for secure communication in production.

### Live Demo

*   **Frontend (React + Nginx):** [https://frontend-623186457718.us-central1.run.app](https://frontend-623186457718.us-central1.run.app)
*   **Backend API (Flask + Gunicorn):** [https://backend-623186457718.us-central1.run.app](https://backend-623186457718.us-central1.run.app)
*   **Alternative Demo (Google Conversational Agent):** [https://aipi-590-llm-website.vercel.app/](https://aipi-590-llm-website.vercel.app/)

