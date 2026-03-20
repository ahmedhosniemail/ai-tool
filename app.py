import streamlit as st
import google.generativeai as genai
from PIL import Image

# إعدادات المحرك
API_KEY = "AIzaSyC9v9vX4ioZm8PKttNwefL7QuOKXAaiFfk"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 مستخرج البيانات الذكي - أحمد حسني")

uploaded_file = st.file_uploader("ارفع صورة الجدول أو الفاتورة", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="📸 الصورة المرفوعة")
    
    if st.button("🚀 استخراج البيانات الآن"):
        with st.spinner("جاري التحليل..."):
            try:
                # طلب بسيط ومباشر
                response = model.generate_content(["اقرأ هذه الصورة واستخرج البيانات منها في جدول", img])
                st.success("✅ تم التحليل!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
                
