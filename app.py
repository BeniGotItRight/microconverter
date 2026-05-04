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
    page_title="Convertex - Smart Suite",
    page_icon="⚡",
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
    .sb-section { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 1.25rem; margin-bottom: 1.25rem; }
    .sb-label { font-size: 0.7rem; font-weight: 800; color: #10b981; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 0.75rem; display: block; }
    
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
    .banner-title { color: #10b981; font-size: 1.5rem; font-weight: 800; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.75rem; }
    .banner-text { color: #94a3b8; font-size: 1.1rem; line-height: 1.5; }
    .banner-action { color: #34d399; font-weight: 700; margin-top: 1rem; cursor: pointer; }

    /* Cards */
    .info-card { background: #1e293b; border-radius: 20px; padding: 2rem; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 2rem; }
    .footer-box { text-align: center; padding: 4rem 0 2rem; border-top: 1px solid #1e293b; margin-top: 4rem; }
</style>
""", unsafe_allow_html=True)

def show_smart_advice(title, message, advice_type="info"):
    icon = "💡" if advice_type=="info" else "⚠️"
    st.markdown(f"""
    <div class="smart-banner">
        <div class="banner-title">{icon} {title}</div>
        <div class="banner-text">{message}</div>
        <div class="banner-action">Smart Suggestion: Adjust settings in 'Advanced Options' below if issues persist.</div>
    </div>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div style="font-size: 2rem; font-weight: 800; color: #10b981; margin-bottom: 2rem;">CONVERTEX</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-section"><span class="sb-label">01. Category</span>', unsafe_allow_html=True)
    category_list = list(CATEGORIES.keys())
    selected_cat = st.radio("Category", category_list, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sb-section"><span class="sb-label">02. Operation</span>', unsafe_allow_html=True)
    conv_options = CATEGORIES[selected_cat]
    conv_labels = [c[0] for c in conv_options]
    selected_label = st.selectbox("Operation", conv_labels, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); padding: 0.75rem; border-radius: 10px; font-size: 0.75rem; color: #10b981; text-align: center; margin-top: 1rem;">
        🔒 <strong>Privacy First</strong><br>Files are processed locally and never stored.
    </div>
    """, unsafe_allow_html=True)

# Main
st.markdown('<h1 style="color:white; font-size:3rem; font-weight:800; margin-bottom:0;">Convertex</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#64748b; font-size:1.2rem; margin-bottom:2.5rem;">Smart File Engine by LexcoreTech & Benson Motari</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    idx = conv_labels.index(selected_label)
    conv_data = conv_options[idx]
    source_exts, target_ext = conv_data[1], conv_data[2]
    
    # SMART SUGGESTIONS TRIGGER
    if selected_label == "PDF → Excel (Bank Statements)":
        show_smart_advice("Bank Statement Expert", "Processing high-precision tables. If your PDF is password-protected or has multiple statement types, use the <b>Advanced Options</b> to specify pages or passwords.")
    elif "CSV" in selected_label:
        show_smart_advice("CSV Smart Sync", "CSV encoding varies by system. If your Excel looks unorganized after conversion, try changing the <b>Delimiter</b> or <b>Encoding</b> in Advanced Options.")

    # Workspace
    st.markdown(f"### 📤 Upload {selected_cat.split()[-1]}")
    ext_mapping = {".pdf":"pdf", ".docx":"docx", ".txt":"txt", ".pptx":"pptx", ".html":"html", ".htm":"html", ".md":"md", ".rtf":"rtf", ".odt":"odt", ".jpg":"jpg", ".jpeg":"jpeg", ".png":"png", ".webp":"webp", ".bmp":"bmp", ".tiff":"tiff", ".tif":"tiff", ".gif":"gif", ".ico":"ico", ".csv":"csv", ".xlsx":"xlsx", ".xls":"xls", ".json":"json", ".xml":"xml", ".yaml":"yaml", ".yml":"yaml"}
    allowed = [ext_mapping[e] for e in source_exts if e in ext_mapping]
    
    uploaded_file = st.file_uploader("Upload", type=allowed, label_visibility="collapsed")

    # ADVANCED OPTIONS (Always visible but grouped by context)
    st.markdown("### ⚙️ Smart Advanced Options")
    encoding, delimiter, pages, password = None, None, None, None
    
    with st.container():
        # Context-aware Advanced Options
        c1, c2 = st.columns(2)
        with c1:
            if any(e in (".csv", ".json", ".xml", ".yaml") for e in source_exts):
                enc_opt = st.selectbox("Text Encoding", ["auto", "utf-8", "latin-1", "iso-8859-1", "cp1252"], help="Fixes weird characters in data.")
                encoding = None if enc_opt == "auto" else enc_opt
            if ".csv" in source_exts:
                delim_opt = st.selectbox("CSV Delimiter", ["auto", "Comma (,)", "Semicolon (;)", "Tab"], help="Fixes columns not splitting correctly.")
                delim_map = {"auto": None, "Comma (,)": ",", "Semicolon (;)": ";", "Tab": "\t"}
                delimiter = delim_map[delim_opt]
        
        with c2:
            if ".pdf" in source_exts:
                pages_str = st.text_input("Specific Pages", placeholder="e.g. 0,2,5-10", help="Zero-based index. Leave empty for all.")
                if pages_str:
                    try:
                        pages = []
                        for p in pages_str.split(","):
                            if "-" in p:
                                start, end = map(int, p.split("-"))
                                pages.extend(range(start, end + 1))
                            else: pages.append(int(p))
                    except: pages = None
                password = st.text_input("File Password", type="password", help="For protected PDF bank statements.") or None

    if uploaded_file:
        file_ext = Path(uploaded_file.name).suffix.lower()
        st.markdown("### 🚀 Step 2: Convert")
        if st.button(f"Process to {target_ext.upper().strip('.')}", type="primary", use_container_width=True):
            try:
                prog = st.progress(0)
                input_p = create_temp_file(file_ext, delete_on_exit=False)
                input_p.write_bytes(uploaded_file.getvalue())
                output_p = create_temp_file(target_ext, delete_on_exit=False)
                
                prog.progress(50)
                _, warning = convert(input_p, output_p, target_ext, encoding=encoding, delimiter=delimiter, pages=pages, password=password)
                
                if warning: show_smart_advice("Engine Notice", warning, "warning")
                
                prog.progress(100)
                st.session_state["conv_data"] = output_p.read_bytes()
                st.session_state["conv_name"] = Path(uploaded_file.name).stem + target_ext
                st.session_state["conv_key"] = (uploaded_file.name, target_ext)
                
                cleanup_temp(input_p)
                cleanup_temp(output_p)
                st.rerun()
            except Exception as e:
                err_msg = str(e)
                if "No extractable data found" in err_msg:
                    show_smart_advice("Scanned PDF Detected", "This PDF appears to be a scanned image. Convertex works best with digital documents. Suggestion: Use an OCR tool first or try a different statement export.", "warning")
                elif "decode" in err_msg.lower():
                    show_smart_advice("Encoding Conflict", "The file encoding couldn't be detected. Suggestion: Try setting Encoding to 'latin-1' or 'cp1252' in Advanced Options.", "warning")
                else:
                    st.error(f"Error: {err_msg}")

        res_key = st.session_state.get("conv_key")
        if res_key == (uploaded_file.name, target_ext) and "conv_data" in st.session_state:
            st.markdown('<div style="background:rgba(16,185,129,0.1); border:2px solid #10b981; border-radius:15px; padding:2rem; text-align:center; margin-top:1rem;">', unsafe_allow_html=True)
            st.success("✅ Conversion Complete")
            st.download_button(label=f"⬇️ Download {st.session_state['conv_name']}", data=st.session_state["conv_data"], file_name=st.session_state["conv_name"], mime="application/octet-stream", type="primary", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div class="footer-box">
    <div class="footer-brand">CONVERTEX</div>
    <div style="font-size: 0.9rem; color: #64748b; margin-bottom: 0.5rem;">Developed by <span style="color:#10b981; font-weight:600;">LexcoreTech</span> | Lead Architect: <span style="color:#10b981; font-weight:600;">Benson Motari</span></div>
    <div style="font-size: 0.85rem;"><a href="mailto:bensonmotari4@gmail.com" style="color:#10b981; text-decoration:none; font-weight:600;">bensonmotari4@gmail.com</a></div>
</div>
""", unsafe_allow_html=True)
