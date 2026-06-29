import streamlit as st

st.set_page_config(layout="wide", page_title="AI Mammogram", page_icon="◐")

# ----------------------------------------------------------------------------
# Session State
# ----------------------------------------------------------------------------
if "help" not in st.session_state:
    st.session_state.help = False
if "lang" not in st.session_state:
    st.session_state.lang = "EN"
if "view_titans" not in st.session_state:
    st.session_state.view_titans = False

# ----------------------------------------------------------------------------
# Localization
# ----------------------------------------------------------------------------
loc = {
    "EN": {
        "title": "AI-Powered Mammogram Analysis",
        "title_accent": "Early Breast Cancer Classification",
        "sub": "A decision-support assistant that helps healthcare professionals review mammogram images and flag patterns worth a closer look. Built to support clinical judgment, never to replace it.",
        "badge": "Decision support only — final diagnosis remains with the physician",
        "begin_btn": "Begin Analysis →",
        "help_btn": "Help",
        "back_btn": "← Back",
        "titans_btn": "⚙ Team",
        "titans_title": "Project Team & Creators",
        "about_title": "About this System",
        "dir": "ltr",
        "roles": {
            "supervisor1": "Asst.Prof. Dr. Wisam Hayder Mahdi",
            "supervisor1_role": "Supervisor",
            "supervisor2": "Asst.Prof. Maha A. Hutaihitt",
            "supervisor2_role": "Co-Supervisor",
            "leader": "Atmanan Kareem",
            "leader_role": "Team Leader",
            "researcher": "Fatima Abdul-Monem",
            "researcher_role": "Researcher",
            "designer": "Saja Mehdi",
            "designer_role": "UI/UX Designer",
            "programmer": "Maryam Muhammad",
            "programmer_role": "Programmer",
            "ai_dev": "Hussein Jameel",
            "ai_dev_role": "AI Engineer & Developer"
        },
        "stats": [
            ("CBIS-DDSM", "Dataset"),
            ("50×50px", "Input Size"),
            ("25", "Epochs"),
            ("Adam", "Optimizer"),
        ],
        "help_sections": [
            ("🩺", "Project Overview", "Supports physicians by classifying mammogram images to assist with early breast cancer detection.", False),
            ("📊", "Datasets", "Trained, tested, and evaluated using CBIS-DDSM combined with hospital-sourced mammogram images.", False),
            ("🧠", "AI Model", "A convolutional network built with TensorFlow/Keras, using custom Conv2D, Dense, and MaxPool structures.", True),
            ("⚙", "Training Config", "Image 50×50 · 25 epochs · batch 75 · Adam optimizer · binary cross-entropy loss.", False),
            ("💻", "Technologies", "Python · Streamlit · TensorFlow · Keras · OpenCV · NumPy · Pandas · Pillow", False),
            ("🚀", "Workflow", "Upload → Preprocess → Predict → Display Result → Clinical Verification", True),
        ]
    },
    "AR": {
        "title": "تحليل صور الماموجرام بالذكاء الاصطناعي",
        "title_accent": "التصنيف المبكر لسرطان الثدي",
        "sub": "مساعد لدعم اتخاذ القرار يساعد المتخصصين في الرعاية الصحية على مراجعة صور الماموجرام وتحديد الأنماط التي تستحق نظرة فاحصة. تم بناؤه لدعم الحكم السريري الطبي، وليس لاستبداله أبداً.",
        "badge": "لدعم القرار فقط — التشخيص النهائي يبقى من اختصاص الطبيب",
        "begin_btn": "← بدء التحليل",
        "help_btn": "المساعدة",
        "back_btn": "العودة →",
        "titans_btn": "⚙ الفريق",
        "titans_title": "فريق العمل ومطوري المشروع",
        "about_title": "حول هذا النظام",
        "dir": "rtl",
        "roles": {
            "supervisor1": "ا.م.د. وسام حيدر مهدي",
            "supervisor1_role": "المشرف",
            "supervisor2": "ا.م. مهاي عباس حطيحط",
            "supervisor2_role": "المشرفة",
            "leader": "اطمئنان كريم",
            "leader_role": "قائد الفريق",
            "researcher": "فاطمة عبدالمنعم",
            "researcher_role": "الباحثة",
            "designer": "سجى مهدي",
            "designer_role": "المصممة",
            "programmer": "مريم محمد",
            "programmer_role": "المبرمجة",
            "ai_dev": "حسين جميل",
            "ai_dev_role": "مطور الذكاء الاصطناعي"
        },
        "stats": [
            ("CBIS-DDSM", "قاعدة البيانات"),
            ("50×50px", "حجم الإدخال"),
            ("25", "حقبة تدريب"),
            ("Adam", "المحسِّن"),
        ],
        "help_sections": [
            ("🩺", "نظرة عامة", "يدعم الأطباء من خلال تصنيف صور الماموجرام للمساعدة في الكشف المبكر عن سرطان الثدي.", False),
            ("📊", "مجموعات البيانات", "تم التدريب والاختبار باستخدام CBIS-DDSM مدمجة مع صور مستشفيات حقيقية.", False),
            ("🧠", "نموذج الذكاء الاصطناعي", "شبكة عصبية تلافيفية مبنية بـ TensorFlow و Keras، بطبقات تلافيفية وكثيفة و MaxPool.", True),
            ("⚙", "معاملات التدريب", "حجم الصورة 50×50 · 25 حقبة · دفعة 75 · محسن Adam · دالة الإنتروبيا المتقاطعة الثنائية.", False),
            ("💻", "التقنيات", "Python · Streamlit · TensorFlow · Keras · OpenCV · NumPy · Pandas · Pillow", False),
            ("🚀", "خطوات العمل", "رفع الصورة ← معالجة ← تنبؤ ← نتيجة ← مراجعة طبية", True),
        ]
    }
}

