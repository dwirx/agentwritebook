# Arsitektur Book Writing Agent

Dokumentasi teknis tentang arsitektur dan desain sistem Book Writing Agent.

## Overview

Book Writing Agent adalah sistem multi-agent yang dirancang untuk menghasilkan buku secara otomatis menggunakan Large Language Models (LLMs) melalui Ollama. Sistem ini menggunakan arsitektur modular dengan separation of concerns yang jelas.

## Arsitektur High-Level

```
┌─────────────────────────────────────────────────────────────┐
│                        CLI Interface                         │
│                      (Typer + Rich)                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Book Orchestrator                         │
│              (Koordinasi & Workflow)                         │
└─────┬──────────────────┬──────────────────┬─────────────────┘
      │                  │                  │
      ▼                  ▼                  ▼
┌──────────┐      ┌──────────┐      ┌──────────┐
│ Planner  │      │  Writer  │      │ Reviewer │
│  Agent   │      │  Agent   │      │  Agent   │
└────┬─────┘      └────┬─────┘      └────┬─────┘
     │                 │                  │
     └─────────────────┴──────────────────┘
                       │
                       ▼
            ┌──────────────────┐
            │  Ollama Client   │
            │    (Wrapper)     │
            └────────┬─────────┘
                     │
                     ▼
            ┌──────────────────┐
            │   Ollama API     │
            │  (Local LLMs)    │
            └──────────────────┘
                     │
            ┌────────┴─────────┐
            ▼                  ▼
     ┌─────────────┐    ┌──────────────┐
     │   gemma3    │    │  qwen2.5:3b  │
     │  (Planner)  │    │   (Writer)   │
     └─────────────┘    └──────────────┘
                  ▼
         ┌──────────────────┐
         │  kimi-k2:1t      │
         │   (Reviewer)     │
         └──────────────────┘
```

## Komponen Utama

### 1. CLI Interface (`main.py`)

**Responsibility**: User interface dan command handling

**Teknologi**: Typer (CLI framework), Rich (terminal formatting)

**Commands**:
- `create`: Membuat buku lengkap
- `outline`: Membuat outline saja
- `models`: Menampilkan konfigurasi model
- `info`: Menampilkan informasi aplikasi

**Flow**:
```
User Input → Command Parser → Orchestrator → Output
```

### 2. Book Orchestrator (`agents/orchestrator.py`)

**Responsibility**: Koordinasi workflow dan manajemen agents

**Key Methods**:
- `create_book()`: Main workflow untuk membuat buku lengkap
- `create_outline_only()`: Workflow untuk outline saja
- `write_single_chapter()`: Menulis satu chapter
- `_revise_chapter()`: Revisi chapter berdasarkan feedback

**Workflow**:
```
1. Call Planner Agent → Generate Outline
2. Create Book Directory
3. For each chapter:
   a. Call Writer Agent → Generate Content
   b. Call Reviewer Agent → Review Content (optional)
   c. Auto Revise if needed (optional)
   d. Save Chapter
4. Combine all chapters → Full Book
5. Save Metadata
```

### 3. Agent System

#### Base Agent (`agents/base_agent.py`)

Abstract base class untuk semua agents dengan shared functionality:

```python
class BaseAgent(ABC):
    - model: str              # Model yang digunakan
    - role: str               # Role agent
    - temperature: float      # Temperature untuk generation

    Methods:
    - execute(**kwargs)       # Abstract: task execution
    - chat(messages)          # Chat dengan model
    - display_status(msg)     # Display status messages
    - create_system_prompt()  # Buat system prompt
```

#### Planner Agent (`agents/planner_agent.py`)

**Model**: `gemma3:latest` (configurable)

**Temperature**: 0.8 (lebih kreatif)

**Responsibility**:
- Membuat outline buku
- Struktur chapter
- Character development (fiksi)
- Learning objectives (non-fiksi)

**Input**:
- Topic/title
- Book type (fiction/non_fiction)
- Number of chapters
- Target audience
- Additional info

**Output**:
```json
{
  "title": "...",
  "genre": "...",
  "synopsis": "...",
  "chapters": [
    {
      "number": 1,
      "title": "...",
      "description": "...",
      "key_events": [...] // or key_points for non-fiction
    }
  ]
}
```

