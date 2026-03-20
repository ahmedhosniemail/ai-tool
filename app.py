import streamlit as st
import google.generativeai as genai
from PIL import Image

# إعداد المفتاح
API_KEY = "AIzaSyC9v9vX4ioZm8PKttNwefL7QuOKXAaiFfk"
genai.configure(api_key=API_KEY)

# استخدام الإصدار الأكثر استقراراً لتجنب خطأ 404
model = genai.GenerativeModel('gemini-1.5-flash-latest')

st.set_page_config(page_title="Ahmed AI Extractor", layout="centered")
st.title("🤖 مستخرج البيانات الذكي - أحمد حسني")

uploaded_file = st.file_uploader("ارفع صورة الجدول أو الفاتورة", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="📸 الصورة المرفوعة", use_column_width=True)
    
    if st.button("🚀 ابدأ تحليل البيانات الآن"):
        with st.spinner("جاري قراءة البيانات بدقة..."):
            try:
                # طلب التحليل
                response = model.generate_content(["استخرج البيانات من هذه الصورة في شكل جدول", img])
                st.success("✅ تم التحليل بنجاح!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"تنبيه: {e}")
                س
