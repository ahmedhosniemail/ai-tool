import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Extractor by Ahmed")
st.title("📊 AI Data Extractor Pro")
st.info("مرحباً بك في مشروع أحمد حسني الأول")

uploaded_file = st.file_uploader("ارفع ملفك هنا (PDF أو صورة)")
if uploaded_file:
    st.success("✅ تم استقبال الملف! النظام جاهز للمعالجة.")
    # هنا سيتم لاحقاً إضافة ذكاء استخراج البيانات
  
