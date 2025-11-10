# Book Writing Agent 📚

AI Agent untuk menulis buku fiksi dan non-fiksi menggunakan Ollama dengan arsitektur multi-agent yang modular.

## Fitur Utama

- **Outline Otomatis**: Membuat struktur dan outline buku secara otomatis berdasarkan topik
- **Multi-Genre**: Support untuk buku fiksi dan non-fiksi
- **Multiple Agents**: Menggunakan agent khusus untuk planning, writing, dan reviewing
- **Quality Control**: Built-in review system untuk memastikan kualitas konten
- **Modular Architecture**: Struktur kode yang terorganisir dan mudah dikembangkan
- **Output Markdown**: Semua output disimpan dalam format Markdown yang rapi

## Arsitektur Agent

Sistem ini menggunakan 3 agent utama:

1. **Planner Agent** (`gemma3:latest`)
   - Membuat outline dan struktur buku
   - Mengatur chapter dan flow cerita/konten
   - Mendefinisikan karakter (fiksi) atau key points (non-fiksi)

2. **Writer Agent** (`qwen2.5:3b`)
   - Menulis konten chapter yang engaging dan berkualitas
   - Menyesuaikan style berdasarkan tipe buku
   - Menghasilkan konten minimal 1500 kata per chapter

3. **Reviewer Agent** (`kimi-k2:1t-cloud`)
   - Melakukan quality control pada setiap chapter
   - Memberikan score dan feedback konstruktif
   - Mengidentifikasi area yang perlu diperbaiki

## Struktur Project

```
agentwritebook/
├── agentwritebook/
│   ├── agents/              # Agent modules
│   │   ├── base_agent.py    # Base class untuk semua agent
│   │   ├── planner_agent.py # Agent untuk membuat outline
│   │   ├── writer_agent.py  # Agent untuk menulis chapter
│   │   ├── reviewer_agent.py # Agent untuk review
│   │   └── orchestrator.py  # Koordinator semua agent
│   ├── config/              # Configuration
│   │   └── settings.py      # Ollama dan model config
│   ├── utils/               # Utilities
│   │   ├── ollama_client.py # Ollama client wrapper
│   │   └── file_manager.py  # File management untuk output
│   └── main.py              # CLI interface
├── output/                  # Output directory (generated)
├── pyproject.toml          # Project dependencies
└── README.md               # Dokumentasi
```

## Instalasi

### Prerequisites

1. **Ollama** harus sudah terinstall dan running
2. **Python 3.10+**
3. **UV** (Python package manager)

### Install Ollama Models

```bash
# Model untuk planner
ollama pull gemma3:latest

# Model untuk writer
ollama pull qwen2.5:3b

# Model untuk reviewer (judge)
ollama pull kimi-k2:1t-cloud

# Model tambahan (optional)
ollama pull gemma3:1b
ollama pull qwen3:1.7b
ollama pull granite-embedding:latest
```

### Install Project

```bash
# Clone atau download project
cd agentwritebook

# Install dependencies menggunakan uv
uv pip install -e .

# Atau menggunakan pip biasa
pip install -e .
```

## Konfigurasi

Edit `agentwritebook/config/settings.py` jika perlu mengubah:

- **Base URL Ollama**: Default `http://172.29.176.1:11434`
- **Model yang digunakan**: Ubah model sesuai kebutuhan
- **Timeout**: Default 300 detik (5 menit)

```python
class OllamaConfig(BaseModel):
    base_url: str = "http://172.29.176.1:11434"  # Sesuaikan dengan setup Ollama Anda
    timeout: int = 300

class ModelConfig(BaseModel):
    main_model: str = "gemma3:latest"        # Untuk planner
    creative_model: str = "qwen2.5:3b"       # Untuk writer
    judge_model: str = "kimi-k2:1t-cloud"    # Untuk reviewer
```

## Cara Penggunaan

### 1. Membuat Buku Lengkap

```bash
# Buku Fiksi
writebook create "Petualangan di Dunia Fantasi" \
    --type fiction \
    --chapters 12 \
    --audience young_adult \
    --min-words 2000

# Buku Non-Fiksi
writebook create "Panduan Python untuk Pemula" \
    --type non_fiction \
    --chapters 15 \
    --audience professional \
    --min-words 1500
```

