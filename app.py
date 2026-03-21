import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الهوية A.H
st.set_page_config(page_title="A.H AI Pro", page_icon="⚡")
st.markdown("<h2 style='text-align: center; color: #27ae60;'>A.H - فحص فوري ذكي 🥗</h2>", unsafe_allow_html=True)

# 2. الربط بالمفتاح الجديد (تم التحديث)
NEW_API_KEY = "AIzaSyAt-pa38pTx0eFa7tGbEeEOpaZTwFYZ_n4"
genai.configure(api_key=NEW_API_KEY)

# استخدام الموديل الأكثر توافقاً
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. واجهة المستخدم
file = st.file_uploader("📸 ارفع صورة المنتج الآن", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, use_container_width=True)
    
    if st.button("🚀 تحليل فوري"):
        with st.spinner("⚡ جاري استخراج البيانات..."):
            try:
                # طلب التحليل المباشر
                
