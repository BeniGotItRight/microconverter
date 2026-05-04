"""
Convertex - The World's Best File Converter
By LexcoreTech & Benson Motari
"""

import streamlit as st
from pathlib import Path
import time

from converter import convert
from utils import create_temp_file, cleanup_temp

# High-Quality Conversion Database
CATEGORIES = {
    "📄 Documents": [
        ("PDF → Word", [".pdf"], ".docx"),
        ("PDF → Text", [".pdf"], ".txt"),
        ("Word → PDF", [".docx"], ".pdf"),
        ("Word → Text", [".docx"], ".txt"),
        ("Text → PDF", [".txt"], ".pdf"),
        ("PowerPoint → PDF", [".pptx"], ".pdf"),
        ("Markdown → PDF", [".md"], ".pdf"),
        ("Markdown → HTML", [".md"], ".html"),
        ("HTML → PDF", [".html", ".htm"], ".pdf"),
        ("RTF → PDF", [".rtf"], ".pdf"),
        ("ODT → PDF", [".odt"], ".pdf"),
    ],
    "📊 Data & Statements": [
        ("PDF → Excel (Bank Statements)", [".pdf"], ".xlsx"),
        ("CSV → Excel", [".csv"], ".xlsx"),
        ("CSV → PDF", [".csv"], ".pdf"),
        ("Excel → CSV", [".xlsx", ".xls"], ".csv"),
        ("Excel → PDF", [".xlsx", ".xls"], ".pdf"),
        ("JSON → Excel", [".json"], ".xlsx"),
        ("JSON → CSV", [".json"], ".csv"),
        ("JSON → PDF", [".json"], ".pdf"),
        ("JSON → YAML", [".json"], ".yaml"),
        ("XML → Excel", [".xml"], ".xlsx"),
        ("XML → CSV", [".xml"], ".csv"),
        ("XML → JSON", [".xml"], ".json"),
        ("YAML → Excel", [".yaml", ".yml"], ".xlsx"),
        ("YAML → JSON", [".yaml", ".yml"], ".json"),
    ],
    "🖼️ Images": [
        ("JPG → PNG", [".jpg", ".jpeg"], ".png"),
        ("PNG → JPG", [".png"], ".jpg"),
        ("Any → WebP", [".jpg", ".jpeg", ".png", ".bmp", ".tiff"], ".webp"),
        ("WebP → JPG/PNG", [".webp"], ".png"),
        ("Image → PDF", [".jpg", ".jpeg", ".png", ".webp", ".bmp"], ".pdf"),
        ("Any → BMP/TIFF", [".jpg", ".png", ".webp"], ".bmp"),
        ("GIF → PNG/JPG", [".gif"], ".png"),
        ("PNG → ICO (Favicon)", [".png"], ".ico"),
    ]
}

