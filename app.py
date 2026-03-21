import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الهوية A.H
st.set_page_config(page_title="A.H AI Pro", page_icon="⚡")

# 2. الربط المباشر بالمفتاح الجديد
# تم استخدام المفتاح: AIzaSyAt-pa38pTx0eFa7tGbEeEOpaZTwFYZ_n4
genai.configure(api_key="AIzaSyAt-pa38pTx0eFa7tGbEeEOpaZTwFYZ_n4")

# استخدام اسم الموديل الأكثر شمولية لتجنب خطأ 404
model = genai.GenerativeModel('gemini-pro-vision')

# تصميم الواجهة
st.markdown("<h2 style='text-align: center; color: #27ae60;'>A.H - الفحص الذكي 🥗</h2>", unsafe_allow_html=True)
# 3. واجهة الرفع
file = st.file_uploader("📸 ارفع صورة المنتج", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, use_container_width=True)
    
    if st.button("🚀 تحليل المنتج الآن"):
        with st.spinner("⏳ جاري استخراج البيانات..."):
            try:
                # طلب بسيط ومباشر
                res = model.generate_content(["حلل مكونات الصورة والتقييم الصحي بالعربية", img])
                st.markdown("---")
                st.success("✅ تم التحليل:")
                st.write(res.text)
                st.balloons()
            except Exception as e:
                # إذا فشل الموديل الأول، الكود سينتقل تلقائياً للموديل البديل فوراً
                try:
                    alt_model = genai.GenerativeModel('gemini-1.5-flash-latest')
                    res = alt_model.generate_content(["حلل الصورة بالعربية", img])
                    st.success("✅ تم التحليل (نسخة احتياطية):")
                    st.write(res.text)
                except:
                    st.error("السيرفر يحتاج لتحديث يدوي: اذهب إلى Manage App ثم Reboot.")

st.markdown("---")
st.caption("Developed by A.H AI Pro © 2026")
