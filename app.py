import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import pandas as pd
import re

# 1. Сайтын ерөнхий тохиргоо
st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# --- СИСТЕМ: ЦЭСНИЙ УДИРДЛАГА ---
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Нүүр хуудас"

# УХААЛАГ МАТЕМАТИК ТАНИГЧ
def smart_math_render(text):
    if not isinstance(text, str): return str(text)
    for label in ['A.', 'B.', 'C.', 'D.']:
        if label in text:
            text = text.replace(label, f'\n\n**{label}**')
    if ('\\' in text or '^' in text or '/' in text) and '$' not in text:
        clean_text = text.replace('\\displaystyle', '').strip()
        text = f"$\\displaystyle {clean_text}$"
    return text

# 2. ДИЗАЙН (Засварласан CSS)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    
    /* ХАЖУУГИЙН ЦЭС */
    [data-testid="stSidebar"] { 
        background-color: #0b4ab1 !important; 
        min-width: 260px !important;
    }
    
    /* "ЦЭС" гарчиг */
    .sidebar-title { 
        color: white; text-align: center; font-size: 45px; font-weight: bold; 
        padding: 20px 0; margin-bottom: 10px;
    }

    /* "Бидний зорилго" хайрцаг */
    .goal-box {
        background: white; padding: 25px; border-radius: 20px;
        border: 1px solid #f0f2f6;
        border-left: 10px solid #0b4ab1; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    
    /* ГАРЧИГ */
    .main-header { 
        color: #0b4ab1; 
        font-size: 45px; 
        font-weight: 800; 
        margin-bottom: 5px;
        line-height: 0.95 !important; 
    }

    /* Төв хэсгийн 3 товчлуур */
    div.stButton {
        width: 100% !important;
    }
    
    div.stButton > button {
        width: 100% !important; 
        height: 190px !important; 
        border-radius: 25px !important; 
        border: 1px solid #f0f0f0 !important;
        background: #fdfdfd !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s ease-in-out !important;
    }

    div.stButton > button p {
        font-size: 22px !important; 
        font-weight: bold !important;
        color: #0b4ab1 !important;
    }

    div.stButton > button:hover {
        transform: translateY(-5px) !important;
        border: 1px solid #0b4ab1 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Цэс)
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    
    menu_options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил"]
    current_index = menu_options.index(st.session_state.selected_menu) if st.session_state.selected_menu in menu_options else 0

    selected = option_menu(
        menu_title=None, 
        options=menu_options,
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        default_index=current_index,
        styles={
            "container": {"background-color": "#0b4ab1", "padding": "0"},
            "icon": {"color": "white", "font-size": "18px"}, 
            "nav-link": {
                "font-size": "16px",  # Хэмжээг 16px болгож томруулсан
                "color": "white", 
                "margin": "5px 0px", 
                "padding": "10px 15px",
                "text-align": "left",
                "font-weight": "500"
            },
            "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)", "font-weight": "bold"},
        }
    )
    if selected != st.session_state.selected_menu:
        st.session_state.selected_menu = selected
        st.rerun()

# 4. НҮҮР ХУУДАС
if st.session_state.selected_menu == "Нүүр хуудас":
    col1, col2 = st.columns([1, 1.2], gap="large")
    with col1:
        if os.path.exists("logo.gif"):
            with open("logo.gif", "rb") as f:
                data_url = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(f'<img src="data:image/gif;base64,{data_url}" style="width: 100%; border-radius: 20px;">', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="goal-box">
                <div class="main-header">Математикийн ертөнцөд тавтай морил!</div>
                <div style="font-size: 19px; line-height: 1.4; color: #444; text-align: justify; text-indent: 20px;">
                Сонирхолтой цахим хичээл, баялаг бодлогын сангаар дамжуулан математик сэтгэлгээгээ бие даан хөгжүүлж, ирээдүйн амжилтынхаа суурийг өнөөдөр тавихад тань бид туслах болно. Хамтдаа суралцаж, хамтдаа хөгжицгөөе!
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1], gap="medium")
    
    with c1:
        if st.button("📺\n\nЦахим контент", key="btn_1", use_container_width=True):
            st.session_state.selected_menu = "Цахим контент"
            st.rerun()
            
    with c2:
        if st.button("📚\n\nДаалгаврын сан", key="btn_2", use_container_width=True):
            st.session_state.selected_menu = "Даалгаврын сан"
            st.rerun()
            
    with c3:
        if st.button("📝\n\nСорил", key="btn_3", use_container_width=True):
            st.session_state.selected_menu = "Сорил"
            st.rerun()

# 5. БУСАД ХУУДАСНУУД
else:
    st.markdown(f"<h1 style='color: #0b4ab1; text-align: center; margin-top: 50px;'>{st.session_state.selected_menu}</h1>", unsafe_allow_html=True)
    st.info("Энэ хэсэг удахгүй нэмэгдэнэ.")
