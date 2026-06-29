import os
import streamlit as st
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import numpy as np
import datetime
import pandas as pd
import cv2
import io

# ----------------------------------------------------------------------------
# 1. إعدادات الصفحة الأساسية والتصميم (من الملف الثاني كلياً)
# ----------------------------------------------------------------------------
st.set_page_config(layout="wide", page_title="Engineering Titans - AI Mammogram", page_icon="◐")

# ----------------------------------------------------------------------------
# 2. إدارة الـ Session State المشتركة للملفين
# ----------------------------------------------------------------------------
if "help" not in st.session_state:
    st.session_state.help = False
if "lang" not in st.session_state:
    st.session_state.lang = "AR"  # افتراضي عربي ويمكن التغيير
if "view_titans" not in st.session_state:
    st.session_state.view_titans = False
if "analysis_started" not in st.session_state:
    st.session_state.analysis_started = False

# حالات الملف الأول
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "patient_records" not in st.session_state:
    st.session_state.patient_records = []
if "mammogram_images" not in st.session_state:
    st.session_state.mammogram_images = []
if "current_diagnosis" not in st.session_state:
    st.session_state.current_diagnosis = None
if "last_processed_img" not in st.session_state:
    st.session_state.last_processed_img = None
if "form_reset_counter" not in st.session_state:
    st.session_state.form_reset_counter = 0
if "current_page" not in st.session_state:
    st.session_state.current_page = "main"

