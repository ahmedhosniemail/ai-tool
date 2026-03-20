import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
from io import BytesIO
from docx import Document
import re

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="Ahmed AI Pro - Deep Blue",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. تصميم CSS عصري، ثابت وأنيق (Deep Blue Theme)
# ==========================================
st.markdown("""
<style>
    /* 💎 لون خلفية ثابت وأنيق (Deep Midnight Blue) */
    .stApp {
        background-color: #1a253a; /* كحلي عميق ملكي */
        color: #ecf0f1; /* نصوص بيضاء فاتحة */
    }

    /* تأثير زجاجي (Glassmorphism) للعناصر الرئيسية */
    .glass-container {
        background: rgba(255, 255, 255, 0.05); /* نصف شفافة */
        border-radius: 20px;
        padding: 25px;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 25px;
        text-align: center;
    }

    /* 🤖 تنسيق صورة الذكاء الاصطناعي الاحترافية */
    .ai-avatar {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #3498db; /* إطار أزرق فاتح */
        box-shadow: 0 0 15px rgba(52, 152, 219, 0.5);
        margin-bottom: 20px;
    }

    /* 💎 تصميم العناوين */
    .main-title {
        color: #ecf0f1;
        font-family: 'Cairo', sans-serif;
        font-weight: bold;
        margin-bottom: 10px;
        font-size: 2.5rem;
    }
    
    .sub-title {
        color: #bdc3c7; /* لون رمادي فاتح */
        font-size: 1.1rem;
        margin-bottom: 0px;
    }

    /* 🚀 تصميم الأزرار الثابت والمحترف (Deep Blue Button) */
    div.stButton > button {
        background-color: #3498db !important; /* أزرق فاتح متماسك */
        color: white !important;
        border-radius: 30px !important;
        padding: 12px 30px !important;
        border: none !important;
        font-size: 18px !important;
        font-weight: bold !important;
        width: 100%;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    div.
    
