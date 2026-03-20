import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
from io import BytesIO
from docx import Document
from fpdf import FPDF
import re

# ==========================================
# 1. إعدادات الصفحة والواجهة الفاتحة الملكية
# ==========================================
st.set_page_config(page_title="Ahmed AI Pro", page_icon="👑", layout="centered")

st.markdown("""
<style>
    /* خلفية سماوية فاتحة وناصعة لراحة القراءة */
    .stApp {
        background: linear-gradient(135deg, #f0f8ff 0%, #ffffff 100%);
        color: #1a253a;
    }
    .main-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid #d4af37; /* إطار ذهبي خفيف كشعار الأندية */
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
    }
    .logo-img {
        width: 150px;
        margin-bottom: 20px;
    }
    h1 { color: #1a253a; font-family: 'Cairo', sans-serif; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. الواجهة والشعار (الاحترافي 3D)
# ==========================================
st.markdown("""
<div class="main-card">
    <img src="https://cdn-icons-png.flaticon.com/512/9167/9167196.png" class="logo-img">
    <h1>AHMED AI PRO | SMART DATA EXTRACTOR</h1>
    <p>Extracting Valuable Data from Images to Excel/Word/PDF</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 3. إعدادات الموديل (تأكد من المفتاح الخاص بك)
# ==========================================
genai.configure(api_key="AIzaSyC9v9vX4ioZm8PKttNwefL7QuOKXAaiFfk")
model = genai.GenerativeModel('gemini-1.5-flash')

# ==========================================
# 4. وظائف التحميل (PDF / Word / Excel)
# ==========================================
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # تنظيف النص من الرموز التي لا يدعمها PDF البسيط
    clean_text = text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_text)
    return pdf.output(dest='S').encode('latin-1')

# ==========================================
# 5. منطقة العمل
# ==========================================
uploaded_file = st.file_uploader("📂 ارفع صورة الجدول، الفاتورة، أو البطاقة (JPG/PNG)", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, use_column_width=True)
    
    if st.button("🚀 ابدأ تحليل واستخراج البيانات الآن"):
        with st.spinner("🧠 جاري المعالجة..."):
            try:
                response = model.generate_content(["Extract data into a table format", img])
                result = response.text
                st.success("✅ تم الاستخراج!")
                st.markdown("### 📊 البيانات المستخرجة:")
                st.markdown(result)
                
                # خيارات التحميل
                st.divider()
                st.markdown("### 📥 تحميل النتائج:")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.download_button("تحميل كملف Excel", data=result.encode('utf-8'), file_name="data.csv")
                with col2:
                    st.download_button("تحميل كملف Word", data=result.encode('utf-8'), file_name="data.doc")
                with col3:
                    pdf_data = create_pdf(result)
                    st.download_button("تحميل كملف PDF", data=pdf_data, file_name="data.pdf", mime="application/pdf")
            
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
                
