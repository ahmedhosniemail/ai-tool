import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الصفحة A.H
st.set_page_config(page_title="A.H Nutri-Scan", page_icon="🥗")

# تنسيق الواجهة
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .header-box {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
        padding: 25px; border-radius: 15px; color: white; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# 2. اللغات
with st.sidebar:
    lang = st.selectbox("🌐 Language", ["العربية", "English"])

if lang == "العربية":
    title, up_txt, btn_txt = "A.H - ماسح التغذية", "📸 ارفع صورة المنتج", "🔍 ابدأ التحليل"
    p_txt = "أنت خبير تغذية، حلل محتوى الصورة بدقة وأعطِ تقييماً صحياً."
else:
    title, up_txt, btn_txt = "A.H - Nutri-Scan", "📸 Upload Product", "🔍 Analyze Now"
    p_txt = "Analyze this food product image and give a health rating."

# 3. الربط (تأكد من المفتاح)
genai.configure(api_key="AIzaSyASr5PjZL2LrY4bXfZ7d4kd265rUhrin4E")
model = genai.GenerativeModel('gemini-1.5-flash')

st.markdown(f'<div class="header-box"><h1>{title}</h1></div>', unsafe_allow_html=True)

# 4. منطقة الرفع المحسنة
file = st.file_uploader(up_txt, type=["jpg", "png", "jpeg"])

if file is not None:
    # عرض الصورة فوراً للتأكد من التحميل
    image = Image.open(file)
    st.image(image, caption="تم رفع الصورة بنجاح ✅", use_container_width=True)
    
    if st.button(btn_txt):
        with st.spinner("⏳ جاري التحليل..."):
            try:
                # إرسال الصورة للذكاء الاصطناعي
                response = model.generate_content([p_txt, image])
                st.markdown("---")
                st.success(response.text)
            except Exception as e:
                st.error(f"عذراً، حدث خطأ: {e}")
                
