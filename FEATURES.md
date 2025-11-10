# Features Overview

Daftar lengkap fitur Book Writing Agent dengan penjelasan detail.

## 🎯 Interactive Mode (NEW!)

Mode wizard step-by-step yang memudahkan pembuatan buku.

### Keunggulan:
- ✅ **User-Friendly**: Tidak perlu hafal command line arguments
- ✅ **Guided Experience**: Dipandu melalui 7 langkah konfigurasi
- ✅ **Smart Recommendations**: Saran otomatis untuk chapter count, model, dll
- ✅ **Input Validation**: Validasi real-time untuk mencegah error
- ✅ **Template Library**: 11+ genre templates siap pakai

### Genre Templates:

**Fiction (6 genres):**
1. **Fantasy** - Magic, dunia fantasi, makhluk mistis
   - Recommended: 15 chapters
   - Examples: Harry Potter, Lord of the Rings
   
2. **Science Fiction** - Futuristik, teknologi canggih, space exploration
   - Recommended: 12 chapters
   - Examples: Dune, Foundation
   
3. **Mystery/Detective** - Investigasi, plot twist, suspense
   - Recommended: 10 chapters
   - Examples: Sherlock Holmes, Agatha Christie
   
4. **Romance** - Love story, character development
   - Recommended: 12 chapters
   - Examples: Pride and Prejudice, The Notebook
   
5. **Thriller/Suspense** - High tension, psychological
   - Recommended: 14 chapters
   - Examples: Gone Girl, The Girl with the Dragon Tattoo
   
6. **Adventure** - Action-packed, exploration
   - Recommended: 13 chapters
   - Examples: Indiana Jones, Treasure Island

**Non-Fiction (5 categories):**
1. **Self-Help/Personal Development** - Motivasi, pengembangan diri
   - Recommended: 10 chapters
   - Examples: Atomic Habits, The 7 Habits
   
2. **Business/Entrepreneurship** - Strategi bisnis, startup, management
   - Recommended: 12 chapters
   - Examples: Good to Great, The Lean Startup
   
3. **Technical/Programming** - Tutorial, coding, tech guides
   - Recommended: 15 chapters
   - Examples: Clean Code, Design Patterns
   
4. **Educational/Tutorial** - Learning materials, how-to guides
   - Recommended: 12 chapters
   - Examples: Various educational books
   
5. **Health & Wellness** - Fitness, nutrition, mental health
   - Recommended: 10 chapters
   - Examples: Why We Sleep, The Body Keeps the Score

### Interactive Wizard Steps:

1. **Book Type Selection**
   - Fiction or Non-Fiction
   
2. **Genre/Category Selection**
   - Beautiful table display with descriptions and examples
   - Genre-specific recommendations
   
3. **Book Details**
   - Title/topic
   - Additional info with examples (setting, characters, tone, etc.)
   
4. **Chapter Configuration**
   - Number of chapters (with smart defaults)
   - Minimum words per chapter
   
5. **Target Audience**
   - General, Young Adult, Children, Professional, Academic, Custom
   
6. **Model Selection**
   - Use defaults (recommended)
   - Custom models with guided selection
   
7. **Writing Options**
   - Enable review (quality control)
   - Auto-revise (automatic improvements)
   - Enable streaming (live preview)

### Usage:
```bash
writebook interactive
```

**[📖 Full Interactive Mode Guide](INTERACTIVE_MODE.md)**

---

## 📝 Streaming Output (NEW!)

Lihat proses penulisan secara real-time.

### Keunggulan:
- ✅ **Live Preview**: Teks muncul saat ditulis AI
- ✅ **Progress Monitoring**: Tahu apa yang sedang dikerjakan
- ✅ **Better Debugging**: Identifikasi masalah lebih cepat
- ✅ **Engaging Experience**: Lebih interaktif dan menarik
- ✅ **Visual Feedback**: Separator dan formatting yang jelas

### How It Works:
```
Chapter 1: Awal Petualangan
────────────────────────────────────────────────────────────

Generating with qwen2.5:3b...
Di sebuah desa terpencil di kaki gunung Himalaya, hiduplah 
seorang pemuda bernama Arjun. Setiap pagi, ia bangun dengan 
suara burung-burung yang berkicau riang...
[Teks muncul kata demi kata secara real-time]
────────────────────────────────────────────────────────────
✓ Chapter 1 selesai! (1847 kata)
```

### Usage:
```bash
# Dalam interactive mode
writebook interactive
# (pilih Yes saat ditanya streaming)

# Atau dengan command line
writebook create "Book Title" --type fiction --chapters 10 --stream
```

