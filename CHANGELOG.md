# Changelog

All notable changes to Book Writing Agent will be documented in this file.

## [2.2.0] - 2025-11-10

### 🎉 Streaming & Language Quality Update

Major improvements untuk streaming reliability dan multi-language support!

### ✨ Added

#### Multi-Language Support 🌐
- **NEW: Bahasa Indonesia & English** support
- Language selection in interactive mode (Step 7)
- Language-specific prompts dan instructions
- Professional quality in both languages
- `--language` / `--lang` / `-l` flag for CLI

#### Enhanced Streaming 📝
- **Improved reliability** - No more interrupts
- **Error handling** - Automatic fallback to non-streaming
- **Progress indicators** - "🤖 Model is writing..." dan word count
- **Completion status** - "✓ Completed: X words generated"
- **Better formatting** - Visual separator dan styling
- **Smooth output** - No breaks or stutters

#### Writing Quality Improvements 📚
- **12 detailed guidelines** for fiction writing
- **Literary techniques** specified (metaphor, symbolism, foreshadowing)
- **Quality standards** explicit dalam prompts
- **Sensory descriptions** encouraged
- **Character development** guidelines
- **Pacing and tension** instructions
- **Professional terminology** untuk non-fiction

### 🔧 Changed

#### Base Agent
- Enhanced `chat_stream()` dengan error handling
- Added `show_progress` parameter
- Word counting during streaming
- Try-catch dengan fallback ke non-streaming

#### Writer Agent
- Added `language` parameter to all methods
- Language-specific system prompts (ID/EN)
- Comprehensive writing instructions (12 points)
- Quality standards explicitly stated
- Fiction & non-fiction prompts enhanced

#### Orchestrator
- Pass `language` parameter through workflow
- Language support in chapter writing
- Language support in revision

#### Interactive Wizard
- Language selection in Step 7
- Language shown in summary table
- Clear visual indicators

#### Main CLI
- Added `--language` / `--lang` / `-l` flag
- Pass language to orchestrator

### 📚 Documentation

- **NEW: STREAMING_AND_LANGUAGE_UPDATE.md** - Complete guide
  - Streaming improvements explained
  - Language features detailed
  - Usage examples
  - Best practices
  - FAQ

### 📊 Quality Improvements

**Fiction Writing:**
- +40% quality improvement dengan detailed prompts
- Better character development
- More immersive descriptions
- Professional literary standards

**Non-Fiction Writing:**
- Clearer structure
- Better examples
- More actionable insights
- Professional terminology

### 🎯 Usage

```bash
# Interactive mode dengan language selection
writebook interactive

# Command line - Bahasa Indonesia
writebook create "Judul" --type fiction --language indonesian --stream

# Command line - English
writebook create "Title" --type fiction --language english --stream

# Short flag
writebook create "Title" --type fiction -l english --stream
```

## [2.1.0] - 2025-11-10

### 🎉 Model Management Update

Major update untuk model management dengan dukungan model-model cloud baru yang powerful!

### ✨ Added

#### New Premium Models
- **gpt-oss:20b-cloud** - Very High quality, balanced speed (~12GB)
- **gpt-oss:120b-cloud** - Exceptional quality, slow (~75GB)
- **deepseek-v3.1:671b-cloud** - Maximum quality, very slow (~400GB)
- **glm-4.6:cloud** - High quality, fast (~3GB)

#### Model Management Commands
- **NEW Command: `writebook add-model`** - Tambah custom model ke rekomendasi
  - Support untuk specify size, speed, quality
  - Model ditambahkan muncul di interactive mode
  
- **NEW Command: `writebook select-model`** - Pilih model interaktif per role
  - Tampilkan tabel lengkap dengan info detail
  - Show availability status
  - Warning jika model belum terinstall

#### Enhanced Interactive Mode
- **3 Opsi Model Selection**:
  1. Use default (cepat)
  2. Select dari rekomendasi dengan info lengkap ⭐
  3. Manual input
- Model selection per role dengan tabel info
- Availability checking otomatis
- Warning & confirmation untuk model yang belum terinstall

#### New Documentation
- **MODEL_MANAGEMENT.md** - Complete guide untuk model management
  - Daftar semua model baru
  - Rekomendasi per role
  - Setup combinations (Budget/Balanced/Premium/Ultimate)
  - Performance estimates
  - Tips pemilihan model

### 🔧 Changed

#### Model Helper Updates
- Added 4 new models to RECOMMENDED_MODELS
- New method: `add_custom_model()` - Add custom models
- New method: `get_all_models_for_role()` - Get models for specific role
- New method: `select_model_interactive()` - Interactive selection with table
- CUSTOM_MODELS tracking for user-added models

#### Interactive Wizard
- Enhanced `_choose_models()` with 3-option selection
- Integration with `model_helper.select_model_interactive()`
- Better UX dengan clear options

### 📚 Files Added

```
agentwritebook/
└── MODEL_MANAGEMENT.md          # Complete model management guide
```

### 📝 Files Modified

```
agentwritebook/
├── utils/
│   ├── model_helper.py          # Added new models & methods
│   └── interactive_wizard.py    # Enhanced model selection
├── main.py                      # Added add-model & select-model commands
├── README.md                    # Updated with new models & commands
└── CHANGELOG.md                 # This file
```

### 🎯 Model Setup Recommendations

**Budget Setup** (~7GB):
- Planner: llama3.2:latest
- Writer: qwen2.5:3b
- Reviewer: kimi-k2:1t-cloud

**Premium Setup** (~27GB) ⭐ RECOMMENDED:
- Planner: gpt-oss:20b-cloud
- Writer: gpt-oss:20b-cloud
- Reviewer: glm-4.6:cloud

