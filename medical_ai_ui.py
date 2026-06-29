import streamlit as st

st.set_page_config(layout="wide", page_title="AI Mammogram", page_icon="◐")

# ----------------------------------------------------------------------------
# Session State Configuration
# ----------------------------------------------------------------------------
if "help" not in st.session_state:
    st.session_state.help = False
if "lang" not in st.session_state:
    st.session_state.lang = "EN"  # Default language is English
if "view_titans" not in st.session_state:
    st.session_state.view_titans = False

# ----------------------------------------------------------------------------
# Localization Dictionary (EN / AR)
# ----------------------------------------------------------------------------
loc = {
    "EN": {
        "title": "AI-Powered Mammogram Analysis<br>for <span class='accent'>Early Breast Cancer Classification</span>",
        "sub": "A decision-support assistant that helps healthcare professionals review mammogram images and flag patterns worth a closer look. Built to support clinical judgment, never to replace it.",
        "badge": "Decision support only — final diagnosis remains with the physician",
        "begin_btn": "Begin Analysis",
        "help_btn": "Help",
        "back_btn": "← Back",
        "titans_btn": "⚙️ Engineering Titans",
        "titans_title": "Project Team & Creators",
        "ref_title": "Reference",
        "about_title": "About this system",
        "dir": "ltr",
        "align": "left",
        "roles": {
            "supervisor1": "Supervisor: Dr. Wisam Haider",
            "supervisor2": "Supervisor: M.Sc. Maha Abbas",
            "leader": "Team Leader: Atmanan Karim",
            "researcher": "Researcher: Fatima Abdul-Monem",
            "designer": "Designer: Saja Mehdi",
            "programmer": "Programmer: Maryam Muhammad",
            "ai_dev": "AI Engineer & Developer: Hussein Jameel"
        }
    },
    "AR": {
        "title": "تحليل صور الماموجرام بالذكاء الاصطناعي<br>لـ <span class='accent'>التصنيف المبكر لسرطان الثدي</span>",
        "sub": "مساعد لدعم اتخاذ القرار يساعد المتخصصين في الرعاية الصحية على مراجعة صور الماموجرام وتحديد الأنماط التي تستحق نظرة فاحصة. تم بناؤه لدعم الحكم السريري الطبي، وليس لاستبداله أبداً.",
        "badge": "لدعم القرار فقط — التشخيص النهائي يبقى من اختصاص الطبيب",
        "begin_btn": "بدء التحليل",
        "help_btn": "المساعدة",
        "back_btn": "→ العودة",
        "titans_btn": "⚙️ عمالقة الهندسة (Titans)",
        "titans_title": "فريق العمل ومطوري المشروع",
        "ref_title": "المراجع",
        "about_title": "حول هذا النظام",
        "dir": "rtl",
        "align": "right",
        "roles": {
            "supervisor1": "المشرف: د. وسام حيدر",
            "supervisor2": "المشرفة: م.م. مها عباس",
            "leader": "قائد الفريق (الليدر): اطمئنان كريم",
            "researcher": "الباحثة: فاطمة عبدالمنعم",
            "designer": "المصممة: سجى مهدي",
            "programmer": "المبرمجة: مريم محمد",
            "ai_dev": "مطور الذكاء الاصطناعي والبرمجيات: حسين جميل"
        }
    }
}

current_loc = loc[st.session_state.lang]

# ----------------------------------------------------------------------------
# CSS Customization with New Design Tokens (Navy + Indigo + Pink Touch)
# ----------------------------------------------------------------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:wght@500;600&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&family=Cairo:wght@400;600;700&display=swap');

:root {{
  --bg: #F4F7F9;
  --ink: #111E2C;
  --muted: #526375;
  --navy: #0F2537;
  --teal: #1D5659;
  --indigo: #2A4365; 
  --pink: #E68EA5;   
  --pink-light: #FDF2F5;
  --card: #FFFFFF;
  --border: #DDE4E9;
}}

html, body, .stApp {{
  background: var(--bg);
  font-family: { "'Cairo', sans-serif" if st.session_state.lang == "AR" else "'Inter', sans-serif" };
  color: var(--ink);
  direction: {current_loc['dir']};
  text-align: {current_loc['align']};
}}
.block-container {{ padding-top: 1.2rem; }}

/* ---- Top Header Bar ---- */
.mark-row {{
  display: flex;
  align-items: center;
  gap: 12px;
}}
.mark {{
  width: 40px; height: 40px; border-radius: 10px;
  background: linear-gradient(135deg, var(--navy), var(--indigo));
  color: #fff; font-family: 'Lora', serif; font-weight: 600; font-size: 18px;
  display: flex; align-items: center; justify-content: center;
  border-bottom: 3px solid var(--pink);
}}
.mark-label {{
  font-family: 'IBM Plex Mono', monospace; font-size: 13px; letter-spacing: 1px;
  color: var(--muted); text-transform: uppercase;
}}

