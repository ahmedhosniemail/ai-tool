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

# 4
