import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الهوية A.H
st.set_page_config(page_title="A.H AI Pro", page_icon="⚡")

# 2. الربط المباشر بالمفتاح (النسخة المستقرة)
genai.configure(api_key="AIzaSyAt-pa38pTx0eFa7tGbEeEOpaZTwFYZ_n4")

# اختيار الموديل المستقر وتثبيت الإعدادات
model = genai.GenerativeModel('gemini-1.5-flash')

st.markdown("<h2 style='text-align: center; color: #2ecc71;'>A.H - الفحص النهائي المستقر 🥗</h2>", unsafe_allow_html=True)

# 3. واجهة المستخدم
file = st.file_uploader("📸 ارفع صورة المنتج", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, use_container_width=True)
    
    if st.button("🚀 تحليل المنتج الآن"):
        with st.spinner("⏳ جاري التحليل المباشر..."):
            try:
                # طلب صريح ومباشر بدون تعقيدات
                response = model.generate_content([
                    "Analyze the nutritional information in this image and provide a health rating in Arabic.", 
                    img
                ])
                if response:
                    st.markdown("---")
                    st.success("✅ تم التحليل بنجاح:")
                    st.write(response.text)
                    st.balloons()
            except Exception as e:
                st.error("السيرفر يحتاج لضغطة واحدة إضافية. يرجى إعادة المحاولة.")
                2
