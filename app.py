import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
from io import BytesIO
from docx import Document

# 1. إعدادات الصفحة واللغة
st.set_page_config(page_title="Ahmed AI Pro", layout="centered")

# القائمة الجانبية للغات (لضمان عدم اختفائها)
st.sidebar.title("Settings / الإعدادات")
lang_choice = st.sidebar.selectbox("Language / اللغة", ["العربية", "English"])

texts = {
    "العربية": {"title": "أحمد حسني - AI PRO", "up": "ارفع الصورة هنا", "btn": "تحليل واستخراج", "res": "النتائج:"},
    "English": {"title": "AHMED AI PRO", "up": "Upload Image", "btn": "Analyze & Extract", "res": "Results:"}
}
t = texts[lang_choice]

st.title(t["title"])

# 2. الحل الجذري لخطأ 404 (تغيير طريقة التعريف)
genai.configure(api_key="AIzaSyC9v9vX4ioZm8PKttNwefL7QuOKXAaiFfk")

# مصفوفة تجريبية لضمان عمل الموديل الصحيح
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = genai.GenerativeModel('gemini-pro-vision') # حل احتياطي

# 3. معالجة الصور والتحليل
file = st.file_uploader(t["up"], type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, use_column_width=True)
    
    if st.button(t["btn"]):
        with st.spinner("🧠 جاري المعالجة..."):
            try:
                # إرسال الطلب
                response = model.generate_content(["Extract all table data clearly", img])
                result = response.text
                
                st.success("✅ تم الاستخراج")
                st.markdown(f"### {t['res']}")
                st.markdown(result)
                
                # أزرار التحميل
                st.divider()
                col1, col2 = st.columns(2)
                
                # Excel
                with col1:
                    st.download_button("Excel", result.encode('utf-8'), "data.csv")
                
                # Word
                with col2:
                    doc = Document()
                    doc.add_paragraph(result)
                    b = BytesIO()
                    doc.save(b)
                    st.download_button("Word", b.getvalue(), "data.docx")
                    
            except Exception as e:
                st.error(f"حدث خطأ في الموديل: {e}")
                