### 2. Membuat Outline Saja

```bash
writebook outline "Misteri di Kota Tua" \
    --type fiction \
    --chapters 20
```

### 3. Options Lengkap

```bash
writebook create "Judul Buku" \
    --type fiction              # fiction atau non_fiction
    --chapters 10               # Jumlah chapter (default: 10)
    --audience general          # Target audience (default: general)
    --min-words 1500           # Minimum kata per chapter (default: 1500)
    --review                    # Enable review (default: true)
    --auto-revise              # Auto revisi jika score rendah (default: false)
    --info "Info tambahan"     # Informasi tambahan tentang buku
```

### 4. Commands Lainnya

```bash
# Lihat konfigurasi model
writebook models

# Lihat informasi aplikasi
writebook info

# Help
writebook --help
writebook create --help
```

## Output

Setiap buku yang dibuat akan menghasilkan folder di `output/` dengan struktur:

```
output/
└── Judul_Buku_20250111_123456/
    ├── 00_outline.md              # Outline buku
    ├── 01_Chapter_Title.md        # Chapter 1
    ├── 02_Chapter_Title.md        # Chapter 2
    ├── ...
    ├── Judul_Buku_full.md        # Buku lengkap
    └── metadata.md                # Metadata (stats, scores, dll)
```

### Format Outline (Fiksi)

```markdown
# Outline: Judul Buku

**Genre:** Fantasy Adventure
**Target Audience:** Young Adult

## Synopsis
[Synopsis 2-3 paragraf]

## Chapters

### Chapter 1: Judul Chapter
[Deskripsi apa yang terjadi di chapter ini]
- Key Events
- Character Development
```

### Format Outline (Non-Fiksi)

```markdown
# Outline: Judul Buku

**Genre:** non-fiction
**Target Audience:** Professional

## Synopsis
[Deskripsi dan apa yang akan dipelajari]

## Chapters

### Chapter 1: Judul Chapter
[Deskripsi pembahasan]
- Key Points
- Learning Objectives
```

## Contoh Penggunaan

### Contoh 1: Novel Fiksi

```bash
writebook create "Rahasia Perpustakaan Kuno" \
    --type fiction \
    --chapters 15 \
    --audience young_adult \
    --min-words 2000 \
    --review \
    --info "Cerita petualangan tentang seorang remaja yang menemukan portal magic di perpustakaan tua"
```

Output:
- 15 chapter dengan masing-masing minimal 2000 kata
- Outline dengan karakter, setting, dan plot lengkap
- Review score untuk setiap chapter
- Total ~30,000 kata

### Contoh 2: Buku Non-Fiksi

```bash
writebook create "Menguasai Python dalam 30 Hari" \
    --type non_fiction \
    --chapters 30 \
    --audience beginner \
    --min-words 1500 \
    --info "Tutorial Python step-by-step dari basic hingga intermediate dengan contoh praktis"
```

Output:
- 30 chapter dengan progression dari basic ke advanced
- Setiap chapter dengan key points dan learning objectives
- Contoh kode dan case studies
- Total ~45,000 kata

### Contoh 3: Outline Saja

```bash
# Buat outline dulu untuk review
writebook outline "Panduan Digital Marketing 2025" \
    --type non_fiction \
    --chapters 12

# Review outline, lalu buat bukunya
writebook create "Panduan Digital Marketing 2025" \
    --type non_fiction \
    --chapters 12 \
    --min-words 2000
```

## Tips & Best Practices

### 1. Pilih Jumlah Chapter yang Sesuai

- **Novel Fiksi**: 12-25 chapters (tergantung kompleksitas plot)
- **Non-Fiksi Tutorial**: 10-30 chapters (satu chapter per konsep/topik)
- **Non-Fiksi General**: 8-15 chapters

### 2. Target Words per Chapter

- **Fiksi**: 2000-3000 kata per chapter
- **Non-Fiksi**: 1500-2500 kata per chapter
- Novel rata-rata: 50,000-80,000 kata total

### 3. Target Audience

Sesuaikan dengan pembaca:
- `children`: Anak-anak (8-12 tahun)
- `young_adult`: Remaja (13-18 tahun)
- `general`: Umum/dewasa
- `professional`: Profesional/akademis
- `beginner`: Pemula (untuk tutorial)