C = loc[st.session_state.lang]
is_ar = st.session_state.lang == "AR"
font_main = "'Cairo', sans-serif" if is_ar else "'Inter', sans-serif"
font_display = "'Cairo', sans-serif" if is_ar else "'Lora', serif"

# ─── CSS ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:wght@500;700&family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&family=Cairo:wght@400;600;700;900&display=swap');

/* ── TOKENS ── */
:root {{
  --bg:          #4A5568;   /* رصاصي متوسط — الخلفية الأساسية */
  --bg-deep:     #2D3748;   
  --indigo-navy: #1A365D;   /* اللون النيلي الفخم للكتابة */
  --indigo-light:#2A4365;   
  --bg-card:     #FFFFFF;   /* كروت بيضاء تماماً بناءً على طلبك */
  --border:      rgba(255,255,255,0.12);
  --steel:       #CBD5E0;   /* نص رصاصي فاتح للبيانات الفرعية الهير */
  --white:       #F7FAFC;   
  --pink:        #E89BB0;
  --pink-soft:   #F3C6D4;
  --pink-glow:   rgba(232,155,176,0.18);
  --pink-border: rgba(232,155,176,0.40);
  --r-sm: 8px; --r-md: 14px; --r-lg: 22px;
  --t: 0.25s cubic-bezier(0.4,0,0.2,1);
}}

*, *::before, *::after {{ box-sizing: border-box; }}
footer, header {{ visibility: hidden !important; }}

/* ── BASE ── */
html, body, .stApp {{
  background: var(--bg) !important;
  font-family: {font_main};
  color: var(--white);
  direction: {C['dir']};
}}

.block-container {{
  max-width: 1160px !important;
  padding: 1.2rem 2rem 4rem !important;
  position: relative;
}}

/* ══════════════════════════════════════
   ANIMATED BACKGROUND — الدوائر والشبكة المتحركة
══════════════════════════════════════ */
.bg-canvas {{
  position: fixed;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}}

.orb {{
  position: absolute;
  border-radius: 50%;
  filter: blur(90px);
  opacity: 0.25;
}}