# ----------------------------------------------------------------------------
# 3. قاموس اللغات والترجمات الموحد (دمج اللغتين من الملفين)
# ----------------------------------------------------------------------------
loc = {
    "EN": {
        "title": "AI-Powered Mammogram Analysis",
        "title_accent": "Early Breast Cancer Classification",
        "sub": "A decision-support assistant that helps healthcare professionals review mammogram images and flag patterns worth a closer look. Built to support clinical judgment, never to replace it.",
        "badge": "Decision support only — final diagnosis remains with the physician",
        "begin_btn": "Begin Analysis →",
        "help_btn": "Help",
        "back_btn": "← Back to Home",
        "titans_btn": "⚙️ Team",
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
            ("Baqubah Hospital", "Dataset"),
        ],
        "help_sections": [
            ("🩺", "Project Overview", "Supports physicians by classifying mammogram images to assist with early breast cancer detection.", False),
            ("📊", "Datasets", "Trained, tested, and evaluated using Online dataset combined with hospital-sourced mammogram images.", False),
            ("🧠", "AI Model", "A convolutional network built with TensorFlow/Keras, using custom Conv2D, Dense, and MaxPool structures.", True),
            ("⚙️", "Training Config", "Image 50×50 · 25 epochs · batch 75 · Adam optimizer · binary cross-entropy loss.", False),
            ("💻", "Technologies", "Python · Streamlit · TensorFlow · Keras · OpenCV · NumPy · Pandas · Pillow", False),
            ("🚀", "Workflow", "Upload → Preprocess → Predict → Display Result → Clinical Verification", True),
        ],
        # ترجمات الملف الأول البديلة المتوافقة
        "login_header": "Doctor / Hospital Login",
        "email": "Email Address",
        "password": "Password",
        "login_btn": "Login",
        "logout_btn": "Logout",
        "patient_header": "Patient Demographics",
        "p_name": "Patient Full Name",
        "p_age": "Age",
        "p_phone": "Phone Number",
        "p_history": "Is there a history of breast cancer in the family?",
        "history_yes": "Yes",
        "history_no": "No",
        "upload_header": "Upload Mammogram Scan",
        "upload_btn": "Choose a mammogram image...",
        "run_scan_btn": "Run Diagnostic Scan",
        "result_header": "Diagnostic Result",
        "processing": "Analyzing scan...",
        "footer": "Your Health Matters",
        "sidebar_title": "Navigation Menu",
        "page_main": "🏥 Diagnostics Screen",
        "page_db": "📊 Patients Database",
        "page_archive": "📁 Mammogram Images Archive",
        "sidebar_support": "Contact Support",
        "support_msg": "Describe the issue you encountered",
        "send_btn": "Send Message",
        "support_success": "Your message has been sent to support successfully.",
        "table_time": "Date & Time",
        "no_data": "No patient records available yet.",
        "benign": "Benign",
        "malignant": "Malignant",
        "save_btn": "Save Record & Clear Form",
        "save_success": "Record saved successfully! Form reset for the next patient.",
        "fill_fields_err": "Please complete the patient details and run the scan before saving.",
        "no_images": "No mammogram images saved yet.",
        "download_btn": "Download Image"
    },
    "AR": {
        "title": "تحليل صور الماموجرام بالذكاء الاصطناعي",
        "title_accent": "التصنيف المبكر لسرطان الثدي",
        "sub": "مساعد لدعم اتخاذ القرار يساعد المتخصصين في الرعاية الصحية على مراجعة صور الماموجرام وتحديد الأنماط التي تستحق نظرة فاحصة. تم بناؤه لدعم الحكم السريري الطبي، وليس لاستبداله أبداً.",
        "badge": "لدعم القرار فقط — التشخيص النهائي يبقى من اختصاص الطبيب",
        "begin_btn": "← بدء التحليل والتشخيص",
        "help_btn": "المساعدة",
        "back_btn": "العودة للرئيسية →",
        "titans_btn": "⚙️ الفريق",
        "titans_title": "فريق العمل ومطوري المشروع",
        "about_title": "حول هذا النظام",
        "dir": "rtl",
        "roles": {
            "supervisor1": "ا.م.د. وسام حيدر مهدي",
            "supervisor1_role": "المشرف",
            "supervisor2": "ا.م.  مها عباس حطيحط",
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
            ("CBIS-DDSM", "بيانات إنترنت"),
            ("مستشفى بعقوبة", "بيانات محلية"),
        ],
        "help_sections": [
            ("🩺", "نظرة عامة", "يدعم الأطباء من خلال تصنيف صور الماموجرام للمساعدة في الكشف المبكر عن سرطان الثدي.", False),
            ("📊", "مجموعات البيانات", "تم التدريب والاختبار باستخدام بيانات الإنترنت مدمجة مع صور مستشفيات حقيقية.", False),
            ("🧠", "نموذج الذكاء الاصطناعي", "شبكة عصبية تلافيفية مبنية بـ TensorFlow و Keras، بطبقات تلافيفية وكثيفة و MaxPool.", True),
            ("⚙️", "معاملات التدريب", "حجم الصورة 50×50 · 25 حقبة · دفعة 75 · محسن Adam · دالة الإنتروبيا المتقاطعة الثنائية.", False),
            ("💻", "التقنيات", "Python · Streamlit · TensorFlow · Keras · OpenCV · NumPy · Pandas · Pillow", False),
            ("🚀", "خطوات العمل", "رفع الصورة ← معالجة ← تنبؤ ← نتيجة ← مراجعة طبية", True),
        ],
        # ترجمات الملف الأول الأصلية بالعربي
        "login_header": "تسجيل دخول الطبيب / المستشفى",
        "email": "البريد الإلكتروني",
        "password": "كلمة المرور",
        "login_btn": "تسجيل الدخول",
        "logout_btn": "تسجيل الخروج",
        "patient_header": "بيانات المريض",
        "p_name": "اسم المريض الثلاثي",
        "p_age": "العمر",
        "p_phone": "رقم الهاتف",
        "p_history": "هل توجد إصابة سابقة بسرطان الثدي في العائلة؟",
        "history_yes": "نعم",
        "history_no": "لا",
        "upload_header": "تحميل صورة الماموغرام",
        "upload_btn": "اختر صورة الأشعة...",
        "run_scan_btn": "بدء الفحص الفوري",
        "result_header": "النتيجة التشخيصية",
        "processing": "جاري تحليل الأشعة...",
        "footer": "صحتك تهمنا",
        "sidebar_title": "قائمة التنقل للأنظمة",
        "page_main": "🏥 شاشة الفحص والتشخيص",
        "page_db": "📊 قاعدة بيانات المرضى",
        "page_archive": "📁 أرشيف صور الماموغرام",
        "sidebar_support": "مراسلة الدعم الفني",
        "support_msg": "اكتب الخطأ الذي واجهك هنا",
        "send_btn": "إرسال الرسالة",
        "support_success": "تم إرسال رسالتك إلى الدعم الفني بنجاح.",
        "table_time": "الوقت والتاريخ",
        "no_data": "لا توجد سجلات مرضى حالياً.",
        "benign": "حميد",
        "malignant": "خبيث",
        "save_btn": "حفظ السجل وتهيئة النظام لمريض جديد",
        "save_success": "تم حفظ السجل بنجاح! تم تفريغ الشاشة بالكامل للمريض التالي.",
        "fill_fields_err": "يرجى ملء بيانات المريض وإجراء الفحص أولاً قبل الحفظ.",
        "no_images": "لا توجد صور ماموغرام محفوظة حالياً.",
        "download_btn": "تحميل الصورة"
    }
}

