import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الهوية A.H
st.set_page_config(page_title="A.H Smart Scan", page_icon="⚡")

st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .header-box {
        background: #27ae60; padding: 20px; 
        border-radius: 15px; color: white; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# 2. الربط واكتشاف الموديل الفعال تلقائياً
API_KEY = "AIzaSyASr5PjZL2LrY4bXfZ7d4kd265rUhrin4E"
genai.configure(api_key=API_KEY)

@st.cache_resource
def load_active_model():
    # يبحث الكود هنا عن أي موديل متاح في حسابك يدعم تحليل الصور
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # يختار الموديل الأنسب (flash أو pro) المتاح حالياً
    for name in available_models:
        if "1.5-flash" in name: return genai.GenerativeModel(name)
    if available_models: return genai.GenerativeModel(available_models[0])
    return genai.GenerativeModel('gemini-1.5-flash') # fallback

model = load_active_model()

st.markdown('<div class="header-box"><h1>A.H - التحليل الذكي 🥗</h1></div>', unsafe_allow_html=True)

# 3. واجهة المستخدم
file = st.file_uploader("📸 ارفع صورة المنتج", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, use_container_width=True)
    
    if st.button("🚀 تحليل فوري للعميل"):
        with st.spinner("⚡ جاري استخراج النتائج..."):
            try:
                # التحليل باستخدام الموديل الذي اكتشفه الكود
                response = model.generate_content(["حلل الصورة باللغة العربية: السعرات، السكر، والتقييم الصحي.", img])
                st.markdown("---")
                st.success("✅ النتيجة جاهزة:")
                st.write(response.text)
                st.balloons()
            except Exception as e:
                st.error(f"تنبيه: السيرفر يحتاج لتحديث بسيط. اضغط Reboot من القائمة.")

st.markdown("---")
st.caption("A.H Pro AI Solution © 2026")