.orb-1 {{
  width: 550px; height: 550px;
  background: radial-gradient(circle, #718096, transparent 70%);
  top: -100px; left: -100px;
  animation: drift1 20s ease-in-out infinite alternate;
}}

.orb-2 {{
  width: 400px; height: 400px;
  background: radial-gradient(circle, var(--pink), transparent 70%);
  bottom: 12%; right: -60px;
  opacity: 0.16;
  animation: drift2 24s ease-in-out infinite alternate;
}}

.orb-3 {{
  width: 320px; height: 320px;
  background: radial-gradient(circle, #A0AEC0, transparent 70%);
  top: 40%; left: 35%;
  opacity: 0.15;
  animation: drift3 16s ease-in-out infinite alternate;
}}

@keyframes drift1 {{
  0%   {{ transform: translate(0px, 0px) scale(1); }}
  50%  {{ transform: translate(70px, 50px) scale(1.05); }}
  100% {{ transform: translate(-20px, 80px) scale(0.95); }}
}}
@keyframes drift2 {{
  0%   {{ transform: translate(0px, 0px) scale(1); }}
  60%  {{ transform: translate(-40px, -50px) scale(1.1); }}
  100% {{ transform: translate(30px, 40px) scale(0.9); }}
}}
@keyframes drift3 {{
  0%   {{ transform: translate(0px, 0px); }}
  100% {{ transform: translate(-50px, -40px) scale(1.05); }}
}}

.grid-lines {{
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 65px 65px;
  pointer-events: none;
  z-index: 0;
  animation: gridFade 5s ease-in-out infinite alternate;
}}
@keyframes gridFade {{ 0% {{ opacity: 0.4; }} 100% {{ opacity: 0.8; }} }}

/* ══════════════════════════════════════
   TOPBAR & HEADER BUTTONS (بيضاء ونصوص نيلي)
══════════════════════════════════════ */
.topbar {{
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 14px;
  position: relative;
  z-index: 10;
}}

.brand-mark {{
  width: 42px; height: 42px;
  border-radius: 11px;
  background: var(--bg-deep);
  border: 1.5px solid var(--pink-border);
  display: flex; align-items: center; justify-content: center;
  font-family: 'Lora', serif; font-weight: 700; font-size: 15px;
  color: var(--white);
  box-shadow: 0 0 18px var(--pink-glow);
  position: relative;
  overflow: hidden;
}}
.brand-mark::after {{
  content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 2.5px;
  background: linear-gradient(90deg, var(--pink), var(--pink-soft));
}}

.brand-label {{
  font-family: 'IBM Plex Mono', monospace;
  font-size: 11px; letter-spacing: 2.5px;
  color: #E2E8F0; text-transform: uppercase;
}}

/* تعديل أزرار التحكم العلوي: خلفية بيضاء ونصوص نيلي */
div[data-testid="column"] .stButton > button {{
  background: #FFFFFF !important;
  color: var(--indigo-navy) !important;
  border: 1px solid #FFFFFF !important;
  border-radius: var(--r-sm) !important;
  font-size: 13px !important; font-weight: 600 !important;
  padding: 7px 16px !important;
  font-family: {font_main} !important;
  transition: var(--t) !important;
  box-shadow: 0 2px 10px rgba(0,0,0,0.15) !important;
}}
div[data-testid="column"] .stButton > button:hover {{
  background: var(--pink-soft) !important;
  border-color: var(--pink) !important;
  color: var(--indigo-navy) !important;
  transform: translateY(-1px) !important;
}}

.hr-line {{
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--border), var(--pink-border), var(--border), transparent);
  margin: 4px 0 20px;
}}

