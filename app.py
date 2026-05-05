"""
Convertex - Hamo & Associates
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
        ("PDF → XML (Bank Statements)", [".pdf"], ".xml"),
        ("PDF → JSON", [".pdf"], ".json"),
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
    "PDF → XML (Bank Statements)": {"description": "Standardized XML export for financial data. Extracts account info, summaries, and transactions into audit-ready schemas.", "use_cases": ["Automated Audits", "Tax Preparation", "ERP Integration"], "tip": "Next-Gen HAAS Intelligence logic."},
    "Word → PDF": {"description": "Convert Word documents to professional PDF files for universal viewing.", "use_cases": ["Resumes", "Official Letters"], "tip": "Preserves basic layout and tables."},
    "CSV → Excel": {"description": "Convert raw CSV data into clean, professionally formatted Excel workbooks.", "use_cases": ["Data Cleaning", "System Exports"], "tip": "Auto-sizes columns and detects encoding."},
}

# Page config
st.set_page_config(
    page_title="Convertex - Hamo & Associates",
    page_icon="assets/hamo_logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Comprehensive UI Styling
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    html, body, [data-testid="stAppViewContainer"] { 
        font-family: 'Plus Jakarta Sans', sans-serif !important; 
        background-color: #0b0f1a !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #020617 100%) !important;
    }
    [data-testid="stSidebar"] [data-testid="stImage"] {
        background: #ffffff;
        border-radius: 14px;
        padding: 0.75rem 1rem;
        margin: 0 auto 1.5rem auto;
        box-shadow: 0 4px 16px rgba(0,0,0,0.25);
    }
    .sb-section { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 1.25rem; margin-bottom: 1.25rem; }
    .sb-label { font-size: 0.7rem; font-weight: 800; color: #10b981; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 0.75rem; display: block; }
    .sb-feature { font-size: 0.85rem; color: #94a3b8; display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.4rem; }

    /* Smart Advice Banner */
    .smart-banner {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #10b981;
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.15);
        animation: slideDown 0.5s ease-out;
    }
    @keyframes slideDown { from { transform: translateY(-20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
    .banner-title { color: #10b981; font-size: 1.5rem; font-weight: 800; margin-bottom: 0.5rem; }
    .banner-text { color: #94a3b8; font-size: 1.1rem; line-height: 1.5; }
    .advice-btn {
        display: inline-block;
        margin-top: 1rem;
        padding: 0.5rem 1.25rem;
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
        border: 1px solid #10b981;
        border-radius: 50px;
        text-decoration: none;
        font-weight: 700;
        font-size: 0.85rem;
        transition: background 0.2s ease;
    }
    .advice-btn:hover { background: rgba(16, 185, 129, 0.2); }

    /* Hero & Client Header */
    .hero-box {
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #064e3b 0%, #0d9468 50%, #10b981 100%);
        border-radius: 24px;
        margin-bottom: 2.5rem;
        text-align: center;
        box-shadow: 0 20px 40px rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(255,255,255,0.08);
    }
    .hero-title { font-size: 3.5rem; font-weight: 800; color: white; letter-spacing: -0.04em; margin-bottom: 0.5rem; }
    .haas-linking {
        font-size: 0.9rem;
        font-weight: 700;
        color: #064e3b;
        background: #6ee7b7;
        padding: 0.6rem 1.5rem;
        border-radius: 50px;
        display: inline-block;
        margin-top: 1.5rem;
        box-shadow: 0 4px 15px rgba(110, 231, 183, 0.3);
    }
    .logo-container {
        background: #ffffff;
        padding: 1.25rem 2.5rem;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 2rem;
        box-shadow: 0 12px 40px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #0b0f1a; }
    ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #10b981; }

    /* Workspace Card */
    .workspace-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 2.5rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-top: 1rem;
    }
    
    /* Animations */
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
        70% { transform: scale(1.05); box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    .pulse-badge {
        animation: pulse 2s infinite;
        display: inline-block;
        background: #064e3b;
        color: white;
        padding: 2px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 0.05em;
    }

    /* Button Glow */
    .stButton > button[kind="primary"] {
        border-radius: 12px !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em;
        transition: all 0.3s ease !important;
        border: none !important;
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.4) !important;
        transform: translateY(-2px);
    }
    
    /* Expander styling */
    [data-testid="stExpander"] {
        border-radius: 12px;
        border-color: rgba(255,255,255,0.08) !important;
        background: rgba(255,255,255,0.01) !important;
    }
    /* Footer */
    .footer-box { text-align: center; padding: 4rem 0 2rem; border-top: 1px solid #1e293b; margin-top: 4rem; }
</style>
""", unsafe_allow_html=True)

