# WikiSurf — AI-Powered Research Agent

An autonomous research agent that accepts a natural-language topic, orchestrates multiple search tools in priority order, and returns a structured summary with cited sources — all rendered in a rich terminal UI.

> **Inspired by** [Tech With Tim — Build an AI Agent in Python](https://www.youtube.com/watch?v=bTMPwUgLZf0)

---

## Architecture

```mermaid
sequenceDiagram
    actor User
    participant CLI as main.py
    participant Factory as ModelFactory
    participant Agent as AgentExecutor (LLM)
    participant Tools as Tools (Wiki / DDG / Save)
    participant Parser as PydanticOutputParser
    participant UI as Rich Terminal UI

    User->>CLI: research topic
    CLI->>Factory: get_llm()
    Factory-->>Agent: LLM instance
    CLI->>Agent: invoke(query)
    loop Thought → Action → Observation (≤10 iterations)
        Agent->>Tools: tool call (LLM-chosen)
        Tools-->>Agent: observation
    end
    Agent-->>Parser: raw output
    Parser-->>UI: ResearchResponse
    UI-->>User: formatted results
```

**Execution flow:**
1. The user supplies a research topic via the CLI or the interactive prompt.
2. `ModelFactory` instantiates the chosen LLM (Anthropic or OpenAI) from environment settings.
3. `ResearchAgent` runs the LangChain `AgentExecutor` in a Thought → Action → Observation loop (up to 10 iterations); the LLM dynamically selects which tool to call — Wikipedia, DuckDuckGo, or Save-to-File — based on its reasoning at each step.
4. The raw output is parsed into a typed `ResearchResponse` (topic, summary, sources, tools used).
5. `ui.py` renders each agent step in a colour-coded panel, a progress bar, and a final structured results box.

---

## Features

- **Multi-tool orchestration** — the LLM dynamically selects from Wikipedia, DuckDuckGo, and a file-save tool across multiple reasoning iterations; tool choice is driven by the agent's own judgment, not a hardcoded sequence.
- **Structured output** — responses are validated against a Pydantic schema and always include topic, summary, sources, and tools used.
- **Provider flexibility** — swap between Anthropic (Claude) and OpenAI (GPT-4o) via a single enum argument; model names are configurable in `.env`.
- **Rich terminal UI** — colour-coded agent steps, a live progress spinner, and formatted result panels powered by the `rich` library.
- **Persistent output** — the `save_text_to_file` tool appends timestamped research results to a local text file.
- **CLI support** — pass a topic directly as a command-line argument or enter it interactively.

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.11+ | Core runtime |
| **Agent Framework** | LangChain (`langchain`, `langchain-classic`) | Agent orchestration, tool-calling, prompt templating |
| **LLM Providers** | `langchain-anthropic`, `langchain-openai` | Claude & GPT-4o integration |
| **Search Tools** | `langchain-community`, `wikipedia`, `duckduckgo-search` | Wikipedia & DuckDuckGo tool wrappers |
| **Data Validation** | `pydantic`, `pydantic-settings` | Typed response schema & environment config |
| **Terminal UI** | `rich`, `pygments` | Colour-coded panels, progress bars, syntax highlighting |
| **Config** | `python-dotenv` | API key management via `.env` |

---

## Getting Started

### Prerequisites
- Python 3.11+
- An Anthropic **or** OpenAI API key

### Installation

```bash
git clone https://github.com/your-username/WikiSurf.git
cd WikiSurf
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here        # optional
```

### Usage

```bash
# Interactive prompt (defaults to Eiffel Tower if left blank)
python main.py

# Pass a topic directly
python main.py Mongolian barbeque history
```

---

## Screenshots

**Interactive prompt**

<img width="603" height="180" alt="Interactive prompt" src="https://github.com/user-attachments/assets/70517021-74e5-4212-8e6d-a51379944b2f" />

**Agent researching a topic (Wikipedia tool)**

<img width="897" height="830" alt="Agent researching" src="https://github.com/user-attachments/assets/ef05f629-0505-467e-9fc2-a2ebb3c4db40" />

**DuckDuckGo fallback in action**

<img width="868" height="860" alt="DuckDuckGo fallback" src="https://github.com/user-attachments/assets/269bfd2f-1768-4dd3-9beb-601cea4fc142" />

**Structured Research Response**

<img width="860" height="567" alt="Structured response" src="https://github.com/user-attachments/assets/b9c03dd8-2ffd-4a30-aeeb-4df27dbd7c5d" />

**CLI argument support**

![CLI argument example](Images%20and%20Text/img_1.png)

---

## Project Structure

```
WikiSurf/
├── main.py           # ModelFactory, ResearchAgent, entry point
├── tools.py          # Wikipedia, DuckDuckGo, and file-save tool definitions
├── ui.py             # Rich terminal UI components and callback handler
├── requirements.txt  # Python dependencies
├── .env              # API keys (not committed)
└── Images and Text/  # Sample output and screenshots
```

---

## Key Technical Decisions

| Decision | Rationale |
|---|---|
| **Factory pattern** (`ModelFactory`) | Decouples LLM instantiation from agent logic; adding a new provider requires only a single map entry |
| **`ModelProvider` str Enum** | Eliminates hardcoded string literals and provides IDE autocompletion and type safety |
| **Pydantic schema for output** | Guarantees a consistent, validated response structure regardless of LLM verbosity or formatting variations |
| **Callback-based UI updates** | LangChain callbacks allow the UI layer to react to each agent step without coupling it to core logic |
| **Dynamic tool selection** | The LLM autonomously decides which tool to call each iteration; no hardcoded sequence is enforced, allowing the agent to adapt its strategy to the specific query |

---

## Changelog

**2026-02-19** — Refactored `main.py` with `ModelProvider` enum, enhanced `ModelFactory`, modular `ResearchAgent` constructor, improved `<result>` tag parsing, and strengthened type hints and docstrings throughout.

**2026-02-18** — Added screenshots; introduced command-line argument support.

---

## Roadmap

The features previously planned here — sub-agent support, additional LLM providers, and expanded tool integrations — are actively being developed in **FinSurf**, the successor project built on the foundations established in WikiSurf. No further feature development is planned for this repository.
