import streamlit as st
import google.generativeai as genai
from PIL import Image

# إعداد المفتاح
API_KEY = "AIzaSyC9v9vX4ioZm8PKttNwefL7QuOKXAaiFfk"
genai.configure(api_key=API_KEY)

# استخدام الموديل المستقر (تحديث الاسم لتجنب خطأ 404)
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Ahmed AI Extractor", layout="centered")
st.title("🤖 مستخرج البيانات الذكي - أحمد حسني")

uploaded_file = st.file_uploader("ارفع صورة الجدول أو الفاتورة", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="📸 الصورة المرفوعة", use_column_width=True)
    
    if st.button("🚀 ابدأ تحليل البيانات الآن"):
        with st.spinner("جاري قراءة البيانات..."):
            try:
                # طلب التحليل من الذكاء الاصطناعي
                prompt = "استخرج كل البيانات من هذه الصورة ونظمها في جدول احترافي."
                response = model.generate_content([prompt, img])
                
                st.success("✅ اكتمل التحليل!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"خطأ تقني: {e}")
                
