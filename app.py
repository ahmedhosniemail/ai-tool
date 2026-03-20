import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
from io import BytesIO
from docx import Document
import re

# 1. إعدادات الصفحة والجماليات
st.set_page_config(page_title="Ahmed AI Pro", page_icon="🤖", layout="centered")

st.markdown("""
<style>
    .stApp {
        background-color: #0d1b2a; /* الكحلي الملكي */
        color: white;
    }
    .glass-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 25px;
        padding: 40px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        backdrop-filter: blur(10px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    }
    .ai-icon {
        width: 140px;
        filter: drop-shadow(0 0 15px #415a77);
        margin-bottom: 20px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #1b263b, #415a77) !important;
        color: white !important;
        border-radius: 15px !important;
        border: 1px solid #778da9 !important;
        height: 55px !important;
        width: 100%;
        font-size: 18px !important;
        transition: 0.3s !important;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 20px rgba(65, 90, 119, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# 2. اللغات المترجمة
translations = {
    'العربية': {
        'title': 'أحمد حسني - AI Pro',
        'sub': 'نظام استخراج البيانات الذكي (Excel & Word)',
        'up': '📂 ارفع صورة الجدول أو الفاتورة',
        'btn': '🚀 ابدأ الاستخراج الآن',
        'res': '📊 البيانات المستخرجة:',
        'dl': '⬇️ تحميل الملفات جاهزة:',
        'prompt': 'استخرج البيانات من الصورة ونظمها في جدول Markdown بدقة.'
    },
    'English': {
        'title': 'Ahmed Hosny - AI Pro',
        'sub': 'Smart Data Extraction System (Excel & Word)',
        'up': '📂 Upload Table or Invoice Image',
        'btn': '🚀 Start Extraction',
        'res': '📊 Extracted Data:',
        'dl': '⬇️ Download Ready Files:',
        'prompt': 'Extract data from the image into a clean Markdown table.'
    }
}

# شريط اختيار اللغة
st.sidebar.markdown("### 🌐 Language / اللغة")
sel_lang = st.sidebar.selectbox("", list(translations.keys()))
lang = translations[sel_lang]

# 3. الواجهة الرسومية (3D Icon)
st.markdown(f"""
<div class="glass-container">
    <img src="https://cdn-icons-png.flaticon.com/512/6221/6221443.png" class="ai-icon">
    <h1 style='margin:0; font-size: 2.5rem;'>{lang['title']}</h1>
    <p style='color: #778da9; font-size: 1.2rem;'>{lang['sub']}</p>
</div>
""", unsafe_allow_html=True)

# 4. الربط مع الموديل
genai.configure(api_key="AIzaSyC9v9vX4ioZm8PKttNwefL7QuOKXAaiFfk")
model = genai.GenerativeModel('models/gemini-1.5-flash')

file = st.file_uploader(lang['up'], type=['jpg', 'jpeg', 'png'])

if file:
    img = Image.open(file)
    st.image(img, caption="Image Uploaded", use_column_width=True)
    
    if st.button(lang['btn']):
        with st.spinner("🧠 جاري معالجة البيانات..."):
            try:
                response = model.generate_content([lang['prompt'], img])
                result = response.text
                st.markdown(f"### {lang['res']}")
                st.markdown(result)
                
                # إنشاء ملفات التحميل
                st.divider()
                st.subheader(lang['dl'])
                col1, col2 = st.columns(2)
                
                # إنشاء ملف Word
                doc = Document()
                doc.add_paragraph(result)
                doc_io = BytesIO()
                doc.save(doc_io)
                with col1:
                    st.download_button("Word (DOCX)", data=doc_io.getvalue(), file_name="Ahmed_AI_Data.docx")
                
                # إنشاء ملف Excel (بسيط من الـ Markdown)
                try:
                    df_list = pd.read_html(result.replace('|', '')) # محاولة بسيطة لقراءة الجدول
                    if df_list:
                        excel_io = BytesIO()
                        df_list[0].to_excel(excel_io, index=False)
                        with col2:
                            st.download_button("Excel (XLSX)", data=excel_io.getvalue(), file_name="Ahmed_AI_Data.xlsx")
                except:
                    with col2:
                        st.info("Excel will be ready in next scan.")

            except Exception as e:
                st.error(f"Error: {e}")