def show_smart_advice(title, message, advice_type="info"):
    icon = "💡" if advice_type=="info" else "⚠️"
    st.markdown(f"""
    <div class="smart-banner">
        <div class="banner-title">{icon} {title}</div>
        <div class="banner-text">{message}</div>
        <a href="#comprehensive-guide" class="advice-btn">📖 View Full Guide & Advice</a>
    </div>
    """, unsafe_allow_html=True)

# Sidebar with Logo
with st.sidebar:
    logo_path = Path("assets/hamo_logo.png")
    if logo_path.exists():
        # Using a standard professional width for sidebar logos
        st.image(str(logo_path), width=150)
    else:
        st.markdown('<div style="font-size: 1.5rem; font-weight: 800; color: #10b981; margin-bottom: 1.5rem; text-align:center;">HAMO & ASSOCIATES</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sb-section"><span class="sb-label">01. Workflow Category</span>', unsafe_allow_html=True)
    category_list = list(CATEGORIES.keys())
    selected_cat = st.radio("Category", category_list, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sb-section"><span class="sb-label">02. Specific Operation</span>', unsafe_allow_html=True)
    conv_options = CATEGORIES[selected_cat]
    conv_labels = [c[0] for c in conv_options]
    selected_label = st.selectbox("Operation", conv_labels, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("📝 QUICK START GUIDE", expanded=False):
        st.markdown('<div class="sb-feature">1️⃣ Choose your format group</div>', unsafe_allow_html=True)
        st.markdown('<div class="sb-feature">2️⃣ Select the target format</div>', unsafe_allow_html=True)
        st.markdown('<div class="sb-feature">3️⃣ Drop your file and convert</div>', unsafe_allow_html=True)
        st.markdown('<div class="sb-feature">4️⃣ Download instant result</div>', unsafe_allow_html=True)

    with st.expander("🎯 EXPERT INSIGHTS", expanded=False):
        st.markdown('<div class="sb-feature">🏦 <b>Bank Expert:</b> Use PDF→Excel for statements.</div>', unsafe_allow_html=True)
        st.markdown('<div class="sb-feature">🏗️ <b>Data:</b> JSON→Excel flattens complex data.</div>', unsafe_allow_html=True)
        st.markdown('<div class="sb-feature">🚀 <b>Speed:</b> WebP is best for website images.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); padding: 0.75rem; border-radius: 10px; font-size: 0.75rem; color: #10b981; text-align: center; margin-top: 1.5rem;">
        🛡️ <strong>Encrypted Session</strong><br>LexcoreTech military-grade security.
    </div>
    """, unsafe_allow_html=True)

# Main Hero Header
st.markdown('<div class="hero-box">', unsafe_allow_html=True)
st.markdown('<div style="font-size: 1rem; font-weight: 700; color: #d1fae5; text-transform: uppercase; letter-spacing: 0.2em; margin-bottom: 1rem;">Hamo & Associates Professional Suite</div>', unsafe_allow_html=True)

st.markdown("""
    <div class="hero-title">Convertex</div>
    <div style="color:rgba(255,255,255,0.9); font-size:1.3rem; font-weight:600; letter-spacing: 0.01em;">Enterprise-Grade File Transformation Suite</div>
    <div class="haas-linking">
        <span style="display: flex; align-items: center; gap: 0.5rem; justify-content: center;">
            <span class="pulse-badge">UPCOMING</span>
            HAAS Financial Intelligence Hub
        </span>
        <div style="font-size:0.8rem; opacity:0.8; font-weight:500; margin-top: 4px;">Autonomous Audit-Ready Workflows & Predictive Tax Analytics Engine.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Workspace
col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    if selected_label == "PDF → Excel (Bank Statements)":
        show_smart_advice("Statement Specialist", "Bank PDFs are structured as tables. If columns are merged, use <b>Advanced Options</b> below.")
    elif "CSV" in selected_label:
        show_smart_advice("Data Normalizer", "CSV encoding depends on the system. Adjust <b>Delimiter</b> or <b>Encoding</b> if the result looks messy.")
    elif "WebP" in selected_label:
        show_smart_advice("Image Optimizer", "WebP is the best format for web speed. It saves 80% space without losing quality.")

    # Workspace logic
    idx = conv_labels.index(selected_label)
    conv_data = conv_options[idx]
    source_exts, target_ext = conv_data[1], conv_data[2]
    
    # Workspace Card
    st.markdown('<div class="workspace-card">', unsafe_allow_html=True)
    
    st.markdown(f"### 📤 Upload {selected_cat.split()[-1]}")
    ext_mapping = {".pdf":"pdf", ".docx":"docx", ".txt":"txt", ".pptx":"pptx", ".html":"html", ".htm":"html", ".md":"md", ".rtf":"rtf", ".odt":"odt", ".jpg":"jpg", ".jpeg":"jpeg", ".png":"png", ".webp":"webp", ".bmp":"bmp", ".tiff":"tiff", ".tif":"tiff", ".gif":"gif", ".ico":"ico", ".csv":"csv", ".xlsx":"xlsx", ".xls":"xls", ".json":"json", ".xml":"xml", ".yaml":"yaml", ".yml":"yaml"}
    allowed = [ext_mapping[e] for e in source_exts if e in ext_mapping]
    uploaded_file = st.file_uploader("Upload", type=allowed, label_visibility="collapsed")

    # Advanced Options
    encoding, delimiter, pages, password = None, None, None, None
    with st.expander("⚙️ SMART ADVANCED OPTIONS", expanded=False):
        st.info("Use these to fix issues like messy columns, weird symbols, or encrypted PDFs.")
        c1, c2 = st.columns(2)
        with c1:
            if any(e in (".csv", ".json", ".xml", ".yaml") for e in source_exts):
                encoding = st.selectbox("Text Encoding", ["auto", "utf-8", "latin-1", "cp1252"])
                encoding = None if encoding == "auto" else encoding
            if ".csv" in source_exts:
                delimiter = st.selectbox("Delimiter", ["auto", ",", ";", "\\t"])
                delimiter = None if delimiter == "auto" else delimiter
        with c2:
            if ".pdf" in source_exts:
                p_str = st.text_input("Specific Pages", placeholder="e.g. 0,1")
                if p_str:
                    try: pages = [int(p.strip()) for p in p_str.split(",")]
                    except: pages = None
                password = st.text_input("File Password", type="password") or None

    if uploaded_file:
        file_ext = Path(uploaded_file.name).suffix.lower()
        st.markdown("### 🚀 Step 2: Convert")
        if st.button(f"Process to {target_ext.upper().strip('.')}", type="primary", use_container_width=True):
            try:
                prog = st.progress(0)
                input_p = create_temp_file(file_ext, delete_on_exit=False)
                input_p.write_bytes(uploaded_file.getvalue())
                output_p = create_temp_file(target_ext, delete_on_exit=False)
                prog.progress(60)
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
            st.markdown('<div style="background:rgba(16,185,129,0.1); border:2px solid #10b981; border-radius:15px; padding:2rem; text-align:center; margin-top:1rem;">', unsafe_allow_html=True)
            st.success("✅ Conversion Complete")
            st.download_button(label=f"⬇️ Download {st.session_state['conv_name']}", data=st.session_state["conv_data"], file_name=st.session_state["conv_name"], mime="application/octet-stream", type="primary", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True) # End Workspace Card

    # Guide
    st.markdown('<div id="comprehensive-guide" style="margin-top:6rem;"></div>', unsafe_allow_html=True)
    with st.expander("📖 COMPREHENSIVE FORMAT GUIDE & ADVICE", expanded=False):
        st.markdown("""
        ### 🧐 When to use which format?
        #### **1. Documents**
        *   **PDF:** Final contracts and invoices. Professional and universal.
        *   **Word (.docx):** Collaborative drafts and text editing.
        *   **Markdown (.md):** Technical documentation and READMEs.
        
        #### **2. Data & Statements**
        *   **Excel (.xlsx):** Data analysis, charts, and calculations.
        *   **CSV:** Universal data exchange between software.
        *   **JSON:** Developer integrations and web data.
        
        #### **3. Images**
        *   **WebP:** Best for websites. Tiny file size, high quality.
        *   **PNG:** Logos/Icons with transparency.
        *   **JPG:** High-quality photographs.
        
        ### 🛠 How Convertex helps you?
        1.  **Privacy:** LexcoreTech Military-grade local silos ensure your files never leak.
        2.  **Accuracy:** Smart Engine fixes broken data formats and table structures automatically.
        3.  **Freedom:** Unlimited conversions with zero subscriptions.
        4.  **Troubleshooting (Advanced Options):** Use these to fix "difficult" files manually. It puts the power in your hands.
        """)

# Footer
st.markdown(f"""
<div class="footer-box">
    <div class="footer-brand">CONVERTEX</div>
    <div style="font-size: 0.9rem; color: #64748b; margin-bottom: 0.5rem;">Developed by <span style="color:#10b981; font-weight:600;">LexcoreTech</span> | Lead Architect: <span style="color:#10b981; font-weight:600;">Benson Motari</span></div>
    <div style="font-size: 0.85rem;"><a href="mailto:bensonmotari4@gmail.com" style="color:#10b981; text-decoration:none; font-weight:600;">bensonmotari4@gmail.com</a></div>
</div>
""", unsafe_allow_html=True)
