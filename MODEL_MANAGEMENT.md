# Model Management Guide

Panduan lengkap untuk mengelola model Ollama di Book Writing Agent.

## 📋 Daftar Model yang Direkomendasikan

### Model Baru yang Ditambahkan (v2.1)

Book Writing Agent sekarang mendukung model-model cloud yang powerful:

#### 🚀 GPT-OSS Models
```bash
# Small - Fast & efficient
ollama pull gpt-oss:20b-cloud

# Large - Exceptional quality
ollama pull gpt-oss:120b-cloud
```

**Spesifikasi:**
- **gpt-oss:20b-cloud**
  - Size: ~12GB
  - Speed: Medium
  - Quality: Very High
  - Best for: Planner, Writer, Reviewer (balanced)

- **gpt-oss:120b-cloud**
  - Size: ~75GB
  - Speed: Slow
  - Quality: Exceptional
  - Best for: Writer (high-quality content)

#### 🧠 DeepSeek V3.1
```bash
ollama pull deepseek-v3.1:671b-cloud
```

**Spesifikasi:**
- Size: ~400GB (sangat besar!)
- Speed: Very Slow
- Quality: Exceptional
- Best for: Writer (maximum quality, tidak untuk production)

#### ⚡ GLM-4.6
```bash
ollama pull glm-4.6:cloud
```

**Spesifikasi:**
- Size: ~3GB
- Speed: Fast
- Quality: High
- Best for: Planner, Reviewer (fast & good quality)

---

## 🎯 Rekomendasi Model per Role

### Planner Agent
**Tugas:** Membuat outline dan struktur buku

**Rekomendasi (pilih salah satu):**

1. **gemma3:latest** (Default) ⭐
   - ✅ Balanced: quality & speed
   - ✅ Well-tested
   - Size: ~9GB

2. **gpt-oss:20b-cloud** (Upgrade)
   - ✅ Higher quality planning
   - ✅ Better structure
   - Size: ~12GB

3. **glm-4.6:cloud** (Fast)
   - ✅ Faster generation
   - ✅ Good quality
   - Size: ~3GB

4. **llama3.2:latest** (Lightweight)
   - ✅ Smallest size
   - ⚠️ Medium quality
   - Size: ~4GB

### Writer Agent
**Tugas:** Menulis konten chapter

**Rekomendasi (pilih salah satu):**

1. **qwen2.5:3b** (Default) ⭐
   - ✅ Very fast
   - ✅ Good quality
   - ✅ Best value
   - Size: ~2GB

2. **gpt-oss:20b-cloud** (Balanced Premium)
   - ✅ Very high quality
   - ✅ Reasonable speed
   - ✅ RECOMMENDED untuk production
   - Size: ~12GB

3. **gpt-oss:120b-cloud** (Quality Focus)
   - ✅ Exceptional quality
   - ⚠️ Slower generation
   - 💡 Best untuk final draft
   - Size: ~75GB

4. **deepseek-v3.1:671b-cloud** (Maximum Quality)
   - ✅ Absolute best quality
   - ⚠️ Very slow
   - ⚠️ Huge disk space
   - 💡 Only for special projects
   - Size: ~400GB

5. **gemma3:latest** (Balanced)
   - ✅ High quality
   - ✅ Medium speed
   - Size: ~9GB

### Reviewer Agent
**Tugas:** Quality control dan review

**Rekomendasi (pilih salah satu):**

1. **kimi-k2:1t-cloud** (Default) ⭐
   - ✅ Very fast
   - ✅ Efficient
   - ✅ Good for QA
   - Size: ~700MB

2. **glm-4.6:cloud** (Fast & Better)
   - ✅ Fast
   - ✅ Higher quality review
   - Size: ~3GB

3. **gpt-oss:20b-cloud** (Premium)
   - ✅ Very high quality feedback
   - ✅ Detailed analysis
   - Size: ~12GB

4. **qwen2.5:3b** (Balanced)
   - ✅ Very fast
   - ✅ Good quality
   - Size: ~2GB

---

## 💡 Kombinasi Model yang Direkomendasikan

### Budget Setup (Fastest)
```
Planner:  llama3.2:latest    (~4GB)
Writer:   qwen2.5:3b          (~2GB)
Reviewer: kimi-k2:1t-cloud    (~700MB)
Total:    ~7GB
Speed:    ⭐⭐⭐⭐⭐
Quality:  ⭐⭐⭐
```

### Balanced Setup (Default) ⭐
```
Planner:  gemma3:latest       (~9GB)
Writer:   qwen2.5:3b          (~2GB)
Reviewer: kimi-k2:1t-cloud    (~700MB)
Total:    ~12GB
Speed:    ⭐⭐⭐⭐
Quality:  ⭐⭐⭐⭐
```

### Premium Setup (Production Quality)
```
Planner:  gpt-oss:20b-cloud   (~12GB)
Writer:   gpt-oss:20b-cloud   (~12GB)
Reviewer: glm-4.6:cloud       (~3GB)
Total:    ~27GB
Speed:    ⭐⭐⭐
Quality:  ⭐⭐⭐⭐⭐
```

