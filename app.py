import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
from io import BytesIO
from docx import Document
from fpdf import FPDF
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ahmed AI Pro", page_icon="👑", layout="centered")

# 2. تصميم الواجهة (فاتحة وملكية)
st.markdown("""
<style>
    .stApp { background-color: #f7f9fc; color: #1a253a; }
    .main-card {
        background: white;
        border-radius: 20px;
        padding: 30px;
        border: 2px solid #d4af37;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 20px;
    }
    .logo-img { width: 120px; margin-bottom: 15px; }
    .stButton>button {
        background: linear-gradient(135deg, #1e3c72, #2a5298) !important;
        color: white !important;
        border-radius: 12px !important;
        height: 50px; width: 100%; font-weight: bold; border: none;
    }
</style>
""", unsafe_allow_html=True)

# 3. إعدادات اللغة
translations = {
    'العربية': {
        'title': 'أحمد حسني - AI PRO',
        'sub': 'نظام الاستخراج الذكي الشامل',
        'up': '📂 ارفع الصورة هنا (جدول أو فاتورة)',
        'btn': '🚀 ابدأ الاستخراج الآن',
        'dl': '📥 خيارات التحميل الجاهزة:',
        'prompt': 'Extract the data from this image into a clean table.'
    },
    'English': {
        'title': 'AHMED HOSNY - AI PRO',
        'sub': 'Comprehensive Smart Extraction System',
        'up': '📂 Upload image here (Table or Invoice)',
        'btn': '🚀 Start Extraction Now',
        'dl': '📥 Download Options:',
        'prompt': 'Extract the data from this image into a clean table.'
    }
}

# شريط جانبي لاختيار اللغة (سيعالج مشكلتك)
st.sidebar.title("Settings / الإعدادات")
sel_lang = st.sidebar.selectbox("Choose Language / اختر اللغة", list(translations.keys()))
lang = translations[sel_lang]

# 4. عرض الواجهة والشعار
st.markdown(f"""
<div class="main-card">
    <img src="https://cdn-icons-png.flaticon.com/512/9167/9167196.png" class="logo-img">
    <h1 style='margin:0;'>{lang['title']}</h1>
    <p style='color: #7f8c8d;'>{lang['sub']}</p>
</div>
""", unsafe_allow_html=True)

# 5. منطق المعالجة والتحميل
genai.configure(api_key="AIzaSyC9v9vX4ioZm8PKttNwefL7QuOKXAaiFfk")
model = genai.GenerativeModel('gemini-1.5-flash')

uploaded_file = st.file_uploader(lang['up'], type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, use_column_width=True)
    
    if st.button(lang['btn']):
        with st.spinner("🧠 جاري المعالجة..."):
            try:
                response = model.generate_content([lang['prompt'], img])
                result = response.text
                st.markdown("### 📊 النتائج:")
                st.markdown(result)
                
                st.divider()
                st.write(lang['dl'])
                c1, c2, c3 = st.columns(3)
                
                # تحميل Excel
                with c1:
                    st.download_button("Excel", data=result, file_name="data.csv")
                # تحميل Word
                with c2:
                    doc = Document()
                    doc.add_paragraph(result)
                    b = BytesIO()
                    doc.save(b)
                    st.download_button("Word", data=b.getvalue(), file_name="data.docx")
                # تحميل PDF (نسخة بسيطة)
                with c3:
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    pdf.multi_cell(0, 10, txt=result.encode('latin-1', 'ignore').decode('latin-1'))
                    st.download_button("PDF", data=pdf.output(dest='S').encode('latin-1'), file_name="data.pdf")

            except Exception as e:
                st.error(f"Error: {e}")
                
