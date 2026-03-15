"""
Convertex - Professional File Converter
By LexcoreTech
"""

import streamlit as st
from pathlib import Path

from converter import convert
from utils import create_temp_file, cleanup_temp

# All available conversions: (label, source_extensions, target_extension)
CONVERSIONS = [
    ("PDF → Word", [".pdf"], ".docx", "Documents"),
    ("PDF → Excel", [".pdf"], ".xlsx", "Data"),
    ("Word → PDF", [".docx"], ".pdf", "Documents"),
    ("Text → PDF", [".txt"], ".pdf", "Documents"),
    ("JPG → PNG", [".jpg", ".jpeg"], ".png", "Images"),
    ("JPG → PDF", [".jpg", ".jpeg"], ".pdf", "Images"),
    ("PNG → JPG", [".png"], ".jpg", "Images"),
    ("PNG → PDF", [".png"], ".pdf", "Images"),
    ("CSV → Excel", [".csv"], ".xlsx", "Data"),
    ("Excel → CSV", [".xlsx", ".xls"], ".csv", "Data"),
    ("Excel → PDF", [".xlsx", ".xls"], ".pdf", "Data"),
]

# Detailed info and examples for each conversion
CONVERSION_INFO = {
    "PDF → Word": {
        "description": "Convert PDF documents to editable Word format. Preserves layout, paragraphs, and structure.",
        "use_cases": ["Contracts", "Reports", "Forms", "Proposals"],
        "tip": "Works best with text-based PDFs. Scanned PDFs may need OCR first.",
        "example": "Turn a contract PDF into an editable Word document so you can edit clauses and add amendments.",
    },
    "PDF → Excel": {
        "description": "Extract tables from PDFs into Excel spreadsheets. Ideal for structured data like statements.",
        "use_cases": ["Bank statements", "M-Pesa Business statements", "Financial reconciliations"],
        "tip": "Best for machine-generated PDFs with clear tables. Scanned PDFs require OCR.",
        "example": "Convert your M-Pesa 'Statement of Accounts' PDF to Excel for filtering, sorting, and reconciliation.",
    },
    "Word → PDF": {
        "description": "Convert Word documents to PDF for sharing, printing, or archiving.",
        "use_cases": ["Reports", "Letters", "Contracts"],
        "tip": "Extracts text and tables. No external dependencies required.",
        "example": "Turn a draft report into a professional PDF for client submission.",
    },
    "Text → PDF": {
        "description": "Convert plain text files to formatted PDF documents.",
        "use_cases": ["Notes", "Transcripts", "Simple documents"],
        "tip": "Preserves line breaks. Use UTF-8 text files for best results.",
        "example": "Convert meeting notes from a .txt file into a clean PDF for distribution.",
    },
    "JPG → PNG": {
        "description": "Convert JPG/JPEG images to PNG format. PNG supports transparency and lossless compression.",
        "use_cases": ["Logos", "Screenshots", "Graphics"],
        "tip": "PNG files are larger but higher quality. Use when you need transparency.",
        "example": "Convert a photo or logo from JPG to PNG for use in designs or presentations.",
    },
    "JPG → PDF": {
        "description": "Convert JPG/JPEG images to PDF. Creates a single-page PDF from each image.",
        "use_cases": ["Photos", "Receipts", "Scanned documents"],
        "tip": "High-quality output. Useful for combining photos into a document.",
        "example": "Turn a receipt photo into a PDF for expense reports or record-keeping.",
    },
    "PNG → JPG": {
        "description": "Convert PNG images to JPG/JPEG. Reduces file size for photos and web use.",
        "use_cases": ["Photos", "Web images", "Email attachments"],
        "tip": "JPG is smaller and ideal for photos. Transparency is flattened to white.",
        "example": "Shrink a large PNG screenshot to JPG for faster email or upload.",
    },
    "PNG → PDF": {
        "description": "Convert PNG images to PDF. Creates a single-page PDF from each image.",
        "use_cases": ["Screenshots", "Charts", "Graphics"],
        "tip": "Preserves image quality. Good for archiving visuals.",
        "example": "Convert a chart or diagram PNG into a PDF for a report or presentation.",
    },
    "CSV → Excel": {
        "description": "Convert CSV files to Excel spreadsheets. Adds formatting and column structure.",
        "use_cases": ["M-Pesa Buy Goods statements", "Paybill exports", "Data imports"],
        "tip": "Auto-detects encoding. Use Advanced options for M-Pesa or international CSVs.",
        "example": "Convert M-Pesa Buy Goods CSV export to Excel for filters, formatting, and internal audits.",
    },
    "Excel → CSV": {
        "description": "Export Excel spreadsheets to CSV format. Preserves data in a universal format.",
        "use_cases": ["Data export", "System imports", "Sharing tabular data"],
        "tip": "Only the first sheet is exported. UTF-8 encoding.",
        "example": "Export a contact list from Excel to CSV for import into another system.",
    },
    "Excel → PDF": {
        "description": "Convert Excel spreadsheets to PDF. Preserves layout for professional distribution.",
        "use_cases": ["Invoices", "Quotes", "Payroll slips"],
        "tip": "All sheets rendered as tables. No external dependencies required.",
        "example": "Convert an invoice or payroll slip to PDF for professional, tamper-proof distribution.",
    },
}