/* ══════════════════════════════════════
   HERO & MAIN CTA (زر بدء التحليل أبيض بنيلي)
══════════════════════════════════════ */
.hero {{ text-align: center; padding: 40px 20px 20px; position: relative; z-index: 5; }}
.hero-eyebrow {{
  display: inline-flex; align-items: center; gap: 8px;
  font-family: 'IBM Plex Mono', monospace; font-size: 11px; letter-spacing: 3px;
  color: var(--pink); padding: 6px 18px; border: 1px solid var(--pink-border);
  border-radius: 30px; background: var(--pink-glow); margin-bottom: 22px;
}}
.hero-eyebrow .dot {{ width: 6px; height: 6px; border-radius: 50%; background: var(--pink); }}

.hero-title {{ font-family: {font_display}; font-size: clamp(26px, 4vw, 44px); font-weight: 700; color: var(--white); line-height: 1.25; max-width: 820px; margin: 0 auto 10px; }}
.hero-accent {{
  display: block;
  background: linear-gradient(120deg, var(--pink) 0%, var(--pink-soft) 55%, #fff 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-top: 6px;
}}
.hero-sub {{ color: #E2E8F0; font-size: 16px; line-height: 1.8; max-width: 650px; margin: 18px auto 0; }}
.badge-wrap {{ display:flex; justify-content:center; margin-top:26px; }}
.badge {{ display:inline-flex; align-items:center; gap:10px; padding: 10px 22px; border: 1px solid var(--border); background: var(--bg-deep); border-radius: 40px; font-size: 13px; color: #E2E8F0; }}

/* Stats */
.stats-row {{ display: flex; max-width: 660px; margin: 35px auto 0; border: 1px solid var(--border); border-radius: var(--r-md); overflow: hidden; position: relative; z-index: 5; }}
.stat-item {{ flex: 1; padding: 16px 14px; text-align: center; background: var(--bg-deep); border-right: 1px solid var(--border); }}
.stat-item:last-child {{ border-right: none; }}
.stat-val {{ font-family: 'IBM Plex Mono', monospace; font-size: 17px; font-weight: 600; color: var(--white); }}
.stat-lbl {{ font-size: 11px; color: var(--steel); margin-top: 4px; text-transform: uppercase; }}

/* زر بدء التحليل الرئيسي: أبيض بالكامل ونصوص نيلي */
.cta-col .stButton > button {{
  background: #FFFFFF !important;
  color: var(--indigo-navy) !important;
  border: none !important;
  border-radius: 50px !important;
  font-size: 16px !important; font-weight: 700 !important;
  padding: 14px 36px !important;
  box-shadow: 0 8px 25px rgba(0,0,0,0.2) !important;
  transition: all 0.25s ease !important;
  font-family: {font_main} !important;
}}
.cta-col .stButton > button:hover {{
  background: var(--pink-soft) !important;
  color: var(--indigo-navy) !important;
  transform: translateY(-3px) scale(1.02) !important;
  box-shadow: 0 12px 35px rgba(0,0,0,0.3) !important;
}}

/* ══════════════════════════════════════
   SECTION HEADER
══════════════════════════════════════ */
.sec-head {{ text-align: center; margin: 30px 0 25px; position: relative; z-index: 5; }}
.sec-title {{ font-family: {font_display}; font-size: 28px; font-weight: 700; color: var(--white); margin-bottom: 6px; }}
.sec-sub {{ font-size: 14px; color: #E2E8F0; }}

/* ══════════════════════════════════════
   لوحة الفريق وموديول المساعدة: كروت بيضاء وكتابة نيلي
══════════════════════════════════════ */
.mcard {{
  background: var(--bg-card) !important; /* خلفية بيضاء */
  border: 1px solid #E2E8F0;
  border-top: 4px solid var(--indigo-light) !important; /* خط علوي نيلي */
  border-radius: var(--r-md);
  padding: 24px 22px;
  margin-bottom: 16px;
  transition: var(--t);
  position: relative; z-index: 5;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}}
.mcard.pink {{ border-top-color: var(--pink) !important; }} /* المشرفين بخط وردي مميز */

.mcard:hover {{
  transform: translateY(-4px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}}

/* نصوص الكروت: نيلي داكن وواضح */
.mcard-icon {{ font-size: 24px; display: block; margin-bottom: 10px; }}
.mcard-role {{ font-family: 'IBM Plex Mono', monospace; font-size: 11px; font-weight:600; letter-spacing: 1.5px; text-transform: uppercase; color: var(--pink); margin-bottom: 6px; }}
.mcard-name {{ font-size: 17px; font-weight: 700; color: var(--indigo-navy) !important; margin-bottom: 8px; }}
.mcard-body {{ font-size: 14px; line-height: 1.6; color: #4A5568 !important; }}

/* Scrollbar */
::-webkit-scrollbar {{ width: 6px; }}
::-webkit-scrollbar-track {{ background: var(--bg-deep); }}
::-webkit-scrollbar-thumb {{ background: #718096; border-radius: 3px; }}
</style>

<div class="bg-canvas">
  <div class="grid-lines"></div>
  <div class="orb orb-1"></div>
  <div class="orb orb-2"></div>
  <div class="orb orb-3"></div>
</div>
""", unsafe_allow_html=True)

# ─── TOPBAR ─────────────────────────────────────────────────────────────────
brand_label_text = "MAMMOGRAM AI" if not is_ar else "ذكاء الماموجرام"

if not is_ar:
    c0, c1, c2, _, c4 = st.columns([4, 1.4, 1.4, 1, 1.5])
    with c0:
        st.markdown(f'<div class="topbar"><div class="brand-mark">MA</div><span class="brand-label">{brand_label_text}</span></div>', unsafe_allow_html=True)
    with c1:
        if st.button(C["titans_btn"], key="titans_toggle"):
            st.session_state.view_titans = not st.session_state.view_titans
            st.session_state.help = False
    with c2:
        lbl = C["back_btn"] if (st.session_state.help or st.session_state.view_titans) else C["help_btn"]
        if st.button(lbl, key="help_toggle"):
            st.session_state.help = not st.session_state.help
            st.session_state.view_titans = False
    with c4:
        if st.button("العربية 🇸🇦", key="lang_toggle"):
            st.session_state.lang = "AR"; st.rerun()
else:
    c0, _, c2, c3, c4 = st.columns([1.5, 1, 1.4, 1.4, 4])
    with c0:
        if st.button("English 🇬🇧", key="lang_toggle"):
            st.session_state.lang = "EN"; st.rerun()
    with c2:
        lbl = C["back_btn"] if (st.session_state.help or st.session_state.view_titans) else C["help_btn"]
        if st.button(lbl, key="help_toggle"):
            st.session_state.help = not st.session_state.help
            st.session_state.view_titans = False
    with c3:
        if st.button(C["titans_btn"], key="titans_toggle"):
            st.session_state.view_titans = not st.session_state.view_titans
            st.session_state.help = False
    with c4:
        st.markdown(f'<div class="topbar" style="justify-content:flex-end"><span class="brand-label">{brand_label_text}</span><div class="brand-mark">MA</div></div>', unsafe_allow_html=True)

st.markdown('<div class="hr-line"></div>', unsafe_allow_html=True)

# ─── VIEW 1: TEAM (كروت بيضاء وكتابة نيلي) ───────────────────────────────────
if st.session_state.view_titans:
    sub_txt = "The people behind the intelligence" if not is_ar else "الفريق الهندسي المطور للنظام"
    st.markdown(f'<div class="sec-head"><div class="sec-title">{C["titans_title"]}</div><div class="sec-sub">{sub_txt}</div></div>', unsafe_allow_html=True)

    r = C["roles"]
    left_cards = [
        ("🩺", r["supervisor1_role"], r["supervisor1"], "Supervision, clinical validation guidance and medical track evaluation.", True),
        ("👑", r["leader_role"], r["leader"], "Project coordination, lifecycle management and sprint execution lead.", False),
        ("🎨", r["designer_role"], r["designer"], "UI/UX architecture, design tokens, aesthetics, and visual assets.", False),
        ("✨", r["ai_dev_role"], r["ai_dev"], "AI infrastructure, model training, core engine deployment and system refinement.", False),
    ]
    right_cards = [
        ("🔬", r["supervisor2_role"], r["supervisor2"], "Co-supervision, engineering review, and technical research verification.", True),
        ("📊", r["researcher_role"], r["researcher"], "Data science research, preprocessing pipelines, CBIS-DDSM dataset analysis.", False),
        ("💻", r["programmer_role"], r["programmer"], "Backend systems development, integration scripts and logic testing.", False),
    ]

    col_l, col_r = st.columns(2, gap="medium")
    with col_l:
        for icon, role, name, body, is_pink in left_cards:
            st.markdown(f"""
            <div class="mcard {'pink' if is_pink else ''}">
              <span class="mcard-icon">{icon}</span>
              <div class="mcard-role">{role}</div>
              <div class="mcard-name">{name}</div>
              <div class="mcard-body">{body}</div>
            </div>""", unsafe_allow_html=True)
    with col_r:
        for icon, role, name, body, is_pink in right_cards:
            st.markdown(f"""
            <div class="mcard {'pink' if is_pink else ''}">
              <span class="mcard-icon">{icon}</span>
              <div class="mcard-role">{role}</div>
              <div class="mcard-name">{name}</div>
              <div class="mcard-body">{body}</div>
            </div>""", unsafe_allow_html=True)

# ─── VIEW 2: HELP (كروت بيضاء وكتابة نيلي) ───────────────────────────────────
elif st.session_state.help:
    sub_txt = "System architecture, datasets, and clinical workflow" if not is_ar else "معمارية النظام، قواعد البيانات، وسير العمل السريري"
    st.markdown(f'<div class="sec-head"><div class="sec-title">{C["about_title"]}</div><div class="sec-sub">{sub_txt}</div></div>', unsafe_allow_html=True)

    sections = C["help_sections"]
    for i in range(0, len(sections), 2):
        pair = sections[i:i+2]
        cols = st.columns(len(pair), gap="medium")
        for col, (icon, title, body, is_pink) in zip(cols, pair):
            with col:
                module_lbl = "Module" if not is_ar else "وحدة"
                st.markdown(f"""
                <div class="mcard {'pink' if is_pink else ''}">
                  <span class="mcard-icon">{icon}</span>
                  <div class="mcard-role">{module_lbl}</div>
                  <div class="mcard-name">{title}</div>
                  <div class="mcard-body">{body}</div>
                </div>""", unsafe_allow_html=True)

# ─── VIEW 3: HERO ────────────────────────────────────────────────────────────
else:
    eyebrow = "Clinical AI · Mammography" if not is_ar else "ذكاء اصطناعي سريري · الماموجرام"
    st.markdown(f"""
    <div class="hero">
      <div class="hero-eyebrow"><span class="dot"></span>{eyebrow}</div>
      <div class="hero-title">
        {C['title']}
        <span class="hero-accent">{C['title_accent']}</span>
      </div>
      <p class="hero-sub">{C['sub']}</p>
      <div class="badge-wrap"><div class="badge">🎀 {C['badge']}</div></div>
    </div>
    """, unsafe_allow_html=True)

    stats_html = '<div class="stats-row">' + "".join(
        f'<div class="stat-item"><div class="stat-val">{v}</div><div class="stat-lbl">{l}</div></div>'
        for v, l in C["stats"]
    ) + '</div>'
    st.markdown(stats_html, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # تقسيم الأعمدة بالتناظر الهندسي لوضع الزر في المنتصف الفيت تماماً
    _, mid, _ = st.columns([1.3, 1, 1.3])
    with mid:
        st.markdown('<div class="cta-col">', unsafe_allow_html=True)
        if st.button(C["begin_btn"], key="begin_analysis_main", use_container_width=True):
            st.toast("Redirecting to Analysis Engine...", icon="🚀")
        st.markdown('</div>', unsafe_allow_html=True)
