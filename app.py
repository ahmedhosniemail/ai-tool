import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
from io import BytesIO
from docx import Document
import re

# ==========================================
# 1. إعدادات الصفحة والواجهة الجذابة
# ==========================================
st.set_page_config(
    page_title="Ahmed AI Pro - مستخرج البيانات الذكي",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded" # فتح القائمة الجانبية تلقائياً لاختيار اللغة
)

# ==========================================
# 2. تصميم CSS مخصص ومبهرج وحديث
# ==========================================
st.markdown("""
<style>
    /* 🎨 خلفية متحركة بألوان متدرجة ( Gradient Background ) */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: white; /* جعل النصوص فاتحة لتتناسب مع الخلفية الغامقة */
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 💎 تصميم العناوين */
    .main-title {
        color: white;
        text-align: center;
        font-family: 'Cairo', sans-serif;
        font-weight: bold;
        padding: 30px;
        background: rgba(255, 255, 255, 0.1); /* خلفية نصف شفافة */
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37); /* تاثير زجاجي */
        backdrop-filter: blur(4px);
        -webkit-backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 20px;
    }
    
    .sub-title {
        color: white;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 30px;
        opacity: 0.9;
    }

    /* 🚀 تصميم الأزرار المبهرج (Button with hover effect) */
    div.stButton > button {
        background: linear-gradient(135deg, #a8dadc 0%, #457b9d 100%); /* لون متدرج للزر */
        color: white !important;
        border-radius: 30px !important;
        padding: 12px 30px !important;
        border: none !important;
        font-size: 18px !important;
        font-weight: bold !important;
        width: 100%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #1d3557 0%, #457b9d 100%) !important;
        transform: scale(1.05) translateY(-3px); /* تاثير تكبير ورفع */
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }

    /* 📋 تنسيق الجداول (تأثير زجاجي) */
    .stMarkdown table {
        border-collapse: collapse;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        background: rgba(255, 255, 255, 0.8) !important; /* خلفية الجدول بيضاء نصف شفافة */
        color: #2c3e50 !important; /* جعل نصوص الجدول غامقة */
    }
    .stMarkdown th, .stMarkdown td {
        padding: 12px 15px;
        text-align: left;
        border-bottom: 1px solid rgba(0,0,0,0.1);
    }
    .stMarkdown th {
        background-color: #f1f1f1 !important;
    }
    
    /* تنسيق القائمة الجانبية (Sidebar) */
    .stSidebar {
        background-color: rgba(0, 0, 0, 0.2) !important;
    }
    .stSidebar p {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. إعدادات اللغة (Dictionary-based translation)
# ==========================================
# ديف يحتوي على كل النصوص المترجمة
translations = {
    'العربية': {
        'title': '🤖 Ahmed AI Pro | مستخرج البيانات الذكي',
        'subtitle': 'حول صور الفواتير والبطاقات إلى ملفات Excel و Word بضغطة واحدة',
        'sidebar_lang_label': '🌐 اختر لغة الواجهة والتحليل:',
        'file_uploader_label': '📂 ارفع صورة الجدول أو الفاتورة (JPG/PNG)',
        'analyze_button': '🚀 ابدأ تحليل واستخراج البيانات الآن',
        'analyzing_spinner': '🧠 جاري القراءة والتحليل بدقة...',
        'success_msg': '✅ تم التحليل بنجاح!',
        'extracted_data_header': '📊 البيانات المستخرجة:',
        'download_header': '⬇️ تحميل النتائج:',
        'excel_button': '📥 تحميل كملف Excel (XLSX)',
        'word_button': '📥 تحميل كملف Word (DOCX)',
        'error_msg': 'حدث خطأ:',
        'footer_text': '© 2024 Ahmed AI Pro | جميع الحقوق محفوظة لأحمد حسني',
        'prompt': 'استخرج البيانات من هذه الصورة في شكل جدول'
    },
    'English': {
        'title': '🤖 Ahmed AI Pro | Smart Data Extractor',
        'subtitle': 'Convert invoice/card images to Excel and Word with one click',
        'sidebar_lang_label': '🌐 Select Interface & Analysis Language:',
        'file_uploader_label': '📂 Upload Table or Invoice Image (JPG/PNG)',
        'analyze_button': '🚀 Start Analysis Now',
        'analyzing_spinner': '🧠 AI is reading and analyzing...',
        'success_msg': '✅ Analysis Successful!',
        'extracted