### 4. Enable Review

Selalu gunakan `--review` untuk quality control, terutama untuk:
- Buku yang akan dipublikasikan
- Konten yang memerlukan akurasi tinggi
- Project penting

### 5. Auto Revise

Gunakan `--auto-revise` jika:
- Ingin hasil terbaik (lebih lama, tapi lebih berkualitas)
- Tidak keberatan dengan waktu eksekusi lebih lama
- Buku untuk publikasi profesional

## Customization

### Mengubah Model

Edit `agentwritebook/config/settings.py`:

```python
class ModelConfig(BaseModel):
    main_model: str = "gemma3:latest"      # Ubah ke model lain
    creative_model: str = "qwen2.5:3b"     # Untuk creativity yang berbeda
    judge_model: str = "kimi-k2:1t-cloud"  # Model reviewer
```

### Mengubah Writing Style

Saat ini default style adalah `"engaging"`. Untuk mengubah, edit di `orchestrator.py`:

```python
chapter_result = self.writer.execute(
    chapter_info=chapter_info,
    book_context=outline,
    writing_style="formal",  # Ubah: engaging, formal, casual, academic
    min_words=min_words_per_chapter
)
```

### Menambahkan Agent Baru

1. Buat class baru yang inherit dari `BaseAgent`
2. Implement method `execute()`
3. Integrate ke `orchestrator.py`

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
        # Your editing logic
        pass
```

## Troubleshooting

### Error: Connection Refused

```
Error: Connection refused to http://172.29.176.1:11434
```

**Solusi:**
1. Pastikan Ollama running: `ollama serve`
2. Cek base URL di `settings.py` sesuai dengan Ollama Anda
3. Test koneksi: `curl http://172.29.176.1:11434`

### Error: Model Not Found

```
Error: model 'gemma3:latest' not found
```

**Solusi:**
1. Pull model yang diperlukan: `ollama pull gemma3:latest`
2. Cek model tersedia: `ollama list`

### Output Terlalu Pendek

**Solusi:**
1. Tingkatkan `--min-words`
2. Tambahkan detail di `--info`
3. Turunkan temperature di `writer_agent.py` (lebih fokus)

### Review Score Rendah

**Solusi:**
1. Gunakan `--auto-revise` untuk revisi otomatis
2. Review outline terlebih dahulu dengan `writebook outline`
3. Tambahkan detail lebih di outline
4. Ubah model writer ke yang lebih powerful

## Performance

### Estimasi Waktu

Waktu tergantung pada:
- Model yang digunakan (model besar = lebih lambat)
- Hardware (CPU/GPU)
- Panjang chapter (min_words)
- Enable review atau tidak

**Estimasi (dengan model default):**
- Outline: ~30-60 detik
- 1 Chapter (1500 kata): ~2-4 menit
- 1 Chapter dengan review: ~3-6 menit
- Buku 10 chapter dengan review: ~30-60 menit

### Optimasi

1. **Gunakan GPU** jika tersedia untuk Ollama
2. **Model lebih kecil** untuk draft cepat (`gemma3:1b`)
3. **Disable review** untuk draft awal (`--no-review`)
4. **Tulis paralel** (future feature)

## Roadmap

### Planned Features

- [ ] Support untuk multi-language output
- [ ] Parallel chapter writing
- [ ] Custom templates untuk outline
- [ ] Export ke PDF/EPUB
- [ ] Web interface
- [ ] Integration dengan grammar checker
- [ ] Character consistency checker (untuk fiksi)
- [ ] Fact checker (untuk non-fiksi)
- [ ] Continue dari chapter tertentu
- [ ] Regenerate specific chapter

## Contributing

Contributions are welcome! Silakan:

1. Fork repository
2. Buat feature branch
3. Commit changes
4. Push ke branch
5. Create Pull Request

## License

MIT License - Silakan gunakan untuk project personal atau komersial.

## Credits

- **Ollama**: Local LLM runtime
- **Models**: gemma3, qwen2.5, kimi-k2
- **Libraries**: typer, rich, pydantic

## Support

Jika ada pertanyaan atau issue:
1. Check documentation ini
2. Review troubleshooting section
3. Open GitHub issue

---

**Happy Writing! 📚✨**

Dibuat dengan ❤️ menggunakan Ollama dan Python
