import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الهوية A.H
st.set_page_config(page_title="A.H AI Pro", page_icon="⚡")

# 2. الربط بالمفتاح الجديد وتجهيز الموديل
genai.configure(api_key="AIzaSyAt-pa38pTx0eFa7tGbEeEOpaZTwFYZ_n4")
model = genai.GenerativeModel('gemini-1.5-flash')

# تنسيق الواجهة
st.markdown("<h2 style='text-align: center; color: #27ae60;'>A.H - فحص فوري ذكي 🥗</h2>", unsafe_allow_html=True)

# 3. واجهة المستخدم
file = st.file_uploader("📸 ارفع صورة المنتج الآن", type=["jpg", "png", "jpeg"])

if file:
    image = Image.open(file)
    st.image(image, use_container_width=True)
    
    if st.button("🚀 ابدأ التحليل الفوري"):
        with st.spinner("⚡ جاري استخراج البيانات..."):
            try:
                # طلب التحليل المباشر من الموديل
                response = model.generate_content([
                    "Analyze this food image in Arabic. Mention ingredients, calories, and health rating.", 
                    image
                ])
                st.markdown("---")
                st.success("✅ التقرير جاهز:")
                st.write(response.text)
                st.balloons()
            except Exception as e:
                st.error(f"حدث خطأ بسيط: {str(e)}")
                st.info("اضغط على الزر مرة أخرى، أحياناً يحتاج السيرفر لدفعة ثانية.")

st.markdown("---")
st.caption("Developed by A.H AI Pro © 2026")
