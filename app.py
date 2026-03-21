import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الهوية والتصميم A.H
st.set_page_config(page_title="A.H Nutri-Scan Pro", page_icon="🥗", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #27ae60; color: white; }
    .result-card { background-color: white; padding: 20px; border-radius: 15px; border-right: 5px solid #27ae60; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 2. الربط بالمفتاح
genai.configure(api_key="AIzaSyAt-pa38pTx0eFa7tGbEeEOpaZTwFYZ_n4")
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🥗 A.H - مساعدك الصحي الذكي")
st.write("ارفع صورة المنتج واحصل على تحليل فوري للمكونات")

# 3. واجهة المستخدم
file = st.file_uploader("", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, caption="المنتج المطلوب فحصه", use_container_width=True)
    
    if st.button("🚀 تحليل المنتج"):
        with st.spinner("⚡ جاري استخراج البيانات وتحليلها..."):
            try:
                # طلب التحليل بصيغة احترافية
                prompt = """
                حلل صورة المنتج الغذائي هذه باللغة العربية ونظم النتيجة كالتالي:
                1. المكونات الأساسية.
                2. جدول السعرات الحرارية (تقريبي).
                3. التقييم الصحي من 10.
                4. نصيحة سريعة للمستهلك.
                """
                response = model.generate_content([prompt, img])
                
                if response:
                    st.markdown("---")
                    st.markdown(f'<div class="result-card">{response.text}</div>', unsafe_allow_html=True)
                    st.balloons()
            except Exception as e:
                st.error("السيرفر مشغول حالياً، يرجى المحاولة مرة أخرى خلال ثوانٍ.")

st.markdown("---")
st.caption("Developed with Intelligence by A.H © 2026")
