# Duke University Chatbot

This project implements an AI-powered chatbot for Duke University information, utilizing LangGraph for agentic search and a Flask backend with a React frontend.

## Project Structure

```
group_project_2/
├── .gitignore
├── README.md
└── duke-chatbot/
    ├── backend/
    │   ├── .env          # Backend environment variables (ignored by git)
    │   ├── app.py        # Main Flask application
    │   ├── requirements.txt # Python dependencies
    │   ├── agents/
    │   ├── graph/
    │   ├── tools/
    │   └── utils/
    └── frontend/
        ├── .env          # Frontend environment variables (ignored by git)
        ├── index.html    # Main HTML entry point
        ├── package.json  # Node.js dependencies and scripts
        ├── tailwind.config.cjs # Tailwind CSS configuration
        ├── vite.config.js # Vite configuration
        ├── node_modules/ # Node.js dependencies (ignored by git)
        ├── public/
        └── src/
            ├── main.jsx      # Main React entry point
            ├── App.jsx       # Root React component
            ├── components/
            ├── services/
            ├── styles/
            └── utils/
```

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd group_project_2
    ```

2.  **Backend Setup:**
    *   Navigate to the backend directory: `cd duke-chatbot/backend`
    *   Create a Python virtual environment (optional but recommended):
        ```bash
        python -m venv venv
        source venv/bin/activate  # On Windows use `venv\Scripts\activate`
        ```
    *   Install Python dependencies:
        ```bash
        pip install -r requirements.txt
        ```
    *   Create a `.env` file and add necessary environment variables (e.g., API keys, backend URLs). See `duke-chatbot/backend/.env.example` if one exists.
        *   Example `.env` content:
            ```
            GEMINI_API_KEY=YOUR_GEMINI_API_KEY
            DUKE_API_AUTH_TOKEN=YOUR_DUKE_AUTH_TOKEN
            # Add other required variables like tool API URLs if not using defaults
            ```

3.  **Frontend Setup:**
    *   Navigate to the frontend directory: `cd ../frontend` (if you were in `backend`) or `cd duke-chatbot/frontend` (from the root)
    *   Install Node.js dependencies:
        ```bash
        npm install
        ```
    *   Create a `.env` file and add the backend API URL:
        ```
        VITE_API_URL=http://127.0.0.1:5000 # Or the address where your Flask backend runs
        ```

## Running the Application

1.  **Run the Backend:**
    *   Navigate to `duke-chatbot/backend`.
    *   Activate the virtual environment if you created one (`source venv/bin/activate`).
    *   Start the Flask development server:
        ```bash
        flask run
        ```
    *   The backend should be running, typically on `http://127.0.0.1:5000`.

2.  **Run the Frontend:**
    *   Open a **new terminal window/tab**.
    *   Navigate to `duke-chatbot/frontend`.
    *   Start the Vite development server:
        ```bash
        npm run dev
        ```
    *   The frontend should be running, typically on `http://localhost:5173` or `http://localhost:5174`. Open this URL in your browser.

## Key Technologies

*   **Backend:** Python, Flask, LangChain, LangGraph, Google Gemini
*   **Frontend:** React, Vite, Tailwind CSS
*   **Environment:** Node.js, npm 