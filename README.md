# Chatbot Tematik

Chatbot rule-based bertema perintah Git. Menjawab pertanyaan seperti `git commit`, `git branch`, `git merge`, cara membatalkan commit, dan solusi undo/penyelamatan kode, dengan fallback ke dokumentasi resmi GitHub.

## Cara Menjalankan

```bash
# 1. Buat virtual environment (sekali saja)
python -m venv .venv
source .venv/bin/activate

# 2. Install dependensi
pip install -r requirements.txt

# 3. Jalankan aplikasi web
python app.py
# buka http://127.0.0.1:5000

# Alternatif: chat lewat terminal
python cli.py

# Evaluasi akurasi dengan data uji
python evaluate.py --tema git
```

## Struktur File

```
.
├── app.py                  # Aplikasi web Flask (route halaman + REST API)
├── cli.py                  # Chat interaktif di terminal
├── evaluate.py             # Evaluasi akurasi intent dengan data uji
├── requirements.txt        # Dependensi Python
├── pytest.ini              # Konfigurasi pytest
├── .gitignore
├── chatbot/
│   ├── __init__.py
│   ├── engine.py           # Mesin pencocokan intent (rule-based)
│   └── database.py         # Penyimpanan riwayat percakapan (SQLite)
├── evaluasi/
│   └── git.csv             # Data uji: kalimat,intent
├── themes/
│   └── git.json            # Basis pengetahuan tema Git (intents & responses)
├── templates/              # Halaman HTML (Jinja2)
│   ├── 404.html
│   ├── admin.html
│   ├── base.html
│   ├── chat.html
│   └── index.html
├── static/
│   ├── css/style.css
│   └── js/chat.js
└── tests/
    ├── __init__.py
    ├── test_app.py         # Uji integrasi route Flask
    └── test_engine.py      # Uji unit mesin chatbot
```

## Penjelasan Singkat

- **`app.py`** — Aplikasi web Flask. Menyajikan halaman chat/admin dan REST API untuk `/api/chat`, `/api/explain`, dan riwayat.
- **`evaluate.py`** — Menghitung akurasi bot terhadap data uji di `evaluasi/<tema>.csv`, dengan opsi `--sweep` untuk membandingkan banyak ambang batas.
- **`cli.py`** — Chat langsung dari terminal tanpa browser, mendukung flag `--tema`, `--ambang`, dan `--debug`.
