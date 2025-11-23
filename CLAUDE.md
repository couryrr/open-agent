# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OpenRunner is an experimental agentic platform for interacting with LLMs (Large Language Models) via a TUI (Text User Interface). The project uses the Textual library for the interface and the Ollama SDK for LLM interactions, with plans to support additional providers via APIs.

## Build System and Development Commands

This project uses `uv` as the package manager and build tool (NOT pip). All development commands should use `uv`.

### Running the Application

```bash
uv run openrunner [OPTIONS]
```

### Testing

Run all tests:
```bash
uv run pytest
```

Run a specific test file:
```bash
uv run pytest tests/test_open_agent_tooling.py
```

Run a specific test function:
```bash
uv run pytest tests/test_open_agent_tooling.py::test_create_provider_script
```

### Installing Dependencies

```bash
uv sync
```

Install with dev dependencies:
```bash
uv sync --group dev
```

## Core Architecture

The codebase follows a modular architecture with clear separation of concerns:

### State Management

The application uses Pydantic models throughout for data validation and serialization. State is persisted to JSON in the user data directory (managed via `platformdirs`).

- **OpenRunnerState** (state.py): Root state container holding all sessions and providers
- Persisted to: `~/.local/share/openrunner/nextbubble/data.json` (Linux)
- State is loaded on startup and saved after modifications

### Core Components

1. **OpenRunner** (app.py): Main orchestrator that manages providers, sessions, and state persistence
2. **OpenRunnerProvider** (provider.py): Represents an LLM provider (e.g., Ollama) with models, auth, URL, and port
3. **OpenRunnerSession** (session.py): Represents a conversation session linked to a specific provider
4. **OpenRunnerContext** (context.py): Message context with role, text, function calls, and metadata
5. **OpenRunnerTooling** (tooling.py): Developer tooling for creating and testing provider scripts

### Provider System

Providers are extensible via a protocol-based plugin system:

- Provider scripts live in `{data_dir}/providers/`
- Must implement `YourProtocol` with `__init__()` and `smoke_test()` methods
- Create via: `--create-provider-script <name>`
- Test via: `--smoke-test-provider <name>.py`
- Dynamically loaded using `importlib.util`

### CLI Interface

The main entry point (\_\_init\_\_.py) provides argument-based commands:

**Session Management:**
- `--create-session <name>`: Create new session
- `--list-sessions`: List all sessions
- `--attach-session`: Attach to existing session (TBD)

**Provider Management:**
- `--add-provider`: Add provider (prompts for details)
- `--list-providers`: List all providers
- `--remove-provider <name>`: Remove provider
- `--add-provider-model`: Add model to provider
- `--remove-provider-model`: Remove model from provider

**Developer Tools:**
- `--create-provider-script <name>`: Create empty provider script
- `--smoke-test-provider <name>.py`: Test provider implementation

## Message Flow and Context

The system builds context using Ollama's message types:
- **system**: Prompt engineering directives
- **user**: User queries
- **assistant**: LLM responses
- **tools**: Tool call results

Each message type can be parsed to determine system state and control flow. See README.md for notes on quirks with tool calling behavior in smaller models.

## Data Directory Structure

```
~/.local/share/openrunner/nextbubble/
├── data.json           # Serialized OpenRunnerState
└── providers/          # Custom provider scripts
    └── *.py           # Provider implementations
```

## Testing Conventions

- Test files mirror source structure: `test_open_runner_<module>.py`
- Use pytest fixtures for common setup
- Tests are located in `tests/` directory
- Pytest configuration in pyproject.toml sets `pythonpath = ["src"]`