CONVERSION_INFO = {
    "PDF → Word": {
        "description": "Transform non-editable PDF documents into fully editable Microsoft Word (.docx) files.",
        "use_cases": ["Contracts", "Manuscripts", "Legal Documents", "Form Editing"],
        "tip": "Works best with digital PDFs. Scanned PDFs will be extracted as text/images.",
        "example": "Turn a static contract PDF into an editable Word document for clause modifications."
    },
    "PDF → Excel (Bank Statements)": {
        "description": "High-precision extraction of tables from PDF documents directly into Excel spreadsheets.",
        "use_cases": ["M-Pesa Statements", "Bank Statements", "Invoices", "Financial Reports"],
        "tip": "Designed for machine-generated PDFs. If tables aren't detected, it falls back to row extraction.",
        "example": "Convert your monthly bank statement PDF into Excel for filtering and reconciliation."
    },
    "Word → PDF": {
        "description": "Convert Microsoft Word documents to professional PDF files for universal viewing.",
        "use_cases": ["Resume sharing", "Official Letters", "Final Reports"],
        "tip": "Preserves basic layout, fonts, and tables without needing Microsoft Word installed.",
        "example": "Turn your draft report into a professional PDF ready for client delivery."
    },
    "PowerPoint → PDF": {
        "description": "Convert PowerPoint presentations into high-quality PDF handouts.",
        "use_cases": ["Slide Sharing", "Study Material", "Presentation Archives"],
        "tip": "Extracts text and tables from every slide into a multi-page PDF document.",
        "example": "Convert a 50-slide deck into a lightweight PDF for easy email sharing."
    },
    "CSV → Excel": {
        "description": "Convert raw CSV data into clean, professionally formatted Excel workbooks.",
        "use_cases": ["Data Cleaning", "M-Pesa Buy Goods Reports", "System Exports"],
        "tip": "Auto-sizes columns and detects the best encoding for your data (UTF-8, Latin-1, etc.).",
        "example": "Turn a messy CSV export into a clean, searchable Excel sheet for your accounts team."
    },
    "JSON → Excel": {
        "description": "Flatten complex, nested JSON data into a simple tabular Excel format.",
        "use_cases": ["API Exports", "Database Dumps", "Developer Data Analysis"],
        "tip": "Automatically flattens nested objects so you can analyze API data in Excel.",
        "example": "Take a list of users from a JSON API and see them clearly in an Excel table."
    },
    "Markdown → PDF": {
        "description": "Convert Markdown text files into beautifully formatted PDF documents.",
        "use_cases": ["Documentation", "Technical Reports", "Project READMEs"],
        "tip": "Supports tables, fenced code blocks, and standard Markdown syntax.",
        "example": "Convert your project README.md into a professional PDF manual."
    },
    "Any → WebP": {
        "description": "Convert images to WebP for superior compression and faster web loading.",
        "use_cases": ["Website Optimization", "Email Attachments", "Storage Saving"],
        "tip": "WebP files are significantly smaller than JPG/PNG with almost no quality loss.",
        "example": "Convert a large 5MB PNG into a 300KB WebP for your blog post."
    }
}

