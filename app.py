import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# 1. إعدادات A.H
st.set_page_config(page_title="A.H AI Pro", page_icon="🥗")
genai.configure(api_key="AIzaSyAt-pa38pTx0eFa7tGbEeEOpaZTwFYZ_n4")

# 2. تهيئة الموديل
model = genai.GenerativeModel('gemini-1.5-flash')

st.markdown("<h2 style='text-align: center;'>🥗 A.H - فحص ذكي</h2>", unsafe_allow_html=True)

file = st.file_uploader("ارفع الصورة", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, use_container_width=True)
    
    if st.button("🚀 تحليل الآن"):
        placeholder = st.empty()
        placeholder.info("⏳ جاري الاتصال المباشر بالسيرفر...")
        
        # محاولة التحليل مع نظام إعادة المحاولة التلقائي
        success = False
        for i in range(3): # سيحاول 3 مرات تلقائياً إذا كان مشغولاً
            try:
                response = model.generate_content(["Briefly analyze this food image in Arabic", img])
                placeholder.empty()
                st.success("✅ النتيجة:")
                st.write(response.text)
                st.balloons()
                success = True
                break
            except Exception as e:
                placeholder.warning(f"محاولة اتصال {i+1}/3... انتظر لحظة")
                time.sleep(2) # انتظار ثانيتين قبل الإعادة
        
        if not success:
            st.error("السيرفر يحتاج لإعادة تشغيل (Reboot) من لوحة التحكم.")
            
