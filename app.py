import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
from io import BytesIO
from docx import Document
import re

# 1. إعدادات الصفحة والواجهة الملكية الناصعة
st.set_page_config(page_title="Ahmed AI Pro", page_icon="👑", layout="centered")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #f0f8ff 0%, #ffffff 100%); color: #1a253a; }
    .glass-container {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 20px; padding: 30px;
        border: 1px solid rgba(212, 175, 55, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        text-align: center; margin-bottom: 25px;
    }
    .company-logo { width: 120px; filter: drop-shadow(0 0 8px rgba(212, 175, 55, 0.4)); }
    div.stButton > button {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important;
        color: white !important; border-radius: 25px !important;
        font-weight: bold !important; width: 100%; height: 50px;
    }
</style>
""", unsafe_allow_html=True)

# 2. إعدادات اللغات (التي اختفت في نسختك السابقة)
translations = {
    'العربية': {
        'title': 'AHMED AI PRO',
        'sub': 'المستخرج الذكي الملكي | Excel, Word, PDF',
        'up': '📂 ارفع صورة الجدول أو الفاتورة (JPG/PNG)',
        'btn': '🚀 ابدأ التحليل الملكي الآن',
        'res': '📊 البيانات المستخرجة:',
        'dl': '⬇️ تحميل النتائج الفاخرة:',
        'prompt': 'Extract data from this image into a clean Markdown table.'
    },
    'English': {
        'title': 'AHMED AI PRO',
        'sub': 'Royal Smart Extractor | Excel, Word, PDF',
        'up': '📂 Upload Table or Invoice Image',
        'btn': '🚀 Start Royal Analysis',
        'res': '📊 Extracted Data:',
        'dl': '⬇️ Download Premium Results:',
        'prompt': 'Extract data from this image into a clean Markdown table.'
    }
}

selected_lang = st.sidebar.selectbox("🌐 Language / اللغة", list(translations.keys()))
lang = translations[selected_lang]

# 3. الواجهة الرئيسية والشعار
st.markdown(f"""
<div class="glass-container">
    <img src="https://cdn-icons-png.flaticon.com/512/9167/9167196.png" class="company-logo">
    <h1 style='color: #1a253a;'>{lang['title']}</h1>
    <p style='color: #7f8c8d;'>{lang['sub']}</p>
</div>
""", unsafe_allow_html=True)

# 4. الربط مع الموديل (تم تصحيح اسم الموديل لتجنب خطأ 404)
genai.configure(api_key="AIzaSyC9v9vX4ioZm8PKttNwefL7QuOKXAaiFfk")
model = genai.GenerativeModel('gemini-1.5-flash')

# 5. دوال المعالجة (الصور الكبيرة + الملفات)
def resize_image(image_file):
    img = Image.open(image_file).convert('RGB')
    if img.size[0] > 2000 or img.size[1] > 2000:
        img.thumbnail((2000, 2000), Image.Resampling.LANCZOS)
    return img

def to_excel(text):
    try:
        tables = re.findall(r'\|.*\|', text)
        data = [row.strip('|').split('|') for row in tables if '-' not in row]
        df = pd.DataFrame(data[1:], columns=data[0])
        out = BytesIO()
        with pd.ExcelWriter(out, engine='xlsxwriter') as w:
            df.to_excel(w, index=False)
        return out.getvalue()
    except: return None

# 6. منطقة التحميل والتشغيل
file = st.file_uploader(lang['up'], type=['jpg', 'jpeg', 'png'])

if file:
    proc_img = resize_image(file)
    st.image(proc_img, use_column_width=True)
    
    if st.button(lang['btn']):
        with st.spinner("🧠 جاري المعالجة..."):
            try:
                response = model.generate_content([lang['prompt'], proc_img])
                res_text = response.text
                st.success("✅ تم بنجاح!")
                st.markdown(f"### {lang['res']}")
                st.markdown(res_text)
                
                st.divider()
                st.subheader(lang['dl'])
                c1, c2 = st.columns(2)
                
                ex_data = to_excel(res_text)
                if ex_data:
                    c1.download_button("📊 Excel (XLSX)", ex_data, "data.xlsx")
                
                doc = Document()
                doc.add_paragraph(res_text)
                w_io = BytesIO()
                doc.save(w_io)
                c2.download_button("📝 Word (DOCX)", w_io.getvalue(), "data.docx")
                
            except Exception as e:
                st.error(f"Error: {e}")
                
