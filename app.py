import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
from io import BytesIO
from docx import Document
import re

# 1. إعدادات الصفحة والواجهة
st.set_page_config(page_title="Ahmed AI Pro", page_icon="💎", layout="centered")

# 2. تصميم CSS عصري ومبهرج (خلفية متدرجة وتأثيرات زجاجية)
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(-45deg, #23a6d5, #23d5ab, #e73c7e, #ee7752);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background: linear-gradient(90deg, #ff8a00, #e52e71);
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# 3. نظام الترجمة واللغات
langs = {
    'العربية': {
        't': '🤖 مستخرج البيانات الذكي - أحمد حسني',
        'sub': 'حوّل صورك إلى بيانات رقمية فوراً',
        'up': 'ارفع صورة (جدول، فاتورة، بطاقة)',
        'btn': '🚀 استخراج البيانات الآن',
        'wait': 'جاري التحليل...',
        'res': '📊 النتائج المستخرجة:',
        'dl': '📥 تحميل النتائج:',
        'prompt': 'استخرج البيانات من الصورة في جدول Markdown واضح'
    },
    'English': {
        't': '🤖 Ahmed AI Pro - Smart Extractor',
        'sub': 'Convert images to digital data instantly',
        'up': 'Upload image (Table, Invoice, Card)',
        'btn': '🚀 Extract Data Now',
        'wait': 'Analyzing...',
        'res': '📊 Extracted Data:',
        'dl': '📥 Download Results:',
        'prompt': 'Extract data from the image into a clear Markdown table'
    },
    'Français': {
        't': '🤖 Ahmed AI Pro - Extracteur Intelligent',
        'sub': 'Convertissez vos images en données numériques',
        'up': 'Charger une image (Tableau, Facture)',
        'btn': '🚀 Extraire les données',
        'wait': 'Analyse en cours...',
        'res': '📊 Données extraites :',
        'dl': '📥 Télécharger :',
        'prompt': 'Extraire les données de l\'image dans un tableau Markdown'
    }
}

# اختيار اللغة من القائمة الجانبية
st.sidebar.title("Settings")
sel_lang = st.sidebar.selectbox("Language / اللغة", list(langs.keys()))
txt = langs[sel_lang]

# الواجهة الرئيسية
st.markdown(f'<div class="glass-card"><h1>{txt["t"]}</h1><p>{txt["sub"]}</p></div>', unsafe_allow_html=True)
st.write("")

# إعداد الذكاء الاصطناعي
genai.configure(api_key="AIzaSyC9v9vX4ioZm8PKttNwefL7QuOKXAaiFfk")
model = genai.GenerativeModel('gemini-1.5-flash')

# رفع الملف
uploaded_file = st.file_uploader(txt['up'], type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, use_column_width=True)
    
    if st.button(txt['btn']):
        with st.spinner(txt['wait']):
            try:
                response = model.generate_content([txt['prompt'], img])
                res_text = response.text
                st.success("✅ Done!")
                st.markdown(f"### {txt['res']}")
                st.markdown(res_text)
                
                # أزرار التحميل
                st.divider()
                st.write(txt['dl'])
                
                # دالة بسيطة للتحميل (Word)
                doc = Document()
                doc.add_paragraph(res_text)
                doc_io = BytesIO()
                doc.save(doc_io)
                
                st.download_button("Word (DOCX)", data=doc_io.getvalue(), file_name="data.docx")
            except Exception as e:
                st.error(f"Error: {e}")
                ص
