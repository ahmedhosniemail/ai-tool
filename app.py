import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الهوية A.H
st.set_page_config(page_title="A.H Nutri-Scan", page_icon="🥗")

st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .header-box {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
        padding: 20px; border-radius: 15px; color: white; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# 2. الربط واكتشاف الموديل تلقائياً
genai.configure(api_key="AIzaSyASr5PjZL2LrY4bXfZ7d4kd265rUhrin4E")

def find_working_model():
    # يبحث في حسابك عن أي موديل يدعم الرؤية (Vision)
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            # نفضل استخدام flash إذا كان متاحاً لسرعته
            if 'flash' in m.name:
                return genai.GenerativeModel(m.name)
    # إذا لم يجد flash، يأخذ أول موديل متاح
    return genai.GenerativeModel('gemini-1.5-flash')

model = find_working_model()

# 3. واجهة المستخدم
with st.sidebar:
    lang = st.selectbox("🌐 Language", ["العربية", "English"])

t = {
    "العربية": ["A.H - ماسح التغذية", "📸 ارفع صورة المنتج", "🔍 تحليل الآن", "أنت خبير تغذية، حلل الصورة بدقة."],
    "English": ["A.H - Nutri-Scan", "📸 Upload Image", "🔍 Analyze Now", "Expert Nutritionist: Analyze this image."]
}[lang]

st.markdown(f'<div class="header-box"><h1>{t[0]}</h1></div>', unsafe_allow_html=True)

file = st.file_uploader(t[1], type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, use_container_width=True)
    
    if st.button(t[2]):
        with st.spinner("⏳ جاري التحليل..."):
            try:
                # التحليل باستخدام الموديل الذي تم اكتشافه
                response = model.generate_content([t[3], img])
                st.markdown("---")
                st.success(response.text)
            except Exception as e:
                st.error(f"عذراً، يرجى المحاولة مرة أخرى: {e}")

st.markdown("---")
st.caption("Developed by A.H AI Pro © 2026")
