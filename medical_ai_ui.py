import streamlit as st

st.set_page_config(layout="wide", page_title="AI Mammogram", page_icon="◐")

if "help" not in st.session_state:
    st.session_state.help = False

# ----------------------------------------------------------------------------
# Design tokens
#   Display face : Lora (serif)      -> clinical authority, used for headline only
#   Body face    : Inter (sans)      -> everything readable
#   Data face    : IBM Plex Mono     -> technical specs (model, training params)
#   Palette      : deep navy + clinical teal on a cool off-white field,
#                  warm terracotta reserved for the single call-to-action
# ----------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:wght@500;600&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root{
  --bg:#F5F8FA;
  --ink:#16263A;
  --muted:#5B6B7B;
  --navy:#163A5C;
  --teal:#2E6B6E;
  --warm:#C2723F;
  --card:#FFFFFF;
  --border:#E2E8EC;
}

html, body, .stApp{
  background:var(--bg);
  font-family:'Inter',sans-serif;
  color:var(--ink);
}
.block-container{padding-top:1.2rem;}

/* ---- header bar ---- */
.topbar{
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:6px 4px 0 4px;
}
.mark{
  width:38px;height:38px;border-radius:9px;
  background:linear-gradient(160deg,var(--navy),var(--teal));
  color:#fff;font-family:'Lora',serif;font-weight:600;font-size:16px;
  display:flex;align-items:center;justify-content:center;
  letter-spacing:.5px;
}
.mark-label{
  font-family:'IBM Plex Mono',monospace;font-size:12px;letter-spacing:1.5px;
  color:var(--muted);text-transform:uppercase;margin-left:10px;
}
.mark-row{display:flex;align-items:center;}

div[data-testid="column"] .stButton>button{
  background:transparent !important;
  color:var(--navy) !important;
  border:1px solid var(--border) !important;
  border-radius:10px !important;
  font-size:15px !important;
  padding:6px 14px !important;
  margin:0 !important;
  box-shadow:none !important;
  font-family:'Inter',sans-serif !important;
}
div[data-testid="column"] .stButton>button:hover{
  border-color:var(--teal) !important;
  color:var(--teal) !important;
}

/* ---- hero ---- */
.hero{
  position:relative;
  text-align:center;
  padding:64px 16px 8px 16px;
  overflow:hidden;
}
.scan-rings{
  position:absolute;
  top:-40px; left:50%;
  transform:translateX(-50%);
  width:520px; height:520px;
  z-index:0;
  opacity:.55;
}
.scan-rings circle{
  fill:none;
  stroke:var(--teal);
  stroke-dasharray:4 7;
}
@keyframes spin-slow{ from{transform:rotate(0deg);} to{transform:rotate(360deg);} }
.scan-rings .r1{animation:spin-slow 60s linear infinite;}
.scan-rings .r2{animation:spin-slow 90s linear infinite reverse;}
@media (prefers-reduced-motion:reduce){
  .scan-rings .r1, .scan-rings .r2{animation:none;}
}

.title{
  position:relative; z-index:1;
  font-family:'Lora',serif;
  font-weight:600;
  color:var(--navy);
  font-size:40px;
  line-height:1.28;
  max-width:780px;
  margin:0 auto;
}
.title .accent{color:var(--teal);}

.sub{
  position:relative; z-index:1;
  color:var(--muted);
  font-size:17px;
  line-height:1.6;
  max-width:620px;
  margin:18px auto 0 auto;
}

.badge{
  position:relative; z-index:1;
  display:inline-flex;
  align-items:center;
  gap:8px;
  margin:22px auto 0 auto;
  padding:7px 16px;
  border:1px solid #E6CDB8;
  background:#FBF3EC;
  color:var(--warm);
  border-radius:30px;
  font-family:'IBM Plex Mono',monospace;
  font-size:12.5px;
  letter-spacing:.3px;
}
.badge::before{content:"●";font-size:8px;}

/* ---- CTA ---- */
div.stButton>button{
  display:block;
  margin:38px auto 10px auto;
  background:var(--warm);
  color:#fff;
  border:none;
  border-radius:10px;
  font-family:'Inter',sans-serif;
  font-weight:600;
  font-size:17px;
  padding:13px 42px;
  letter-spacing:.2px;
  box-shadow:0 6px 16px rgba(194,114,63,.28);
  transition:transform .15s ease, box-shadow .15s ease;
}
div.stButton>button:hover{
  transform:translateY(-1px);
  box-shadow:0 8px 20px rgba(194,114,63,.36);
  color:#fff;
}

