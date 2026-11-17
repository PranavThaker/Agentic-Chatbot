# Agentic Chatbot

A persistent, multi-turn chatbot built with [LangGraph](https://langchain-ai.github.io/langgraph/) and [Streamlit](https://streamlit.io/), powered by Groq's `openai/gpt-oss-120b` model. Conversations are checkpointed so a thread's history survives across turns (and, in the SQLite variant, across app restarts), and the UI supports switching between multiple saved conversation threads.

## Features

- **Streaming responses** — assistant replies are streamed token-by-token via `st.write_stream`.
- **Conversation checkpointing** — powered by LangGraph's checkpointer, so each thread remembers its own message history.
- **Two persistence backends**:
  - `MemorySaver` — in-memory checkpointing (resets when the app restarts).
  - `SqliteSaver` — checkpoints saved to a local `chatbot.db` file, so conversations persist across restarts.
- **Multi-thread chat UI** — a sidebar lets you start a new chat or revisit any previous conversation thread.

## Project Structure

| File | Description |
|---|---|
| `agentic_chatbot_backend.py` | LangGraph workflow using `MemorySaver` (in-memory checkpointing). |
| `agentic_chatbot_db_backend.py` | LangGraph workflow using `SqliteSaver` (persistent checkpointing to `chatbot.db`), plus a helper to list all saved threads. |
| `app_simple.py` | Minimal Streamlit chat UI — single thread, no sidebar, backed by `agentic_chatbot_backend`. |
| `app_thread.py` | Streamlit chat UI with multi-thread sidebar support, backed by the in-memory `agentic_chatbot_backend` (threads are not persisted across restarts). |
| `app_db.py` | Streamlit chat UI with multi-thread sidebar support, backed by `agentic_chatbot_db_backend` (threads persist across restarts via SQLite). |
| `notebooks/Chatbot_workflow.ipynb` | Notebook used to prototype the LangGraph workflow. |
| `requirements.txt` | Python dependencies. |
| `.env.example` | Template for required environment variables. |

## Requirements

- Python 3.10+
- A [Groq API key](https://console.groq.com/)

## Setup

1. **Clone the repository and install dependencies:**

   ```bash
   git clone https://github.com/PranavThaker/Agentic-Chatbot
   cd Agentic-Chatbot-main
   pip install -r requirements.txt
   ```

2. **Configure your environment:**

   Copy `.env.example` to `.env` and add your Groq API key:

   ```bash
   cp .env.example .env
   ```

   ```env
   GROQ_API_KEY = "your-groq-api-key"
   ```

## Usage

Run whichever app fits what you need:

```bash
# Minimal single-thread chatbot
streamlit run app_simple.py

# Multi-thread chatbot, in-memory only (resets on restart)
streamlit run app_thread.py

# Multi-thread chatbot with persistent history (recommended)
streamlit run app_db.py
```

Open the URL Streamlit prints (typically `http://localhost:8501`) in your browser.

- Use **New Chat** in the sidebar to start a fresh conversation thread.
- Click any entry under **My Conversations** to reload that thread's history.

## How It Works

Each backend defines a single-node LangGraph `StateGraph`:

```
START -> chat_node -> END
```

`chat_node` takes the running list of messages (`ChatState.messages`), invokes the Groq-hosted LLM, and appends the response. LangGraph's checkpointer (`MemorySaver` or `SqliteSaver`) keyed by `thread_id` is what gives each conversation its memory — every call to `.stream()`/`.get_state()` is scoped to a thread, so the graph recalls prior turns in that thread without the app needing to manage history itself.

## License

MIT — see [LICENSE](LICENSE).
