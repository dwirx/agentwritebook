# Interactive Mode Guide

Mode interaktif adalah cara termudah untuk membuat buku dengan Book Writing Agent. Mode ini memandu Anda langkah demi langkah melalui wizard yang user-friendly.

## Menggunakan Interactive Mode

```bash
writebook interactive
```

## Fitur Utama

### 1. **Wizard Step-by-Step**
Mode interaktif memandu Anda melalui 7 langkah:

#### Step 1: Pilih Tipe Buku
- Fiction (Fiksi)
- Non-Fiction (Non-Fiksi)

#### Step 2: Pilih Genre/Kategori
Pilih dari template yang sudah disediakan:

**Fiction:**
- Fantasy - Dunia magic, makhluk mistis
- Science Fiction - Futuristik, teknologi canggih
- Mystery/Detective - Investigasi, plot twist
- Romance - Cerita cinta
- Thriller/Suspense - Ketegangan tinggi
- Adventure - Petualangan seru

**Non-Fiction:**
- Self-Help/Personal Development
- Business/Entrepreneurship
- Technical/Programming
- Educational/Tutorial
- Health & Wellness

Setiap genre memiliki rekomendasi jumlah chapter yang optimal.

#### Step 3: Detail Buku
- Masukkan judul atau topik buku
- Informasi tambahan (opsional):
  - Setting cerita
  - Karakter utama
  - Tone yang diinginkan
  - Fokus spesifik

#### Step 4: Konfigurasi Chapters
- Jumlah chapter (default sesuai genre)
- Minimum kata per chapter (default: 1500)

#### Step 5: Target Audience
Pilih target pembaca:
- General (Umum)
- Young Adult (Remaja)
- Children (Anak-anak)
- Professional (Profesional)
- Academic (Akademik)
- Custom (Kustom)

#### Step 6: Pilih Models
Opsi untuk menggunakan:
- Model default (recommended)
- Custom models untuk setiap agent:
  - Planner model
  - Writer model
  - Reviewer model

#### Step 7: Opsi Penulisan
- **Enable Review**: Review otomatis setiap chapter
- **Auto Revise**: Revisi otomatis jika score rendah
- **Enable Streaming**: Tampilkan proses real-time ⭐

### 2. **Streaming Output** ⭐ NEW

Dengan fitur streaming, Anda bisa:
- Melihat teks ditulis secara real-time
- Monitor progress secara langsung
- Mengetahui apa yang sedang dikerjakan AI
- Pengalaman yang lebih interaktif dan engaging

```
Chapter 1: Awal Petualangan
────────────────────────────────────────────────────────────

Generating with qwen2.5:3b...
Di sebuah desa terpencil di kaki gunung Himalaya, hiduplah 
seorang pemuda bernama Arjun. Setiap pagi, ia bangun dengan 
suara burung-burung yang berkicau...
[Teks muncul secara real-time saat AI menulis]
────────────────────────────────────────────────────────────
```

### 3. **Template Genre**

Setiap genre memiliki karakteristik khusus:

**Fantasy Template:**
- 15 chapters (recommended)
- Fokus: World-building, magic system, character arcs
- Style: Immersive, descriptive

**Business Template:**
- 12 chapters (recommended)
- Fokus: Actionable insights, case studies
- Style: Professional, practical

## Contoh Penggunaan

### Contoh 1: Membuat Novel Fantasy

```bash
writebook interactive
```

1. Pilih: Fiction
2. Genre: Fantasy
3. Judul: "Jejak Bintang di Lembah Tersembunyi"
4. Info tambahan: "Setting dunia magic dengan 4 elemen, protagonis muda yang mencari jati diri"
5. Chapters: 15 (default)
6. Min words: 2000
7. Audience: Young Adult
8. Models: Default
9. Options:
   - Review: Yes
   - Auto Revise: No
   - Streaming: Yes ✓

### Contoh 2: Membuat Buku Tutorial Python

```bash
writebook interactive
```

1. Pilih: Non-Fiction
2. Genre: Technical/Programming
3. Judul: "Python untuk Data Science: Panduan Praktis"
4. Info: "Fokus pada pandas, numpy, dan visualisasi data"
5. Chapters: 15
6. Min words: 2500
7. Audience: Professional
8. Models: Default
9. Options:
   - Review: Yes
   - Auto Revise: Yes
   - Streaming: Yes ✓

## Streaming vs Non-Streaming

### Non-Streaming (Default pada command `create`)
```bash
writebook create "Judul Buku" --type fiction --chapters 10
```
- Lebih cepat (tidak ada overhead display)
- Cocok untuk batch processing
- Tidak bisa melihat proses

### Streaming (Recommended untuk Interactive)
```bash
writebook create "Judul Buku" --type fiction --chapters 10 --stream
# atau
writebook interactive  # (akan ditanya saat wizard)
```
- Live preview saat menulis
- Bisa monitor progress
- Lebih engaging dan interaktif
- Tahu kapan ada error/stuck

## Tips Menggunakan Interactive Mode

### 1. Persiapan
✓ Pastikan Ollama sudah running: `ollama serve`
✓ Model sudah di-pull: `ollama pull gemma3:latest qwen2.5:3b kimi-k2:1t-cloud`
✓ Pikirkan konsep buku terlebih dahulu

