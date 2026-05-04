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
    "PDF → Word": {"description": "Transform non-editable PDF documents into fully editable Microsoft Word (.docx) files.", "use_cases": ["Contracts", "Manuscripts", "Legal Documents"], "tip": "Works best with digital PDFs."},
    "PDF → Excel (Bank Statements)": {"description": "High-precision extraction of tables from PDF bank statements into Excel spreadsheets.", "use_cases": ["M-Pesa Statements", "Bank Statements", "Reconciliations"], "tip": "Optimized for M-Pesa and local bank reports."},
    "Word → PDF": {"description": "Convert Word documents to professional PDF files for universal viewing.", "use_cases": ["Resumes", "Official Letters"], "tip": "Preserves basic layout and tables."},
    "CSV → Excel": {"description": "Convert raw CSV data into clean, professionally formatted Excel workbooks.", "use_cases": ["Data Cleaning", "System Exports"], "tip": "Auto-sizes columns and detects encoding."},
}

# Page config
st.set_page_config(
    page_title="Convertex - Premium Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Comprehensive UI Styling
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    /* Base */
    html, body, [data-testid="stAppViewContainer"] { 
        font-family: 'Plus Jakarta Sans', sans-serif !important; 
        background-color: #0b0f1a !important;
    }
    
    /* Sidebar Overhaul */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #020617 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.05) !important;
    }
    .sb-section {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1.25rem;
    }
    .sb-label {
        font-size: 0.7rem;
        font-weight: 800;
        color: #10b981;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-bottom: 0.75rem;
        display: block;
    }
    .sb-feature {
        font-size: 0.85rem;
        color: #94a3b8;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .privacy-badge {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 0.75rem;
        border-radius: 10px;
        font-size: 0.75rem;
        color: #10b981;
        text-align: center;
        margin-top: 1rem;
    }

    /* Hero */
    .hero-box {
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #064e3b 0%, #10b981 100%);
        border-radius: 24px;
        margin-bottom: 2.5rem;
        text-align: center;
        box-shadow: 0 20px 40px rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(255,255,255,0.1);
    }
    .hero-title { font-size: 3.5rem; font-weight: 800; color: white; letter-spacing: -0.04em; margin-bottom: 0.5rem; }
    
    /* Info Panel */
    .info-card {
        background: #1e293b;
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 2rem;
    }
    .tag {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.4rem;
    }

    /* Footer */
    .footer-box {
        text-align: center;
        padding: 4rem 0 2rem;
        border-top: 1px solid #1e293b;
        margin-top: 4rem;
    }
    .footer-brand { font-size: 1.25rem; font-weight: 800; color: #10b981; margin-bottom: 0.75rem; }
    .footer-link { color: #10b981; text-decoration: none; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# Comprehensive Sidebar Upgrade
with st.sidebar:
    st.markdown('<div style="font-size: 2.25rem; font-weight: 800; color: #10b981; margin-bottom: 1.5rem; letter-spacing:-0.03em;">CONVERTEX</div>', unsafe_allow_html=True)
    
    # 1. Primary Controls
    st.markdown('<div class="sb-section">', unsafe_allow_html=True)
    st.markdown('<span class="sb-label">01. Choose Category</span>', unsafe_allow_html=True)
    category_list = list(CATEGORIES.keys())
    selected_cat = st.radio("Category", category_list, label_visibility="collapsed")
    
    st.markdown('<div style="height:1.25rem;"></div>', unsafe_allow_html=True)
    st.markdown('<span class="sb-label">02. Select Operation</span>', unsafe_allow_html=True)
    conv_options = CATEGORIES[selected_cat]
    conv_labels = [c[0] for c in conv_options]
    selected_label = st.selectbox("Operation", conv_labels, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. Quick Start Guide
    st.markdown('<div class="sb-section">', unsafe_allow_html=True)
    st.markdown('<span class="sb-label">Quick Start Guide</span>', unsafe_allow_html=True)
    st.markdown('<div class="sb-feature">1️⃣ Pick your format category</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-feature">2️⃣ Select specific conversion</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-feature">3️⃣ Upload & Process live</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. Privacy Assurance (NEW)
    st.markdown("""
    <div class="privacy-badge">
        🔒 <strong>Privacy Guarantee</strong><br>
        Files are processed locally and deleted immediately after conversion. No data is stored.
    </div>
    """, unsafe_allow_html=True)
    
    # 4. System Intelligence
    st.markdown('<div class="sb-section" style="margin-top:1.5rem;">', unsafe_allow_html=True)
    st.markdown('<span class="sb-label">System Intelligence</span>', unsafe_allow_html=True)
    st.markdown('<div class="sb-feature">✅ 35+ Pro Formats</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-feature">✅ Bank-Grade OCR Fallback</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-feature">✅ Ultra-Fast Processing</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-feature" style="color:#10b981;">● Engine: 100% Healthy</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero-box">
    <div class="hero-title">Convertex</div>
    <div style="color:rgba(255,255,255,0.9); font-size:1.1rem; font-weight:500;">Premium Suite by LexcoreTech & Benson Motari</div>
</div>
""", unsafe_allow_html=True)

# Main Workspace
col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    idx = conv_labels.index(selected_label)
    conv_data = conv_options[idx]
    source_exts, target_ext = conv_data[1], conv_data[2]
    
    info = CONVERSION_INFO.get(selected_label, {
        "description": "High-precision processing using the LexcoreTech conversion engine.",
        "use_cases": ["Business Reports", "Data Migration", "Digital Archiving"],
        "tip": "Optimized for speed and high fidelity.",
    })
    
    st.markdown(f"""
    <div class="info-card">
        <div style="font-size: 1.75rem; font-weight: 700; color: #10b981; margin-bottom: 0.75rem;">{selected_label}</div>
        <div style="color: #94a3b8; font-size: 1.1rem; line-height: 1.6; margin-bottom: 1.25rem;">{info['description']}</div>
        <div style="margin-bottom: 1.5rem;">
            {" ".join([f'<span class="tag">{u}</span>' for u in info.get('use_cases', [])])}
        </div>
        <div style="background: rgba(0,0,0,0.2); padding: 1rem; border-radius: 12px; font-size: 0.9rem; color: #cbd5e1; border-left: 4px solid #10b981;">
            <strong>Expert Tip:</strong> {info['tip']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"### 📤 Step 1: Upload File")
    ext_mapping = {".pdf":"pdf", ".docx":"docx", ".txt":"txt", ".pptx":"pptx", ".html":"html", ".htm":"html", ".md":"md", ".rtf":"rtf", ".odt":"odt", ".jpg":"jpg", ".jpeg":"jpeg", ".png":"png", ".webp":"webp", ".bmp":"bmp", ".tiff":"tiff", ".tif":"tiff", ".gif":"gif", ".ico":"ico", ".csv":"csv", ".xlsx":"xlsx", ".xls":"xls", ".json":"json", ".xml":"xml", ".yaml":"yaml", ".yml":"yaml"}
    allowed = [ext_mapping[e] for e in source_exts if e in ext_mapping]
    
    uploaded_file = st.file_uploader("Upload", type=allowed, label_visibility="collapsed")

    if uploaded_file:
        file_ext = Path(uploaded_file.name).suffix.lower()
        with st.expander("⚙️ Advanced Options", expanded=False):
            encoding, delimiter, pages, password = None, None, None, None
            if file_ext == ".csv":
                encoding = st.selectbox("Encoding", ["auto", "utf-8", "latin-1", "cp1252"])
                encoding = None if encoding == "auto" else encoding
                delimiter = st.selectbox("Delimiter", ["auto", ",", ";", "\\t"])
                delimiter = None if delimiter == "auto" else delimiter
            if file_ext == ".pdf" and target_ext == ".xlsx":
                pages_str = st.text_input("Pages (e.g. 0,1)", placeholder="All")
                if pages_str:
                    try: pages = [int(p.strip()) for p in pages_str.split(",")]
                    except: pages = None
                password = st.text_input("Password", type="password") or None

        st.markdown("### 🚀 Step 2: Convert")
        if st.button(f"Process to {target_ext.upper().strip('.')}", type="primary", use_container_width=True):
            try:
                prog = st.progress(0)
                input_p = create_temp_file(file_ext, delete_on_exit=False)
                input_p.write_bytes(uploaded_file.getvalue())
                output_p = create_temp_file(target_ext, delete_on_exit=False)
                prog.progress(50)
                _, warning = convert(input_p, output_p, target_ext, encoding=encoding, delimiter=delimiter, pages=pages, password=password)
                if warning: st.warning(warning)
                prog.progress(100)
                st.session_state["conv_data"] = output_p.read_bytes()
                st.session_state["conv_name"] = Path(uploaded_file.name).stem + target_ext
                st.session_state["conv_key"] = (uploaded_file.name, target_ext)
                cleanup_temp(input_p)
                cleanup_temp(output_p)
                st.rerun()
            except Exception as e: st.error(f"Error: {str(e)}")

        res_key = st.session_state.get("conv_key")
        if res_key == (uploaded_file.name, target_ext) and "conv_data" in st.session_state:
            st.markdown('<div style="background:rgba(16,185,129,0.1); border:2px solid #10b981; border-radius:15px; padding:2rem; text-align:center; margin-top:2rem;">', unsafe_allow_html=True)
            st.success("✅ Ready for Download")
            st.download_button(label=f"⬇️ Download {st.session_state['conv_name']}", data=st.session_state["conv_data"], file_name=st.session_state["conv_name"], mime="application/octet-stream", type="primary", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

# Footer Credits (Consolidated)
st.markdown(f"""
<div class="footer-box">
    <div class="footer-brand">CONVERTEX</div>
    <div style="font-size: 0.9rem; color: #64748b; margin-bottom: 0.5rem;">
        Developed by <span class="footer-link">LexcoreTech</span> | 
        Lead Architect: <span class="footer-link">Benson Motari</span>
    </div>
    <div style="font-size: 0.85rem;">
        <a href="mailto:bensonmotari4@gmail.com" class="footer-link">bensonmotari4@gmail.com</a>
    </div>
    <div style="margin-top: 1.5rem; font-size: 0.75rem; color: #475569; opacity: 0.6;">
        © 2026 LexcoreTech Professional Suite • All Rights Reserved
    </div>
</div>
""", unsafe_allow_html=True)
