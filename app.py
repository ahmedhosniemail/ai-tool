import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
from io import BytesIO
from docx import Document
import re

# 1. إعدادات الصفحة والواجهة الجذابة
st.set_page_config(
    page_title="Ahmed AI Pro - مستخرج البيانات الذكي",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. تصميم CSS مخصص للألوان والجمال
st.markdown("""
<style>
    /* تغيير لون الخلفية */
    .stApp {
        background-color: #f0f8ff; /* لون أزرق فاتح مريح */
    }
    /* تصميم العنوان الرئيسي */
    .main-title {
        color: #2c3e50; /* لون كحلي غامق */
        text-align: center;
        font-family: 'Cairo', sans-serif;
        font-weight: bold;
        padding: 20px;
        background: linear-gradient(135deg, #a8dadc 0%, #e0f7fa 100%);
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    /* تصميم الأزرار */
    div.stButton > button {
        background-color: #457b9d !important; /* لون أزرق غامق للأزرار */
        color: white !important;
        border-radius: 25px !important;
        padding: 10px 25px !important;
        border: none !important;
        font-size: 18px !important;
        width: 100%;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #1d3557 !important; /* لون أغمق عند التمرير */
        transform: scale(1.02);
    }
    /* تنسيق الجداول */
    .stMarkdown table {
        border-collapse: collapse;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# العنوان الجذاب
st.markdown('<h1 class="main-title">🤖 Ahmed AI Pro | مستخرج البيانات الذكي</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #457b9d; font-size: 18px;'>حول صور الفواتير والجداول إلى ملفات Excel و Word بضغطة واحدة</p>", unsafe_allow_html=True)

# 3. إعدادات المفتاح (لقد قمت بتحديث اسم الموديل للطريقة المستقرة)
API_KEY = "AIzaSyC9v9vX4ioZm8PKttNwefL7QuOKXAaiFfk"
genai.configure(api_key=API_KEY)

# الحل الجذري لخطأ 404: استخدام الاسم الرسمي الكامل
model = genai.GenerativeModel('models/gemini-1.5-flash')

# 4. رفع الملفات
uploaded_file = st.file_uploader("📂 ارفع صورة الجدول أو الفاتورة (JPG/PNG)", type=["jpg", "jpeg", "png"])

# ميزة متعدد اللغات: اختيار لغة المخرج
output_lang = st.selectbox("🌐 اختر لغة النتائج", ["العربية", "English", "Français"])

# 5. دوال تحويل البيانات لملفات
def to_excel(markdown_text):
    # دالة بسيطة لاستخراج الجدول من الـ Markdown وتحويله لـ DataFrame
    tables = re.findall(r'\|.*\|', markdown_text)
    if not tables:
        return None
    # هذه مجرد دالة بسيطة، قد تحتاج لتعديل حسب دقة الجدول
    try:
        data = [row.strip('|').split('|') for row in tables if '-' not in row]
        df = pd.DataFrame(data[1:], columns=data[0])
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        return output.getvalue()
    except:
        return None

def to_word(text):
    doc = Document()
    # لتنظيم اللغة العربية
    doc.add_paragraph(text)
    output = BytesIO()
    doc.save(output)
    return output.getvalue()

# 6. المعالجة الرئيسية
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="📸 الصورة المرفوعة", use_column_width=True)
    
    if st.button("🚀 ابدأ تحليل واستخراج البيانات الآن"):
        with st.spinner("🧠 جاري القراءة والتحليل بدقة..."):
            try:
                # طلب التحليل
                prompt = f"استخرج جميع البيانات الموجودة في هذه الصورة بدقة ونظمها في جدول Markdown. اجعل النتائج بلغة: {output_lang}."
                response = model.generate_content([prompt, img])
                
                result_text = response.text
                st.success("✅ تم التحليل بنجاح!")
                st.markdown("### 📊 البيانات المستخرجة:")
                st.markdown(result_text)
                
                st.divider()
                st.markdown("### ⬇️ تحميل النتائج:")
                col1, col2 = st.columns(2)
                
                # أزرار التحميل
                excel_data = to_excel(result_text)
                if excel_data:
                    with col1:
                        st.download_button(
                            label="📥 تحميل كملف Excel (XLSX)",
                            data=excel_data,
                            file_name=f'extracted_data_{uploaded_file.name}.xlsx',
                            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                        )
                
                with col2:
                    st.download_button(
                        label="📥 تحميل كملف Word (DOCX)",
                        data=to_word(result_text),
                        file_name=f'extracted_data_{uploaded_file.name}.docx',
                        mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                    )
                    
            except Exception as e:
                st.error(f"تنبيه: {e}")
                st.info("نصيحة: تأكد من تحديث ملف requirements.txt لضمان عمل الموديل")

# 7. التذييل (Footer) الجذاب
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© 2024 Ahmed AI Pro | جميع الحقوق محفوظة لأحمد حسني</p>", unsafe_allow_html=True)