### Technical Implementation:
- Uses Ollama's streaming API
- Word-by-word display via Rich console
- Buffering for smooth display
- Full content saved regardless of display

---

## 🤖 Multi-Agent System

Arsitektur modular dengan 3 agent spesialisasi.

### 1. Planner Agent
**Model**: `gemma3:latest` (default)
**Temperature**: 0.8 (creative planning)
**Role**: Strategic planning and structure

**Responsibilities:**
- Create book outline
- Define chapter structure
- Fiction: Character development, plot arcs
- Non-Fiction: Learning objectives, key points
- Ensure logical flow

**Output:**
```json
{
  "title": "Book Title",
  "genre": "fantasy",
  "synopsis": "...",
  "chapters": [
    {
      "number": 1,
      "title": "Chapter Title",
      "description": "...",
      "key_events": [...]
    }
  ]
}
```

### 2. Writer Agent
**Model**: `qwen2.5:3b` (default)
**Temperature**: 0.85 (high creativity)
**Role**: Content generation

**Responsibilities:**
- Write chapter content
- Adapt style to genre and audience
- Maintain consistency with outline
- Meet word count requirements
- Engaging narrative/clear explanations

**Features:**
- Fiction: Show don't tell, vivid descriptions, natural dialogue
- Non-Fiction: Clear structure, actionable insights, examples

### 3. Reviewer Agent
**Model**: `kimi-k2:1t-cloud` (default)
**Temperature**: 0.3 (objective evaluation)
**Role**: Quality control

**Responsibilities:**
- Evaluate chapter quality
- Score 1-10 scale
- Provide constructive feedback
- Identify improvement areas
- Recommend revisions if needed

**Scoring Criteria:**
- **Fiction**: Engagement, pacing, character development, dialogue, description
- **Non-Fiction**: Clarity, structure, depth, examples, actionable insights

---

## ⚙️ Model Management (NEW!)

Comprehensive model selection and management.

### Features:

1. **List Available Models**
```bash
writebook models --available
```
Shows all models installed in Ollama with role recommendations.

2. **Show Recommended Models**
```bash
writebook models --recommended
```
Displays recommended models per agent role with specs:
- Model name
- Size
- Speed
- Quality
- Availability status

3. **Current Configuration**
```bash
writebook models
```
Shows currently configured models.

### Model Recommendations:

**Planner Models:**
- `gemma3:latest` (9GB) - High quality, medium speed
- `llama3.2:latest` (4GB) - Good balance
- `qwen2.5:7b` (4.7GB) - High quality

**Writer Models:**
- `qwen2.5:3b` (2GB) - Fast, good quality ⭐ Recommended
- `gemma3:latest` (9GB) - High quality
- `llama3.2:3b` (2GB) - Fast, decent quality

**Reviewer Models:**
- `kimi-k2:1t-cloud` (700MB) - Very fast ⭐ Recommended
- `qwen2.5:3b` (2GB) - Fast, good
- `gemma3:latest` (9GB) - High quality

### Custom Model Selection:
```bash
# Via interactive mode
writebook interactive
# (Select custom models in step 6)

# Or programmatically (for advanced users)
# Edit config/settings.py
```

---

## ✅ Quality Control

Multi-layer quality assurance system.

### Review System:
- **Automatic Scoring**: 1-10 scale per chapter
- **Detailed Feedback**: Strengths and weaknesses
- **Improvement Suggestions**: Specific actionable feedback
- **Threshold Detection**: Flags chapters needing work

### Auto-Revision:
```bash
writebook create "Title" --type fiction --auto-revise
```
- Automatically rewrites low-scoring chapters
- Uses higher temperature for creativity
- Incorporates reviewer feedback
- Retry until acceptable quality

### Manual Options:
```bash
# Disable review for faster generation
writebook create "Title" --type fiction --no-review

# Enable review but no auto-revise
writebook create "Title" --type fiction --review
```

---

## 📊 Smart Configuration

Genre-aware and audience-tailored settings.

### Automatic Optimization:
- **Chapter Count**: Genre-specific recommendations
- **Word Count**: Adjusted per book type
- **Writing Style**: Adapted to audience
- **Temperature Settings**: Role-optimized

### Audience Targeting:
- **General**: Accessible to all
- **Young Adult**: Teen-friendly
- **Children**: Simple language
- **Professional**: Business/technical tone
- **Academic**: Scholarly approach

