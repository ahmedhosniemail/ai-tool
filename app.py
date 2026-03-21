import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="A.H Nutri-Scan 2026", page_icon="🥗", layout="centered")

# تنسيق الواجهة
st.markdown("""
<style>
    .stApp { background-color: #ffffff; color: #2c3e50; }
    .header-box {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
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

# 2. القائمة الجانبية
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    lang = st.selectbox("🌐 Language", ["العربية", "English"])

# 3. النصوص (تم تبسيطها لتجنب أخطاء التنصيص)
if lang == "العربية":
    title = "A.H - ماسح التغذية الذكي"
    sub = "حلل جودة طعامك فوراً بالذكاء الاصطناعي"
    up_text = "📸 ارفع صورة الملصق الغذائي"
    btn_text = "🔍 ابدأ التحليل الآن"
    p_text = "أنت خبير تغذية. حلل الصورة: استخرج السعرات والسكريات. أعطِ تقييماً (🟢 صحي، 🟡 متوسط، 🔴 ضار) ونصيحة."
else:
    title = "A.H - Nutri-Scan AI"
    sub = "Instant Food Health Analysis"
    up_text = "📸 Upload Nutrition Facts"
    btn_text = "🔍 Analyze Now"
    p_text = "Analyze image: extract calories, sugars. Rate it 🟢, 🟡, or 🔴 and give advice."

# 4. الربط بالمفتاح الجديد
genai.configure(api_key="AIzaSyASr5PjZL2LrY4bXfZ7d4kd265rUhrin4E")
model = genai.GenerativeModel('gemini-1.5-flash')

# 5. الواجهة
st.markdown(f'<div class="header-box"><h1>{title}</h1><p>{sub}</p></div>', unsafe_allow_html=True)

file = st.file_uploader(up_text, type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, use_container_width=True)
    
    if st.button(btn_text):
        with st.spinner("⏳..."):
            try:
                response = model.generate_content([p_text, img])
                st.markdown("---")
                st.success(response.text)
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.caption("Developed by A.H AI Pro © 2026")
