# Quick Start Guide

Panduan cepat untuk mulai menggunakan Book Writing Agent.

> 🎯 **NEW!** Sekarang ada **Interactive Mode** - cara termudah untuk membuat buku!

## Setup (5 menit)

### 1. Install Ollama

Jika belum ada, install Ollama:
```bash
# Linux/Mac
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Download dari https://ollama.com/download
```

### 2. Pull Models

```bash
ollama pull gemma3:latest
ollama pull qwen2.5:3b
ollama pull kimi-k2:1t-cloud
```

### 3. Install Project

```bash
cd agentwritebook
uv pip install -e .
# atau: pip install -e .
```

### 4. Test Installation

```bash
writebook info
```

## Penggunaan Pertama

### 🎯 Cara 1: Interactive Mode (RECOMMENDED!)

Cara termudah untuk pemula - wizard akan memandu Anda:

```bash
writebook interactive
```

Wizard akan menanyakan:
1. Tipe buku (Fiction/Non-Fiction)
2. Genre (Fantasy, Sci-Fi, Business, dll) 
3. Judul buku
4. Jumlah chapter (ada rekomendasi)
5. Target audience
6. Opsi streaming (lihat proses real-time!)

**[📖 Panduan Lengkap Interactive Mode](INTERACTIVE_MODE.md)**

---

### 📝 Cara 2: Command Line (Untuk yang sudah familiar)

```bash
# Dengan streaming (lihat proses real-time)
writebook create "Petualangan Pertamaku" \
    --type fiction \
    --chapters 5 \
    --min-words 1000 \
    --stream

# Tanpa streaming (lebih cepat)
writebook create "Petualangan Pertamaku" \
    --type fiction \
    --chapters 5 \
    --min-words 1000
```

Tunggu ~10-15 menit, lalu check folder `output/`!

### Lihat Hasil

```bash
cd output/Petualangan_Pertamaku_*/
ls -la

# Lihat outline
cat 00_outline.md

# Lihat chapter pertama
cat 01_*.md

# Lihat buku lengkap
cat *_full.md
```

## Contoh Quick Commands

### Novel Pendek (30 menit)
```bash
writebook create "Misteri Malam Ini" \
    --type fiction \
    --chapters 8 \
    --min-words 1500
```

### Buku Tutorial (45 menit)
```bash
writebook create "Belajar JavaScript" \
    --type non_fiction \
    --chapters 12 \
    --min-words 1500
```

### Outline Saja (1 menit)
```bash
writebook outline "Ide Bukuku" \
    --chapters 15
```

## Tips untuk Pemula

1. **Mulai dengan chapter sedikit** (5-8) untuk test
2. **Gunakan min-words 1000-1500** untuk lebih cepat
3. **Review outline dulu** sebelum generate full book
4. **Baca hasil** dan adjust prompt jika perlu

## Next Steps

Setelah comfortable dengan basic usage:

1. Baca [README.md](README.md) untuk fitur lengkap
2. Check [examples.md](examples.md) untuk use cases
3. Customize settings di `agentwritebook/config/settings.py`
4. Experiment dengan different parameters

## Common Issues

### Ollama Not Running
```bash
# Start Ollama
ollama serve
```

### Model Not Found
```bash
# Pull missing model
ollama pull gemma3:latest
```

### Slow Generation
- Gunakan GPU jika ada
- Reduce --min-words
- Use --no-review untuk draft

## Support

- Check README.md untuk dokumentasi lengkap
- Check examples.md untuk contoh-contoh
- Open issue jika ada bug

---

Selamat menulis! 📚
