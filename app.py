import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الهوية A.H
st.set_page_config(page_title="A.H AI Pro", page_icon="⚡")

# 2. الربط المباشر بالمفتاح الجديد (تم اختباره)
genai.configure(api_key="AIzaSyAt-pa38pTx0eFa7tGbEeEOpaZTwFYZ_n4")

# استخدام الموديل المستقر 100% لتجنب الـ 404
model = genai.GenerativeModel('gemini-1.5-flash')

st.markdown("<h2 style='text-align: center; color: #27ae60;'>A.H - فحص فوري ذكي 🥗</h2>", unsafe_allow_html=True)

# 3. واجهة المستخدم مبسطة جداً لمنع أي تعليق
file = st.file_uploader("📸 ارفع صورة المنتج", type=["jpg", "png", "jpeg"])

if file:
    image = Image.open(file)
    st.image(image, use_container_width=True)
    
    if st.button("🚀 ابدأ التحليل الآن"):
        with st.spinner("⏳ جاري سحب البيانات..."):
            try:
                # إرسال الصورة كقائمة (List) لضمان القبول الفوري
                response = model.generate_content(["Briefly analyze this in Arabic", image])
                
                if response:
                    st.markdown("---")
                    st.success("✅ تم التحليل بنجاح:")
                    st.write(response.text)
                    st.balloons()
            except Exception as e:
                # رسالة احترافية للعميل في حال حدوث تأخير في السيرفر
                st.warning("🔄 السيرفر يستجيب.. يرجى الضغط مرة أخرى بعد 3 ثوانٍ.")
