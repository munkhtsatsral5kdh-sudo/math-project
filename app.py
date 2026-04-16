import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import pandas as pd

# 1. Сайтын ерөнхий тохиргоо
st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# --- СИСТЕМ: ЦЭСНИЙ УДИРДЛАГА ---
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Нүүр хуудас"

# 2. ДИЗАЙН (Modern & Clean UI)
st.markdown("""
    <style>
    /* Ерөнхий дэвсгэр */
    .stApp { background-color: #f4f7f9; }
    
    /* Хажуугийн цэс - Илүү зөөлөн цэнхэр */
    [data-testid="stSidebar"] { 
        background-color: #1e3a8a !important; 
        min-width: 320px !important;
    }
    
    .sidebar-title { 
        color: white; text-align: center; font-size: 32px; font-weight: 700; 
        padding: 30px 0; letter-spacing: 2px;
    }

    /* "Бидний зорилго" карт */
    .goal-box {
        background: white; padding: 40px; border-radius: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.05);
        border: none;
        transition: 0.3s;
    }
    .main-header { 
        color: #1e3a8a; font-size: 48px; font-weight: 800; margin-bottom: 15px;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Төв хэсгийн товчлуурууд - Илүү "Premium" харагдац */
    div.stButton > button {
        width: 100% !important; 
        height: 320px !important; 
        border-radius: 30px !important; 
        border: none !important; 
        background: white !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.04) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }

    div.stButton > button:hover {
        transform: translateY(-12px) !important;
        box-shadow: 0 20px 45px rgba(30,58,138,0.12) !important;
        background: linear-gradient(145deg, #ffffff, #f0f4ff) !important;
    }

    /* Товчлуур доторх текстийг засах */
    div.stButton > button p {
        font-size: 22px !important; 
        font-weight: 600 !important;
        color: #1e3a8a !important;
        margin-top: 15px !important;
    }

    /* Сорил, Даалгаврын сангийн картууд */
    .math-card {
        background: white; padding: 30px; border-radius: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.03);
        margin-bottom: 25px;
        border: 1px solid #edf2f7;
    }

    /* Streamlit-ийн зарим default элементүүдийг нуух/засах */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Цэс)
with st.sidebar:
    st.markdown('<p class="sidebar-title">МАТЕМАТИК</p>', unsafe_allow_html=True)
    
    menu_options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил"]
    current_index = menu_options.index(st.session_state.selected_menu) if st.session_state.selected_menu in menu_options else 0

    selected = option_menu(
        menu_title=None, 
        options=menu_options,
        icons=['house-door', 'play-circle', 'journal-text', 'pencil-square', 'people-fill', 'heart-pulse'],
        default_index=current_index,
        styles={
            "container": {"background-color": "transparent", "padding": "10px"},
            "icon": {"color": "#94a3b8", "font-size": "20px"}, 
            "nav-link": {"font-size": "17px", "color": "white", "font-weight": "500", "padding": "15px", "border-radius": "12px", "margin-bottom": "8px"},
            "nav-link-selected": {"background-color": "rgba(255,255,255,0.15)", "color": "white", "font-weight": "700"},
        }
    )
    if selected != st.session_state.selected_menu:
        st.session_state.selected_menu = selected
        st.rerun()

# 4. НҮҮР ХУУДАС
if st.session_state.selected_menu == "Нүүр хуудас":
    # Дээд хэсэг: Лого болон Зорилго
    col_img, col_txt = st.columns([1, 1], gap="large")
    
    with col_img:
        if os.path.exists("logo.gif"):
            with open("logo.gif", "rb") as f:
                data_url = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(f'<img src="data:image/gif;base64,{data_url}" style="width: 100%; border-radius: 30px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
        else:
            st.image("https://via.placeholder.com/500x400.png?text=Logo+Image", use_column_width=True)
    
    with col_txt:
        st.markdown(f"""
            <div class="goal-box">
                <div class="main-header">Бидний зорилго</div>
                <div style="font-size: 22px; line-height: 1.8; color: #475569; font-family: 'Inter', sans-serif;">
                    Математикийн ертөнцөөр хамтдаа аялж, сонирхолтой цахим хичээл, 
                    бодлогын сангаар дамжуулан өөрийн мэдлэг чадвараа бие даан ахиулж, 
                    ирээдүйн амжилтынхаа эхлэлийг өнөөдөр тавьцгаая!
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Доод хэсэг: 3 Үндсэн сонголт
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="large")
    
    # Текстүүдийг илүү цэвэрхэн харагдуулахын тулд HTML ашиглаж болно, гэвч Streamlit button-д Markdown дэмждэггүй тул \n ашиглав
    with c1:
        if st.button("📺\n\nЦахим контент\n\nҮзэх", key="btn_1"):
            st.session_state.selected_menu = "Цахим контент"
            st.rerun()
            
    with c2:
        if st.button("📚\n\nДаалгаврын сан\n\nНээх", key="btn_2"):
            st.session_state.selected_menu = "Даалгаврын сан"
            st.rerun()
            
    with c3:
        if st.button("📝\n\nСорил\n\nЭхлэх", key="btn_3"):
            st.session_state.selected_menu = "Сорил"
            st.rerun()

# 5. ДААЛГАВРЫН САН (Жишээ)
elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown("<h1 style='color: #1e3a8a; text-align: center; font-weight: 800;'>📚 Бодлогын сан</h1>", unsafe_allow_html=True)
    # Excel-ээс унших код энд байрлана... (өмнөх логик хэвээрээ)
    st.info("Бодлогын сан хэсэг рүү шилжлээ. Excel файл бэлэн бол бодлогууд харагдана.")

else:
    st.markdown(f"<h1 style='color: #1e3a8a; text-align: center; margin-top: 50px;'>{st.session_state.selected_menu}</h1>", unsafe_allow_html=True)
    st.info("Энэ хэсэг одоогоор бэлтгэгдэж байна.")