### Ultimate Setup (Maximum Quality)
```
Planner:  gpt-oss:20b-cloud       (~12GB)
Writer:   gpt-oss:120b-cloud      (~75GB)
Reviewer: gpt-oss:20b-cloud       (~12GB)
Total:    ~99GB
Speed:    ⭐⭐
Quality:  ⭐⭐⭐⭐⭐⭐
```

### Research/Academic Setup
```
Planner:  gpt-oss:20b-cloud       (~12GB)
Writer:   deepseek-v3.1:671b-cloud (~400GB)
Reviewer: gpt-oss:20b-cloud       (~12GB)
Total:    ~424GB (!)
Speed:    ⭐
Quality:  ⭐⭐⭐⭐⭐⭐⭐
```

---

## 🔧 Cara Menggunakan

### 1. Lihat Model yang Tersedia

```bash
# Lihat semua model yang terinstall
writebook models --available

# Lihat rekomendasi untuk setiap role
writebook models --recommended

# Lihat konfigurasi saat ini
writebook models
```

### 2. Install Model Baru

```bash
# Install model yang diinginkan
ollama pull gpt-oss:20b-cloud
ollama pull gpt-oss:120b-cloud
ollama pull deepseek-v3.1:671b-cloud
ollama pull glm-4.6:cloud

# Check apakah sudah terinstall
ollama list
```

### 3. Tambahkan Model Custom

Jika Anda punya model Ollama lain yang ingin ditambahkan ke rekomendasi:

```bash
writebook add-model <model-name> \
  --role <planner|writer|reviewer> \
  --size "~XGB" \
  --speed "<Very Fast|Fast|Medium|Slow|Very Slow>" \
  --quality "<Good|High|Very High|Exceptional>"
```

**Contoh:**
```bash
# Tambah model baru ke writer
writebook add-model my-custom-model:latest \
  --role writer \
  --size "~10GB" \
  --speed Fast \
  --quality "Very High"

# Model akan muncul di interactive mode dan select-model
```

### 4. Pilih Model Interaktif

```bash
# Pilih model untuk role tertentu
writebook select-model planner
writebook select-model writer
writebook select-model reviewer
```

Output akan menampilkan tabel dengan info lengkap:
- Model name
- Size
- Speed
- Quality
- Status (✓ Ready / ✗ Not installed)

### 5. Gunakan di Interactive Mode

```bash
writebook interactive
```

Pada step 6 (Pilih Models):
1. **Opsi 1**: Gunakan default (cepat)
2. **Opsi 2**: Pilih dari rekomendasi (dengan tabel info) ⭐
3. **Opsi 3**: Input manual

Pilih opsi 2 untuk melihat semua model dengan detail lengkap!

### 6. Gunakan di Command Line

```bash
# Tidak ada flag --model di CLI
# Harus gunakan interactive mode atau edit settings.py
```

---

## 📊 Perbandingan Model

### Speed vs Quality

```
Quality ↑
    │
  ★ │                           ● deepseek-v3.1:671b-cloud
  ★ │                   ● gpt-oss:120b-cloud
  ★ │           ● gpt-oss:20b-cloud
  ★ │       ● gemma3:latest  ● glm-4.6:cloud
  ★ │   ● qwen2.5:3b
  ★ │ ● llama3.2:latest ● kimi-k2:1t-cloud
    └───────────────────────────────────────→ Speed
      Fast                              Slow
```

### Size vs Quality

```
Quality ↑
    │
  ★ │                                       ● deepseek-v3.1:671b-cloud
  ★ │                           ● gpt-oss:120b-cloud
  ★ │           ● gpt-oss:20b-cloud ● gemma3:latest
  ★ │       ● glm-4.6:cloud ● llama3.2:latest
  ★ │   ● qwen2.5:3b
  ★ │ ● kimi-k2:1t-cloud
    └─────────────────────────────────────────→ Size
      Small                               Large
```

---

## 🎓 Tips Pemilihan Model

### Untuk Pemula
✅ Gunakan **Balanced Setup** (default)
- Mudah setup
- Disk space reasonable
- Quality bagus
- Speed acceptable

### Untuk Production
✅ Gunakan **Premium Setup**
- gpt-oss:20b-cloud untuk planner & writer
- glm-4.6:cloud untuk reviewer
- Best balance quality & speed

### Untuk Eksperimen Cepat
✅ Gunakan **Budget Setup**
- Model kecil, cepat
- Cocok untuk testing outline
- Iterate cepat

### Untuk Quality Maksimal
✅ Gunakan **Ultimate Setup** atau **Research Setup**
- Siapkan disk space besar
- Sabar menunggu
- Untuk final draft atau project penting

### Untuk Buku Teknis/Non-Fiksi
```
Planner:  gpt-oss:20b-cloud   (struktur detail)
Writer:   gpt-oss:20b-cloud   (explanation jelas)
Reviewer: gpt-oss:20b-cloud   (technical accuracy)
```

