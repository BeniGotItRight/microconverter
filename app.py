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
        ("PDF → Word", [".pdf"], ".docx", "📝"),
        ("PDF → Text", [".pdf"], ".txt", "📄"),
        ("Word → PDF", [".docx"], ".pdf", "📑"),
        ("Word → Text", [".docx"], ".txt", "📝"),
        ("Text → PDF", [".txt"], ".pdf", "📄"),
        ("PowerPoint → PDF", [".pptx"], ".pdf", "📊"),
        ("Markdown → PDF", [".md"], ".pdf", "📉"),
        ("Markdown → HTML", [".md"], ".html", "🌐"),
        ("HTML → PDF", [".html", ".htm"], ".pdf", "🌍"),
        ("RTF → PDF", [".rtf"], ".pdf", "🖋️"),
        ("ODT → PDF", [".odt"], ".pdf", "📂"),
    ],
    "📊 Data & Statements": [
        ("PDF → Excel (Bank)", [".pdf"], ".xlsx", "🏦"),
        ("CSV → Excel", [".csv"], ".xlsx", "📉"),
        ("CSV → PDF", [".csv"], ".pdf", "📄"),
        ("Excel → CSV", [".xlsx", ".xls"], ".csv", "📁"),
        ("Excel → PDF", [".xlsx", ".xls"], ".pdf", "📑"),
        ("JSON → Excel", [".json"], ".xlsx", "📦"),
        ("JSON → CSV", [".json"], ".csv", "📁"),
        ("JSON → PDF", [".json"], ".pdf", "📄"),
        ("JSON → YAML", [".json"], ".yaml", "📜"),
        ("XML → Excel", [".xml"], ".xlsx", "🗄️"),
        ("XML → CSV", [".xml"], ".csv", "📁"),
        ("XML → JSON", [".xml"], ".json", "📦"),
        ("YAML → Excel", [".yaml", ".yml"], ".xlsx", "📉"),
        ("YAML → JSON", [".yaml", ".yml"], ".json", "📦"),
    ],
    "🖼️ Images": [
        ("JPG → PNG", [".jpg", ".jpeg"], ".png", "📸"),
        ("PNG → JPG", [".png"], ".jpg", "🖼️"),
        ("Any → WebP", [".jpg", ".jpeg", ".png", ".bmp", ".tiff"], ".webp", "🌐"),
        ("WebP → PNG/JPG", [".webp"], ".png", "🖼️"),
        ("Image → PDF", [".jpg", ".jpeg", ".png", ".webp", ".bmp"], ".pdf", "📄"),
        ("Any → BMP/TIFF", [".jpg", ".png", ".webp"], ".bmp", "🖼️"),
        ("GIF → PNG/JPG", [".gif"], ".png", "🎞️"),
        ("PNG → ICO", [".png"], ".ico", "🎯"),
    ]
}

CONVERSION_INFO = {
    "PDF → Word": {"description": "Transform non-editable PDF documents into fully editable Microsoft Word files.", "tip": "Best for text-based PDFs."},
    "PDF → Excel (Bank)": {"description": "High-precision extraction of tables from PDF bank statements into Excel.", "tip": "Optimized for M-Pesa and Bank reports."},
    "CSV → Excel": {"description": "Convert raw CSV data into clean, professionally formatted Excel workbooks.", "tip": "Auto-sizes columns and detects encoding."},
    "Any → WebP": {"description": "Convert images to WebP for superior compression and faster web loading.", "tip": "Smallest file size with zero quality loss."},
}

# Page config
st.set_page_config(page_title="Convertex - Premium Suite", page_icon="⚡", layout="wide")

