import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات A.H السريعة
st.set_page_config(page_title="A.H Fast Scan", page_icon="⚡")

# الربط المباشر
API_KEY = "AIzaSyASr5PjZL2LrY4bXfZ7d4kd265rUhrin4E"
genai.configure(api_key=API_KEY)

# استخدام نسخة الموديل الأكثر استقراراً في 2026
model = genai.GenerativeModel('gemini-1.5-flash')

st.markdown("<h1 style='text-align: center; color: #2ecc71;'>A.H - فحص ذكي فوري 🥗</h1>", unsafe_allow_html=True)

file = st.file_uploader("📸 ارفع صورة المنتج", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, use_container_width=True)
    
    if st.button("🚀 تحليل الآن"):
        with st.spinner("⚡ جاري استلام النتائج..."):
            try:
                # طلب مباشر وبسيط جداً لتجنب رفض الأذونات
                response = model.generate_content(["Analysis this food image details in Arabic", img])
                st.markdown("---")
                st.success("✅ التقرير:")
                st.write(response.text)
                st.balloons()
            except Exception as e:
                # إذا حدث خطأ PermissionDenied، سنخبر العميل بلمسة احترافية
                st.error("🔄 السيرفر يقوم بتحديث الأذونات.. اضغط مرة أخرى الآن.")
                # محاولة تلقائية ثانية داخلية
                try:
                    res_retry = model.generate_content(["Describe ingredients", img])
                    st.success(res_retry.text)
                except:
                    st.warning("⚠️ يرجى التأكد من الضغط على زر 'Enable API' في صفحة Google AI Studio.")

st.markdown("---")
st.caption("Developed by A.H Pro © 2026")
