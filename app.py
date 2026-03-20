import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
from io import BytesIO
from docx import Document
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ahmed AI Pro", page_icon="🤖", layout="centered")

# 2. تصميم CSS احترافي (لون كحلي ثابت مع لمسة زجاجية)
st.markdown("""
<style>
    .stApp {
        background-color: #0d1b2a;
        color: white;
    }
    .main-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .ai-image {
        width: 150px;
        border-radius: 50%;
        margin-bottom: 20px;
        border: 3px solid #1b263b;
        box-shadow: 0 0 20px #415a77;
    }
    .stButton>button {
        background: #415a77 !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        border: none !important;
        height: 50px !important;
        transition: 0.3s !important;
    }
    .stButton>button:hover {
        background: #778da9 !important;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# 3. نصوص اللغات
translations = {
    'العربية': {
        'title': 'أحمد حسني - AI Pro',
        'sub': 'نظام استخراج البيانات الذكي من الوثائق والجداول',
        'up': 'ارفع الصورة هنا (JPG/PNG)',
        'btn': '🚀 استخراج البيانات الآن',
        'wait': 'جاري التحليل الرقمي...',
        'res': '📊 البيانات المستخرجة:',
        'prompt': 'استخرج البيانات من الصورة في جدول Markdown واضح بدقة عالية'
    },
    'English': {
        'title': 'Ahmed Hosny - AI Pro',
        'sub': 'Smart Data Extraction System for Documents & Tables',
        'up': 'Upload image here (JPG/PNG)',
        'btn': '🚀 Extract Data Now',
        'wait': 'Digital analysis in progress...',
        'res': '📊 Extracted Data:',
        'prompt': 'Extract data from the image into a clear, high-precision Markdown table'
    }
}

# القائمة الجانبية
st.sidebar.title("Settings")
lang_choice = st.sidebar.selectbox("Language / اللغة", list(translations.keys()))
lang = translations[lang_choice]

# 4. الواجهة الأمامية (صورة AI احترافية)
st.markdown(f"""
<div class="main-container">
    <img src="https://cdn-icons-png.flaticon.com/512/2103/2103811.png" class="ai-image">
    <h1 style='margin-bottom:0;'>{lang['title']}</h1>
    <p style='color: #778da9;'>{lang['sub']}</p>
</div>
""", unsafe_allow_html=True)

# 5. منطق العمل
genai.configure(api_key="AIzaSyC9v9vX4ioZm8PKttNwefL7QuOKXAaiFfk")
model = genai.GenerativeModel('gemini-1.5-flash')

file = st.file_uploader(lang['up'], type=['jpg', 'jpeg', 'png'])

if file:
    img = Image.open(file)
    st.image(img, use_column_width=True)
    
    if st.button(lang['btn']):
        with st.spinner(lang['wait']):
            try:
                response = model.generate_content([lang['prompt'], img])
                result = response.text
                st.markdown(f"### {lang['res']}")
                st.markdown(result)
                
                # أزرار التحميل
                doc = Document()
                doc.add_paragraph(result)
                bio = BytesIO()
                doc.save(bio)
                st.download_button("Word (DOCX)", data=bio.getvalue(), file_name="data.docx")
            except Exception as e:
                st.error(f"Error: {e}")
                
