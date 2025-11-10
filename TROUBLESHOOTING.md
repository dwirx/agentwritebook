# Troubleshooting Guide

Solusi untuk masalah umum yang mungkin dihadapi saat menggunakan Book Writing Agent.

## Installation Issues

### Error: Multiple top-level packages discovered

**Gejala:**
```
error: Multiple top-level packages discovered in a flat-layout: ['output', 'agentwritebook'].
```

**Penyebab:**
Setuptools menemukan folder `output/` di root project dan menganggapnya sebagai package.

**Solusi:**
```bash
# 1. Hapus folder output dan egg-info
rm -rf output/ agentwritebook.egg-info/

# 2. Install ulang
uv pip install -e .
```

**Pencegahan:**
Sudah ditangani di `pyproject.toml` dengan:
```toml
[tool.setuptools.packages.find]
include = ["agentwritebook*"]
exclude = ["output*", "*.egg-info", ".venv*"]
```

### Error: uv command not found

**Solusi:**
```bash
# Install uv
pip install uv

# Atau gunakan pip langsung
pip install -e .
```

### Error: Python version mismatch

**Gejala:**
```
requires-python = ">=3.10" but current is 3.9
```

**Solusi:**
```bash
# Check Python version
python --version

# Install Python 3.10+ atau gunakan pyenv
pyenv install 3.10
pyenv local 3.10
```

## Ollama Connection Issues

### Error: Connection refused

**Gejala:**
```
Error: Connection refused to http://172.29.176.1:11434
```

**Solusi:**
```bash
# 1. Start Ollama
ollama serve

# 2. Test koneksi
curl http://172.29.176.1:11434/api/tags

# 3. Jika URL berbeda, edit config
# File: agentwritebook/config/settings.py
# Ubah: base_url = "http://localhost:11434"  # sesuaikan
```

### Error: Model not found

**Gejala:**
```
Error: model 'gemma3:latest' not found
```

**Solusi:**
```bash
# Check model tersedia
ollama list

# Pull model yang diperlukan
ollama pull gemma3:latest
ollama pull qwen2.5:3b
ollama pull kimi-k2:1t-cloud
```

### Error: Timeout

**Gejala:**
Generation terlalu lama dan timeout

**Solusi:**
```python
# Edit: agentwritebook/config/settings.py
class OllamaConfig(BaseModel):
    base_url: str = "http://172.29.176.1:11434"
    timeout: int = 600  # Increase dari 300 ke 600 (10 menit)
```

## Runtime Issues

### Chapter terlalu pendek

**Penyebab:**
Model menghasilkan konten kurang dari `min_words`

**Solusi:**
```bash
# 1. Tingkatkan min-words
writebook create "Title" --min-words 2000

# 2. Berikan detail lebih di --info
writebook create "Title" \
    --info "Detailed description dengan specific requirements..."

# 3. Gunakan model yang lebih powerful
# Edit settings.py, gunakan gemma3:latest untuk writer
```

### Review score rendah

**Penyebab:**
Kualitas konten tidak memenuhi criteria

**Solusi:**
```bash
# 1. Gunakan auto-revise
writebook create "Title" --auto-revise

# 2. Review outline terlebih dahulu
writebook outline "Title" --chapters 10
# Review dan adjust di output/
# Lalu create dengan info yang lebih detail

# 3. Gunakan model lebih baik
# Edit settings.py
```

### Chapter generation gagal

**Gejala:**
Beberapa chapter gagal di-generate, muncul di failed_chapters

**Penyebab:**
- Model error
- Out of memory
- Prompt terlalu kompleks

**Solusi:**
```bash
# 1. Check error message di console
# 2. Reduce min-words untuk chapter yang kompleks
# 3. Simplify outline description
# 4. Regenerate chapter secara manual (future feature)
```

### JSON parsing error di Planner

**Gejala:**
```
Warning: Gagal parse JSON, membuat struktur default
```

**Penyebab:**
Model tidak menghasilkan valid JSON

**Solusi:**
- Sistem akan fallback ke default structure
- Output masih akan dihasilkan
- Untuk hasil lebih baik, coba lagi atau gunakan model berbeda

## Output Issues

### Folder output tidak dibuat

**Penyebab:**
Permission issue atau disk full

**Solusi:**
```bash
# Check permissions
ls -la

# Create manually jika perlu
mkdir -p output
chmod 755 output

# Check disk space
df -h
```

### File tidak terbaca (encoding issue)

**Penyebab:**
Special characters dalam judul/konten

**Solusi:**
- System menggunakan UTF-8 encoding
- Hindari special characters di judul buku
- File akan disanitize otomatis

