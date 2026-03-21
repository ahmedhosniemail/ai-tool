import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ahmed Nutri-Scan 2026", page_icon="🥗", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #ffffff; color: #2c3e50; }
    .header-box {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
        padding: 30px; border-radius: 20px; color: white;
        text-align: center; margin-bottom: 25px;
        box-shadow: 0 10px 20px rgba(46, 204, 113, 0.2);
    }
    div.stButton > button {
        background: #27ae60 !important; color: white !important;
        border-radius: 12px !important; font-weight: bold !important;
        height: 50px; width: 100%; border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. القائمة الجانبية
with st.sidebar:
    st.markdown("### ⚙️ الإعدادات / Settings")
    lang = st.selectbox("🌐 اختر لغة التحليل:", ["العربية", "English"])

# 3. محتوى اللغات (تم تصحيح علامات التنصيص هنا)
content = {
    "العربية": {
        "title": "أحمد - ماسح التغذية الذكي",
        "sub": "حلل جودة طعامك فوراً باستخدام الذكاء الاصطناعي",
        "up": "📸 ارفع صورة الملصق الغذائي (Nutrition Facts)",
        "btn": "🔍 ابدأ التحليل الصحي الآن",
        "prompt": "أنت خبير تغذية. حلل الصورة: استخرج السعرات، السكريات، والمواد الحافظة. أعطِ تقييم (صحي 🟢، متوسط 🟡، ضار 🔴) ونصيحة قصيرة جدا ومفيدة."
    },
    "English": {
        "title": "Ahmed - Nutri-Scan AI",
        "sub": "Instant Food Analysis & Health Rating",
        "up": "📸 Upload Nutrition Facts / Ingredients",
        "btn": "🔍 Analyze Health Now",
        "prompt": "You are a nutritionist. Analyze image: extract calories, sugars, and preservatives. Give a rating (Healthy 🟢, Medium 🟡, Unhealthy 🔴) and brief advice."
    }
}[lang]

# 4. تفعيل المفتاح الجديد
API_KEY = "AIzaSyASr5PjZL2LrY4bXfZ7d4kd265rUhrin4E" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 5. واجهة المستخدم
st.markdown(f'<div class="header-box"><h1>{content["title"]}</h1><p>{content["sub"]}</p></div>', unsafe_allow_html=True)

file = st.file_uploader(content['up'], type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, use_container_width=True)
    
    if st.button(content['btn']):
        with st.spinner("⏳ جاري التحليل..."):
            try:
                response = model.generate_content([content['prompt'], img])
                st.markdown("---")
                st.success(response.text)
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.caption("Developed by Ahmed AI Pro © 2026")
