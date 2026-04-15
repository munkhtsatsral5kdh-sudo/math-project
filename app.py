import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64

# 1. Сайтын ерөнхий тохиргоо
st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# 2. ДИЗАЙН (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }

    /* Хажуугийн цэс */
    [data-testid="stSidebar"] {
        background-color: #004aad !important;
        min-width: 300px !important;
    }
    
    .sidebar-title {
        color: #ffffff !important;
        text-align: center;
        font-family: 'Arial Black', sans-serif;
        font-size: 40px !important;
        font-weight: bold;
        padding: 20px 0;
        border-bottom: 2px solid rgba(255,255,255,0.3);
        margin-bottom: 20px;
    }

    /* БИДНИЙ ЗОРИЛГО - ГАРЧИГ */
    .main-header {
        color: #004aad !important;
        font-family: 'Arial Black', sans-serif !important;
        font-size: 55px !important;
        font-weight: 900 !important;
        margin: 0px 0px 15px 0px !important;
        line-height: 1.1 !important;
    }

    /* ЗОРИЛГЫН ТЕКСТ - ШИНЭ ТЕКСТТЭЙ */
    .goal-text {
        font-size: 24px !important;
        color: #333;
        line-height: 1.6;
        background: white;
        padding: 35px;
        border-left: 15px solid #004aad;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        text-align: justify;
    }

    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* КАРТУУД */
    .custom-card {
        background: white;
        border-radius: 25px;
        padding: 35px 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        border: 1px solid #eee;
        height: 280px;
    }
    .custom-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 35px rgba(0,74,173,0.15);
    }
    .card-icon { font-size: 60px; margin-bottom: 15px; }
    .card-title { color: #004aad; font-size: 24px; font-weight: bold; }
    
    /* Илүүдэл элементийг нуух */
    [data-testid="stHeaderActionElements"], .stAppDeployButton { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Цэс) - Алдааг зассан хэсэг
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None, 
        options=["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил төлөвшил МХБ"],
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        default_index=0,
        styles={
            "container": {"background-color": "#004aad", "padding": "0"},
            "icon": {"color": "white", "font-size": "20px"}, 
            "nav-link": {"font-size": "17px", "color": "white", "font-family": "Arial", "font-weight": "bold", "margin": "5px"},
            "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)"},
        }
    )

# 4. АГУУЛГА
if selected == "Нүүр хуудас":
    col1, col2 = st.columns([1, 1.4], gap="large")
    
    with col1:
        logo_path = "logo.gif" 
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                data = f.read()
                data_url = base64.b64encode(data).decode("utf-8")
            st.markdown(f'<div class="logo-container"><img src="data:image/gif;base64,{data_url}" width="100%"></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<p class="main-header">Бидний зорилго</p>', unsafe_allow_html=True)
        st.markdown("""
            <div class="goal-text">
                Математикийн ертөнцөөр хамтдаа аялж, сонирхолтой цахим хичээл, 
                бодлогын сангаар дамжуулан өөрийн мэдлэг чадвараа бие даан ахиулж, 
                ирээдүйн амжилтынхаа эхлэлийг өнөөдөр тавьцгаая!
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="medium")
    
    cards = [
        {"icon": "📺", "title": "Цахим контент", "desc": "Видео хичээл болон интерактив материалууд"},
        {"icon": "📚", "title": "Даалгаврын сан", "desc": "Өөрийгөө сорих бодлого, дасгалууд"},
        {"icon": "📝", "title": "Сорил", "desc": "Мэдлэгээ шалгах онлайн шалгалтууд"}
    ]
    
    for i, col in enumerate([c1, c2, c3]):
        with col:
            st.markdown(f"""
                <div class="custom-card">
                    <div class="card-icon">{cards[i]['icon']}</div>
                    <div class="card-title">{cards[i]['title']}</div>
                    <p style='color:#777; font-size:15px; margin-top:10px;'>{cards[i]['desc']}</p>
                </div>
            """, unsafe_allow_html=True)
else:
    st.markdown(f"<h1 style='color: #004aad; text-align: center; margin-top: 50px;'>{selected}</h1>", unsafe_allow_html=True)