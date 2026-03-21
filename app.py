import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات A.H
st.set_page_config(page_title="A.H AI Pro", page_icon="⚡")
st.markdown("<h2 style='text-align: center; color: #27ae60;'>A.H - فحص فوري ذكي 🥗</h2>", unsafe_allow_html=True)

# 2. الربط بالمفتاح
genai.configure(api_key="AIzaSyAt-pa38pTx0eFa7tGbEeEOpaZTwFYZ_n4")

# دالة ذكية لاكتشاف الموديل المتاح (تجنب الـ 404)
def get_working_model():
    try:
        # البحث عن أي موديل يدعم الصور في حسابك حالياً
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'flash' in m.name or 'pro' in m.name:
                    return genai.GenerativeModel(m.name)
        return genai.GenerativeModel('gemini-1.5-flash')
    except:
        return genai.GenerativeModel('gemini-pro-vision')

model = get_working_model()

# 3. الواجهة
file = st.file_uploader("📸 ارفع صورة المنتج", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, use_container_width=True)
    
    if st.button("🚀 تحليل المنتج الآن"):
        with st.spinner("⏳ جاري التحليل..."):
            try:
                # محاولة التحليل
                response = model.generate_content(["حلل مكونات الصورة والتقييم الصحي بالعربية", img])
                st.success("✅ النتيجة:")
                st.write(response.text)
                st.balloons()
            except Exception as e:
                st.error(f"خطأ في الاتصال بالسيرفر. يرجى عمل Reboot للتطبيق.")
                
