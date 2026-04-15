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
    [data-testid="stSidebar"] { background-color: #004aad !important; min-width: 300px !important; }
    .sidebar-title { color: #ffffff !important; text-align: center; font-size: 40px !important; font-weight: bold; padding: 20px 0; border-bottom: 2px solid rgba(255,255,255,0.3); margin-bottom: 20px; }
    .main-header { color: #004aad !important; font-size: 55px !important; font-weight: 900; margin: 0px 0px 15px 0px !important; line-height: 1.1 !important; }
    .goal-text { font-size: 24px !important; color: #333; line-height: 1.6; background: white; padding: 35px; border-left: 15px solid #004aad; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); text-align: justify; }
    .logo-container { display: flex; justify-content: center; align-items: center; }
    .custom-card { background: white; border-radius: 25px; padding: 35px 20px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.05); transition: all 0.3s ease; border: 1px solid #eee; height: 280px; }
    .custom-card:hover { transform: translateY(-10px); box-shadow: 0 15px 35px rgba(0,74,173,0.15); }
    .card-icon { font-size: 60px; margin-bottom: 15px; }
    .card-title { color: #004aad; font-size: 24px; font-weight: bold; }
    .quiz-card { background: white; padding: 30px; border-radius: 20px; border-top: 10px solid #004aad; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-top: 20px; }
    [data-testid="stHeaderActionElements"], .stAppDeployButton { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Цэс)
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
        st.markdown('<div class="goal-text">Математикийн ертөнцөөр хамтдаа аялж, сонирхолтой цахим хичээл, бодлогын сангаар дамжуулан өөрийн мэдлэг чадвараа бие даан ахиулж, ирээдүйн амжилтынхаа эхлэлийг өнөөдөр тавьцгаая!</div>', unsafe_allow_html=True)
# --- Нүүр хуудас ---
if selected == "Нүүр хуудас":
    st.markdown('<p class="main-header">Математикийн сургалтын системд тавтай морил!</p>', unsafe_allow_html=True)
    st.write("Бид танд математикийн хичээлийг илүү сонирхолтой, хялбар аргаар сурахад туслах болно.")
    
    # Картуудыг товчлуур болгож холбох
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="custom-card"><div class="card-icon">📺</div><div class="card-title">Цахим контент</div></div>', unsafe_allow_html=True)
        if st.button("Үзэх", key="btn_content"):
            st.session_state.menu_option = "Цахим контент"
            st.rerun()

    with col2:
        st.markdown('<div class="custom-card"><div class="card-icon">📚</div><div class="card-title">Даалгаврын сан</div></div>', unsafe_allow_html=True)
        if st.button("Нээх", key="btn_bank"):
            st.session_state.menu_option = "Даалгаврын сан"
            st.rerun()

    with col3:
        st.markdown('<div class="custom-card"><div class="card-icon">📝</div><div class="card-title">Сорил</div></div>', unsafe_allow_html=True)
        if st.button("Эхлэх", key="btn_test"):
            # "Сорил" цэс рүү үсэрч орох
            st.session_state.menu_option = "Сорил"
            st.rerun()

# --- Сорил хэсэг ---
elif selected == "Сорил" or (hasattr(st.session_state, 'menu_option') and st.session_state.menu_option == "Сорил"):
    import time
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=1000, key="timer_refresh")

    st.markdown('<p class="main-header" style="text-align: center;">📝 Онлайн сорилтын систем</p>', unsafe_allow_html=True)

    if 'current_test' not in st.session_state:
        # Таны зургийн дагуу яг ижил нэршлүүд
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
                col1, col2, col3, col4 = st.columns(4)
                for j, var in enumerate(['A', 'B', 'C', 'D']):
                    if [col1, col2, col3, col4][j].button(f"{var} хувилбар", key=f"btn_{i}_{var}"):
                        st.session_state.current_test = {"unit": i, "variant": var, "name": unit_name}
                        st.session_state.test_start_time = time.time()
                        st.rerun()
    else:
        # Шалгалт өгөх болон үр дүн харах хэсэг (Өмнөх логик хэвээрээ)
        test = st.session_state.current_test
        st.info(f"📖 {test['name']} - {test['variant']} хувилбар")
        if st.button("🔙 Сорил сонгох руу буцах"):
            del st.session_state.current_test
            st.rerun()
