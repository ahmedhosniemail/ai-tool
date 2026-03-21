import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الصفحة (تصميم عصري ونظيف يركز على الصحة)
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
        transition: 0.3s;
    }
    div.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

# 2. القائمة الجانبية للغات
with st.sidebar:
    st.markdown("### ⚙️ الإعدادات / Settings")
    lang = st.selectbox("🌐 اختر لغة التحليل:", ["العربية", "English"])

content = {
    "العربية": {
        "title": "أحمد - ماسح التغذية الذكي",
        "sub": "حلل جودة طعامك فوراً باستخدام الذكاء الاصطناعي",
        "up": "📸 ارفع صورة الملصق الغذائي (Nutrition Facts)",
        "btn": "🔍 ابدأ التحليل الصحي الآن",
        "prompt": "أنت خبير تغذية. حلل الصورة: استخرج السعرات، السكريات، والمواد الحافظة. أعطِ تقييماً (صحياً 🟢، متوسطاً 🟡، ضاراً 🔴) ونصيحة قصيرة جدا
        
