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
            ("Online", "Dataset"),
            ("Baqubah Hospital", "Dataset"),
        ],
        "help_sections": [
            ("🩺", "Project Overview", "Supports physicians by classifying mammogram images to assist with early breast cancer detection.", False),
            ("📊", "Datasets", "Trained, tested, and evaluated using Online dataset combined with hospital-sourced mammogram images.", False),
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
            "supervisor2": "ا.م. مها عباس حطيحط",
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
            ("الإنترنت (Online)", "بيانات"),
            ("مستشفى بعقوبة", "بيانات"),
        ],
        "help_sections": [
            ("🩺", "نظرة عامة", "يدعم الأطباء من خلال تصنيف صور الماموجرام للمساعدة في الكشف المبكر عن سرطان الثدي.", False),
            ("📊", "مجموعات البيانات", "تم التدريب والاختبار باستخدام بيانات الإنترنت مدمجة مع صور مستشفيات حقيقية.", False),
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
  --bg:          #4A5568;   /* رصاصي ثابت ومضمون للخلفية */
  --bg-deep:     #2D3748;   
  --indigo-navy: #1A365D;   /* اللون النيلي المطلوب للكتابة */
  --indigo-dark: #0A192F;
  --bg-card:     #FFFFFF;   /* خلفية الكروت بيضاء بالكامل */
  --border:      rgba(255,255,255,0.12);
  --steel:       #CBD5E0;   
  --white:       #F7FAFC;   
  --pink:        #E89BB0;   /* اللون الوردي لزر بدء التحليل */
  --pink-soft:   #F3C6D4;
  --pink-glow:   rgba(232,155,176,0.18);
  --pink-border: rgba(232,155,176,0.40);
  --r-sm: 8px; --r-md: 14px;
  --t: 0.2s ease-in-out;
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
}}

/* خلفية رصاصية تفاعلية */
.bg-canvas {{
  position: fixed;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}}
