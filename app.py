import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الصفحة (تصميم فاتح وبسيط جداً)
st.set_page_config(page_title="Ahmed AI", layout="centered")

# 2. خيار اللغة (في القائمة الجانبية)
st.sidebar.title("Settings")
lang = st.sidebar.selectbox("Language / اللغة", ["العربية", "English"])

# 3. نصوص الواجهة
txt = {
    "العربية": {"title": "أحمد حسني - AI", "up": "ارفع صورة", "btn": "تحليل"},
    "English": {"title": "Ahmed AI Pro", "up": "Upload Image", "btn": "Analyze"}
}[lang]

st.title(txt["title"])

# 4. الربط مع الذكاء الاصطناعي (Gemini 1.5 Flash)
genai.configure(api_key="AIzaSyC9v9vX4ioZm8PKttNwefL7QuOKXAaiFfk")
model = genai.GenerativeModel('gemini-1.5-flash')

# 5. منطقة العمل
file = st.file_uploader(txt["up"], type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, use_column_width=True)
    
    if st.button(txt["btn"]):
        with st.spinner("..."):
            try:
                # التحليل
                response = model.generate_content(["Extract data as a table", img])
                st.markdown("### Results:")
                st.write(response.text)
                
                # أزرار التحميل (بسيطة جداً كبداية لضمان عمل الموقع)
                st.download_button("Download Text", response.text, "data.txt")
            except Exception as e:
                st.error(f"Error: {e}")
                