**Design Patterns**:
- Strategy Pattern: Different strategies untuk fiction vs non-fiction
- Template Method: Shared outline generation dengan customization per type

#### Writer Agent (`agents/writer_agent.py`)

**Model**: `qwen2.5:3b` (configurable)

**Temperature**: 0.85 (high creativity)

**Responsibility**:
- Menulis konten chapter
- Maintain consistency dengan outline
- Adaptive writing style

**Input**:
- Chapter info dari outline
- Book context
- Writing style preference
- Minimum word count

**Output**:
```python
{
  "chapter_number": int,
  "chapter_title": str,
  "content": str,
  "word_count": int,
  "char_count": int
}
```

**Features**:
- Different prompts untuk fiction vs non-fiction
- Style-aware generation
- Length control
- Section expansion capability

#### Reviewer Agent (`agents/reviewer_agent.py`)

**Model**: `kimi-k2:1t-cloud` (judge model)

**Temperature**: 0.3 (objektif dan konsisten)

**Responsibility**:
- Quality control
- Scoring berdasarkan criteria
- Constructive feedback
- Issue identification

**Input**:
- Chapter content
- Chapter info
- Book context
- Review criteria

**Output**:
```python
{
  "overall_score": float,  # 1-10
  "criteria_scores": dict,
  "feedback": str,
  "needs_revision": bool
}
```

**Review Criteria**:

Fiction:
- story_engagement
- character_development
- dialogue_quality
- pacing
- writing_style

Non-Fiction:
- clarity
- information_quality
- structure
- actionability
- writing_style

### 4. Configuration (`config/settings.py`)

**Pydantic Models** untuk type-safe configuration:

```python
OllamaConfig:
- base_url: str
- timeout: int

ModelConfig:
- main_model: str        # Planner
- fast_model: str
- creative_model: str    # Writer
- detail_model: str
- judge_model: str       # Reviewer
- embedding_model: str
```

**Singleton Pattern**: Global config instances

### 5. Utilities

#### Ollama Client (`utils/ollama_client.py`)

**Responsibility**: Wrapper untuk Ollama API dengan error handling

**Methods**:
- `chat()`: Chat completion
- `generate()`: Text generation
- `list_models()`: List available models

**Features**:
- Custom configuration
- Error handling
- Temperature control
- Streaming support (future)

#### File Manager (`utils/file_manager.py`)

**Responsibility**: File operations dan output management

**Methods**:
- `create_book_directory()`: Buat folder untuk buku
- `save_outline()`: Simpan outline
- `save_chapter()`: Simpan chapter
- `save_full_book()`: Gabung semua chapter
- `save_metadata()`: Simpan metadata

**Output Structure**:
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

## Design Patterns

### 1. Strategy Pattern

Digunakan di Planner dan Writer untuk handling fiction vs non-fiction:

```python
if book_type == "fiction":
    outline = self._create_fiction_outline(...)
else:
    outline = self._create_nonfiction_outline(...)
```

### 2. Template Method Pattern

Base Agent menyediakan template dengan hooks untuk customization:

```python
class BaseAgent(ABC):
    @abstractmethod
    def execute(self, **kwargs):
        pass

    def chat(self, messages):
        # Shared implementation
```

### 3. Singleton Pattern

Configuration dan client instances:

```python
ollama_config = OllamaConfig()
model_config = ModelConfig()
ollama_client = OllamaClient()
file_manager = FileManager()
orchestrator = BookOrchestrator()
```

### 4. Facade Pattern

Orchestrator menyediakan simplified interface untuk complex subsystem:

```python
orchestrator.create_book(...)  # Hides complexity dari multi-agent coordination
```

### 5. Builder Pattern (Implicit)

File Manager membangun struktur output secara bertahap.

## Data Flow

### Create Book Flow

```
User Command
    ↓
CLI Parser
    ↓
Orchestrator.create_book()
    ↓
PlannerAgent.execute()
    ↓ (outline)
FileManager.create_book_directory()
    ↓
For each chapter:
    ↓
    WriterAgent.execute()
        ↓ (content)
    ReviewerAgent.execute() [optional]
        ↓ (review)
    Auto-revise [if needed]
        ↓
    FileManager.save_chapter()
    ↓
FileManager.save_full_book()
    ↓
FileManager.save_metadata()
    ↓
Display Summary
```

