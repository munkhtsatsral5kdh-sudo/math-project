import streamlit as st
from streamlit_option_menu import option_menu
import time

# 1. Сонгогдсон цэсийг санах ойд хадгалах
if 'menu_option' not in st.session_state:
    st.session_state.menu_option = "Нүүр хуудас"

# Вэбсайтын тохиргоо
st.set_page_config(page_title="Математикийн сургалт", layout="wide")

# CSS загвар (Таны өөрийн загвар)
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
    selected = option_menu(
        "ЦЭС", 
        menu_list,
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        menu_icon="cast", 
        default_index=menu_list.index(st.session_state.menu_option),
        key="main_menu_key"
    )
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
            st.session_state.menu_option = "Сорил"
            st.rerun()

# 📝 СОРИЛ ХЭСЭГ
elif st.session_state.menu_option == "Сорил":
    st.markdown('<h1 style="text-align: center;">📝 Онлайн сорилтын систем</h1>', unsafe_allow_html=True)
    
    # Таны хүссэн нэршлүүд
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
            col_a, col_b, col_c, col_d = st.columns(4)
            # 4 хувилбарын товчлуур
            if col_a.button(f"A хувилбар", key=f"a_{i}"):
                st.info(f"{unit_name}-ын A хувилбар бэлтгэгдэж байна.")
            if col_b.button(f"B хувилбар", key=f"b_{i}"):
                st.info(f"{unit_name}-ын B хувилбар бэлтгэгдэж байна.")
            if col_c.button(f"C хувилбар", key=f"c_{i}"):
                st.info(f"{unit_name}-ын C хувилбар бэлтгэгдэж байна.")
            if col_d.button(f"D хувилбар", key=f"d_{i}"):
                st.info(f"{unit_name}-ын D хувилбар бэлтгэгдэж байна.")

# БУСАД ХУУДАСНУУД
else:
    st.write(f"### {st.session_state.menu_option} хуудас бэлтгэгдэж байна.")
