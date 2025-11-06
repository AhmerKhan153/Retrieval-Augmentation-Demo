# RAG (Retrieval-Augmentation-Demo)

This repository contains a retrieval-augmented incidents chatbot. The project is split into two main parts:

- Backend: Python (Flask API + retrieval/LLM logic)
	- Path: `Backend/` (main code under `Backend/src/`)
- Frontend: React (interactive chat UI)
	- Path: `Frontend/`

This README explains how to set up and run both parts on Windows (PowerShell), how to connect the React frontend to the Flask backend, and common troubleshooting steps.

---

## Quick summary

- Backend (Flask) serves `/chat` and uses your existing Python logic (see `Backend/src/UI/app.py` which wraps `src.main.answer_query`).
- Frontend (React) provides a simple chat UI in `Frontend/src/components/ChatBox.js` that POSTs to `http://localhost:5000/chat`.
- A local Qdrant vector DB is recommended for the retrieval layer; you can run it with Docker.

---

## Prerequisites

- Python 3.10+ (this repo has been used with Python 3.13 in the dev environment).
- Node.js + npm (for the React frontend).
- Docker Desktop (optional, for Qdrant).
- Git (optional)

---

## Backend setup (Windows PowerShell)

1. Open PowerShell and change to the backend folder:

```powershell
cd "Incidents Chatbot\Backend"
```

2. Create and activate a virtual environment (if you don't already have one):

```powershell
# Create venv (only if not present)
python -m venv venv

# Activate venv (PowerShell)
.\venv\Scripts\Activate.ps1
```

3. Install required Python packages (example list used while developing):

```powershell
pip install langchain sentence-transformers ollama requests streamlit flask flask-cors qdrant-client
```

Note: If you prefer a `requirements.txt`, you can create one from your environment:

```powershell
pip freeze > requirements.txt
```

4. Run the Flask backend:

```powershell
# From Backend folder with venv activated
python -m src.UI.app
# OR
python src/UI/app.py
```

The app runs on `http://localhost:5000` by default and exposes the `/chat` endpoint.

### Debugging in VS Code

If you want to debug the backend in VS Code, add or update `.vscode/launch.json` to set the working directory to `Backend` so Python finds the `src` package. Example:

```json
{
	"name": "Python: Flask",
	"type": "debugpy",
	"request": "launch",
	"module": "src.UI.app",
	"cwd": "${workspaceFolder}/Backend",
	"env": {
		"FLASK_APP": "src/UI/app.py",
		"FLASK_ENV": "development"
	},
	"args": ["run", "--no-debugger", "--no-reload"],
	"jinja": true
}
```

Then set breakpoints in `Backend/src/UI/app.py` or other modules and run the configuration.

---

## Frontend setup (React)

1. Change to the frontend directory:

```powershell
cd "Incidents Chatbot\Frontend"
```

2. Install Node dependencies (run once):

```powershell
npm install
```

If you see the error `'react-scripts' is not recognized`, run:

```powershell
npm install react-scripts --save
```

3. Start the development server:

```powershell
npm start
```

This opens the React app in your browser (usually at `http://localhost:3000`). The chat UI component `ChatBox` posts messages to `http://localhost:5000/chat`.

---

## Example: Test the backend directly (curl / PowerShell)

Send a POST to the `/chat` endpoint to check the backend is working.

PowerShell (curl alias):

```powershell
curl -Method POST -Uri http://localhost:5000/chat -ContentType 'application/json' -Body '{"message":"Hello"}'
```

Or using curl.exe (if installed):

```powershell
curl.exe -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d "{\"message\": \"Hello\"}"
```

You should receive JSON like:

```json
{ "response": "...the answer..." }
```

---

## Qdrant (optional) - run with Docker

If your retrieval layer needs Qdrant, start it with Docker Desktop running:

```powershell
docker run -d -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

If the daemon is not running you'll see an error. Start Docker Desktop and retry.

---

## How the frontend connects to the backend

- `Frontend/src/components/ChatBox.js` sends a POST with `{ message }` to `http://localhost:5000/chat`.
- `Backend/src/UI/app.py` receives the message and calls your project logic (e.g. `answer_query` in `src/main.py`) and returns `{ response }`.

If your Flask app is running on a different host / port, update the `fetch` URL accordingly in `ChatBox.js`.

---

## Memory / context behavior (backend)

A lightweight approach used for prototyping is an in-memory store to keep per-user/session chat history. `Backend/src/UI/app.py` can be extended to:

- Check if a user/session has prior messages (context).
- If context exists, call the LLM/retriever with context.
- If no context, return a direct message like "No context found" or call the LLM without context depending on desired behavior.

For production, store chat history in a database or persistent store rather than process memory.

---

## Troubleshooting

- "Fatal error in launcher: Unable to create process" — This happens when a virtualenv was moved; delete and recreate the `venv` and reinstall packages.
- `ModuleNotFoundError: No module named 'src'` — Set the working directory to `Backend` or run Python with `-m src.UI.app` from the `Backend` folder.
- Docker errors like `open //./pipe/docker_engine: The system cannot find the file specified.` — start Docker Desktop.
- `react-scripts` missing — `npm install` may not have completed; install `react-scripts` manually: `npm install react-scripts --save`.

---

## Files of interest

- `Backend/src/UI/app.py` — Flask entrypoint for the chat endpoint.
- `Backend/src/main.py` — (existing) main orchestration / entry logic used by backend.
- `Backend/src/llm.py`, `retriever.py`, `memory.py`, `prompts.py` — core logic for retrieval and LLM.
- `Frontend/src/components/ChatBox.js` — interactive chat UI connecting to the backend.
- `Frontend/src/App.js` — renders `ChatBox`.

---

## Next steps and recommendations

- Add a `requirements.txt` or `pyproject.toml` to pin Python dependencies.
- Add a `README-frontend.md` in the `Frontend/` folder with Node version and React-specific notes.
- Add integration tests for the backend `/chat` endpoint.
- Replace in-memory chat memory with a persistent store (Redis / DB) for multi-process reliability.

---

If you'd like, I can:

- Add `requirements.txt` and `package.json` improvements.
- Add a small Postman collection or automated test script for the `/chat` endpoint.
- Wire up a production-ready configuration (Gunicorn + Nginx) or containerize the backend.

Tell me which you'd like next and I'll add it to the plan.