## Error Handling

### Levels

1. **Agent Level**: Try-catch dalam setiap agent execution
2. **Orchestrator Level**: Track failed chapters, continue dengan yang lain
3. **CLI Level**: User-friendly error messages

### Recovery Strategies

- **Model tidak tersedia**: Fallback ke model alternatif (future)
- **Chapter gagal**: Lanjut ke chapter berikutnya, track failures
- **Review score rendah**: Auto-revise jika enabled
- **Connection error**: Retry dengan exponential backoff (future)

## Performance Considerations

### Bottlenecks

1. **LLM Inference**: Terbesar, depend on model size dan hardware
2. **Network Latency**: Minimal (local Ollama)
3. **File I/O**: Minimal

### Optimization Strategies

1. **Model Selection**:
   - Use faster models untuk drafts
   - Use better models untuk final version

2. **Parallel Processing** (Future):
   - Write multiple chapters in parallel
   - Async operations

3. **Caching** (Future):
   - Cache common prompts
   - Reuse outline untuk multiple attempts

4. **Streaming** (Future):
   - Stream chapter content as generated
   - Real-time progress display

## Security Considerations

### Current

- Local execution only (no external API calls)
- File system access controlled
- No sensitive data storage

### Future

- Input sanitization untuk user prompts
- Rate limiting untuk API calls
- Secure credential storage jika cloud models

## Extensibility

### Adding New Agents

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

### Adding New Book Types

Extend Planner dan Writer:

```python
def _create_poetry_outline(self, ...):
    # Poetry-specific outline
    pass
```

### Adding New Output Formats

Extend File Manager:

```python
def export_to_pdf(self, book_dir: Path) -> Path:
    # PDF export implementation
    pass
```

## Testing Strategy (Future)

### Unit Tests

- Test each agent independently dengan mock Ollama client
- Test utility functions
- Test configuration loading

### Integration Tests

- Test agent coordination dalam orchestrator
- Test file operations
- Test end-to-end workflows

### Performance Tests

- Benchmark generation time
- Memory usage profiling
- Model comparison

## Dependencies

### Core
- `ollama`: Ollama Python SDK
- `pydantic`: Data validation
- `rich`: Terminal formatting
- `typer`: CLI framework

### Why These Dependencies?

- **ollama**: Official SDK, reliable, well-maintained
- **pydantic**: Type safety, validation, excellent DX
- **rich**: Beautiful terminal output, progress bars
- **typer**: Modern CLI framework, built on click

## Configuration Management

### Levels

1. **Code Level**: Default values di `settings.py`
2. **Environment Variables** (Future): Override defaults
3. **Config File** (Future): User-specific settings

### Current

All configuration via `settings.py`:
```python
ollama_config = OllamaConfig()
model_config = ModelConfig()
```

## Monitoring & Logging (Future)

### Planned Features

- Structured logging dengan levels
- Performance metrics
- Error tracking
- Usage analytics

## Deployment

### Current: Local Development

```bash
uv pip install -e .
writebook create "Title"
```

### Future: Distribution

- PyPI package
- Docker container
- Standalone binary

## Roadmap

### v1.0 (Current)
- ✅ Multi-agent system
- ✅ Fiction & non-fiction support
- ✅ Review system
- ✅ CLI interface
- ✅ Markdown output

### v1.1 (Next)
- [ ] Parallel chapter generation
- [ ] Streaming output
- [ ] Better error recovery
- [ ] Configuration file support

### v2.0 (Future)
- [ ] Web interface
- [ ] PDF/EPUB export
- [ ] Multi-language support
- [ ] Cloud model support
- [ ] Character consistency checker
- [ ] Fact checker

## Contributing Guidelines

### Code Style

- Follow PEP 8
- Use type hints
- Docstrings for all public methods
- Keep functions small and focused

### Pull Request Process

1. Fork repository
2. Create feature branch
3. Write tests
4. Update documentation
5. Submit PR

## License

MIT License - See LICENSE file

---

**Maintainer**: Book Writing Agent Team
**Version**: 1.0.0
**Last Updated**: 2025-01-11
