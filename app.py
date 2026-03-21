import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 1. إعدادات الهوية A.H - منع التخزين المؤقت للأخطاء
st.set_page_config(page_title="A.H AI Pro", page_icon="⚡")

# 2. الربط الإجباري بالمفتاح الجديد
# تأكد من أن هذا هو المفتاح: AIzaSyAt-pa38pTx0eFa7tGbEeEOpaZTwFYZ_n4
API_KEY = "AIzaSyAt-pa38pTx0eFa7tGbEeEOpaZTwFYZ_n4"
genai.configure(api_key=API_KEY)

# استخدام الموديل المستقر "فقط" لتجنب خطأ 404
model = genai.GenerativeModel('gemini-1.5-flash')

st.markdown("<h2 style='text-align: center; color: #2ecc71;'>A.H - فحص فوري نهائي 🥗</h2>", unsafe_allow_html=True)

# 3. واجهة المستخدم
file = st.file_uploader("📸 ارفع صورة المنتج", type=["jpg", "png", "jpeg"], key="ah_uploader")

if file:
    img = Image.open(file)
    st.image(img, use_container_width=True)
    
    if st.button("🚀 تحليل المنتج الآن", key="ah_button"):
        with st.spinner("⏳ جاري سحب البيانات مباشرة من جوجل..."):
            try:
                # محاولة التحليل - هيكلة الطلب بأبسط صورة ممكنة
                response = model.generate_content(["Describe this food nutrition in Arabic", img])
                
                if response:
                    st.markdown("---")
                    st.success("✅ النتيجة جاهزة للعميل:")
                    st.write(response.text)
                    st.balloons()
            except Exception as e:
                # إذا فشل، الكود سيعطيه تعليمات واضحة بدلاً من رسالة حمراء
                st.error("⚠️ تنبيه تقني: السيرفر يحتاج لضغطة 'تحديث' (Refresh) من المتصفح.")
                st.info("اضغط F5 أو اسحب الشاشة للأسفل وجرب مرة أخرى.")

st.markdown("---")
st.caption("A.H AI Pro - 2026 Ultimate Edition")
