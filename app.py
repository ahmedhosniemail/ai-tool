import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الصفحة A.H
st.set_page_config(page_title="A.H Nutri-Scan", page_icon="🥗")

st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .header-box {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
        padding: 25px; border-radius: 15px; color: white; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    lang = st.selectbox("🌐 Language", ["العربية", "English"])

# الربط بالمفتاح
genai.configure(api_key="AIzaSyASr5PjZL2LrY4bXfZ7d4kd265rUhrin4E")

# 2. دالة ذكية لاختيار الموديل المتاح تلقائياً
def get_model():
    # نحاول أولاً مع الموديل الأحدث، ثم الأقدم، حتى ينجح واحد
    models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro-vision']
    for m_name in models_to_try:
        try:
            m = genai.GenerativeModel(m_name)
            # تجربة وهمية للتأكد من وجود الموديل
            return m
        except:
            continue
    return genai.GenerativeModel('gemini-1.5-flash-latest')

model = get_model()

# نصوص الواجهة
t = {
    "العربية": ["A.H - ماسح التغذية", "📸 ارفع صورة المنتج", "🔍 ابدأ التحليل", "حلل الصورة بدقة"],
    "English": ["A.H - Nutri-Scan", "📸 Upload Product", "🔍 Analyze Now", "Analyze this image"]
}[lang]

st.markdown(f'<div class="header-box"><h1>{t[0]}</h1></div>', unsafe_allow_html=True)

file = st.file_uploader(t[1], type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, use_container_width=True)
    
    if st.button(t[2]):
        with st.spinner("⏳..."):
            try:
                # إرسال التحليل
                response = model.generate_content([t[3], img])
                st.success(response.text)
            except Exception as e:
                st.error("جاري التبديل للموديل الاحتياطي...")
                # محاولة أخيرة بموديل عام
                fallback = genai.GenerativeModel('gemini-1.5-flash-8b')
                res = fallback.generate_content([t[3], img])
                st.success(res.text)

st.markdown("---")
st.caption("Developed by A.H AI Pro © 2026")
