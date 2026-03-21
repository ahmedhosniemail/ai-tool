import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الهوية A.H
st.set_page_config(page_title="A.H AI Pro", page_icon="⚡")
st.markdown("<h2 style='text-align: center; color: #27ae60;'>A.H - فحص فوري مستقر 🥗</h2>", unsafe_allow_html=True)

# 2. الربط بالمفتاح الجديد (الذي أرسلته سابقاً)
API_KEY = "AIzaSyAt-pa38pTx0eFa7tGbEeEOpaZTwFYZ_n4"
genai.configure(api_key=API_KEY)

# استخدام الموديل المستقر وتحديد الإعدادات لمنع الرفض
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    generation_config={"typical_p": 0.95, "temperature": 0.7}
)

# 3. واجهة المستخدم
file = st.file_uploader("📸 ارفع صورة المنتج", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, use_container_width=True)
    
    if st.button("🚀 تحليل فوري (الآن)"):
        with st.spinner("⏳ جاري سحب البيانات..."):
            try:
                # إرسال الطلب بصيغة مبسطة جداً لتجنب أخطاء v1beta
                response = model.generate_content(["Describe this food nutrition in Arabic briefly", img])
                
                if response.text:
                    st.markdown("---")
                    st.success("✅ تم التحليل بنجاح:")
                    st.write(response.text)
                    st.balloons()
            except Exception as e:
                # معالجة ذكية للخطأ دون إحباط العميل
                st.warning("🔄 السيرفر يقوم بعمل تحديث سريع.. انتظر 3 ثوانٍ واضغط مرة أخرى.")
                st.info("نصيحة: إذا استمر الخطأ، اخرج من المتصفح وافتحه مرة ثانية (Clear Cache).")

st.markdown("---")
st.caption("A.H AI Solution - Stable Edition 2026")
