import streamlit as st
import google.generativeai as genai
from PIL import Image

# إعدادات واجهة A.H
st.set_page_config(page_title="A.H AI Pro", page_icon="⚡")
st.markdown("<h2 style='text-align: center; color: #27ae60;'>A.H - فحص فوري ذكي 🥗</h2>", unsafe_allow_html=True)

# الربط بالمفتاح الجديد الفعال
API_KEY = "AIzaSyAt-pa38pTx0eFa7tGbEeEOpaZTwFYZ_n4"
genai.configure(api_key=API_KEY)

# استخدام الموديل المستقر
model = genai.GenerativeModel('gemini-1.5-flash')

# رفع الصورة
file = st.file_uploader("📸 ارفع صورة المنتج", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, use_container_width=True)
    
    if st.button("🚀 تحليل المنتج الآن"):
        with st.spinner("⏳ جاري سحب البيانات..."):
            try:
                # طلب التحليل بصيغة بسيطة جداً
                response = model.generate_content(["Briefly analyze this food image in Arabic", img])
                if response:
                    st.markdown("---")
                    st.success("✅ النتيجة:")
                    st.write(response.text)
                    st.balloons()
            except Exception as e:
                st.error("السيرفر يحتاج لدفعة ثانية. اضغط على الزر مرة أخرى فوراً.")
                