text = loc[st.session_state.lang]
is_ar = st.session_state.lang == "AR"
font_main = "'Cairo', sans-serif" if is_ar else "'Inter', sans-serif"
font_display = "'Cairo', sans-serif" if is_ar else "'Lora', serif"
brand_label_text = "MAMMOGRAM AI" if not is_ar else "ذكاء الماموجرام"

# ----------------------------------------------------------------------------
# 4. بناء الـ CSS الثابت والمحسن بالكامل للتصميم المظلم والاحترافي (الملف الثاني)
# ----------------------------------------------------------------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:wght@500;700&family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&family=Cairo:wght@400;600;700;900&display=swap');

:root {{
  --bg:          #0F172A;
  --bg-deep:     #020617;   
  --indigo-navy: #111827;
  --bg-card:     #1E293B;   
  --border:      rgba(255,255,255,0.12);
  --steel:       #94A3B8;   
  --white:       #F8FAFC;   
  --pink:        #EC4899;
  --pink-soft:   #F472B6;
}}

footer, header {{ visibility: hidden !important; }}

html, body, .stApp {{
  background: var(--bg) !important;
  font-family: {font_main};
  color: var(--white);
  direction: {text['dir']};
}}

.block-container {{
  max-width: 1160px !important;
  padding: 1.5rem 2rem 4rem !important;
}}

/* تخصيص نصوص وألوان المدخلات في الفورم للملف الأول ليكون متناسقاً */
label, p, span, h1, h2, h3, h4, h5, h6 {{
  color: var(--white) !important;
  direction: {text['dir']} !important;
  text-align: {'right' if is_ar else 'left'} !important;
}}