/* ---- Custom Top Buttons ---- */
div[data-testid="column"] .stButton>button {{
  background: var(--card) !important;
  color: var(--navy) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  font-size: 14px !important;
  padding: 6px 14px !important;
  font-family: inherit !important;
}}
div[data-testid="column"] .stButton>button:hover {{
  border-color: var(--pink) !important;
  color: var(--pink) !important;
}}

/* ---- Hero Section ---- */
.hero {{
  position: relative;
  text-align: center;
  padding: 50px 16px 20px 16px;
  overflow: hidden;
}}
.title {{
  font-family: 'Lora', serif;
  font-weight: 600;
  color: var(--navy);
  font-size: 38px;
  line-height: 1.3;
  max-width: 850px;
  margin: 0 auto;
}}
.title .accent {{ color: var(--indigo); border-bottom: 2px dashed var(--pink); }}

.sub {{
  color: var(--muted);
  font-size: 16.5px;
  line-height: 1.7;
  max-width: 720px;
  margin: 20px auto 0 auto;
  text-align: center; /* تضمن توسيط العبارة تماماً */
}}

.badge {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin: 25px auto 0 auto;
  padding: 8px 18px;
  border: 1px solid var(--pink);
  background: var(--pink-light);
  color: var(--navy);
  border-radius: 30px;
  font-size: 13px;
}}

/* ---- Main CTA Button (Indigo) ---- */
div.stButton>button.cta-btn {{
  display: block;
  margin: 30px auto 10px auto;
  background: var(--indigo) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 10px !important;
  font-weight: 600 !important;
  font-size: 18px !important;
  padding: 12px 50px !important;
  box-shadow: 0 6px 20px rgba(42, 67, 101, 0.25) !important;
  transition: all 0.2s ease;
}}
div.stButton>button.cta-btn:hover {{
  background: var(--navy) !important;
  border-top: 2px solid var(--pink) !important;
  box-shadow: 0 8px 25px rgba(42, 67, 101, 0.35) !important;
}}

/* ---- Cards Layout ---- */
.card {{
  background: var(--card);
  padding: 20px 22px;
  border-radius: 12px;
  margin-bottom: 16px;
  border: 1px solid var(--border);
  border-top: 4px solid var(--indigo); /* الافتراضي نيلي لجميع البطاقات وحسين جميل */
  box-shadow: 0 3px 12px rgba(0,0,0,0.03);
}}
.card.pink-accent {{ 
  border-top-color: var(--pink) !important; /* خاص بالمشرفين فقط باللون الوردي */
}}
.card h3 {{
  font-weight: 600;
  font-size: 17px;
  color: var(--navy);
  margin: 0 0 10px 0;
}}
.card p {{
  color: var(--muted);
  font-size: 14.5px;
  line-height: 1.6;
  margin: 0;
}}

