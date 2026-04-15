import streamlit as st
from streamlit_option_menu import option_menu
import time

# 1. Сонгогдсон цэсийг санах ойд хадгалах (Энэ хэсэг шилжилтийг хариуцна)
if 'menu_option' not in st.session_state:
    st.session_state.menu_option = "Нүүр хуудас"

# Вэбсайтын тохиргоо
st.set_page_config(page_title="Математикийн сургалт", layout="wide")

# CSS загвар (Таны өмнөх загвар хэвээрээ)
st.markdown("""
    <style>
    .main-header { font-size: 36px; font-weight: bold; color: #1E88E5; text-align: center; margin-bottom: 30px; }
    .custom-card { background-color: #f8f9fa; padding: 20px; border-radius: 15px; border: 1px solid #dee2e6; text-align: center; height: 200px; }
    .card-icon { font-size: 50px; margin-bottom: 10px; }
    .card-title { font-size: 20px; font-weight: bold; color: #333; }
    </style>
    """, unsafe_allow_html=True)

# 2. Зүүн талын цэс
menu_list = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил төлөвшлөө МХБ"]

with st.sidebar:
    # default_index нь товчлуур дарахад цэсийг дагаж хөдлөхөд тусална
    selected = option_menu(
        "ЦЭС", 
        menu_list,
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        menu_icon="cast", 
        default_index=menu_list.index(st.session_state.menu_option),
        key="main_menu_key"
    )
    # Цэс дээр дарахад төлөвийг шинэчлэх
    st.session_state.menu_option = selected

# --- ХУУДАСНУУДЫН УДИРДЛАГА ---

# 🏠 НҮҮР ХУУДАС
if st.session_state.menu_option == "Нүүр хуудас":
    st.markdown('<p class="main-header">Математикийн сургалтын систем</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="custom-card"><div class="card-icon">📺</div><div class="card-title">Цахим контент</div></div>', unsafe_allow_html=True)
        if st.button("Үзэх", key="go_content"):
            st.session_state.menu_option = "Цахим контент"
            st.rerun()

    with col2:
        st.markdown('<div class="custom-card"><div class="card-icon">📚</div><div class="card-title">Даалгаврын сан</div></div>', unsafe_allow_html=True)
        if st.button("Нээх", key="go_bank"):
            st.session_state.menu_option = "Даалгаврын сан"
            st.rerun()

    with col3:
        st.markdown('<div class="custom-card"><div class="card-icon">📝</div><div class="card-title">Сорил</div></div>', unsafe_allow_html=True)
        if st.button("Эхлэх", key="go_test"):
            # ЭНД ДАРАХАД СОРИЛ РУУ ҮСРЭН ОРНО!
            st.session_state.menu_option = "Сорил"
            st.rerun()

# 📝 СОРИЛ ХЭСЭГ
elif st.session_state.menu_option == "Сорил":
    st.markdown('<p class="main-header">📝 Онлайн сорилтын систем</p>', unsafe_allow_html=True)
    
    # Таны нэршлээр