.orb {{ position: absolute; border-radius: 50%; filter: blur(90px); opacity: 0.2; }}
.orb-1 {{ width: 500px; height: 500px; background: radial-gradient(circle, #718096, transparent 70%); top: -50px; left: -50px; }}
.orb-2 {{ width: 400px; height: 400px; background: radial-gradient(circle, var(--pink), transparent 70%); bottom: 10%; right: -50px; }}
.grid-lines {{
  position: fixed; inset: 0;
  background-image: linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
  background-size: 60px 60px; pointer-events: none; z-index: 0;
}}

/* ══════════════════════════════════════
   أزرار التحكم العلوية الإلزامية (خلفية بيضاء خط نيلي ثابت)
══════════════════════════════════════ */
.topbar {{
  display: flex; align-items: center; gap: 12px; padding-bottom: 14px; position: relative; z-index: 10;
}}
.brand-mark {{
  width: 42px; height: 42px; border-radius: 11px; background: var(--bg-deep); border: 1.5px solid var(--pink-border);
  display: flex; align-items: center; justify-content: center; font-family: 'Lora', serif; font-weight: 700; font-size: 15px; color: var(--white);
}}
.brand-label {{ font-family: 'IBM Plex Mono', monospace; font-size: 11px; letter-spacing: 2.5px; color: #E2E8F0; }}

/* استهداف مباشر وقوي لجميع أزرار التحكم العلوية لحل مشكلة النص الأبيض */
div[data-testid="column"] button[kind="secondary"] {{
  background-color: #FFFFFF !important;
  color: var(--indigo-navy) !important;
  border: 1px solid #FFFFFF !important;
  border-radius: var(--r-sm) !important;
  font-size: 14px !important;
  font-weight: 700 !important;
  padding: 8px 18px !important;
  font-family: {font_main} !important;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
  opacity: 1 !important;
}}

/* حالة الحركية عند تمرير الماوس للأزرار العلوية */
div[data-testid="column"] button[kind="secondary"]:hover,
div[data-testid="column"] button[kind="secondary"]:focus,
div[data-testid="column"] button[kind="secondary"]:active {{
  background-color: #E2E8F0 !important;
  color: var(--indigo-dark) !important;
  border-color: #E2E8F0 !important;
  box-shadow: 0 6px 15px rgba(0,0,0,0.2) !important;
}}

.hr-line {{
  height: 1px; background: linear-gradient(90deg, transparent, var(--border), var(--pink-border), var(--border), transparent); margin: 4px 0 20px;
}}

/* ══════════════════════════════════════
   زر بدء التحليل (خلفية وردية خط أبيض ثابت)
══════════════════════════════════════ */
.cta-col button {{
  background-color: var(--pink) !important;
  color: #FFFFFF !important;
  border: 2px solid var(--pink) !important;
  border-radius: 50px !important;
  font-size: 16px !important;
  font-weight: 700 !important;
  padding: 14px 42px !important;
  font-family: {font_main} !important;
  box-shadow: 0 6px 22px rgba(232,155,176,0.4) !important;
  display: block !important;
  width: 100% !important;
  opacity: 1 !important;
}}

.cta-col button:hover, .cta-col button:focus, .cta-col button:active {{
  background-color: var(--pink-soft) !important;
  color: var(--indigo-navy) !important;
  border-color: var(--pink-soft) !important;
  box-shadow: 0 8px 28px rgba(232,155,176,0.6) !important;
  transform: translateY(-2px);
}}

/* ══════════════════════════════════════
   HERO & STATS
══════════════════════════════════════ */
.hero {{ text-align: center; padding: 30px 20px 10px; position: relative; z-index: 5; }}
.hero-title {{ font-family: {font_display}; font-size: clamp(26px, 4vw, 44px); font-weight: 700; color: var(--white); line-height: 1.25; }}
.hero-accent {{ display: block; background: linear-gradient(120deg, var(--pink) 0%, var(--pink-soft) 55%, #fff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
.hero-sub {{ color: #E2E8F0; font-size: 16px; line-height: 1.8; max-width: 650px; margin: 18px auto 0; }}
.badge-wrap {{ display:flex; justify-content:center; margin-top:22px; }}
.badge {{ display:inline-flex; align-items:center; gap:10px; padding: 10px 22px; border: 1px solid var(--border); background: var(--bg-deep); border-radius: 40px; font-size: 13px; }}

.stats-row {{ display: flex; max-width: 480px; margin: 35px auto 0; border: 1px solid var(--border); border-radius: 14px; overflow: hidden; position: relative; z-index: 5; }}
.stat-item {{ flex: 1; padding: 16px 14px; text-align: center; background: var(--bg-deep); border-right: 1px solid var(--border); }}
.stat-item:last-child {{ border-right: none; }}
.stat-val {{ font-size: 16px; font-weight: 700; color: var(--white); }}
.stat-lbl {{ font-size: 11px; color: var(--steel); margin-top: 4px; }}

/* لوحة الفريق */
.sec-head {{ text-align: center; margin: 30px 0 25px; position: relative; z-index: 5; }}
.sec-title {{ font-family: {font_display}; font-size: 28px; font-weight: 700; color: var(--white); }}
.sec-sub {{ font-size: 14px; color: #E2E8F0; }}

.mcard {{
  background: var(--bg-card) !important; border: 1px solid #E2E8F0; border-top: 4px solid var(--indigo-light) !important;
  border-radius: 14px; padding: 24px 22px; margin-bottom: 16px; position: relative; z-index: 5; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}}
.mcard.pink {{ border-top-color: var(--pink) !important; }}
.mcard-icon {{ font-size: 24px; display: block; margin-bottom: 10px; }}
.mcard-role {{ font-family: 'IBM Plex Mono', monospace; font-size: 11px; font-weight:600; color: var(--pink); margin-bottom: 6px; }}
.mcard-name {{ font-size: 17px; font-weight: 700; color: var(--indigo-navy) !important; margin-bottom: 8px; }}
.mcard-body {{ font-size: 14px; line-height: 1.6; color: #4A5568 !important; }}
</style>

<div class="bg-canvas">
  <div class="grid-lines"></div>
  <div class="orb orb-1"></div>
  <div class="orb orb-2"></div>
</div>
""", unsafe_allow_html=True)

# ─── TOPBAR ─────────────────────────────────────────────────────────────────
brand_label_text = "MAMMOGRAM AI" if not is_ar else "ذكاء الماموجرام"

if not is_ar:
    c0, c1, c2, _, c4 = st.columns([4, 1.4, 1.4, 1, 1.5])
    with c0:
        st.markdown(f'<div class="topbar"><div class="brand-mark">MA</div><span class="brand-label">{brand_label_text}</span></div>', unsafe_allow_html=True)
    with c1:
        if st.button(C["titans_btn"], key="titans_toggle", kind="secondary"):
            st.session_state.view_titans = not st.session_state.view_titans
            st.session_state.help = False
    with c2:
        lbl = C["back_btn"] if (st.session_state.help or st.session_state.view_titans) else C["help_btn"]
        if st.button(lbl, key="help_toggle", kind="secondary"):
            st.session_state.help = not st.session_state.help
            st.session_state.view_titans = False
    with c4:
        if st.button("العربية 🇸🇦", key="lang_toggle", kind="secondary"):
            st.session_state.lang = "AR"; st.rerun()
else:
    c0, _, c2, c3, c4 = st.columns([1.5, 1, 1.4, 1.4, 4])
    with c0:
        if st.button("English 🇬🇧", key="lang_toggle", kind="secondary"):
            st.session_state.lang = "EN"; st.rerun()
    with c2:
        lbl = C["back_btn"] if (st.session_state.help or st.session_state.view_titans) else C["help_btn"]
        if st.button(lbl, key="help_toggle", kind="secondary"):
            st.session_state.help = not st.session_state.help
            st.session_state.view_titans = False
    with c3:
        if st.button(C["titans_btn"], key="titans_toggle", kind="secondary"):
            st.session_state.view_titans = not st.session_state.view_titans
            st.session_state.help = False
    with c4:
        st.markdown(f'<div class="topbar" style="justify-content:flex-end"><span class="brand-label">{brand_label_text}</span><div class="brand-mark">MA</div></div>', unsafe_allow_html=True)

st.markdown('<div class="hr-line"></div>', unsafe_allow_html=True)

# ─── VIEW 1: TEAM ───────────────────────────────────────────────────────────
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
        ("📊", r["researcher_role"], r["researcher"], "Data science research, preprocessing pipelines, dataset analysis.", False),
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

# ─── VIEW 2: HELP ───────────────────────────────────────────────────────────
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
    
    # سنترة زر بدء التحليل بشكل فيت هندسي
    _, mid, _ = st.columns([1.3, 1, 1.3])
    with mid:
        st.markdown('<div class="cta-col">', unsafe_allow_html=True)
        if st.button(C["begin_btn"], key="begin_analysis_main", use_container_width=True):
            st.toast("Redirecting to Analysis Engine...", icon="🚀")
        st.markdown('</div>', unsafe_allow_html=True)