footer, header {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Header Actions (Language, Help, Titans Toggle)
# ----------------------------------------------------------------------------
top_cols = st.columns([4, 2, 2, 2, 2]) if st.session_state.lang == "EN" else st.columns([2, 2, 2, 2, 4])

# Define order based on language direction
if st.session_state.lang == "EN":
    with top_cols[0]:
        st.markdown('<div class="mark-row"><div class="mark">MX</div><span class="mark-label">MAMMOGRAM AI</span></div>', unsafe_allow_html=True)
    with top_cols[1]:
        if st.button(current_loc["titans_btn"], key="titans_toggle"):
            st.session_state.view_titans = not st.session_state.view_titans
            st.session_state.help = False
    with top_cols[2]:
        lbl = current_loc["back_btn"] if st.session_state.help else current_loc["help_btn"]
        if st.button(lbl, key="help_toggle"):
            st.session_state.help = not st.session_state.help
            st.session_state.view_titans = False
    with top_cols[4]:
        lang_label = "العربية 🇸🇦" if st.session_state.lang == "EN" else "English 🇬🇧"
        if st.button(lang_label, key="lang_toggle"):
            st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"
            st.rerun()
else:
    with top_cols[0]:
        lang_label = "English 🇬🇧" if st.session_state.lang == "AR" else "العربية 🇸🇦"
        if st.button(lang_label, key="lang_toggle"):
            st.session_state.lang = "EN" if st.session_state.lang == "AR" else "AR"
            st.rerun()
    with top_cols[2]:
        lbl = current_loc["back_btn"] if st.session_state.help else current_loc["help_btn"]
        if st.button(lbl, key="help_toggle"):
            st.session_state.help = not st.session_state.help
            st.session_state.view_titans = False
    with top_cols[3]:
        if st.button(current_loc["titans_btn"], key="titans_toggle"):
            st.session_state.view_titans = not st.session_state.view_titans
            st.session_state.help = False
    with top_cols[4]:
        st.markdown('<div class="mark-row"><div class="mark">MX</div><span class="mark-label">ذكاء الماموجرام</span></div>', unsafe_allow_html=True)

st.markdown("<hr style='margin:10px 0; border:0; border-top:1px solid var(--border);'>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# View 1: Engineering Titans Section (فريق العمل)
# ----------------------------------------------------------------------------
if st.session_state.view_titans:
    st.markdown(f"""
    <div class="help-header">
        <div class="help-eyebrow">TITANS ENGINE</div>
        <div class="help-title">{current_loc['titans_title']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Grid System for Team Members
    c_t1, c_t2 = st.columns(2)
    
    with c_t1:
        st.markdown(f"""
        <div class="card pink-accent">
            <h3>🩺 {current_loc['roles']['supervisor1']}</h3>
            <p>Supervision, clinical validation guidance and medical track evaluation.</p>
        </div>
        <div class="card">
            <h3>👑 {current_loc['roles']['leader']}</h3>
            <p>Project coordination, lifecycle management and sprint execution lead.</p>
        </div>
        <div class="card">
            <h3>🎨 {current_loc['roles']['designer']}</h3>
            <p>UI/UX Architect, aesthetics controller, design tokens and assets designer.</p>
        </div>
        <div class="card">
            <h3>✨ {current_loc['roles']['ai_dev']}</h3>
            <p>AI Infrastructure, model training architecture, core engine deployment and system refinement.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c_t2:
        st.markdown(f"""
        <div class="card pink-accent">
            <h3>🔬 {current_loc['roles']['supervisor2']}</h3>
            <p>Co-Supervision, engineering review, and technical research verification.</p>
        </div>
        <div class="card">
            <h3>📊 {current_loc['roles']['researcher']}</h3>
            <p>Data science research, preprocessing pipelines, CBIS-DDSM dataset analysis.</p>
        </div>
        <div class="card">
            <h3>💻 {current_loc['roles']['programmer']}</h3>
            <p>Backend systems software development, integration scripts and logic testing.</p>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# View 2: Reference / Help View
# ----------------------------------------------------------------------------
elif st.session_state.help:
    st.markdown(f"""
    <div class="help-header">
        <div class="help-eyebrow">{current_loc['ref_title']}</div>
        <div class="help-title">{current_loc['about_title']}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.lang == "EN":
        sections = [
            ("🩺", "Project Overview", "Supports physicians by classifying mammogram images to assist with early breast cancer detection.", ""),
            ("📊", "Datasets", "Trained, tested, and evaluated using CBIS-DDSM combined with hospital-sourced mammogram images.", ""),
            ("🧠", "AI Model", "A convolutional network built with TensorFlow/Keras, using custom Conv2D, Dense, and MaxPool structures.", ""),
            ("⚙️", "Training", "Image size 50×50 · 25 epochs · batch size 75 · Adam optimizer · binary cross-entropy loss.", "pink-accent"),
            ("💻", "Technologies", "Python · Streamlit · TensorFlow · Keras · OpenCV · NumPy · Pandas · Pillow.", ""),
            ("🚀", "Workflow", "Upload image → preprocessing → AI prediction → result → doctor clinical verification.", ""),
        ]
    else:
        sections = [
            ("🩺", "نظرة عامة على المشروع", "يدعم الأطباء من خلال تصنيف صور الماموجرام للمساعدة في الكشف المبكر عن سرطان الثدي.", ""),
            ("📊", "مجموعات البيانات", "تم التدريب والاختبار والتقييم باستخدام مجموعة بيانات CBIS-DDSM مدمجة مع صور مستشفيات حقيقية.", ""),
            ("🧠", "نموذج الذكاء الاصطناعي", "شبكة عصبية تلافيفية مبنية بـ TensorFlow و Keras، باستخدام طبقات تلافيفية، كثيفة، و MaxPool مخصصة.", ""),
            ("⚙️", "معاملات التدريب", "حجم الصورة 50×50 · 25 حقبة (Epochs) · حجم الدفعة 75 · محسن Adam · دالة خسارة الإنتروبيا المتقاطعة الثنائية.", "pink-accent"),
            ("💻", "التقنيات المستخدمة", "Python · Streamlit · TensorFlow · Keras · OpenCV · NumPy · Pandas · Pillow.", ""),
            ("🚀", "خطوات العمل", "رفع الصورة ← المعالجة المسبقة ← تنبؤ النموذج الكاشف ← ظهور النتيجة ← المراجعة والاعتماد الطبي.", ""),
        ]

    for i in range(0, len(sections), 2):
        cols = st.columns(2)
        for col, (icon, title, body, kind) in zip(cols, sections[i:i + 2]):
            with col:
                cls = f"card {kind}".strip()
                st.markdown(f"<div class='{cls}'><h3>{icon} {title}</h3><p>{body}</p></div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# View 3: Default Hero View
# ----------------------------------------------------------------------------
else:
    st.markdown(f"""
    <div class="hero">
        <div class="title">{current_loc['title']}</div>
        <p class="sub">{current_loc['sub']}</p>
        <div class="badge">🎀 {current_loc['badge']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Centered CTA Trigger using the custom styling 'cta-btn'
    _, mid, _ = st.columns([4, 3, 4])
    with mid:
        if st.button(current_loc["begin_btn"], key="begin_analysis_main", type="primary"):
            st.toast("Redirecting to Analysis Engine...", icon="🚀")