# Page config
st.set_page_config(
    page_title="Convertex - The Ultimate File Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# World-Class UI Styling
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    /* Base Typography & Theme */
    html, body, [data-testid="stAppViewContainer"] { 
        font-family: 'Plus Jakarta Sans', sans-serif !important; 
        background-color: #0b0f1a !important;
    }
    .main .block-container { padding-top: 1.5rem !important; max-width: 1200px !important; }

    /* Glassmorphism Hero */
    .hero-container {
        position: relative;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, #064e3b 0%, #065f46 40%, #10b981 100%);
        border-radius: 30px;
        margin-bottom: 3rem;
        box-shadow: 0 20px 50px rgba(16, 185, 129, 0.2);
        overflow: hidden;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.5rem;
        letter-spacing: -0.05em;
        text-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .hero-subtitle {
        font-size: 1.25rem;
        color: rgba(255,255,255,0.9);
        font-weight: 500;
        margin-bottom: 1rem;
    }
    .hero-badge {
        display: inline-block;
        padding: 0.5rem 1.25rem;
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        border-radius: 50px;
        color: white;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        border: 1px solid rgba(255,255,255,0.2);
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: #0f172a !important;
        border-right: 1px solid rgba(255,255,255,0.05) !important;
    }
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: 800;
        color: #10b981;
        margin-bottom: 0.5rem;
    }
    
    /* Info Cards */
    .info-card {
        background: #1e293b;
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 2rem;
    }
    .info-title { font-size: 1.75rem; font-weight: 700; color: #10b981; margin-bottom: 1rem; }
    .info-desc { font-size: 1.1rem; color: #94a3b8; line-height: 1.6; margin-bottom: 1.5rem; }
    .use-case-tag {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .info-tip {
        background: rgba(0,0,0,0.2);
        padding: 1rem;
        border-radius: 12px;
        font-size: 0.9rem;
        color: #cbd5e1;
        border-left: 4px solid #10b981;
    }

    /* Upload Area */
    [data-testid="stFileUploader"] {
        background: #0f172a !important;
        border: 2px dashed #334155 !important;
        border-radius: 20px !important;
        padding: 2rem !important;
    }
    [data-testid="stFileUploader"]:hover { border-color: #10b981 !important; }

    /* Primary Button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 15px !important;
        padding: 0.8rem 2rem !important;
        border: none !important;
        box-shadow: 0 10px 20px rgba(16, 185, 129, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 15px 30px rgba(16, 185, 129, 0.4) !important;
    }

    /* Footer */
    .footer-container {
        text-align: center;
        padding: 4rem 0;
        margin-top: 4rem;
        border-top: 1px solid #1e293b;
    }
    .footer-brand { font-size: 1.5rem; font-weight: 800; color: #10b981; margin-bottom: 1rem; }
    .footer-credit { font-size: 0.9rem; color: #64748b; margin-bottom: 0.5rem; }
    .footer-email { color: #10b981; text-decoration: none; font-weight: 600; }
    
    /* Animation */
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    .animated { animation: fadeIn 0.6s ease-out forwards; }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown('<div class="sidebar-header">🔄 Convertex</div>', unsafe_allow_html=True)
    st.caption("Engineered for Maximum Precision")
    st.markdown("---")
    
    st.markdown("**1. Choose Category**")
    category_list = list(CATEGORIES.keys())
    selected_cat = st.radio("Category", category_list, label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("**2. Select Conversion**")
    conv_options = CATEGORIES[selected_cat]
    conv_labels = [c[0] for c in conv_options]
    selected_label = st.selectbox("Conversion Task", conv_labels, label_visibility="collapsed")
    
    # Get configuration for selected conversion
    idx = conv_labels.index(selected_label)
    conv_data = conv_options[idx]
    source_exts, target_ext = conv_data[1], conv_data[2]
    
    st.markdown("---")
    st.markdown("### Professional Credits")
    st.markdown("**Primary Developer:**")
    st.markdown("- **LexcoreTech**")
    st.markdown("**Lead Architect:**")
    st.markdown("- **Benson Motari**")
    st.markdown(f'<a href="mailto:bensonmotari4@gmail.com" class="footer-email">bensonmotari4@gmail.com</a>', unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Version 2.0 (Ultimate Edition)")

# Hero Section
st.markdown("""
<div class="hero-container animated">
    <div class="hero-badge">World Class Processing</div>
    <div class="hero-title">Convertex</div>
    <div class="hero-subtitle">The ultimate document and data engine by LexcoreTech & Benson Motari</div>
</div>
""", unsafe_allow_html=True)

# Main Workspace
col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    # Information Panel
    info = CONVERSION_INFO.get(selected_label, {
        "description": "Premium file conversion using LexcoreTech's proprietary processing engine.",
        "use_cases": ["Business Reports", "Data Migration", "Professional Archiving"],
        "tip": "Optimized for high-precision output and data integrity.",
        "example": "Ready for your most critical professional tasks."
    })
    
    st.markdown(f"""
    <div class="info-card animated">
        <div class="info-title">{selected_label}</div>
        <div class="info-desc">{info['description']}</div>
        <div style="margin-bottom: 1.5rem;">
            {" ".join([f'<span class="use-case-tag">{u}</span>' for u in info.get('use_cases', [])])}
        </div>
        <div class="info-tip">
            <strong>💡 Expert Tip:</strong> {info['tip']}<br>
            <div style="margin-top: 0.5rem; opacity: 0.8; font-style: italic;">Example: {info.get('example', '')}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Upload Section
    st.markdown(f"### 📤 Step 1: Upload your {selected_cat.split()[-1]} file")
    
    ext_mapping = {
        ".pdf": "pdf", ".docx": "docx", ".txt": "txt", ".pptx": "pptx",
        ".html": "html", ".htm": "html", ".md": "md", ".rtf": "rtf", ".odt": "odt",
        ".jpg": "jpg", ".jpeg": "jpeg", ".png": "png", ".webp": "webp",
        ".bmp": "bmp", ".tiff": "tiff", ".tif": "tiff", ".gif": "gif", ".ico": "ico",
        ".csv": "csv", ".xlsx": "xlsx", ".xls": "xls", ".json": "json",
        ".xml": "xml", ".yaml": "yaml", ".yml": "yaml"
    }
    allowed = [ext_mapping[e] for e in source_exts if e in ext_mapping]
    
    uploaded_file = st.file_uploader(
        f"Select a {', '.join(e.upper().strip('.') for e in source_exts)} file",
        type=allowed,
        label_visibility="collapsed"
    )

    if uploaded_file:
        file_ext = Path(uploaded_file.name).suffix.lower()
        
        # Expert Options
        with st.expander("⚙️ Advanced Processing Options", expanded=False):
            encoding, delimiter, pages, password = None, None, None, None
            
            if file_ext == ".csv":
                c1, c2 = st.columns(2)
                with c1:
                    enc_opt = st.selectbox("File Encoding", ["auto", "utf-8", "latin-1", "cp1252"], help="Auto-detect works for most files.")
                    encoding = None if enc_opt == "auto" else enc_opt
                with c2:
                    delim_opt = st.selectbox("Column Delimiter", ["auto", "Comma (,)", "Semicolon (;)", "Tab"], help="M-Pesa CSVs often use 'auto'.")
                    delim_map = {"auto": None, "Comma (,)": ",", "Semicolon (;)": ";", "Tab": "\t"}
                    delimiter = delim_map[delim_opt]
            
            if file_ext == ".pdf" and target_ext == ".xlsx":
                c1, c2 = st.columns(2)
                with c1:
                    pages_str = st.text_input("Page Range", placeholder="e.g. 0,1,5-10", help="Zero-indexed. Leave empty for all.")
                    if pages_str:
                        try:
                            # Basic range parsing logic
                            pages = []
                            for p in pages_str.split(","):
                                if "-" in p:
                                    start, end = map(int, p.split("-"))
                                    pages.extend(range(start, end + 1))
                                else:
                                    pages.append(int(p))
                        except: pages = None
                with c2:
                    password = st.text_input("PDF Password", type="password", help="Only if the file is encrypted.") or None

        # Process Button
        st.markdown("### 🚀 Step 2: Begin Processing")
        if st.button(f"Convert to {target_ext.upper().strip('.')}", type="primary", use_container_width=True):
            try:
                # Progress simulation for "World Class" feel
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("📁 Initializing LexcoreTech engine...")
                progress_bar.progress(20)
                time.sleep(0.3)
                
                input_p = create_temp_file(file_ext, delete_on_exit=False)
                input_p.write_bytes(uploaded_file.getvalue())
                output_p = create_temp_file(target_ext, delete_on_exit=False)
                
                status_text.text("⚡ Executing advanced conversion algorithms...")
                progress_bar.progress(60)
                
                # Actual Conversion
                _, warning = convert(
                    input_p, output_p, target_ext,
                    encoding=encoding, delimiter=delimiter,
                    pages=pages, password=password
                )
                
                status_text.text("✨ Finalizing output and optimizing file size...")
                progress_bar.progress(90)
                time.sleep(0.3)
                
                if warning: st.warning(warning)
                
                result_data = output_p.read_bytes()
                st.session_state["conv_data"] = result_data
                st.session_state["conv_name"] = Path(uploaded_file.name).stem + target_ext
                st.session_state["conv_key"] = (uploaded_file.name, target_ext)
                
                progress_bar.progress(100)
                status_text.text("✅ Conversion Complete!")
                
                cleanup_temp(input_p)
                cleanup_temp(output_p)
                time.sleep(0.5)
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Processing Error: {str(e)}")

        # Result Display
        current_key = st.session_state.get("conv_key")
        if current_key == (uploaded_file.name, target_ext) and "conv_data" in st.session_state:
            st.markdown("""
            <div style="background: rgba(16, 185, 129, 0.1); border: 2px solid #10b981; border-radius: 20px; padding: 2.5rem; text-align: center; margin-top: 2rem;" class="animated">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🎉</div>
                <h2 style="color: #10b981; margin-bottom: 1rem;">Ready for Download</h2>
                <p style="color: #94a3b8; margin-bottom: 2rem;">Your file has been processed to perfection by the LexcoreTech engine.</p>
            """, unsafe_allow_html=True)
            
            st.download_button(
                label=f"⬇️ Download {st.session_state['conv_name']}",
                data=st.session_state["conv_data"],
                file_name=st.session_state["conv_name"],
                mime="application/octet-stream",
                type="primary",
                use_container_width=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

# World Class Footer
st.markdown(f"""
<div class="footer-container">
    <div class="footer-brand">CONVERTEX</div>
    <div class="footer-credit">Engineered by <strong>LexcoreTech</strong></div>
    <div class="footer-credit">Lead Architect: <strong>Benson Motari</strong></div>
    <div class="footer-credit">
        <a href="mailto:bensonmotari4@gmail.com" class="footer-email">bensonmotari4@gmail.com</a>
    </div>
    <div style="margin-top: 2rem; font-size: 0.8rem; color: #475569; letter-spacing: 0.05em;">
        © 2026 LexcoreTech Professional Suite • All Rights Reserved
    </div>
</div>
""", unsafe_allow_html=True)
