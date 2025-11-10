# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Book Writing Agent is a multi-agent AI system for automatically generating fiction and non-fiction books using Ollama LLMs. The system uses three specialized agents (Planner, Writer, Reviewer) orchestrated to create complete books with quality control.

## Development Commands

### Installation
```bash
# Install dependencies (requires Python 3.10+)
uv pip install -e .
# or using pip
pip install -e .
```

### Running the Application
```bash
# Create a complete book
writebook create "Book Title" --type fiction --chapters 10 --min-words 1500

# Create outline only
writebook outline "Book Title" --type fiction --chapters 10

# Show model configuration
writebook models

# Show app info
writebook info
```

### Prerequisites
The following Ollama models must be pulled before running:
```bash
ollama pull gemma3:latest        # Planner agent
ollama pull qwen2.5:3b          # Writer agent
ollama pull kimi-k2:1t-cloud    # Reviewer agent
```

Ensure Ollama is running (`ollama serve`) before executing commands.

## Architecture

### Multi-Agent System
The system follows a **Facade + Strategy pattern** architecture with three specialized agents:

1. **PlannerAgent** (`agents/planner_agent.py`)
   - Model: `gemma3:latest` (temperature: 0.8)
   - Creates book outlines with chapter structure
   - Uses different strategies for fiction vs non-fiction
   - Output: JSON structure with title, synopsis, and chapter descriptions

2. **WriterAgent** (`agents/writer_agent.py`)
   - Model: `qwen2.5:3b` (temperature: 0.85)
   - Writes chapter content based on outline
   - Adapts writing style to book type and audience
   - Enforces minimum word count requirements

3. **ReviewerAgent** (`agents/reviewer_agent.py`)
   - Model: `kimi-k2:1t-cloud` (temperature: 0.3)
   - Evaluates chapter quality with scoring criteria
   - Provides feedback for revisions
   - Different criteria for fiction vs non-fiction

4. **BookOrchestrator** (`agents/orchestrator.py`)
   - Coordinates the workflow between agents
   - Manages file I/O through FileManager
   - Handles review and auto-revision logic
   - Progress tracking with Rich library

### Agent Workflow
```
1. PlannerAgent creates outline
2. FileManager creates output directory
3. For each chapter:
   a. WriterAgent generates content
   b. ReviewerAgent evaluates (if enabled)
   c. Auto-revise if score < threshold (optional)
   d. FileManager saves chapter
4. FileManager combines chapters into full book
5. Metadata saved with statistics
```

### Base Agent Pattern
All agents inherit from `BaseAgent` (`agents/base_agent.py`):
- Template Method pattern for shared functionality
- Abstract `execute()` method for agent-specific logic
- Shared `chat()` method wrapping Ollama client
- Consistent status display via Rich console

## Configuration

### Model Configuration (`config/settings.py`)
Uses Pydantic models for type-safe configuration:
- `OllamaConfig`: base_url and timeout settings
- `ModelConfig`: model names for each agent role
- Singleton instances: `ollama_config`, `model_config`

**Important**: The Ollama base URL is hardcoded to `http://172.29.176.1:11434`. Adjust in `settings.py` for different environments.

### File Structure
```
agentwritebook/
├── agents/
│   ├── base_agent.py      # Abstract base class
│   ├── planner_agent.py   # Outline generation
│   ├── writer_agent.py    # Content writing
│   ├── reviewer_agent.py  # Quality control
│   └── orchestrator.py    # Workflow coordination
├── config/
│   └── settings.py        # Ollama and model config
├── utils/
│   ├── ollama_client.py   # Ollama API wrapper
│   └── file_manager.py    # File operations
└── main.py                # Typer CLI interface
```

Output structure (created at runtime):
```
output/
└── Book_Title_YYYYMMDD_HHMMSS/
    ├── 00_outline.md
    ├── 01_Chapter_Title.md
    ├── 02_Chapter_Title.md
    ├── ...
    ├── Book_Title_full.md
    └── metadata.md
```

## Key Design Decisions

### Strategy Pattern for Book Types
Fiction vs non-fiction handling is implemented via conditional strategies in Planner and Writer agents. Different prompts, evaluation criteria, and structure formats are used based on `book_type` parameter.

### Temperature Settings
- **Planner**: 0.8 (creative planning)
- **Writer**: 0.85 (high creativity for engaging content)
- **Reviewer**: 0.3 (objective, consistent evaluation)

### Error Handling
- Agent-level: Try-catch in each agent's execute()
- Orchestrator-level: Track failed chapters, continue processing
- CLI-level: User-friendly error messages via Rich console

### File Management
All file operations centralized in `FileManager` utility:
- UTF-8 encoding for all files
- Automatic title sanitization for filenames
- Timestamp-based directory naming to avoid conflicts

## Extending the System

### Adding a New Agent
```python
from .base_agent import BaseAgent

class EditorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            model="gemma3:latest",
            role="Editor",
            temperature=0.5
        )

    def execute(self, content: str) -> str:
        # Implementation
        pass
```

Then integrate in `orchestrator.py`.

### Adding New Book Types
Extend the strategy logic in `PlannerAgent` and `WriterAgent` with new conditional branches for the book type.

### Changing Models
Edit `config/settings.py`:
```python
class ModelConfig(BaseModel):
    main_model: str = "gemma3:latest"      # Planner
    creative_model: str = "qwen2.5:3b"     # Writer
    judge_model: str = "kimi-k2:1t-cloud"  # Reviewer
```

## Common Issues

### Connection Refused
- Ensure Ollama is running: `ollama serve`
- Verify base_url in `settings.py` matches your Ollama instance

### Model Not Found
- Pull required models with `ollama pull <model-name>`
- Check available models with `ollama list`

### Short Output
- Increase `--min-words` parameter
- Provide more detail in `--info` parameter
- Models may not always respect word count; this is a known limitation

### Installation Error
If you see "Multiple top-level packages discovered":
```bash
rm -rf output/ agentwritebook.egg-info/
uv pip install -e .
```

## Important Notes

- The system uses **local Ollama models only** - no external API calls
- Generation time depends heavily on model size and hardware (GPU recommended)
- Word count requirements are enforced via prompts but not guaranteed
- Fiction books use character-based structure; non-fiction uses topic-based
- Review scores range 1-10 with different criteria per book type
- Auto-revise feature will regenerate chapters scoring below threshold (typically 7.0)