### Configuration Priority:
1. User explicit input (highest)
2. Genre recommendations
3. Audience preferences
4. System defaults (fallback)

---

## 📄 Output Management

Professional output with organized file structure.

### Output Structure:
```
output/
└── Book_Title_20250110_150423/
    ├── 00_outline.md              # Complete outline
    ├── 01_Chapter_One.md          # Chapter 1
    ├── 02_Chapter_Two.md          # Chapter 2
    ├── ...
    ├── Book_Title_full.md         # Complete book
    └── metadata.md                # Statistics & scores
```

### Features:
- **Timestamped Directories**: Avoid conflicts
- **UTF-8 Encoding**: Full Unicode support
- **Markdown Format**: Easy to edit and convert
- **Metadata Tracking**: Statistics and scores
- **Incremental Saving**: Chapters saved as completed

### Metadata Includes:
- Total words
- Chapter count
- Average review score
- Generation time
- Model configuration
- Failed chapters (if any)

---

## 🔧 Advanced Features

For power users and developers.

### 1. Outline-Only Mode
```bash
writebook outline "Book Title" --type fiction --chapters 10
```
Generate outline without writing chapters.

### 2. Custom Temperature
Modify agent temperatures in code for specific needs.

### 3. API Integration
Use agents programmatically:
```python
from agentwritebook.agents import PlannerAgent, WriterAgent

planner = PlannerAgent()
outline = planner.execute(topic="My Book", ...)

writer = WriterAgent()
chapter = writer.execute(chapter_info=..., ...)
```

### 4. Extensibility
- Add new genres in `interactive_wizard.py`
- Customize prompts in agent files
- Add new agents by extending `BaseAgent`
- Create custom orchestration workflows

---

## 🚀 Performance

Optimized for efficiency.

### Speed Factors:
- **Model Size**: Smaller = faster
- **Hardware**: GPU > CPU
- **Streaming**: Minimal overhead
- **Parallel Processing**: Multiple chapters possible (planned)

### Estimated Times (per chapter):
- **Small Models** (1-3B): 2-5 minutes
- **Medium Models** (7-8B): 5-10 minutes
- **Large Models** (13B+): 10-20 minutes

*Times vary based on hardware, word count, and complexity*

### Optimization Tips:
- Use `qwen2.5:3b` for speed
- Disable review for drafts
- Lower word count for faster iteration
- Use GPU if available

---

## 🛡️ Error Handling

Robust error management system.

### Features:
- **Graceful Degradation**: Continue on chapter failures
- **Progress Saving**: Completed chapters preserved
- **Clear Error Messages**: User-friendly explanations
- **Retry Logic**: Auto-retry on temporary failures
- **Validation**: Input validation prevents common errors

### Resume Capability (Planned):
Future versions will support resuming interrupted generations.

---

## 📝 Workflow Comparison

| Feature | Interactive Mode | Command Line | Outline Only |
|---------|-----------------|--------------|--------------|
| Ease of Use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Speed | Medium | Fast | Very Fast |
| Guidance | Full | None | None |
| Templates | ✓ Built-in | Manual | Manual |
| Streaming | ✓ Optional | ✓ Flag | ✗ |
| Best For | Beginners | Power users | Planning phase |

---

## 🎓 Learning Resources

- **[README.md](README.md)** - Complete documentation
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
- **[INTERACTIVE_MODE.md](INTERACTIVE_MODE.md)** - Interactive mode deep dive
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Problem solving
- **[CLAUDE.md](CLAUDE.md)** - Architecture and development guide
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

---

## 🔮 Upcoming Features

See [CHANGELOG.md](CHANGELOG.md) for planned features in upcoming versions.

### Version 2.1.0 (Next):
- Chapter editing command
- Resume functionality
- Export to PDF/EPUB
- Multi-language support

### Version 3.0.0 (Future):
- RAG-enhanced writing
- Image generation
- Audio book generation
- Web UI

---

## ❓ FAQ

**Q: Which mode should I use?**
A: Start with `writebook interactive` for the best experience.

**Q: Can I edit the output?**
A: Yes! All files are Markdown and easily editable.

**Q: Does streaming affect quality?**
A: No, it only changes how output is displayed.

**Q: Can I use different models?**
A: Yes, via interactive mode or by editing `config/settings.py`.

**Q: How long does it take?**
A: 5-15 minutes per chapter with medium models on standard hardware.

**Q: Can I cancel during generation?**
A: Yes (Ctrl+C). Completed chapters are saved.

---

**Ready to start? Try:**
```bash
writebook interactive
```

Happy writing! 📚✨

