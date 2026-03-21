import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# 1. إعدادات سريعة A.H
st.set_page_config(page_title="A.H Quick Scan", page_icon="⚡")

# 2. الربط (تأكد من عدم وجود مسافات في المفتاح)
API_KEY = "AIzaSyASr5PjZL2LrY4bXfZ7d4kd265rUhrin4E"
genai.configure(api_key=API_KEY)

# استخدام الموديل الأكثر استجابة للطلبات السريعة
model = genai.GenerativeModel('gemini-1.5-flash')

st.markdown("<h1 style='text-align: center; color: #27ae60;'>A.H - فحص فوري 🚀</h1>", unsafe_allow_html=True)

file = st.file_uploader("📸 ارفع الصورة الآن", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, use_container_width=True)
    
    if st.button("🔍 تحليل فوري"):
        placeholder = st.empty()
        placeholder.info("⚡ جاري الاتصال المباشر بالسيرفر...")
        
        # محاولة التحليل 3 مرات متتالية في ثوانٍ بسيطة لتجاوز الرفض المؤقت
        success = False
        for i in range(3):
            try:
                response = model.generate_content(["Analysis this food image", img])
                placeholder.success("✅ تم التحليل بنجاح!")
                st.write(response.text)
                success = True
                break
            except Exception as e:
                placeholder.warning(f"🔄 محاولة اتصال رقم {i+1}...")
                time.sleep(1) # انتظار ثانية واحدة فقط
        
        if not success:
            st.error("❌ السيرفر مشغول حالياً. جرب الضغط على الزر مرة أخرى.")

st.markdown("---")
st.caption("A.H AI Pro - Fast Response Edition 2026")