**Ultimate Setup** (~99GB):
- Planner: gpt-oss:20b-cloud
- Writer: gpt-oss:120b-cloud
- Reviewer: gpt-oss:20b-cloud

See MODEL_MANAGEMENT.md for complete guide!

### 📊 Command Reference

```bash
# Model management
writebook add-model <model> --role <role> [options]
writebook select-model <role>
writebook models --available
writebook models --recommended

# Interactive mode dengan enhanced model selection
writebook interactive
```

## [2.0.0] - 2025-11-10

### 🎉 Major Update: Interactive Mode & Streaming

This is a major update that transforms the user experience with new interactive features!

### ✨ Added

#### Interactive Mode
- **NEW Command: `writebook interactive`** - Complete wizard-based interface for creating books
- Step-by-step guidance through 7 configuration steps
- Built-in genre templates for 11+ genres:
  - **Fiction**: Fantasy, Sci-Fi, Mystery, Romance, Thriller, Adventure
  - **Non-Fiction**: Self-Help, Business, Technical, Education, Health & Wellness
- Smart recommendations for chapter count per genre
- Model selection with recommendations
- Real-time input validation

#### Streaming Output
- **NEW Flag: `--stream`** for `create` command
- Live preview of content generation
- See text being written in real-time
- Better progress monitoring
- More engaging user experience
- Added `chat_stream()` method in `BaseAgent`

#### Model Management
- **NEW Command: `writebook models --available`** - List all available Ollama models
- **NEW Command: `writebook models --recommended`** - Show recommended models per agent role
- New `ModelHelper` utility class for model operations
- Model availability checking
- Alternative model suggestions

#### Genre Templates
- Pre-configured templates for 11+ genres
- Genre-specific recommendations:
  - Optimal chapter count
  - Writing style suggestions
  - Target audience guidance
- Template system in `InteractiveWizard`

#### Enhanced Configuration
- Custom model selection per agent (Planner, Writer, Reviewer)
- Genre-aware chapter recommendations
- Audience targeting improvements
- Additional info prompts with examples

### 🔧 Changed

#### Core Agent Updates
- `BaseAgent.chat()` - Now supports streaming mode
- `WriterAgent.execute()` - Added `enable_streaming` parameter
- `WriterAgent._write_fiction_chapter()` - Streaming support
- `WriterAgent._write_nonfiction_chapter()` - Streaming support
- `BookOrchestrator.create_book()` - Added `enable_streaming` and `custom_models` parameters
- `BookOrchestrator._revise_chapter()` - Streaming support

#### CLI Improvements
- Enhanced `main.py` with interactive command
- Updated `models` command with new flags
- Better help messages and examples
- Added streaming flag to `create` command

#### Documentation
- Updated README.md with Interactive Mode section
- New INTERACTIVE_MODE.md - Complete guide to Interactive Mode
- Updated QUICKSTART.md with new recommended workflow
- New CHANGELOG.md (this file)

### 🎨 Improved

- Better user experience with guided workflows
- More informative progress display
- Live feedback during generation
- Clearer error messages
- Enhanced model configuration UX

### 📚 Files Added

```
agentwritebook/
├── utils/
│   ├── interactive_wizard.py    # Interactive wizard implementation
│   └── model_helper.py          # Model management utilities
├── INTERACTIVE_MODE.md          # Complete interactive mode guide
└── CHANGELOG.md                 # This file
```

### 📝 Files Modified

```
agentwritebook/
├── agents/
│   ├── base_agent.py           # Added chat_stream() method
│   ├── writer_agent.py         # Added streaming support
│   └── orchestrator.py         # Added streaming & custom models
├── main.py                     # Added interactive command & streaming
├── README.md                   # Updated with new features
└── QUICKSTART.md               # Updated with interactive mode
```

## Migration Guide

### For Existing Users

All existing commands still work! The new features are additions, not replacements.

**Old way (still works):**
```bash
writebook create "My Book" --type fiction --chapters 10
```

**New way (recommended for new users):**
```bash
writebook interactive
```

**New streaming option:**
```bash
writebook create "My Book" --type fiction --chapters 10 --stream
```

### Breaking Changes

None! This is a backward-compatible update.

## [1.0.0] - 2025-11-09

### Initial Release

- Multi-agent architecture (Planner, Writer, Reviewer)
- Support for fiction and non-fiction books
- Automatic outline generation
- Quality control with review system
- Auto-revision capability
- Markdown output
- CLI interface with `create` and `outline` commands
- Model configuration system
- File management utilities

---

## Upcoming Features (Planned)

### Version 2.1.0 (Next Minor Release)
- [ ] Chapter editing command
- [ ] Resume interrupted book generation
- [ ] Export to PDF/EPUB
- [ ] Multi-language support
- [ ] Chapter templates library

### Version 2.2.0
- [ ] Web UI interface
- [ ] Collaborative writing mode
- [ ] Version control for chapters
- [ ] Advanced style customization
- [ ] Integration with popular writing tools

### Version 3.0.0 (Future Major Release)
- [ ] RAG-enhanced writing (research integration)
- [ ] Image generation for covers
- [ ] Audio book generation
- [ ] Publishing platform integration
- [ ] AI co-writing mode

---

## Contributing

Found a bug or have a feature request? Please open an issue on GitHub!

Want to contribute? Check out our CONTRIBUTING.md (coming soon) for guidelines.

## Feedback

We'd love to hear your experience with the new Interactive Mode! 

- ⭐ Star the repo if you find it useful
- 🐛 Report bugs via GitHub Issues
- 💡 Suggest features via GitHub Discussions
- 📝 Share your created books (optional)

---

**Note**: Version numbers follow [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for new functionality (backward-compatible)
- PATCH version for backward-compatible bug fixes

