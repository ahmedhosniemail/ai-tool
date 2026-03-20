import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
from io import BytesIO
from docx import Document
from fpdf import FPDF
import re

# إعدادات الصفحة والواجهة الفاتحة
st.set_page_config(page_title="Ahmed AI Pro", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; color: #1a253a; }
    .main-header { text-align: center; padding: 20px; background: white; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 1px solid #d4af37; margin-bottom: 20px; }
    div.stButton > button { background: linear-gradient(135deg, #1e3c72, #2a5298) !important; color: white !important; border-radius: 10px !important; width: 100%; height: 50px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# خيار اللغات (في السايد بار لضمان عدم اختفائه)
st.sidebar.title("Settings / الإعدادات")
sel_lang = st.sidebar.selectbox("Language / اللغة", ["العربية", "English", "Français"])

# نصوص الواجهة
texts = {
    "العربية": {"title": "أحمد حسني - AI PRO", "up": "ارفع صورة (جدول/فاتورة)", "btn": "تحليل واستخراج", "dl": "تحميل النتائج:"},
    "English": {"title": "AHMED AI PRO", "up": "Upload Image (Table/Invoice)", "btn": "Analyze & Extract", "dl": "Download Results:"},
    "Français": {"title": "AHMED AI PRO", "up": "Charger une image", "btn": "Analyser", "dl": "Télécharger:"}
}
t = texts[sel_lang]

st.markdown(f'<div class="main-header"><h1>{t["title"]}</h1></div>', unsafe_allow_html=True)

# الربط مع الموديل (حل مشكلة 404)
genai.configure(api_key="AIzaSyC9v9vX4ioZm8PKttNwefL7QuOKXAaiFfk")
model = genai.GenerativeModel('gemini-1.5-flash')

# دوال التحميل
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=text.encode('latin-1', 'ignore').decode('latin-1'))
    return pdf.output(dest='S').encode('latin-1')

def create_excel(text):
    output = BytesIO()
    # تحويل بسيط جدا للجدول
    lines = [line.strip() for line in text.split('\n') if '|' in line]
    if lines:
        df = pd.DataFrame([l.split('|') for l in lines])
        df.to_excel(output, index=False, header=False)
    return output.getvalue()

# منطقة العمل
file = st.file_uploader(t["up"], type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, use_column_width=True)
    
    if st.button(t["btn"]):
        with st.spinner("🧠 جاري المعالجة..."):
            try:
                response = model.generate_content(["Extract data as table", img])
                res = response.text
                st.success("✅ تم!")
                st.markdown(res)
                
                st.divider()
                st.write(t["dl"])
                c1, c2, c3 = st.columns(3)
                
                with c1:
                    st.download_button("Excel", create_excel(res), "data.xlsx")
                with c2:
                    doc = Document()
                    doc.add_paragraph(res)
                    b = BytesIO()
                    doc.save(b)
                    st.download_button("Word", b.getvalue(), "data.docx")
                with c3:
                    st.download_button("PDF", create_pdf(res), "data.pdf")
                    
            except Exception as e:
                st.error(f"Error: {e}")
                
