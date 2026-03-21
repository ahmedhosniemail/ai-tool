import streamlit as st
import google.generativeai as genai
from PIL import Image

# إعدادات الواجهة (Apple Health Style)
st.set_page_config(page_title="Nutri-Scan 2026", page_icon="🥗")

# القائمة الجانبية للغات
with st.sidebar:
    lang = st.selectbox("🌐 Language", ["العربية", "English"])

# الربط مع الـ API
genai.configure(api_key="AIzaSyC9v9vX4ioZm8PKttNwefL7QuOKXAaiFfk")

# دالة ذكية لاختيار الموديل المتاح لتجنب خطأ 404
def get_working_model():
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # نفضل flash إذا كان متاحاً، وإلا نأخذ أول موديل رؤية (Vision) متاح
    for target in ['models/gemini-1.5-flash', 'models/gemini-pro-vision']:
        if target in available_models:
            return genai.GenerativeModel(target)
    return genai.GenerativeModel(available_models[0]) if available_models else None

model = get_working_model()

# نصوص الواجهة
t = {
    "العربية": {"h": "ماسح التغذية الذكي", "btn": "تحليل الصحة"},
    "English": {"h": "Nutri-Scan AI", "btn": "Analyze Health"}
}[lang]

st.title(t["h"])

file = st.file_uploader("📸", type=["jpg", "png", "jpeg"])

if file and model:
    img = Image.open(file)
    st.image(img)
    if st.button(t["btn"]):
        with st.spinner("⏳"):
            response = model.generate_content(["Is this food healthy? analyze ingredients", img])
            st.success(response.text)
            