### 2. Memilih Genre
- Pilih genre yang paling sesuai dengan ide Anda
- Lihat contoh untuk inspirasi
- Perhatikan rekomendasi jumlah chapter

### 3. Informasi Tambahan
Berikan detail yang membantu AI:
- **Fiction**: Setting, karakter utama, konflik, tone
- **Non-Fiction**: Target pembaca, fokus topik, level (pemula/advanced)

Contoh bagus:
```
"Setting: Dunia steampunk di era Victorian, 
Protagonis: Inventor muda bernama Clara, 
Konflik: Melawan guild yang mengontrol teknologi, 
Tone: Light-hearted adventure dengan elemen mystery"
```

### 4. Jumlah Chapter
- Gunakan rekomendasi sebagai panduan
- Fiction kompleks: 12-20 chapters
- Non-fiction tutorial: 10-15 chapters
- Short story: 5-8 chapters

### 5. Minimum Kata
- Default 1500 kata sudah cukup untuk kebanyakan chapter
- Untuk konten detail: 2000-2500 kata
- Untuk ebook pendek: 1000-1500 kata

### 6. Review dan Auto-Revise
- **Enable Review**: Selalu aktifkan untuk quality control
- **Auto Revise**: 
  - ✓ Aktifkan jika menginginkan kualitas maksimal
  - ✗ Non-aktifkan jika ingin cepat (bisa revisi manual nanti)

### 7. Streaming
- ✓ Aktifkan untuk pengalaman interaktif
- ✓ Berguna untuk debugging (melihat output langsung)
- ✗ Non-aktifkan jika ingin lebih cepat

## Troubleshooting

### "Model tidak tersedia"
Cek model yang tersedia:
```bash
writebook models --available
```

Lihat rekomendasi:
```bash
writebook models --recommended
```

Pull model yang dibutuhkan:
```bash
ollama pull gemma3:latest
ollama pull qwen2.5:3b
ollama pull kimi-k2:1t-cloud
```

### Streaming tidak muncul
- Pastikan terminal support output real-time
- Coba non-aktifkan streaming jika ada masalah

### Process terlalu lama
- Gunakan model yang lebih kecil (qwen2.5:3b, llama3.2:3b)
- Kurangi jumlah chapter
- Non-aktifkan auto-revise

## Perbandingan Mode

| Fitur | Interactive Mode | Command Line |
|-------|-----------------|--------------|
| Ease of Use | ⭐⭐⭐⭐⭐ Sangat mudah | ⭐⭐⭐ Perlu tahu parameter |
| Customization | ⭐⭐⭐⭐ Full control | ⭐⭐⭐⭐⭐ Maximum |
| Genre Templates | ✓ Built-in | ✗ Manual |
| Model Selection | ✓ Guided | Manual |
| Streaming | ✓ Optional | --stream flag |
| Rekomendasi | ✓ Yes | ✗ No |
| Validation | ✓ Real-time | Post-execution |

## Command Line Alternative

Jika sudah familiar, bisa langsung menggunakan command line dengan semua fitur:

```bash
# Dengan streaming
writebook create "Judul Buku" \
  --type fiction \
  --chapters 15 \
  --min-words 2000 \
  --audience young_adult \
  --review \
  --stream \
  --info "Setting dunia fantasy dengan magic system"

# Tanpa streaming (lebih cepat)
writebook create "Judul Buku" \
  --type non_fiction \
  --chapters 12 \
  --min-words 1500 \
  --audience professional \
  --review \
  --auto-revise
```

## FAQ

**Q: Apakah bisa mengganti model di tengah proses?**
A: Tidak. Model harus dipilih di awal. Untuk menggunakan model berbeda, mulai proses baru.

**Q: Apakah streaming mempengaruhi kualitas output?**
A: Tidak. Streaming hanya mengubah cara output ditampilkan, tidak mempengaruhi konten.

**Q: Berapa lama proses pembuatan buku?**
A: Tergantung:
- Model size (kecil = lebih cepat)
- Jumlah chapter
- Panjang kata per chapter
- Hardware (GPU lebih cepat)

Estimasi: 5-15 menit per chapter dengan model medium pada hardware standar.

**Q: Bisa cancel di tengah proses?**
A: Ya, tekan `Ctrl+C`. Chapter yang sudah selesai akan tetap tersimpan.

**Q: Apakah bisa edit hasil setelah selesai?**
A: Ya! File disimpan dalam format Markdown (.md) yang mudah diedit dengan text editor apapun.

## Next Steps

Setelah membuat buku dengan interactive mode:

1. **Review Output**: Buka folder output dan baca hasilnya
2. **Edit Manual**: Edit file .md sesuai kebutuhan
3. **Revisi Chapter**: Tulis ulang chapter tertentu jika perlu
4. **Export**: Convert ke format lain (PDF, EPUB, dll) jika diperlukan

## Kesimpulan

Interactive mode adalah cara terbaik untuk:
- ✓ Pemula yang baru mencoba tool
- ✓ Ingin guided experience
- ✓ Perlu rekomendasi genre dan model
- ✓ Ingin melihat proses secara real-time

**Mulai sekarang:**
```bash
writebook interactive
```

Happy writing! 📚✨

