# Contoh Penggunaan Book Writing Agent

## Contoh 1: Novel Fiksi - Fantasy Adventure

```bash
writebook create "Legenda Pedang Naga" \
    --type fiction \
    --chapters 18 \
    --audience young_adult \
    --min-words 2500 \
    --review \
    --info "Sebuah petualangan epik tentang seorang pemuda yang menemukan pedang legendaris dan harus menghadapi pasukan kegelapan untuk menyelamatkan kerajaannya"
```

**Output yang Dihasilkan:**
- 18 chapter dengan plot yang koheren
- Karakter utama dan pendukung yang well-developed
- World-building yang detail
- Dialog yang natural
- Total ~45,000 kata

## Contoh 2: Novel Fiksi - Mystery Thriller

```bash
writebook create "Misteri Pembunuhan di Mansion Tua" \
    --type fiction \
    --chapters 15 \
    --audience general \
    --min-words 2000 \
    --review \
    --auto-revise \
    --info "Thriller misteri tentang detektif yang harus memecahkan kasus pembunuhan di mansion tua dengan 12 tersangka. Plot twists dan red herrings di setiap chapter"
```

**Fitur:**
- Auto-revise untuk kualitas maksimal
- Plot twist yang engaging
- Character development yang kuat
- Clue dan red herrings yang tersebar

## Contoh 3: Buku Non-Fiksi - Tutorial Programming

```bash
writebook create "Python untuk Data Science: Dari Nol hingga Hero" \
    --type non_fiction \
    --chapters 25 \
    --audience beginner \
    --min-words 1800 \
    --review \
    --info "Tutorial komprehensif Python untuk data science dengan fokus pada pandas, numpy, matplotlib, dan scikit-learn. Setiap chapter dengan hands-on examples dan exercises"
```

**Struktur:**
- Chapter 1-5: Python basics
- Chapter 6-10: Data manipulation dengan pandas
- Chapter 11-15: Visualization dengan matplotlib
- Chapter 16-20: Machine learning basics
- Chapter 21-25: Advanced topics dan projects

## Contoh 4: Buku Non-Fiksi - Business

```bash
writebook create "Strategi Digital Marketing 2025" \
    --type non_fiction \
    --chapters 12 \
    --audience professional \
    --min-words 2200 \
    --review \
    --info "Panduan lengkap digital marketing modern meliputi SEO, SEM, social media marketing, content marketing, email marketing, dan analytics. Dengan case studies dan actionable strategies"
```

**Konten:**
- Teori dan praktik
- Real-world case studies
- Actionable tips dan strategies
- Metrics dan KPIs
- Tools dan resources

## Contoh 5: Buku Non-Fiksi - Self-Help

```bash
writebook create "Menemukan Tujuan Hidup: Panduan Praktis" \
    --type non_fiction \
    --chapters 10 \
    --audience general \
    --min-words 2000 \
    --review \
    --info "Buku self-help dengan pendekatan praktis untuk menemukan purpose, mengatasi obstacles, dan mencapai fulfillment. Kombinasi psychology, philosophy, dan practical exercises"
```

## Contoh 6: Membuat Outline Dulu

```bash
# Step 1: Buat outline
writebook outline "Rahasia Produktivitas Maksimal" \
    --type non_fiction \
    --chapters 15

# Step 2: Review outline di output/

# Step 3: Jika outline sudah OK, buat bukunya
writebook create "Rahasia Produktivitas Maksimal" \
    --type non_fiction \
    --chapters 15 \
    --min-words 1500 \
    --review \
    --info "Buku praktis tentang productivity hacks, time management, focus techniques, habit building, dan work-life balance"
```

## Contoh 7: Quick Draft (Tanpa Review)

```bash
# Untuk draft cepat tanpa review
writebook create "Draft: Cerita Pendek Collection" \
    --type fiction \
    --chapters 5 \
    --audience general \
    --min-words 1000 \
    --no-review
```

**Kegunaan:**
- Brainstorming ideas
- Quick prototype
- Testing concepts
- Fast iteration

## Contoh 8: High-Quality Output

```bash
# Untuk hasil berkualitas tinggi dengan auto-revise
writebook create "Masterpiece: Novel Sejarah Indonesia" \
    --type fiction \
    --chapters 20 \
    --audience general \
    --min-words 3000 \
    --review \
    --auto-revise \
    --info "Novel sejarah epik berlatar perang kemerdekaan Indonesia dengan riset mendalam tentang tokoh, peristiwa, dan kondisi sosial masa itu"
```

**Catatan:**
- Waktu lebih lama karena auto-revise
- Kualitas output lebih konsisten
- Review score rata-rata lebih tinggi

## Contoh 9: Buku Anak-Anak