/* ---- help page ---- */
.help-header{
  text-align:center;
  margin:18px 0 30px 0;
}
.help-eyebrow{
  font-family:'IBM Plex Mono',monospace;
  font-size:12.5px;
  letter-spacing:2px;
  color:var(--teal);
  text-transform:uppercase;
}
.help-title{
  font-family:'Lora',serif;
  font-weight:600;
  font-size:32px;
  color:var(--navy);
  margin-top:6px;
}

.card{
  background:var(--card);
  padding:22px 24px;
  border-radius:12px;
  margin:0 0 18px 0;
  border:1px solid var(--border);
  border-top:3px solid var(--teal);
  box-shadow:0 2px 10px rgba(22,38,58,.05);
  height:100%;
}
.card h3{
  font-family:'Inter',sans-serif;
  font-weight:600;
  font-size:16.5px;
  color:var(--navy);
  margin:0 0 8px 0;
}
.card p{
  color:var(--muted);
  font-size:14.5px;
  line-height:1.55;
  margin:0;
}
.card.spec p, .card.spec code{
  font-family:'IBM Plex Mono',monospace;
  font-size:13px;
}
.card.warn{border-top-color:var(--warm);}
.card.warn h3{color:var(--warm);}

footer, header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
c1, c2 = st.columns([10, 1])
with c1:
    st.markdown(
        '<div class="mark-row"><div class="mark">MX</div>'
        '<span class="mark-label">Mammogram Analysis</span></div>',
        unsafe_allow_html=True,
    )
with c2:
    label = "← Back" if st.session_state.help else "Help"
    if st.button(label, key="help_toggle"):
        st.session_state.help = not st.session_state.help

# ----------------------------------------------------------------------------
# Main view
# ----------------------------------------------------------------------------
if not st.session_state.help:
    st.markdown("""
    <div class="hero">
        <svg class="scan-rings" viewBox="0 0 520 520">
            <circle class="r1" cx="260" cy="260" r="230"/>
            <circle class="r2" cx="260" cy="260" r="170"/>
            <circle cx="260" cy="260" r="110" stroke-dasharray="2 5" opacity=".6"/>
        </svg>
        <div class="title">AI-Powered Mammogram Analysis<br>for <span class="accent">Early Breast Cancer Classification</span></div>
        <p class="sub">A decision-support assistant that helps healthcare professionals review mammogram images and flag patterns worth a closer look. Built to support clinical judgment, never to replace it.</p>
        <div class="badge">Decision support only — final diagnosis remains with the physician</div>
    </div>
    """, unsafe_allow_html=True)

    _, mid, _ = st.columns([4, 2, 4])
    with mid:
        st.button("Begin Analysis")

else:
    st.markdown("""
    <div class="help-header">
        <div class="help-eyebrow">Reference</div>
        <div class="help-title">About this system</div>
    </div>
    """, unsafe_allow_html=True)

    sections = [
        ("🩺", "Project overview", "Supports physicians by classifying mammogram images to assist with early breast cancer detection.", ""),
        ("📊", "Datasets", "Trained, tested, and evaluated using CBIS-DDSM combined with hospital-sourced mammogram images.", ""),
        ("🧠", "AI model", "A convolutional neural network built with TensorFlow and Keras, using convolution, ReLU, max-pooling, dense, and softmax layers.", ""),
        ("⚙️", "Training", "Image size 50×50 · 25 epochs · batch size 75 · Adam optimizer · binary cross-entropy loss.", "spec"),
        ("💻", "Technologies", "Python · Streamlit · TensorFlow · Keras · OpenCV · NumPy · Pandas · Pillow · OpenPyXL.", "spec"),
        ("🚀", "Workflow", "Upload image → preprocessing → AI prediction → result → doctor review.", ""),
        ("⚠️", "Disclaimer", "This tool assists healthcare professionals and does not replace medical diagnosis.", "warn"),
    ]

    for i in range(0, len(sections), 2):
        cols = st.columns(2)
        for col, (icon, title, body, kind) in zip(cols, sections[i:i + 2]):
            with col:
                cls = f"card {kind}".strip()
                st.markdown(
                    f"<div class='{cls}'><h3>{icon} {title}</h3><p>{body}</p></div>",
                    unsafe_allow_html=True,
                )
