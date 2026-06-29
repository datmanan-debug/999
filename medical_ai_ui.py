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
        "ref_title": "Reference",
        "about_title": "About this System",
        "dir": "ltr",
        "align": "left",
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
        "begin_btn": "بدء التحليل ←",
        "help_btn": "المساعدة",
        "back_btn": "→ العودة",
        "titans_btn": "⚙ الفريق",
        "titans_title": "فريق العمل ومطوري المشروع",
        "ref_title": "المراجع",
        "about_title": "حول هذا النظام",
        "dir": "rtl",
        "align": "right",
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
font_family = "'Cairo', 'Noto Sans Arabic', sans-serif" if is_ar else "'Inter', sans-serif"

# ----------------------------------------------------------------------------
# MASTER CSS — Navy · Slate · Pink
# ----------------------------------------------------------------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,500;0,700;1,500&family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&family=Cairo:wght@400;600;700;900&display=swap');

/* ═══════════════════════════════════════════
   TOKENS
═══════════════════════════════════════════ */
:root {{
  --navy:       #0D1F35;
  --navy-mid:   #162B45;
  --slate:      #2C3E55;
  --slate-light:#3D5166;
  --steel:      #8FA3B1;
  --fog:        #C8D6E0;
  --ghost:      #EEF3F7;
  --white:      #F8FAFC;
  --pink:       #E89BB0;
  --pink-soft:  #F3C6D4;
  --pink-glow:  rgba(232,155,176,0.18);
  --pink-line:  rgba(232,155,176,0.45);
  --accent:     #3B82F6;
  --success:    #34D399;
  --radius-sm:  8px;
  --radius-md:  14px;
  --radius-lg:  22px;
  --shadow-sm:  0 2px 8px rgba(13,31,53,0.12);
  --shadow-md:  0 6px 24px rgba(13,31,53,0.18);
  --shadow-lg:  0 16px 48px rgba(13,31,53,0.25);
  --transition: 0.28s cubic-bezier(0.4,0,0.2,1);
}}

/* ═══════════════════════════════════════════
   BASE RESET
═══════════════════════════════════════════ */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body, .stApp {{
  background: var(--navy) !important;
  font-family: {font_family};
  color: var(--white);
  direction: {C['dir']};
}}

.block-container {{
  max-width: 1180px !important;
  padding: 1.4rem 2rem 3rem !important;
}}

footer, header {{ visibility: hidden !important; }}

/* ═══════════════════════════════════════════
   ANIMATED BACKGROUND MESH
═══════════════════════════════════════════ */
.stApp::before {{
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 60% 50% at 20% 20%, rgba(59,130,246,0.06) 0%, transparent 70%),
    radial-gradient(ellipse 50% 40% at 80% 80%, rgba(232,155,176,0.07) 0%, transparent 65%),
    radial-gradient(ellipse 40% 60% at 60% 10%, rgba(22,43,69,0.9) 0%, transparent 60%);
  pointer-events: none;
  z-index: 0;
  animation: meshPulse 8s ease-in-out infinite alternate;
}}

@keyframes meshPulse {{
  0%   {{ opacity: 0.7; }}
  100% {{ opacity: 1; }}
}}

/* ═══════════════════════════════════════════
   TOPBAR
═══════════════════════════════════════════ */
.topbar {{
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 2px 14px;
}}

.brand-mark {{
  width: 44px; height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--slate), var(--navy-mid));
  border: 1.5px solid var(--slate-light);
  display: flex; align-items: center; justify-content: center;
  font-family: 'Lora', serif; font-weight: 700; font-size: 16px;
  color: var(--white);
  box-shadow: var(--shadow-sm), 0 0 0 1px var(--pink-line);
  position: relative;
  overflow: hidden;
  animation: brandIn 0.6s ease both;
}}

.brand-mark::after {{
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--pink), var(--pink-soft));
}}

@keyframes brandIn {{
  from {{ opacity: 0; transform: scale(0.8) rotate(-5deg); }}
  to   {{ opacity: 1; transform: scale(1) rotate(0); }}
}}

.brand-label {{
  font-family: 'IBM Plex Mono', monospace;
  font-size: 11px; letter-spacing: 2.5px;
  color: var(--steel); text-transform: uppercase;
  animation: fadeUp 0.5s 0.1s ease both;
}}

@keyframes fadeUp {{
  from {{ opacity: 0; transform: translateY(6px); }}
  to   {{ opacity: 1; transform: translateY(0); }}
}}

