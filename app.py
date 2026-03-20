import streamlit as st
import google.generativeai as genai
from PIL import Image

# إعداد المحرك بمفتاحك الذي استخرجته للتو
genai.configure(api_key="AIzaSyC9v9vX4ioZm8PKttNwefL7QuOKXAaiFfk")
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Ahmed AI Pro", layout="centered")
st.title("🤖 مستخرج البيانات الذكي - أحمد حسني")
st.write("ارفع صورة فاتورة أو وثيقة وسأقوم بتحليلها لك فوراً")

uploaded_file = st.file_uploader("اختر صورة (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="📸 الصورة المرفوعة", use_column_width=True)
    
    if st.button("🚀 استخراج البيانات الآن"):
        with st.spinner("جاري القراءة والتحليل..."):
            try:
                # أمر الذكاء الاصطناعي
                response = model.generate_content(["اقرأ هذه الصورة واستخرج البيانات المهمة منها في جدول واشرح المحتوى باختصار.", img])
                st.success("✅ تم التحليل!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
                