# Advanced UI Styling
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    html, body, [data-testid="stAppViewContainer"] { font-family: 'Plus Jakarta Sans', sans-serif !important; background-color: #0b0f1a !important; }
    
    /* Operation Cards */
    .op-card {
        background: #1e293b;
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(255,255,255,0.05);
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .op-card:hover {
        background: rgba(16, 185, 129, 0.1);
        border-color: #10b981;
        transform: translateY(-5px);
    }
    .op-icon { font-size: 2.5rem; margin-bottom: 0.75rem; }
    .op-label { font-weight: 700; font-size: 1rem; color: white; }
    .op-ext { font-size: 0.75rem; color: #64748b; margin-top: 0.25rem; }
    
    /* Selected Card */
    .op-card-selected {
        background: rgba(16, 185, 129, 0.15) !important;
        border: 2px solid #10b981 !important;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.2);
    }

    /* Sidebar Section */
    [data-testid="stSidebar"] { background: #0f172a !important; }
    .sb-section { background: rgba(255,255,255,0.03); border-radius: 12px; padding: 1rem; margin-bottom: 1rem; border: 1px solid rgba(255,255,255,0.05); }
    .sb-title { font-size: 0.7rem; font-weight: 700; color: #10b981; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem; }

    /* Buttons */
    .stButton > button { border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div style="font-size: 1.75rem; font-weight: 800; color: #10b981; margin-bottom: 1rem;">CONVERTEX</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-title">Active Suite</div>', unsafe_allow_html=True)
    category_list = list(CATEGORIES.keys())
    selected_cat = st.radio("Category", category_list, label_visibility="collapsed")
    
    st.markdown('<div class="sb-title">Platform Status</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-section">● Engine: Online<br>● Security: Local Only<br>● Version: 2.1.0</div>', unsafe_allow_html=True)

# Main Area
st.markdown(f'<h1 style="color:white; font-size: 2.5rem; letter-spacing:-0.04em;">{selected_cat}</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#64748b; font-size:1.1rem; margin-bottom:2rem;">Select an operation below to begin processing your files.</p>', unsafe_allow_html=True)

# Operation Grid
ops = CATEGORIES[selected_cat]
cols = st.columns(4)

# Use session state to track selection
if "selected_op_idx" not in st.session_state or st.session_state.get("last_cat") != selected_cat:
    st.session_state["selected_op_idx"] = 0
    st.session_state["last_cat"] = selected_cat

for i, (label, src, target, icon) in enumerate(ops):
    with cols[i % 4]:
        is_selected = (st.session_state["selected_op_idx"] == i)
        # We use a button to handle clicks, but style the container
        card_class = "op-card op-card-selected" if is_selected else "op-card"
        st.markdown(f"""
        <div class="{card_class}">
            <div class="op-icon">{icon}</div>
            <div class="op-label">{label}</div>
            <div class="op-ext">{", ".join(src).upper()} → {target.upper()}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Select {label}", key=f"btn_{i}", use_container_width=True, label_visibility="collapsed"):
            st.session_state["selected_op_idx"] = i
            st.rerun()

# Workspace for Selected Operation
st.markdown("---")
selected_op = ops[st.session_state["selected_op_idx"]]
label, source_exts, target_ext, icon = selected_op

col_l, col_r = st.columns([2, 3])

with col_l:
    info = CONVERSION_INFO.get(label, {"description": "Professional high-precision conversion.", "tip": "Optimized for speed and accuracy."})
    st.markdown(f"""
    <div style="background:#1e293b; padding:2rem; border-radius:20px; border:1px solid #10b981;">
        <h2 style="color:#10b981; margin-top:0;">{icon} {label}</h2>
        <p style="color:#94a3b8;">{info['description']}</p>
        <div style="background:rgba(0,0,0,0.2); padding:1rem; border-radius:12px; font-size:0.9rem; border-left:3px solid #10b981;">
            <strong>Pro Tip:</strong> {info['tip']}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_r:
    st.markdown("### 📤 Step 1: Upload")
    ext_mapping = {".pdf":"pdf", ".docx":"docx", ".txt":"txt", ".pptx":"pptx", ".html":"html", ".htm":"html", ".md":"md", ".rtf":"rtf", ".odt":"odt", ".jpg":"jpg", ".jpeg":"jpeg", ".png":"png", ".webp":"webp", ".bmp":"bmp", ".tiff":"tiff", ".tif":"tiff", ".gif":"gif", ".ico":"ico", ".csv":"csv", ".xlsx":"xlsx", ".xls":"xls", ".json":"json", ".xml":"xml", ".yaml":"yaml", ".yml":"yaml"}
    allowed = [ext_mapping[e] for e in source_exts if e in ext_mapping]
    uploaded_file = st.file_uploader("Upload", type=allowed, label_visibility="collapsed")

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
                _, warning = convert(input_p, output_p, target_ext)
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
            st.markdown('<div style="background:rgba(16,185,129,0.1); border:1px solid #10b981; border-radius:15px; padding:1.5rem; text-align:center; margin-top:1rem;">', unsafe_allow_html=True)
            st.success("✅ Ready for Download")
            st.download_button(label=f"⬇️ Download {st.session_state['conv_name']}", data=st.session_state["conv_data"], file_name=st.session_state["conv_name"], mime="application/octet-stream", type="primary", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div style="text-align:center; padding:4rem 0; border-top:1px solid #1e293b; margin-top:4rem;">
    <div style="font-size:1.25rem; font-weight:800; color:#10b981; margin-bottom:0.5rem;">CONVERTEX</div>
    <div style="font-size:0.85rem; color:#64748b;">Developed by <strong>LexcoreTech</strong> | Lead Architect: <strong>Benson Motari</strong></div>
    <div style="font-size:0.8rem; color:#475569; margin-top:0.25rem;"><a href="mailto:bensonmotari4@gmail.com" style="color:#10b981; text-decoration:none;">bensonmotari4@gmail.com</a></div>
</div>
""", unsafe_allow_html=True)