.topbar {{
  display: flex; align-items: center; gap: 12px; padding-bottom: 14px; position: relative; z-index: 10;
}}
.brand-mark {{
  width: 42px; height: 42px; border-radius: 11px; background: var(--bg-deep); border: 1.5px solid rgba(232,155,176,0.3);
  display: flex; align-items: center; justify-content: center; font-family: 'Lora', serif; font-weight: 700; font-size: 15px; color: var(--white);
}}
.brand-label {{ font-family: 'IBM Plex Mono', monospace; font-size: 11px; letter-spacing: 2.5px; color: #94A3B8; }}

div[data-testid="stButton"] button {{
  background-color: #FFFFFF !important;
  border: 1px solid #FFFFFF !important;
  border-radius: 8px !important;
  padding: 8px 22px !important;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
  transition: all 0.2s ease-in-out !important;
}}

div[data-testid="stButton"] button p, 
div[data-testid="stButton"] button span,
div[data-testid="stButton"] button div {{
  color: var(--indigo-navy) !important;
  font-family: {font_main} !important;
  font-weight: 700 !important;
  font-size: 14px !important;
}}

div[data-testid="stButton"] button:hover {{
  background-color: #475569 !important;
  border-color: #475569 !important;
  box-shadow: 0 6px 16px rgba(0,0,0,0.3) !important;
}}

.hr-line {{
  height: 1px; background: linear-gradient(90deg, transparent, var(--border), rgba(232,155,176,0.3), var(--border), transparent); margin: 4px 0 25px;
}}

.cta-container div[data-testid="stButton"] button {{
  background-color: var(--pink) !important;
  border: 2px solid var(--pink) !important;
  border-radius: 50px !important;
  padding: 14px 50px !important;
  width: 100% !important;
  box-shadow: 0 8px 24px rgba(232,155,176,0.35) !important;
}}

.cta-container div[data-testid="stButton"] button p,
.cta-container div[data-testid="stButton"] button span {{
  color: #FFFFFF !important;
  font-size: 17px !important;
  font-weight: 700 !important;
}}

.cta-container div[data-testid="stButton"] button:hover {{
  background-color: var(--pink-soft) !important;
  border-color: var(--pink-soft) !important;
  box-shadow: 0 10px 28px rgba(244,63,94,0.5) !important;
  transform: translateY(-2px);
}}

.hero {{ text-align: center; padding: 20px 10px 10px; position: relative; z-index: 5; }}
.hero-title {{ font-family: {font_display}; font-size: clamp(28px, 4vw, 44px); font-weight: 700; color: var(--white); line-height: 1.25; }}
.hero-accent {{ display: block; background: linear-gradient(120deg, var(--pink) 0%, #F43F5E 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
.hero-sub {{ color: #94A3B8; font-size: 16px; line-height: 1.8; max-width: 700px; margin: 18px auto 0; }}
.badge-wrap {{ display:flex; justify-content:center; margin-top:22px; }}
.badge {{ display:inline-flex; align-items:center; gap:10px; padding: 10px 22px; border: 1px solid var(--border); background: var(--bg-deep); border-radius: 40px; font-size: 13px; color: #E2E8F0; }}

.stats-row {{ display: flex; max-width: 480px; margin: 35px auto 0; border: 1px solid var(--border); border-radius: 14px; overflow: hidden; }}
.stat-item {{ flex: 1; padding: 16px 14px; text-align: center; background: var(--bg-deep); border-right: 1px solid var(--border); }}
.stat-item:last-child {{ border-right: none; }}
.stat-val {{ font-size: 16px; font-weight: 700; color: var(--white); }}
.stat-lbl {{ font-size: 11px; color: var(--steel); margin-top: 4px; }}

.sec-head {{ text-align: center; margin: 30px 0 25px; }}
.sec-title {{ font-family: {font_display}; font-size: 28px; font-weight: 700; color: var(--white); }}
.sec-sub {{ font-size: 14px; color: #94A3B8; }}

.mcard {{
  background: var(--bg-card) !important; border-top: 4px solid var(--indigo-navy) !important;
  border-radius: 14px; padding: 24px 22px; margin-bottom: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}}
.mcard.pink {{ border-top-color: var(--pink) !important; }}
.mcard-icon {{ font-size: 24px; display: block; margin-bottom: 10px; }}
.mcard-role {{ font-family: {font_main}; font-size: 12px; font-weight: 700; color: var(--pink) !important; margin-bottom: 6px; letter-spacing: 0.5px; }}
.mcard-name {{ font-size: 17px; font-weight: 700; color: #FFFFFF !important; margin-bottom: 8px; margin-top: 2px; }}
.mcard-body {{ font-size: 14px; line-height: 1.6; color: #CBD5E1 !important; }}

/* صندوق النتيجة الحصري من الملف الأول وتحديثه ليكون متوافقاً مع المظهر الجديد */
.result-box {{
    padding: 20px;
    border-radius: 10px;
    background-color: #311F27;
    border: 1px solid var(--pink);
    color: #F472B6 !important;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 25px;
}}
.center-text {{ text-align: center !important; margin-bottom: 15px; margin-top: 15px; color: var(--white); }}
.footer-text {{ text-align: center !important; font-size: 14px; margin-top: 40px; font-style: italic; color: #6B7280; }}
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# 5. تحميل الموديل بدقة (من الملف الأول - لوجيك أساسي)
# ----------------------------------------------------------------------------
@st.cache_resource
def load_my_model():
    try:
        return keras.models.load_model('breast_cancer_cnn.keras')
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_my_model()

if model is None:
    st.stop()


# ----------------------------------------------------------------------------
# 6. البار العلوي الديناميكي للتنقل (من الملف الثاني)
# ----------------------------------------------------------------------------
is_sub_page = st.session_state.help or st.session_state.view_titans or st.session_state.analysis_started

if not is_ar:
    cols_specs = [3.5, 1.3, 1.3, 1.3, 1] if is_sub_page else [4.5, 1.4, 1.4, 1.2]
    cols = st.columns(cols_specs)
    
    with cols[0]:
        st.markdown(f'<div class="topbar"><div class="brand-mark">MA</div><span class="brand-label">{brand_label_text}</span></div>', unsafe_allow_html=True)
    with cols[1]:
        if st.button(text["titans_btn"], key="titans_toggle"):
            st.session_state.view_titans = True
            st.session_state.help = False
            st.session_state.analysis_started = False
    with cols[2]:
        if st.button(text["help_btn"], key="help_toggle"):
            st.session_state.help = True
            st.session_state.view_titans = False
            st.session_state.analysis_started = False
            
    if is_sub_page:
        with cols[3]:
            if st.button(text["back_btn"], key="back_home_btn"):
                st.session_state.help = False
                st.session_state.view_titans = False
                st.session_state.analysis_started = False
                st.rerun()
        with cols[4]:
            if st.button("العربية 🇸🇦", key="lang_toggle"):
                st.session_state.lang = "AR"; st.rerun()
    else:
        with cols[3]:
            if st.button("العربية 🇸🇦", key="lang_toggle"):
                st.session_state.lang = "AR"; st.rerun()
else:
    cols_specs = [1, 1.3, 1.3, 1.3, 3.5] if is_sub_page else [1.2, 1.4, 1.4, 4.5]
    cols = st.columns(cols_specs)
    
    with cols[0]:
        if st.button("English 🇬🇧", key="lang_toggle"):
            st.session_state.lang = "EN"; st.rerun()
            
    if is_sub_page:
        with cols[1]:
            if st.button(text["back_btn"], key="back_home_btn"):
                st.session_state.help = False
                st.session_state.view_titans = False
                st.session_state.analysis_started = False
                st.rerun()
        idx_help, idx_team, idx_brand = 2, 3, 4
    else:
        idx_help, idx_team, idx_brand = 1, 2, 3
        
    with cols[idx_help]:
        if st.button(text["help_btn"], key="help_toggle"):
            st.session_state.help = True
            st.session_state.view_titans = False
            st.session_state.analysis_started = False
    with cols[idx_team]:
        if st.button(text["titans_btn"], key="titans_toggle"):
            st.session_state.view_titans = True
            st.session_state.help = False
            st.session_state.analysis_started = False
    with cols[idx_brand]:
        st.markdown(f'<div class="topbar" style="justify-content:flex-end"><span class="brand-label">{brand_label_text}</span><div class="brand-mark">MA</div></div>', unsafe_allow_html=True)

st.markdown('<div class="hr-line"></div>', unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# 7. عرض الشاشات والتحويل المنطقي (Logic & Routing)
# ----------------------------------------------------------------------------

# ─── الشاشة أ: شاشة فريق العمل (View 1) ───
if st.session_state.view_titans:
    sub_txt = "The people behind the intelligence" if not is_ar else "الفريق الهندسي المطور للنظام"
    st.markdown(f'<div class="sec-head"><div class="sec-title">{text["titans_title"]}</div><div class="sec-sub">{sub_txt}</div></div>', unsafe_allow_html=True)

    r = text["roles"]
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

# ─── الشاشة ب: شاشة المساعدة (View 2) ───
elif st.session_state.help:
    sub_txt = "System architecture, datasets, and clinical workflow" if not is_ar else "معمارية النظام، قواعد البيانات، وسير العمل السريري"
    st.markdown(f'<div class="sec-head"><div class="sec-title">{text["about_title"]}</div><div class="sec-sub">{sub_txt}</div></div>', unsafe_allow_html=True)

    sections = text["help_sections"]
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

# ─── الشاشة ج: شاشة الفحص والنظام الطبي الكامل (View 3 - الملف الأول الفعلي) ───
elif st.session_state.analysis_started:
    
    # 1. واجهة تسجيل الدخول في حال لم يتم الدخول مسبقاً
    if not st.session_state.logged_in:
        st.markdown(f'<h3 class="center-text">{text["login_header"]}</h3>', unsafe_allow_html=True)

        email_input = st.text_input(text["email"], placeholder="doctor@hospital.com")
        password_input = st.text_input(text["password"], type="password")

        if st.button(text["login_btn"], use_container_width=True):
            if "@" in email_input and "." in email_input and len(password_input) >= 4:
                st.session_state.logged_in = True
                st.rerun()
            else:
                if is_ar:
                    st.error("يرجى إدخال بريد إلكتروني وكلمة مرور صالحة")
                else:
                    st.error("Please enter a valid email address and password")

    # 2. واجهة العمل بعد تسجيل الدخول مع القائمة الجانبية المخصصة لها
    else:
        # --- القائمة الجانبية للأنظمة الفرعية التابعة للملف الأول ---
        with st.sidebar:
            st.title(text["sidebar_title"])
            
            if st.button(text["page_main"], use_container_width=True):
                st.session_state.current_page = "main"
                st.rerun()
                
            if st.button(text["page_db"], use_container_width=True):
                st.session_state.current_page = "database"
                st.rerun()
                
            if st.button(text["page_archive"], use_container_width=True):
                st.session_state.current_page = "archive"
                st.rerun()
                
            st.write("---")
            
            with st.expander(text["sidebar_support"]):
                support_text = st.text_area(text["support_msg"], key="support_box")
                if st.button(text["send_btn"]):
                    if support_text.strip() != "":
                        st.success(text["support_success"])
                        
            st.write("---")
            if st.button(text["logout_btn"], use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.current_diagnosis = None
                st.session_state.current_page = "main"
                st.session_state.analysis_started = False
                st.rerun()

        # ---------------- شاشة الفحص الرئيسية (من الملف الأول كلياً) ----------------
        if st.session_state.current_page == "main":
            st.markdown(f'<h3 class="center-text">{text["patient_header"]}</h3>', unsafe_allow_html=True)

            cnt = st.session_state.form_reset_counter
            p_name = st.text_input(text["p_name"], autocomplete="new-password", key=f"p_name_{cnt}")
            p_age = st.text_input(text["p_age"], autocomplete="new-password", key=f"p_age_{cnt}")
            p_phone = st.text_input(text["p_phone"], autocomplete="new-password", key=f"p_phone_{cnt}")
            p_history = st.radio(text["p_history"], [text["history_no"], text["history_yes"]], key=f"p_history_{cnt}")

            st.write("---")

            st.markdown(f'<h3 class="center-text">{text["upload_header"]}</h3>', unsafe_allow_html=True)
            uploaded_file = st.file_uploader(text["upload_btn"], type=["jpg", "png", "jpeg"], key=f"uploader_{cnt}")

            if uploaded_file is not None:
                display_image = Image.open(uploaded_file).convert("RGB")
                st.image(display_image, caption="", use_container_width=True)

                if st.button(text["run_scan_btn"], use_container_width=True):
                    st.write(text["processing"])

                    try:
                        file_bytes = np.asarray(bytearray(uploaded_file.getvalue()), dtype=np.uint8)
                        cv2_img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

                        if cv2_img is None:
                            if is_ar:
                                st.error("خطأ: تعذر قراءة الصورة.")
                            else:
                                st.error("Error: Could not decode the image.")
                            st.stop()

                        cv2_img = cv2.resize(cv2_img, (50, 50), interpolation=cv2.INTER_LINEAR)
                        img_array = np.array(cv2_img, dtype=np.float32) / 255.0
                        img_array = np.expand_dims(img_array, axis=0)

                        prediction = model.predict(img_array, verbose=0)
                        predicted_class = np.argmax(prediction, axis=1)[0]
                        
                        if predicted_class == 0:
                            st.session_state.current_diagnosis = text["benign"]
                        else:
                            st.session_state.current_diagnosis = text["malignant"]
                        
                        st.session_state.last_processed_img = display_image
                        st.rerun()
                    
                    except Exception as e:
                        st.error(f"Processing Error: {e}")

            if st.session_state.current_diagnosis is not None:
                st.markdown(f'<h3 class="center-text">{text["result_header"]}</h3>', unsafe_allow_html=True)
                st.markdown(f'<div class="result-box">{st.session_state.current_diagnosis}</div>', unsafe_allow_html=True)
                
                if st.button(text["save_btn"], use_container_width=True, type="primary"):
                    if p_name.strip() != "":
                        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        record = {
                            text["p_name"]: p_name,
                            text["p_age"]: p_age,
                            text["p_phone"]: p_phone,
                            text["p_history"]: p_history,
                            text["result_header"]: st.session_state.current_diagnosis,
                            text["table_time"]: current_time
                        }
                        st.session_state.patient_records.append(record)
                        
                        if st.session_state.last_processed_img is not None:
                            image_record = {
                                "image": st.session_state.last_processed_img,
                                "result": st.session_state.current_diagnosis
                            }
                            st.session_state.mammogram_images.append(image_record)

                        st.success(text["save_success"])
                        
                        st.session_state.current_diagnosis = None
                        st.session_state.last_processed_img = None
                        st.session_state.form_reset_counter += 1 
                        st.rerun()
                    else:
                        st.error(text["fill_fields_err"])

        # ---------------- شاشة قاعدة البيانات المستقلة ----------------
        elif st.session_state.current_page == "database":
            st.markdown(f'<h3>{text["page_db"]}</h3>', unsafe_allow_html=True)
            if len(st.session_state.patient_records) > 0:
                df = pd.DataFrame(st.session_state.patient_records)
                st.dataframe(df, use_container_width=True)
            else:
                st.info(text["no_data"])

        # ---------------- شاشة أرشيف الصور ----------------
        elif st.session_state.current_page == "archive":
            st.markdown(f'<h3>{text["page_archive"]}</h3>', unsafe_allow_html=True)
            if len(st.session_state.mammogram_images) > 0:
                cols = st.columns(3)
                for idx, img_item in enumerate(st.session_state.mammogram_images):
                    with cols[idx % 3]:
                        st.image(img_item['image'], use_container_width=True)
                        st.write(f"📊 **{img_item['result']}**")
                        
                        buf = io.BytesIO()
                        img_item['image'].save(buf, format="PNG")
                        byte_im = buf.getvalue()
                        
                        st.download_button(
                            label=text["download_btn"],
                            data=byte_im,
                            file_name=f"mammogram_{idx+1}.png",
                            mime="image/png",
                            key=f"dl_{idx}"
                        )
                        st.write("---")
            else:
                st.info(text["no_images"])

        st.markdown(f'<div class="footer-text">{text["footer"]}</div>', unsafe_allow_html=True)

# ─── الشاشة د: الواجهة الترحيبية للرئيسية (View 4 - ملف التصميم الثاني) ───
else:
    eyebrow = "Clinical AI · Mammography" if not is_ar else "ذكاء اصطناعي سريري · الماموجرام"
    st.markdown(f"""
    <div class="hero">
      <div class="hero-title">
        {text['title']}
        <span class="hero-accent">{text['title_accent']}</span>
      </div>
      <p class="hero-sub">{text['sub']}</p>
      <div class="badge-wrap"><div class="badge">🎀 {text['badge']}</div></div>
    </div>
    """, unsafe_allow_html=True)

    stats_html = '<div class="stats-row">' + "".join(
        f'<div class="stat-item"><div class="stat-val">{v}</div><div class="stat-lbl">{l}</div></div>'
        for v, l in text["stats"]
    ) + '</div>'
    st.markdown(stats_html, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    _, mid, _ = st.columns([1.2, 1, 1.2])
    with mid:
        st.markdown('<div class="cta-container">', unsafe_allow_html=True)
        if st.button(text["begin_btn"], key="begin_analysis_main", use_container_width=True):
            st.session_state.analysis_started = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