/* ═══════════════════════════════════════════
   TOPBAR BUTTONS (all stButtons in top cols)
═══════════════════════════════════════════ */
div[data-testid="column"] .stButton > button {{
  background: rgba(44,62,85,0.5) !important;
  color: var(--fog) !important;
  border: 1px solid rgba(143,163,177,0.2) !important;
  border-radius: var(--radius-sm) !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  padding: 7px 16px !important;
  font-family: {font_family} !important;
  transition: var(--transition) !important;
  letter-spacing: 0.3px;
  backdrop-filter: blur(8px);
}}

div[data-testid="column"] .stButton > button:hover {{
  background: rgba(232,155,176,0.12) !important;
  border-color: var(--pink-line) !important;
  color: var(--pink-soft) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 12px var(--pink-glow) !important;
}}

/* ═══════════════════════════════════════════
   DIVIDER
═══════════════════════════════════════════ */
.hr-divider {{
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(143,163,177,0.2), var(--pink-line), rgba(143,163,177,0.2), transparent);
  margin: 8px 0 0;
  animation: shimmer 3s ease-in-out infinite;
}}

@keyframes shimmer {{
  0%, 100% {{ opacity: 0.5; }}
  50%       {{ opacity: 1; }}
}}

/* ═══════════════════════════════════════════
   HERO SECTION
═══════════════════════════════════════════ */
.hero {{
  text-align: center;
  padding: 56px 20px 32px;
  position: relative;
}}

.hero-eyebrow {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 11px;
  letter-spacing: 3px;
  color: var(--pink);
  text-transform: uppercase;
  margin-bottom: 20px;
  padding: 6px 16px;
  border: 1px solid var(--pink-line);
  border-radius: 30px;
  background: var(--pink-glow);
  animation: fadeDown 0.6s ease both;
}}

.hero-eyebrow::before {{
  content: '';
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--pink);
  box-shadow: 0 0 8px var(--pink);
  animation: blink 1.8s ease-in-out infinite;
}}

@keyframes blink {{
  0%,100% {{ opacity: 1; }}
  50%      {{ opacity: 0.3; }}
}}

@keyframes fadeDown {{
  from {{ opacity: 0; transform: translateY(-12px); }}
  to   {{ opacity: 1; transform: translateY(0); }}
}}

.hero-title {{
  font-family: 'Lora', serif;
  font-size: clamp(28px, 4.5vw, 48px);
  font-weight: 700;
  color: var(--white);
  line-height: 1.2;
  margin-bottom: 12px;
  animation: fadeUp 0.7s 0.1s ease both;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}}