```bash
writebook create "Petualangan Si Kelinci Cerdik" \
    --type fiction \
    --chapters 8 \
    --audience children \
    --min-words 800 \
    --review \
    --info "Cerita anak tentang kelinci yang menggunakan kecerdasannya untuk membantu teman-teman hewan di hutan. Setiap chapter dengan moral lesson yang positif"
```

**Karakteristik:**
- Bahasa sederhana
- Chapter lebih pendek (800 kata)
- Moral lessons
- Karakter yang relatable untuk anak

## Contoh 10: Academic/Research Book

```bash
writebook create "Artificial Intelligence: Teori dan Implementasi" \
    --type non_fiction \
    --chapters 20 \
    --audience professional \
    --min-words 2500 \
    --review \
    --info "Textbook akademis tentang AI covering machine learning algorithms, deep learning, NLP, computer vision, dan ethics. Dengan mathematical foundations, pseudocode, dan citations ke papers"
```

## Tips Memilih Parameter

### Jumlah Chapter

| Tipe Buku | Recommended Chapters |
|-----------|---------------------|
| Short Story Collection | 5-8 |
| Novella | 10-15 |
| Novel | 15-30 |
| Tutorial/Guide | 10-25 |
| Academic Textbook | 15-30 |
| Self-Help | 8-15 |
| Business Book | 10-15 |

### Minimum Words per Chapter

| Genre | Recommended Words |
|-------|------------------|
| Children's Book | 500-1000 |
| Young Adult Fiction | 2000-3000 |
| Adult Fiction | 2500-4000 |
| Non-Fiction Tutorial | 1500-2500 |
| Academic | 2500-4000 |
| Self-Help | 1500-2500 |

### Target Audience

- **children**: 6-12 tahun, bahasa simple, cerita pendek
- **young_adult**: 13-18 tahun, tema relatable, bahasa casual
- **general**: Dewasa umum, balanced tone
- **professional**: Profesional/expert, formal, technical
- **beginner**: Pemula di suatu topik, step-by-step, clear

## Workflow Recommendations

### Workflow 1: Fast Iteration

```bash
# 1. Buat outline cepat
writebook outline "Topic" --chapters 10

# 2. Review outline

# 3. Buat draft tanpa review
writebook create "Topic" --chapters 10 --no-review --min-words 1000

# 4. Manual review dan refinement
```

### Workflow 2: Quality-First

```bash
# 1. Buat outline dengan detail
writebook outline "Topic" --chapters 15 --info "Detailed info here"

# 2. Review dan adjust

# 3. Buat buku dengan review dan auto-revise
writebook create "Topic" \
    --chapters 15 \
    --min-words 2000 \
    --review \
    --auto-revise \
    --info "Same detailed info"
```

### Workflow 3: Iterative Development

```bash
# 1. Start dengan outline
writebook outline "Big Project" --chapters 30

# 2. Buat batch pertama (10 chapters)
writebook create "Big Project - Part 1" --chapters 10 --review

# 3. Review hasil

# 4. Adjust dan lanjut batch 2
writebook create "Big Project - Part 2" --chapters 10 --review

# 5. Dst...

# 6. Manual merge semua parts
```

## Advanced Usage

### Custom Info untuk Hasil Lebih Baik

Berikan detail sebanyak mungkin di `--info`:

```bash
writebook create "Novel Komplex" \
    --type fiction \
    --chapters 20 \
    --info "Genre: Sci-fi dystopian. Setting: Jakarta 2150 setelah climate disaster. Protagonis: Ana (28), engineer yang menemukan conspiracy. Tema: technology vs humanity, hope vs despair. Tone: Dark tapi dengan hope. Include: plot twists, moral dilemmas, technical accuracy"
```

### Testing Different Models

Edit `settings.py` untuk experiment dengan model combinations:

```python
# Untuk lebih creative
creative_model: str = "qwen2.5:3b"

# Untuk lebih consistent
creative_model: str = "gemma3:latest"

# Untuk faster drafts
creative_model: str = "gemma3:1b"
```

## Expected Output Quality

### Dengan Review (--review)
- Overall score: 7-9/10
- Consistent quality
- Good structure
- Minor issues yang bisa di-polish manual

### Dengan Auto-Revise (--auto-revise)
- Overall score: 8-10/10
- High quality consistent
- Better coherence
- 2x waktu eksekusi

### Tanpa Review (--no-review)
- Quality varies
- Faster generation
- Good untuk drafts
- Perlu manual review lebih banyak

## Common Use Cases

1. **NaNoWriMo**: Generate 50k words novel dalam 1-2 jam
2. **Content Creation**: Buat ebook untuk lead magnet
3. **Tutorial Writing**: Generate technical documentation
4. **Story Brainstorming**: Generate plot ideas dan outlines
5. **Academic Writing**: Generate textbook drafts
6. **Self-Publishing**: Generate books untuk Amazon KDP

---

Untuk pertanyaan atau contoh lainnya, silakan check README.md atau buka issue di GitHub!
