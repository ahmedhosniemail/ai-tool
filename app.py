import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الهوية A.H
st.set_page_config(page_title="A.H Fast Scan", page_icon="⚡")

# الربط (استخدام النسخة الأكثر استقراراً)
genai.configure(api_key="AIzaSyASr5PjZL2LrY4bXfZ7d4kd265rUhrin4E")
model = genai.GenerativeModel('gemini-1.5-flash')

st.markdown("<h1 style='text-align: center; color: #2ecc71;'>A.H - التحليل الذكي 🥗</h1>", unsafe_allow_html=True)

file = st.file_uploader("📸 ارفع صورة المنتج", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, use_container_width=True)
    
    if st.button("🚀 ابدأ الفحص الفوري"):
        # استخدام خاصية الـ stream لعرض النتائج فوراً
        try:
            with st.spinner("⚡ جاري استخراج البيانات..."):
                response = model.generate_content(
                    ["Analyze this nutrition label, mention calories, sugar, and a health rating (🟢, 🟡, 🔴) in Arabic.", img],
                    stream=True
                )
                
                st.markdown("---")
                st.markdown("### 🧬 النتائج:")
                
                # عرض النتائج فور ولادتها من السيرفر
                full_text = ""
                message_placeholder = st.empty()
                for chunk in response:
                    full_text += chunk.text
                    message_placeholder.markdown(full_text + "▌")
                message_placeholder.markdown(full_text)
                st.balloons() # احتفال بالنجاح!
        except Exception as e:
            st.error(f"خطأ في الاتصال: {e}")
            st.info("💡 نصيحة لـ A.H: تأكد من تفعيل Gemini API في Google Cloud لهذا المفتاح.")

st.markdown("---")
st.caption("Developed by A.H Pro © 2026")