### Untuk Novel/Fiksi Kreatif
```
Planner:  gemma3:latest           (creative plotting)
Writer:   gpt-oss:120b-cloud      (rich narrative)
Reviewer: glm-4.6:cloud           (fast feedback)
```

---

## ⚠️ Pertimbangan Penting

### Disk Space
- **Minimum**: ~7GB (budget setup)
- **Recommended**: ~12-30GB (balanced/premium)
- **Ultimate**: ~100GB+
- **Research**: ~400GB+ (!)

Pastikan Anda punya cukup disk space sebelum pull model besar.

### RAM Requirements
Model besar butuh RAM lebih:
- Small models (3B): ~4-8GB RAM
- Medium models (20B): ~16-32GB RAM
- Large models (120B): ~64GB+ RAM
- Huge models (671B): ~256GB+ RAM (!)

### GPU vs CPU
- **GPU**: 10-100x lebih cepat
- **CPU**: Tetap bisa, tapi lambat

Untuk model 120B+, GPU sangat direkomendasikan.

### Generation Time Estimates

Per chapter (~1500 kata):

| Model | CPU | GPU |
|-------|-----|-----|
| qwen2.5:3b | 3-5 min | 30-60 sec |
| gpt-oss:20b-cloud | 10-15 min | 2-4 min |
| gpt-oss:120b-cloud | 30-60 min | 10-15 min |
| deepseek-v3.1:671b-cloud | 2-4 hours | 30-60 min |

*Estimasi, tergantung hardware*

---

## 🚀 Quick Setup Examples

### Setup 1: Cepat Start (5 menit)
```bash
# Pull models default
ollama pull gemma3:latest
ollama pull qwen2.5:3b
ollama pull kimi-k2:1t-cloud

# Langsung pakai
writebook interactive
# (Pilih opsi 1: use default)
```

### Setup 2: Premium Quality (15 menit)
```bash
# Pull premium models
ollama pull gpt-oss:20b-cloud
ollama pull glm-4.6:cloud

# Interactive mode
writebook interactive
# Step 6: Pilih opsi 2
# Planner: gpt-oss:20b-cloud
# Writer: gpt-oss:20b-cloud
# Reviewer: glm-4.6:cloud
```

### Setup 3: Ultimate (1+ jam download)
```bash
# Pull ultimate models
ollama pull gpt-oss:20b-cloud
ollama pull gpt-oss:120b-cloud

# Interactive mode
writebook interactive
# Step 6: Pilih opsi 2
# Planner: gpt-oss:20b-cloud
# Writer: gpt-oss:120b-cloud
# Reviewer: gpt-oss:20b-cloud
```

---

## 📝 Command Reference

```bash
# Lihat semua commands
writebook --help

# Model management
writebook models                    # Current config
writebook models --available        # Installed models
writebook models --recommended      # Recommendations

# Add custom model
writebook add-model <name> --role <role> [options]

# Select model interactively
writebook select-model <role>

# Interactive mode (dengan model selection)
writebook interactive
```

---

## 🔮 Future Plans

### v2.2 (Planned)
- [ ] Persistent model configuration
- [ ] Model performance benchmarks
- [ ] Auto-download recommended models
- [ ] Model switching mid-generation

### v2.3 (Planned)
- [ ] Multi-model writing (ensemble)
- [ ] Model comparison mode
- [ ] Custom model training integration

---

## ❓ FAQ

**Q: Model mana yang harus saya gunakan?**
A: Untuk start, gunakan default (Balanced Setup). Jika butuh quality lebih, upgrade ke Premium Setup dengan gpt-oss:20b-cloud.

**Q: Apakah bisa mix model dari setup berbeda?**
A: Ya! Anda bebas kombinasi. Misal: gemma3 (planner) + gpt-oss:120b-cloud (writer) + kimi-k2 (reviewer).

**Q: Model cloud butuh internet?**
A: Tidak. Model "cloud" di Ollama tetap run lokal. Nama "cloud" hanya naming convention.

**Q: Disk saya terbatas, model mana yang paling worth it?**
A: gpt-oss:20b-cloud (~12GB). Best bang for buck: quality tinggi dengan size reasonable.

**Q: Apakah model besar selalu lebih baik?**
A: Tidak selalu. Untuk draft cepat atau outline, model kecil sudah cukup. Model besar untuk final polish.

**Q: Bisakah menambah model dari Hugging Face?**
A: Tidak langsung. Harus convert ke format Ollama dulu. Lihat Ollama docs untuk tutorial.

**Q: Model mana yang paling hemat listrik?**
A: qwen2.5:3b dan kimi-k2:1t-cloud. Kecil, cepat, efisien.

---

## 📚 Resources

- **Ollama Models**: https://ollama.com/library
- **Model Specs**: https://ollama.com/library/<model-name>
- **GPU Requirements**: Check Ollama documentation
- **Performance Benchmarks**: Community benchmarks (coming soon)

---

**Ready to upgrade your model setup?**

```bash
# See what you have
writebook models --available

# See what's recommended
writebook models --recommended

# Try interactive selection
writebook interactive
```

Happy writing with powerful models! 🚀📚