# Page config - must be first Streamlit command
st.set_page_config(
    page_title="Convertex - File Converter",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Premium Dashboard CSS
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    /* Base */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', system-ui, sans-serif !important;
    }
    .block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; max-width: 1200px !important; }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #0c1222 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.06) !important;
    }
    [data-testid="stSidebar"] .stMarkdown { color: #94a3b8 !important; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #f8fafc !important; }
    [data-testid="stSidebar"] .stRadio label { font-size: 0.9rem !important; padding: 0.4rem 0 !important; }
    
    /* Hero - emerald gradient */
    .hero-dashboard {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #064e3b 0%, #047857 40%, #10b981 100%);
        border-radius: 20px;
        margin-bottom: 2.5rem;
        box-shadow: 0 8px 32px rgba(16, 185, 129, 0.25);
        border: 1px solid rgba(255,255,255,0.08);
    }
    .hero-dashboard .hero-title {
        font-size: 2.75rem;
        font-weight: 800;
        color: #fff;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.03em;
    }
    .hero-dashboard .hero-tagline {
        font-size: 1.1rem;
        color: rgba(255,255,255,0.9);
        margin: 0 0 1rem 0;
    }
    .hero-dashboard .hero-brand {
        font-size: 0.75rem;
        color: rgba(255,255,255,0.7);
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }
    
    /* Step indicators */
    .step-row {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }
    .step-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #64748b;
        font-size: 0.85rem;
        font-weight: 500;
    }
    .step-num {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: #334155;
        color: #94a3b8;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.8rem;
    }
    .step-item.active .step-num {
        background: #10b981;
        color: #fff;
    }
    
    /* Main content column - card style (nth-child targets middle of 3-col layout) */
    [data-testid="stHorizontalBlock"] > div:nth-child(2) {
        background: #1e293b !important;
        border-radius: 16px !important;
        padding: 2.5rem !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        box-shadow: 0 4px 24px rgba(0,0,0,0.2) !important;
    }
    
    /* Upload zone */
    [data-testid="stFileUploader"] {
        padding: 2rem !important;
        border-radius: 16px !important;
        background: rgba(15, 23, 42, 0.6) !important;
        border: 2px dashed #334155 !important;
    }
    [data-testid="stFileUploader"]:hover { border-color: #10b981 !important; }
    
    /* Format chips */
    .format-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    .format-chip {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        padding: 0.35rem 0.85rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid rgba(16, 185, 129, 0.25);
    }
    
    /* Buttons */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4) !important;
        border: none !important;
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.5) !important;
        transform: translateY(-1px);
    }
    
    /* Selectbox / inputs - dark */
    .stSelectbox > div, .stTextInput > div { background: #0f172a !important; }
    
    /* Expander */
    .streamlit-expanderHeader { background: #1e293b !important; border-radius: 12px !important; }
    
    /* Success / Download card */
    .success-card {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 1.25rem;
        margin-top: 1rem;
    }
    
    /* Info card */
    .info-card {
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 14px;
        padding: 1.5rem 1.75rem;
        margin-bottom: 1.5rem;
    }
    .info-card .info-title { font-size: 1.1rem; font-weight: 700; color: #34d399; margin-bottom: 0.5rem; }
    .info-card .info-desc { color: #94a3b8; font-size: 0.9rem; line-height: 1.5; margin-bottom: 0.75rem; }
    .info-card .info-usecases { color: #64748b; font-size: 0.85rem; margin-bottom: 0.5rem; }
    .info-card .info-tip { color: #6b8e6b; font-size: 0.8rem; font-style: italic; margin-bottom: 0.75rem; }
    .info-card .info-example { background: rgba(0,0,0,0.2); padding: 0.75rem 1rem; border-radius: 8px; font-size: 0.85rem; color: #cbd5e1; }
    
    /* Footer */
    .app-footer {
        text-align: center;
        padding: 2rem 0 1rem;
        margin-top: 2rem;
        color: #475569;
        font-size: 0.8rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# Sidebar - conversion picker (partitioned by category)
with st.sidebar:
    st.markdown("## 🔄 Convertex")
    st.markdown("*Professional file conversion*")
    st.markdown("---")
    st.markdown("**Choose conversion**")
    
    conversion_labels = [c[0] for c in CONVERSIONS]
    # Grouped options: "Documents » PDF → Word", "Images » JPG → PNG", etc.
    opts_display = [f"{c[3]} » {c[0]}" for c in CONVERSIONS]
    
    selected_display = st.selectbox(
        "Conversion",
        options=opts_display,
        label_visibility="collapsed",
        key="conversion_select",
    )
    selected_label = selected_display.split(" » ", 1)[1]
    idx = conversion_labels.index(selected_label)
    selected_conversion = CONVERSIONS[idx]
    source_exts, target_ext = selected_conversion[1], selected_conversion[2]
    st.markdown("---")
    st.caption(f"Selected: **{selected_label}**")
    st.caption(f"Upload: {', '.join(e.upper().strip('.') for e in source_exts)} → {target_ext.upper().strip('.')}")
    st.markdown("---")
    st.markdown("**By LexcoreTech**")
    st.caption("© 2025")

# Main
st.markdown("""
<div class="hero-dashboard">
    <p class="hero-title">Convertex</p>
    <p class="hero-tagline">Convert documents, images, and spreadsheets with confidence</p>
    <p class="hero-brand">By LexcoreTech</p>
</div>
""", unsafe_allow_html=True)

# Step indicators
st.markdown("""
<div class="step-row">
    <span class="step-item active"><span class="step-num">1</span> Upload</span>
    <span class="step-item"><span class="step-num">2</span> Convert</span>
    <span class="step-item"><span class="step-num">3</span> Download</span>
</div>
""", unsafe_allow_html=True)

# Main content
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    # Info card - conversion details and example
    info = CONVERSION_INFO.get(selected_label, {})
    if info:
        use_cases_str = " • ".join(info.get("use_cases", []))
        st.markdown(f"""
        <div class="info-card">
            <div class="info-title">{selected_label}</div>
            <div class="info-desc">{info.get("description", "")}</div>
            <div class="info-usecases"><strong>Use cases:</strong> {use_cases_str}</div>
            <div class="info-tip">💡 {info.get("tip", "")}</div>
            <div class="info-example"><strong>Example:</strong> {info.get("example", "")}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"**📤 Upload file for: {selected_label}**")
    chips_html = "".join(f'<span class="format-chip">{e.upper().strip(".")}</span>' for e in source_exts)
    st.markdown(f'<div class="format-chips">{chips_html}</div>', unsafe_allow_html=True)
    st.markdown("")
    
    # Build allowed types from source extensions
    ext_to_type = {".pdf": "pdf", ".docx": "docx", ".txt": "txt", ".jpg": "jpg", ".jpeg": "jpeg", ".png": "png", ".csv": "csv", ".xlsx": "xlsx", ".xls": "xls"}
    allowed_types = [ext_to_type[e] for e in source_exts if e in ext_to_type]
    
    uploaded = st.file_uploader(
        "Upload",
        type=allowed_types,
        help=f"Upload {selected_label.split('→')[0].strip()} file",
        label_visibility="collapsed",
    )

    if uploaded:
        input_ext = Path(uploaded.name).suffix.lower()
        if input_ext not in source_exts:
            st.error(f"Wrong file type for {selected_label}. Please upload a {' or '.join(e.upper().strip('.') for e in source_exts)} file.")
        else:
            encoding = None
            pages = None
            password = None
            delimiter = None

            with st.expander("⚙️ Advanced options", expanded=False):
                if input_ext in (".csv",):
                    enc_opt = st.selectbox("CSV encoding", ["auto", "utf-8", "latin-1", "iso-8859-1", "cp1252"], help="Auto-detects if not sure")
                    encoding = None if enc_opt == "auto" else enc_opt
                    delim_opt = st.selectbox("Delimiter", ["auto", "Comma (,)", "Semicolon (;)", "Tab"], help="For M-Pesa or custom CSVs")
                    delim_map = {"auto": None, "Comma (,)": ",", "Semicolon (;)": ";", "Tab": "\t"}
                    delimiter = delim_map.get(delim_opt)
                if input_ext == ".pdf" and target_ext == ".xlsx":
                    pages_str = st.text_input("PDF pages (e.g. 0,1,2 or leave empty for all)", placeholder="0,1,2")
                    if pages_str:
                        try:
                            pages = [int(p.strip()) for p in pages_str.split(",")]
                        except ValueError:
                            pages = None
                    password = st.text_input("PDF password (if protected)", type="password")
                    password = password or None

            st.markdown(f"**Convert to {target_ext.upper().strip('.')}**")
            btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
            with btn_col2:
                if st.button("Convert", type="primary", use_container_width=True):
                    input_temp = None
                    output_temp = None
                    try:
                        input_temp = create_temp_file(Path(uploaded.name).suffix, delete_on_exit=False)
                        input_temp.write_bytes(uploaded.getvalue())
                        output_temp = create_temp_file(target_ext, delete_on_exit=False)
                        with st.spinner("Converting... Please wait."):
                            _, warning = convert(input_temp, output_temp, target_ext, encoding=encoding, delimiter=delimiter, pages=pages, password=password)
                        if warning:
                            st.warning(warning)
                        data = output_temp.read_bytes()
                        # Store in session (cleared when conversion/format changes)
                        st.session_state["converted_data"] = data
                        st.session_state["converted_name"] = Path(uploaded.name).stem + target_ext
                        st.session_state["converted_for"] = (uploaded.name, target_ext)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Conversion failed: {str(e)}")
                    finally:
                        if input_temp and input_temp.exists():
                            cleanup_temp(input_temp)
                        if output_temp and output_temp.exists():
                            cleanup_temp(output_temp)

            conv_for = st.session_state.get("converted_for")
            if conv_for == (uploaded.name, target_ext) and "converted_data" in st.session_state:
                st.markdown('<div class="success-card">', unsafe_allow_html=True)
                st.success("✓ Conversion complete. Download your file below.")
                st.download_button(
                    label="⬇️ Download converted file",
                    data=st.session_state["converted_data"],
                    file_name=st.session_state["converted_name"],
                    mime="application/octet-stream",
                    type="primary",
                    use_container_width=True,
                    key="download_btn",
                )
                st.markdown('</div>', unsafe_allow_html=True)

# Value props
with st.expander("Why Convertex?", expanded=False):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Bank & M-Pesa**")
        st.caption("PDF statements to Excel. CSV exports to formatted spreadsheets.")
    with c2:
        st.markdown("**Professional outputs**")
        st.caption("Invoices, quotes, payroll to PDF. High-quality image conversions.")
    with c3:
        st.markdown("**Privacy first**")
        st.caption("All processing is local. No files sent to external servers.")

st.markdown('<div class="app-footer">© LexcoreTech — Convertex</div>', unsafe_allow_html=True)
