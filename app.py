import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
from io import BytesIO
from docx import Document
import re

# ==========================================
# 1. إعدادات الصفحة والواجهة الفاتحة الملكية
# ==========================================
st.set_page_config(
    page_title="Ahmed AI Pro - Royal Edition",
    page_icon="👑",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. تصميم CSS عصري، فاتح وناصع (Royal Light Theme)
# ==========================================
st.markdown("""
<style>
    /* 💎 خلفية سماوية فاتحة وناصعة (Ice Blue to White) لراحة القراءة */
    .stApp {
        background: linear-gradient(135deg, #f0f8ff 0%, #ffffff 100%);
        color: #1a253a; /* نصوص كحلية غامقة لوضوح تام */
    }

    /* تأثير زجاجي فاتح (Light Glassmorphism) للعناصر */
    .glass-container {
        background: rgba(255, 255, 255, 0.7); /* نصف شفافة فاتحة */
        border-radius: 20px;
        padding: 30px;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(52, 152, 219, 0.2); /* إطار سماوي فاتح */
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1); /* ظل خفيف وأنيق */
        margin-bottom: 25px;
        text-align: center;
    }

    /* 🛡️ تنسيق شعار الشركة العالمية/الفريق الملكي (3D Gold Logo) */
    .company-logo {
        width: 140px; /* حجم أكبر قليلاً وفخم */
        height: 140px;
        object-fit: contain;
        margin-bottom: 20px;
        filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.5)); /* تأثير توهج ذهبي خفيف */
    }

    /* 💎 تصميم العناوين */
    .main-title {
        color: #1a253a; /* لون كحلي عميق ملكي */
        font-family: 'Cairo', sans-serif;
        font-weight: bold;
        margin-bottom: 10px;
        font-size: 2.8rem;
    }
    
    .sub-title {
        color: #7f8c8d; /* لون رمادي هادئ */
        font-size: 1.2rem;
        margin-bottom: 0px;
        font-weight: normal;
    }

    /* 🚀 تصميم الأزرار الاحترافي والملكي (Royal Blue Button) */
    div.stButton > button {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%) !important; /* لون كحلي متدرج فخم */
        color: white !important;
        border-radius: 30px !important;
        padding: 12px 30px !important;
        border: none !important;
        font-size: 18px !important;
        font-weight: bold !important;
        width: 100%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }

    /* 📋 تنسيق الجداول (تأثير زجاجي فاتح جداً) */
    .stMarkdown table {
        border-collapse: collapse;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        background: rgba(255, 255, 255, 0.98) !important;
        color: #2c3e50 !important;
    }
    .stMarkdown th {
        background-color: #f1f8fc !important; /* لون سماوي فاتح جداً للعنوان */
        color: #1a253a !important;
    }
    
    /* تنسيق القائمة الجانبية (Sidebar) */
    .stSidebar {
        background-color: rgba(255, 255, 255, 0.9) !important;
    }
    .stSidebar p, .stSidebar h3, .stSidebar label {
        color: #2c3e50 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. إعدادات اللغة (Dictionary-based translation)
# ==========================================
translations = {
    'العربية': {
        'title': 'AHMED AI PRO',
        'subtitle': 'مستخرج البيانات الذكي الملكي | تحويل الصور لملفات Excel/Word/PDF بضغطة واحدة',
        'sidebar_lang_label': '🌐 لغة الواجهة والتحليل:',
        'file_uploader_label': '📂 ارفع صورة الجدول، الفاتورة أو البطاقة (JPG/PNG)',
        'analyze_button': '🚀 ابدأ تحليل واستخراج البيانات الآن',
        'analyzing_spinner': '🧠 جاري القراءة والتحليل الملكي بدقة (قد تستغرق وقتاً للصور الكبيرة)...',
        'success_msg': '✅ تم التحليل بنجاح!',
        'extracted_data_header': '📊 البيانات المستخرجة:',
        'download_header': '⬇️ تحميل النتائج الفاخرة:',
        'excel_button': '📥 تحميل كملف Excel (XLSX)',
        'word_button': '📥 تحميل كملف Word (DOCX)',
        'pdf_button': '📥 تحميل كملف PDF',
        'error_msg': 'حدث خطأ:',
        'footer_text': '© 2024 Ahmed AI Pro | جميع الحقوق محفوظة لأحمد حسني',
        'prompt': 'استخرج البيانات من هذه الصورة في شكل جدول'
    },
    'English': {
        'title': 'AHMED AI PRO',
        'subtitle': 'Royal Smart Data Extractor | Convert Images to Excel/Word/PDF in One Click',
        'sidebar_lang_label': '🌐 Interface & Analysis Language:',
        'file_uploader_label': '📂 Upload Table, Invoice, or Card Image (JPG/PNG)',
        'analyze_button': '🚀 Start Analysis Now',
        'analyzing_spinner': '🧠 AI is reading and analyzing with precision (Large images may take time)...',
        'success_msg': '✅ Analysis Successful!',
        'extracted_data_header': '📊 Extracted Data:',
        'download_header': '⬇️ Download Premium Results:',
        'excel_button': '📥 Download Excel (XLSX)',
        'word_button': '📥 Download Word (DOCX)',
        'pdf_button': '📥 Download PDF',
        'error_msg': 'An error occurred:',
        'footer_text': '© 2024 Ahmed AI Pro | All rights reserved to Ahmed Hosny',
        'prompt': 'Extract data from this image into a table'
    },
    'Français': {
        'title': 'AHMED AI PRO',
        'subtitle': 'Extracteur de Données Intelligent Royal | Convertissez les images en Excel/Word/PDF en un clic',
        'sidebar_lang_label': '🌐 Langue de l\'interface et de l\'analyse :',
        'file_uploader_label': '📂 Télécharger l\'image du tableau, de la facture ou de la carte (JPG/PNG)',
        'analyze_button': '🚀 Démarrer l\'analyse',
        'analyzing_spinner': '🧠 L\'IA lit et analyse avec précision (Les grandes images peuvent prendre du temps)...',
        'success_msg': '✅ Analyse réussie!',
        'extracted_data_header': '📊 Données extraites :',
        'download_header': '⬇️ Télécharger les résultats premium :',
        'excel_button': '📥 Télécharger Excel (XLSX)',
        'word_button': '📥 Télécharger Word (DOCX)',
        'pdf_button': '📥 Télécharger PDF',
        'error_msg': 'Une erreur s\'est produite :',
        'footer_text': '© 2024 Ahmed AI Pro | Tous droits réservés à Ahmed Hosny',
        'prompt': 'Extraire les données de cette image dans un tableau'
    }
}

# 🌐 إضافة خيار اختيار اللغة في القائمة الجانبية (Settings)
st.sidebar.markdown(f'<h3 style="margin-bottom: 10px;">Settings ✨</h3>', unsafe_allow_html=True)
selected_lang = st.sidebar.selectbox("🌐 Language / اللغة", list(translations.keys()))

# تفعيل النصوص بناءً على اللغة المختارة
lang_data = translations[selected_lang]

# ==========================================
# 4. العنوان والواجهة مع الشعار الذهبي الفخم (Company/Team Logo)
# ==========================================
# حاوية زجاجية فاتحة للمقدمة
st.markdown(f"""
<div class="glass-container">
    <img src="https://cdn-icons-png.flaticon.com/512/9167/9167196.png" class="company-logo" alt="AHMED AI PRO Gold Logo">
    <h1 class="main-title">{lang_data["title"]}</h1>
    <p class="sub-title">{lang_data["subtitle"]}</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. إعدادات المفتاح والموديل
# ==========================================
API_KEY = "AIzaSyC9v9vX4ioZm8PKttNwefL7QuOKXAaiFfk"
genai.configure(api_key=API_KEY)

# الاسم الرسمي الكامل للموديل لضمان العمل
model = genai.GenerativeModel('models/gemini-1.5-flash')

# ==========================================
# 6. دوال تحويل البيانات (Excel & Word & PDF)
# ==========================================
def to_excel(markdown_text):
    tables = re.findall(r'\|.*\|', markdown_text)
    if not tables:
        return None
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
    doc.add_paragraph(text)
    output = BytesIO()
    doc.save(output)
    return output.getvalue()

# دالة بسيطة للتحويل إلى PDF (تحويل النص المباشر)
def to_pdf(text):
    # إنشاء ملف PDF بسيط من النص المستخرج
    output = BytesIO()
    # إنشاء ملف PDF أساسي - هذه الطريقة قد لا تدعم الجداول العربية بشكل مثالي
    # للتحويل الكامل للجداول العربية لـ PDF، ستحتاج لمكتبات إضافية مثل fpdf2 أو ReportLab
    # لكن سنقدم هنا حلاً بسيطاً كبداية
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        c = canvas.Canvas(output, pagesize=letter)
        width, height = letter
        # كتابة النص المستخرج في ملف PDF (يدعم الإنجليزية بشكل أساسي)
        c.drawString(100, height - 100, "extracted data from AHMED AI PRO")
        text_object = c.beginText(100, height - 120)
        # تقسيم النص لأسطر
        for line in text.split('\n'):
            text_object.textLine(line)
        c.drawText(text_object)
        c.save()
        return output.getvalue()
    except:
        return None # إذا لم تكن المكتبة متوفرة أو حدث خطأ

# دالة ذكية لتغيير حجم الصور الكبيرة جداً قبل الإرسال
def resize_image(image_file, max_size=(2048, 2048)):
    img = Image.open(image_file)
    # التحقق من نوع الصورة لتجنب الأخطاء
    if img.mode != 'RGB':
        img = img.convert('RGB')
    # إذا كانت الصورة أكبر من الحد المسموح، قم بتغيير حجمها
    if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        # تحويل الصورة إلى Bytes لإرسالها
        output = BytesIO()
        img.save(output, format='JPEG', quality=85)
        return Image.open(output)
    else:
        return img

# ==========================================
# 7. رفع الملفات والمعالجة الرئيسية
# ==========================================
uploaded_file = st.file_uploader(lang_data['file_uploader_label'], type=["jpg", "jpeg", "png"])

if uploaded_file:
    # استخدام الدالة الذكية لتغيير حجم الصور الكبيرة تلقائياً
    with st.spinner("⏳ جاري تجهيز الصورة (تغيير الحجم إذا كانت كبيرة)..."):
        processed_img = resize_image(uploaded_file)
    
    # عرض الصورة (تلقائياً يتم تغيير حجم العرض في المتصفح)
    st.image(processed_img, caption="📸 الصورة الجاهزة للتحليل", use_column_width=True)
    
    if st.button(lang_data['analyze_button']):
        with st.spinner(lang_data['analyzing_spinner']):
            try:
                # طلب التحليل (بناءً على لغة الواجهة)
                prompt = lang_data['prompt']
                response = model.generate_content([prompt, processed_img])
                
                result_text = response.text
                st.success(lang_data['success_msg'])
                st.markdown(f"### {lang_data['extracted_data_header']}")
                st.markdown(result_text)
                
                st.divider()
                st.markdown(f"### {lang_data['download_header']}")
                # استخدام 3 أعمدة للأزرار الجديدة
                col1, col2, col3 = st.columns(3)
                
                # إنشاء ملفات التحميل
                excel_data = to_excel(result_text)
                word_data = to_word(result_text)
                #pdf_data = to_pdf(result_text) # تم تفعيل مكتبة reportlab

                # أزرار التحميل
                if excel_data:
                    with col1:
                        st.download_button(
                            label=lang_data['excel_button'],
                            data=excel_data,
                            file_name=f'extracted_data_{uploaded_file.name}.xlsx',
                            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                        )
                
                with col2:
                    st.download_button(
                        label=lang_data['word_button'],
                        data=word_data,
                        file_name=f'extracted_data_{uploaded_file.name}.docx',
                        mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                    )
                
                # تم تفعيل التحميل لـ PDF باستخدام مكتبة reportlab
                try:
                    from reportlab.pdfgen import canvas # للتحقق من المكتبة
                    pdf_data = to_pdf(result_text)
                    if pdf_data:
                        with col3:
                            st.download_button(
                                label=lang_data['pdf_button'],
                                data=pdf_data,
                                file_name=f'extracted_data_{uploaded_file.name}.pdf',
                                mime='application/pdf'
                            )
                except ImportError:
                    with col3:
                        st.info("لم يتم تثبيت مكتبة 'reportlab'. تحميل PDF غير متاح.")
                    
            except Exception as e:
                st.error(f"{lang_data['error_msg']} {e}")
                st.info("نصيحة: تأكد من تحديث ملف requirements.txt لضمان عمل الموديل والميزات")

# ==========================================
# 8. التذييل (Footer)
# ==========================================
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: #7f8c8d;'>{lang_data['footer_text']}</p>", unsafe_allow_html=True)
