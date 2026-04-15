import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import time

# 1. Сонгогдсон цэсийг санах ойд хадгалах
if 'menu_option' not in st.session_state:
    st.session_state.menu_option = "Нүүр хуудас"

# 2. Сайтын ерөнхий тохиргоо
st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# 3. ДИЗАЙН (Таны анхны цэнхэр загвар)
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #004aad !important; min-width: 300px !important; }
    .sidebar-title { color: #ffffff !important; text-align: center; font-size: 40px !important; font-weight: bold; padding: 20px 0; border-bottom: 2px solid rgba(255,255,255,0.3); margin-bottom: 20px; }
    .main-header { color: #004aad !important; font-size: 55px !important; font-weight: 900; margin: 0px 0px 15px 0px !important; line-height: 1.1 !important; text-align: center; }
    .goal-text { font-size: 24px !important; color: #333; line-height: 1.6; background: white; padding: 35px; border-left: 15px solid #004aad; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); text-align: justify; }
    .custom-card { background: white; border-radius: 25px; padding: 35px 20px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.05); transition: all 0.3s ease; border: 1px solid #eee; height: 280px; margin-bottom: 20px; }
    .card-icon { font-size: 60px; margin-bottom: 15px; }
    .card-title { color: #004aad; font-size: 24px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR (Цэс)
menu_list = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил төлөвшил МХБ"]

with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None, 
        options=menu_list,
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        default_index=menu_list.index(st.session_state.menu_option),
        key="main_menu",
        styles={
            "container": {"background-color": "#004aad", "padding": "0"},
            "icon": {"color": "white", "font-size": "20px"}, 
            "nav-link": {"font-size": "17px", "color": "white", "font-weight": "bold", "margin": "5px"},
            "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)"},
        }
    )
    st.session_state.menu_option = selected

# 5. АГУУЛГА УДИРДАХ
# --- НҮҮР ХУУДАС ---
if st.session_state.menu_option == "Нүүр хуудас":
    st.markdown('<p class="main-header">Бидний зорилго</p>', unsafe_allow_html=True)
    st.markdown('<div class="goal-text">Математикийн ертөнцөөр хамтдаа аялж, сонирхолтой цахим хичээл, бодлогын сангаар дамжуулан өөрийн мэдлэг чадвараа бие даан ахиулж, ирээдүйн амжилтынхаа эхлэлийг өнөөдөр тавьцгаая!</div>', unsafe_allow_html=True)
    st.write("") # Зай авах
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="custom-card"><div class="card-icon">📺</div><div class="card-title">Цахим контент</div></div>', unsafe_allow_html=True)
        if st.button("Үзэх", key="btn_content"):
            st.session_state.menu_option = "Цахим контент"; st.rerun()
    with col2:
        st.markdown('<div class="custom-card"><div class="card-icon">📚</div><div class="card-title">Даалгаврын сан</div></div>', unsafe_allow_html=True)
        if st.button("Нээх", key="btn_bank"):
            st.session_state.menu_option = "Даалгаврын сан"; st.rerun()
    with col3:
        st.markdown('<div class="custom-card"><div class="card-icon">📝</div><div class="card-title">Сорил</div></div>', unsafe_allow_html=True)
        if st.button("Эхлэх", key="btn_test"):
            st.session_state.menu_option = "Сорил"; st.rerun()

# --- СОРИЛ ХЭСЭГ ---
elif st.session_state.menu_option == "Сорил":
    st.markdown('<p class="main-header">📝 Онлайн сорилтын систем</p>', unsafe_allow_html=True)
    
    units = [
        "Үнэлгээний нэгж 1. Тоон олонлог, зэрэг, язгуур, тоог жиших, тоймлох",
        "Үнэлгээний нэгж 2. Харьцаа, пропорц, процент",
        "Үнэлгээний нэгж 3. Алгебрын илэрхийлэл, тэгшитгэл, тэнцэтгэл биш",
        "Үнэлгээний нэгж 4. Дараалал, функц",
        "Үнэлгээний нэгж 5. Өнцөг, дүрс, байгуулалт",
        "Үнэлгээний нэгж 6. Байршил, хөдөлгөөн, хувиргалт",
        "Үнэлгээний нэгж 7. Хэмжигдэхүүн",
        "Үнэлгээний нэгж 8. Магадлал, статистик"
    ]

    for i, unit_name in enumerate(units, 1):
        with st.expander(f"🔹 {unit_name}"):
            st.write("Аль хувилбарыг бөглөх вэ?")
            c1, c2, c3, c4 = st.columns(4)
            for j, var in enumerate(['A', 'B', 'C', 'D']):
                if [c1, c2, c3, c4][j].button(f"{var} хувилбар", key=f"v_{i}_{var}"):
                    st.success(f"{unit_name}-ын {var} хувилбар удахгүй нэмэгдэнэ.")

# --- БУСАД ХУУДАС ---
else:
    st.markdown(f'<p class="main-header">{st.session_state.menu_option}</p>', unsafe_allow_html=True)
    st.write("Энэ хуудасны агуулга бэлтгэгдэж байна.")