### File kosong

**Penyebab:**
Chapter generation gagal tanpa error

**Solusi:**
```bash
# Check console output untuk error
# Retry generation
# Reduce complexity
```

## Performance Issues

### Generation terlalu lambat

**Penyebab:**
- Model besar di CPU
- Banyak chapters
- Review enabled

**Solusi:**
```bash
# 1. Use faster model
# Edit settings.py: creative_model = "gemma3:1b"

# 2. Disable review untuk draft
writebook create "Title" --no-review

# 3. Reduce chapters
writebook create "Title" --chapters 5

# 4. Use GPU untuk Ollama
# Configure Ollama dengan GPU support
```

### Out of memory

**Gejala:**
```
Error: Out of memory
```

**Solusi:**
```bash
# 1. Use smaller model
# gemma3:1b instead of qwen2.5:3b

# 2. Close other applications

# 3. Reduce min-words
writebook create "Title" --min-words 1000

# 4. Generate in batches
writebook outline "Title" --chapters 30
# Lalu generate per batch:
# Part 1: chapters 1-10
# Part 2: chapters 11-20
# etc.
```

## CLI Issues

### Command not found: writebook

**Solusi:**
```bash
# 1. Reinstall
uv pip install -e .

# 2. Check installation
pip list | grep agentwritebook

# 3. Use directly
python -m agentwritebook.main --help

# 4. Check PATH
which writebook
```

### Import errors

**Gejala:**
```
ModuleNotFoundError: No module named 'ollama'
```

**Solusi:**
```bash
# Reinstall dependencies
uv pip install -e .

# Or individually
pip install ollama pydantic rich typer
```

## Model-Specific Issues

### gemma3 tidak tersedia

**Solusi:**
```bash
ollama pull gemma3:latest

# Atau gunakan alternatif
# Edit settings.py
main_model = "llama2:latest"  # atau model lain
```

### kimi-k2:1t-cloud tidak tersedia

**Solusi:**
```bash
ollama pull kimi-k2:1t-cloud

# Atau gunakan alternatif untuk reviewer
# Edit settings.py
judge_model = "gemma3:latest"
```

## Configuration Issues

### Settings tidak apply

**Penyebab:**
Perlu restart atau reinstall

**Solusi:**
```bash
# Setelah edit settings.py
uv pip install -e .

# Atau restart python session
```

### Base URL salah

**Solusi:**
```bash
# Check Ollama URL
ollama serve
# Note the URL (usually localhost:11434)

# Edit settings.py
base_url = "http://localhost:11434"
```

## Quality Issues

### Konten tidak konsisten

**Solusi:**
1. Buat outline detail terlebih dahulu
2. Review outline sebelum generate
3. Gunakan temperature lebih rendah (edit agent)
4. Enable review dan auto-revise

### Karakter tidak konsisten (Fiction)

**Solusi:**
1. Define karakter detail di outline
2. Use character consistency checker (future feature)
3. Manual review dan edit

### Facts tidak akurat (Non-Fiction)

**Solusi:**
1. Berikan detail akurat di --info
2. Manual fact-checking diperlukan
3. Use fact checker (future feature)

## Debug Mode

Untuk troubleshooting lebih detail:

```python
# Edit agentwritebook/utils/ollama_client.py
# Tambahkan logging:
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Getting Help

Jika masalah masih berlanjut:

1. **Check dokumentasi**:
   - README.md
   - ARCHITECTURE.md
   - examples.md

2. **Check logs**:
   - Console output
   - Error messages

3. **Collect info**:
   ```bash
   # System info
   python --version
   ollama --version

   # Package versions
   pip list | grep -E "(ollama|pydantic|rich|typer)"

   # Models
   ollama list
   ```

4. **Open issue** di GitHub dengan:
   - Error message lengkap
   - System info
   - Steps to reproduce

## Common Fixes Summary

```bash
# Reset everything
rm -rf output/ agentwritebook.egg-info/ .venv/
uv pip install -e .

# Verify installation
writebook info
writebook models

# Test dengan minimal example
writebook create "Test" \
    --type fiction \
    --chapters 3 \
    --min-words 500 \
    --no-review
```

## Prevention Tips

1. **Always check models tersedia** sebelum run
2. **Start dengan outline** untuk review structure
3. **Use --no-review** untuk quick tests
4. **Keep Ollama running** sebelum generate
5. **Monitor disk space** untuk output
6. **Backup important outputs** sebelum regenerate

---

**Last Updated**: 2025-01-11
**Version**: 1.0.0
