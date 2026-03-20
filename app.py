import streamlit as st
import google.generativeai as genai
from PIL import Image

# إعداد المفتاح والموديل
API_KEY = "AIzaSyC9v9vX4ioZm8PKttNwefL7QuOKXAaiFfk"
genai.configure(api_key=API_KEY)

# استخدام أحدث موديل مستقر
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Ahmed AI Extractor", layout="centered")
st.title("🤖 مستخرج البيانات الذكي - أحمد حسني")

uploaded_file = st.file_uploader("ارفع صورة الجدول أو الفاتورة", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="📸 الصورة التي رفعتها", use_column_width=True)
    
    if st.button("🚀 ابدأ تحليل البيانات الآن"):
        with st.spinner("جاري قراءة الصورة بدقة..."):
            try:
                # الأمر السحري للذكاء الاصطناعي
                prompt = "استخرج جميع البيانات الموجودة في هذه الصورة بدقة ونسقها في جدول. إذا كانت باللغة الفرنسية أو العربية اتركها كما هي."
                response = model.generate_content([prompt, img])
                
                st.success("✅ تم التحليل بنجاح!")
                st.markdown("### 📊 البيانات المستخرجة:")
                st.write(response.text)
            except Exception as e:
                st.error(f"حدث خطأ بسيط: {e}")
                st.info("نصيحة: تأكد من تحديث ملف requirements.txt")
                2
