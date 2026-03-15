# Convertex

**Professional file conversion by LexcoreTech**

Convert documents, images, and spreadsheets with high-quality output. Ideal for bank statements, M-Pesa reports, invoices, and more.

## Supported Conversions

| From   | To       |
|--------|----------|
| PDF    | Word, Excel |
| Word   | PDF      |
| Text   | PDF      |
| JPG/PNG| PNG/JPG, PDF |
| CSV    | Excel    |
| Excel  | CSV, PDF |

## Quick Start

**Requires:** Python 3.9+ ([python.org](https://python.org))

### Option A: Cross-platform (Windows, macOS, Linux)

```bash
python run.py
```

This creates a virtual environment, installs dependencies, and starts the app. Use on any OS.

### Option B: Platform-specific

**Windows** — Double-click `run.bat` or run in Command Prompt:
```
run.bat
```

**macOS / Linux** — In Terminal:
```bash
./run.sh
```

### Option C: Manual setup

```bash
# Create virtual environment
python -m venv .venv

# Activate (choose one):
#   Windows CMD:        .venv\Scripts\activate.bat
#   Windows PowerShell: .venv\Scripts\Activate.ps1
#   macOS / Linux:     source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

### Open in browser

- **Local:** http://localhost:8501
- **Same network:** http://YOUR_IP:8501 (replace YOUR_IP with your machine's IP)

Pick a conversion type from the sidebar, then upload your file.

## Features

- **File size limit:** Max 50 MB per file
- CSV encoding selection (for M-Pesa and international CSVs)
- Delimiter selection (comma, semicolon, tab)
- PDF page range for PDF → Excel
- Password-protected PDF support

## Use Cases

- **Bank & M-Pesa statements** — Convert PDF statements to Excel for reconciliations
- **M-Pesa Buy Goods / Paybill** — CSV exports to formatted Excel
- **Invoices & payroll** — Excel to PDF for professional distribution
- **Images** — High-quality JPG/PNG conversions and image-to-PDF

## Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → connect your GitHub repo
4. Set **Main file path** to `app.py`
5. Deploy — users access your app via the generated URL

## Privacy

All processing happens locally. No files are sent to external servers. Temporary files are deleted after conversion.

## License

© LexcoreTech