.hero-accent {{
  color: transparent;
  background: linear-gradient(135deg, var(--pink) 0%, var(--pink-soft) 60%, #fff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: block;
  margin-top: 6px;
}}

.hero-sub {{
  color: var(--steel);
  font-size: 16px;
  line-height: 1.8;
  max-width: 660px;
  margin: 20px auto 0;
  animation: fadeUp 0.7s 0.2s ease both;
}}

/* ═══════════════════════════════════════════
   BADGE
═══════════════════════════════════════════ */
.badge-wrap {{
  display: flex;
  justify-content: center;
  margin: 28px 0 0;
  animation: fadeUp 0.7s 0.3s ease both;
}}

.badge {{
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 22px;
  border: 1px solid var(--pink-line);
  background: linear-gradient(135deg, rgba(22,43,69,0.8), rgba(44,62,85,0.5));
  backdrop-filter: blur(10px);
  border-radius: 40px;
  font-size: 13px;
  color: var(--fog);
  letter-spacing: 0.2px;
  box-shadow: 0 0 20px var(--pink-glow);
}}

/* ═══════════════════════════════════════════
   STATS RIBBON
═══════════════════════════════════════════ */
.stats-row {{
  display: flex;
  justify-content: center;
  gap: 0;
  margin: 44px auto 0;
  max-width: 680px;
  border: 1px solid rgba(143,163,177,0.15);
  border-radius: var(--radius-md);
  overflow: hidden;
  backdrop-filter: blur(12px);
  animation: fadeUp 0.7s 0.4s ease both;
}}

.stat-item {{
  flex: 1;
  padding: 18px 16px;
  text-align: center;
  background: rgba(22,43,69,0.6);
  border-right: 1px solid rgba(143,163,177,0.1);
  transition: var(--transition);
  position: relative;
  overflow: hidden;
}}

.stat-item:last-child {{ border-right: none; }}

.stat-item::before {{
  content: '';
  position: absolute;
  inset: 0;
  background: var(--pink-glow);
  opacity: 0;
  transition: var(--transition);
}}

.stat-item:hover::before {{ opacity: 1; }}
.stat-item:hover {{ transform: translateY(-2px); }}

.stat-val {{
  font-family: 'IBM Plex Mono', monospace;
  font-size: 18px;
  font-weight: 500;
  color: var(--white);
  letter-spacing: 0.5px;
}}

.stat-lbl {{
  font-size: 11px;
  color: var(--steel);
  margin-top: 4px;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}}

/* ═══════════════════════════════════════════
   CTA BUTTON
═══════════════════════════════════════════ */
.cta-wrap {{
  display: flex;
  justify-content: center;
  margin-top: 36px;
  animation: fadeUp 0.7s 0.5s ease both;
}}

/* Target the begin analysis button specifically */
div.stButton > button[kind="primary"],
div.stButton > button:has(+ div) {{
  /* fallback for primary buttons */
}}

.stButton > button[data-testid*="begin"],
div[data-testid="column"] .stButton > button[key="begin_analysis_main"] {{
  background: linear-gradient(135deg, var(--slate), var(--navy-mid)) !important;
  color: var(--white) !important;
}}

/* Override hero CTA button via column trick */
.cta-col .stButton > button {{
  background: linear-gradient(135deg, var(--pink) 0%, #c46b8a 100%) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 50px !important;
  font-size: 16px !important;
  font-weight: 600 !important;
  padding: 14px 36px !important;
  letter-spacing: 0.5px !important;
  box-shadow: 0 8px 28px rgba(232,155,176,0.35) !important;
  transition: all 0.3s ease !important;
  font-family: {font_family} !important;
}}

.cta-col .stButton > button:hover {{
  transform: translateY(-3px) scale(1.02) !important;
  box-shadow: 0 14px 40px rgba(232,155,176,0.5) !important;
  background: linear-gradient(135deg, #f0a8bf 0%, var(--pink) 100%) !important;
}}

/* ═══════════════════════════════════════════
   CARDS (Titans & Help)
═══════════════════════════════════════════ */
.section-title {{
  font-family: 'Lora', serif;
  font-size: 28px;
  font-weight: 700;
  color: var(--white);
  text-align: center;
  margin-bottom: 8px;
  animation: fadeDown 0.5s ease both;
}}

.section-sub {{
  font-size: 14px;
  color: var(--steel);
  text-align: center;
  margin-bottom: 36px;
  animation: fadeDown 0.5s 0.1s ease both;
}}

.mcard {{
  background: linear-gradient(145deg, rgba(22,43,69,0.9), rgba(13,31,53,0.95));
  border: 1px solid rgba(143,163,177,0.12);
  border-radius: var(--radius-md);
  padding: 24px 22px;
  margin-bottom: 16px;
  position: relative;
  overflow: hidden;
  transition: var(--transition);
  animation: cardIn 0.5s ease both;
  backdrop-filter: blur(12px);
}}

@keyframes cardIn {{
  from {{ opacity: 0; transform: translateY(16px); }}
  to   {{ opacity: 1; transform: translateY(0); }}
}}

.mcard:hover {{
  transform: translateY(-4px);
  border-color: rgba(143,163,177,0.25);
  box-shadow: var(--shadow-lg), 0 0 0 1px rgba(232,155,176,0.15);
}}

.mcard::before {{
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--slate), var(--slate-light));
  transition: var(--transition);
}}

.mcard:hover::before {{
  background: linear-gradient(90deg, var(--pink), var(--pink-soft));
}}

.mcard.pink::before {{
  background: linear-gradient(90deg, var(--pink), var(--pink-soft));
}}

.mcard-icon {{
  font-size: 22px;
  margin-bottom: 10px;
  display: block;
}}

.mcard-role {{
  font-family: 'IBM Plex Mono', monospace;
  font-size: 10px;
  letter-spacing: 2px;
  color: var(--pink);
  text-transform: uppercase;
  margin-bottom: 6px;
}}

.mcard-name {{
  font-size: 16px;
  font-weight: 600;
  color: var(--white);
  margin-bottom: 8px;
}}

.mcard-body {{
  font-size: 13.5px;
  color: var(--steel);
  line-height: 1.65;
}}

/* stagger card animations */
.mcard:nth-child(1) {{ animation-delay: 0.05s; }}
.mcard:nth-child(2) {{ animation-delay: 0.12s; }}
.mcard:nth-child(3) {{ animation-delay: 0.19s; }}
.mcard:nth-child(4) {{ animation-delay: 0.26s; }}

/* ═══════════════════════════════════════════
   SCROLLBAR
═══════════════════════════════════════════ */
::-webkit-scrollbar {{ width: 6px; }}
::-webkit-scrollbar-track {{ background: var(--navy); }}
::-webkit-scrollbar-thumb {{ background: var(--slate); border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{ background: var(--pink); }}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# TOPBAR
# ----------------------------------------------------------------------------
brand_text = "MA"
brand_label_text = "MAMMOGRAM AI" if not is_ar else "ذكاء الماموجرام"

if not is_ar:
    c0, c1, c2, c3, c4 = st.columns([4, 1.5, 1.5, 1.5, 1.5])
    with c0:
        st.markdown(f"""
        <div class="topbar">
          <div class="brand-mark">{brand_text}</div>
          <span class="brand-label">{brand_label_text}</span>
        </div>""", unsafe_allow_html=True)
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
        lang_label = "العربية 🇸🇦"
        if st.button(lang_label, key="lang_toggle"):
            st.session_state.lang = "AR"
            st.rerun()
else:
    c0, c1, c2, c3, c4 = st.columns([1.5, 1.5, 1.5, 1.5, 4])
    with c0:
        lang_label = "English 🇬🇧"
        if st.button(lang_label, key="lang_toggle"):
            st.session_state.lang = "EN"
            st.rerun()
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
        st.markdown(f"""
        <div class="topbar" style="justify-content:flex-end">
          <span class="brand-label">{brand_label_text}</span>
          <div class="brand-mark">{brand_text}</div>
        </div>""", unsafe_allow_html=True)

st.markdown('<div class="hr-divider"></div>', unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# VIEW 1 — Team / Titans
# ----------------------------------------------------------------------------
if st.session_state.view_titans:
    st.markdown(f"""
    <div style="margin-top:32px;">
      <div class="section-title">{C['titans_title']}</div>
      <div class="section-sub">The people behind the intelligence</div>
    </div>""", unsafe_allow_html=True)

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
            cls = "mcard pink" if is_pink else "mcard"
            st.markdown(f"""
            <div class="{cls}">
              <span class="mcard-icon">{icon}</span>
              <div class="mcard-role">{role}</div>
              <div class="mcard-name">{name}</div>
              <div class="mcard-body">{body}</div>
            </div>""", unsafe_allow_html=True)
    with col_r:
        for icon, role, name, body, is_pink in right_cards:
            cls = "mcard pink" if is_pink else "mcard"
            st.markdown(f"""
            <div class="{cls}">
              <span class="mcard-icon">{icon}</span>
              <div class="mcard-role">{role}</div>
              <div class="mcard-name">{name}</div>
              <div class="mcard-body">{body}</div>
            </div>""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# VIEW 2 — Help / About
# ----------------------------------------------------------------------------
elif st.session_state.help:
    st.markdown(f"""
    <div style="margin-top:32px;">
      <div class="section-title">{C['about_title']}</div>
      <div class="section-sub">System architecture, datasets, and clinical workflow</div>
    </div>""", unsafe_allow_html=True)

    sections = C["help_sections"]
    for i in range(0, len(sections), 2):
        pair = sections[i:i+2]
        cols = st.columns(len(pair), gap="medium")
        for col, (icon, title, body, is_pink) in zip(cols, pair):
            with col:
                cls = "mcard pink" if is_pink else "mcard"
                st.markdown(f"""
                <div class="{cls}">
                  <span class="mcard-icon">{icon}</span>
                  <div class="mcard-role">Module</div>
                  <div class="mcard-name">{title}</div>
                  <div class="mcard-body">{body}</div>
                </div>""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# VIEW 3 — Hero
# ----------------------------------------------------------------------------
else:
    eyebrow_text = "Clinical AI · Mammography" if not is_ar else "ذكاء اصطناعي سريري · صور الماموجرام"
    st.markdown(f"""
    <div class="hero">
      <div class="hero-eyebrow">{eyebrow_text}</div>
      <div class="hero-title">
        {C['title']}
        <span class="hero-accent">{C['title_accent']}</span>
      </div>
      <p class="hero-sub">{C['sub']}</p>
      <div class="badge-wrap">
        <div class="badge">🎀 {C['badge']}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats ribbon
    stats_html = '<div class="stats-row">'
    for val, lbl in C["stats"]:
        stats_html += f'<div class="stat-item"><div class="stat-val">{val}</div><div class="stat-lbl">{lbl}</div></div>'
    stats_html += '</div>'
    st.markdown(stats_html, unsafe_allow_html=True)

    # CTA Button
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, cta_col, _ = st.columns([1, 1.2, 1])
    with cta_col:
        st.markdown('<div class="cta-col">', unsafe_allow_html=True)
        if st.button(C["begin_btn"], key="begin_analysis_main", use_container_width=True):
            st.toast("Redirecting to Analysis Engine...", icon="🚀")
        st.markdown('</div>', unsafe_allow_html=True)
