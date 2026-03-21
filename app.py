import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الواجهة (تصميم عصري ونظيف)
st.set_page_config(page_title="Ahmed Nutri-Scan 2026", page_icon="🥗", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #ffffff; color: #2c3e50; }
    .header-box {
        background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
        padding: 30px; border-radius: 20px; color: white;
        text-align: center; margin-bottom: 25px;
    }
    div.stButton > button {
        background: #27ae60 !important; color: white !important;
        border-radius: 12px !important; font-weight: bold !important;
        height: 50px; width: 100%; border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. القائمة الجانبية للغات (مضمونة الظهور)
with st.sidebar:
    st.header("⚙️ Settings")
    lang = st.selectbox("🌐 Choose Language / اختر اللغة", ["العربية", "English"])

content = {
    "العربية": {
        "title": "أحمد - ماسح التغذية الذكي",
        "desc": "صور ملصق المكونات وسأحلل لك جودتها الصحية فوراً",
        "up": "📸 ارفع صورة المكونات هنا",
        "btn": "🔍 تحليل الصحة الآن",
        "prompt": "حلل هذه الصورة لمنتج غذائي. هل هو صحي؟ استخرج السعرات والمواد الضارة وأعطِ تقييماً بـ 🟢 أو 🟡 أو 🔴"
    },
    "English": {
        "title": "Ahmed - Nutri-Scan AI",
        "desc": "Scan ingredients and get instant health analysis",
        "up": "📸 Upload ingredients image",
        "btn": "🔍 Analyze Health Now",
        "prompt": "Analyze this food product image. Is it healthy? Extract calories, harmful ingredients, and rate it with 🟢, 🟡, or 🔴"
    }
}[lang]

# 3. الربط مع المفتاح الجديد (ضع مفتاحك هنا)
# تأكد من وضع المفتاح الجديد بين علامات التنصيص
API_KEY = "AIzaSyASr5PjZL2LrY4bXfZ7d4kd265rUhrin4E" 
genai.configure(api_key=API_KEY)

# استخدام اسم الموديل الأكثر استقراراً في 2026
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. واجهة المستخدم
st.markdown(f"""
<div class="header-box">
    <h1>{content['title']}</h1>
    <p>{content['desc']}</p>
</div>
""", unsafe_allow_html=True)

file = st.file_uploader(content['up'], type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, use_container_width=True)
    
    if st.button(content['btn']):
        with st.spinner("⏳ جاري الفحص..."):
            try:
                # إرسال الصورة للتحليل
                response = model.generate_content([content['prompt'], img])
                st.markdown("---")
                st.markdown("### 🧬 التقرير الصحي:")
                st.success(response.text)
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
                st.info("نصيحة: تأكد من صحة مفتاح الـ API الجديد في الكود.")

st.markdown("---")
st.caption("Ahmed AI Vision 2026 - Pro")
