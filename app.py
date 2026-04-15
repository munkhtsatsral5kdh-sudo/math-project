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
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="medium")
    # Нүүр хуудасны картуудыг товчлуур болгох
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
            # Энэ товчийг дарахад зүүн талын цэсний "Сорил" сонгогдоно
            st.query_params["page"] = "Сорил" 
            st.session_state.menu_option = "Сорил"
            st.rerun()
elif selected == "Сорил":
    import time
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=1000, key="timer_refresh")

    # 1. Шалгалт дууссаны дараах төлөвийг шалгах
    if 'test_finished' not in st.session_state:
        st.session_state.test_finished = False

    st.markdown('<p class="main-header" style="text-align: center;">📝 Онлайн сорилтын систем</p>', unsafe_allow_html=True)

    # 2. Сорил сонгох хэсэг
    if 'current_test' not in st.session_state:
        units = ["Үнэлгээний нэгж 1", "Үнэлгээний нэгж 2", "Үнэлгээний нэгж 3", "Үнэлгээний нэгж 4", 
                 "Үнэлгээний нэгж 5", "Үнэлгээний нэгж 6", "Үнэлгээний нэгж 7", "Үнэлгээний нэгж 8"]
        for i, unit in enumerate(units, 1):
            with st.expander(f"🔹 {unit}"):
                cols = st.columns(4)
                for j, var in enumerate(['A', 'B', 'C', 'D']):
                    if cols[j].button(f"{var} хувилбар", key=f"v_{i}_{var}"):
                        st.session_state.current_test = {"unit": i, "variant": var, "name": unit}
                        st.session_state.test_start_time = time.time()
                        st.session_state.test_finished = False
                        st.rerun()

    # 3. Үр дүн харуулах хэсэг (Шалгалт дууссаны дараа)
    elif st.session_state.test_finished:
        st.success(f"🏁 {st.session_state.current_test['name']} - {st.session_state.current_test['variant']} хувилбар дууслаа.")
        
        # iMath шиг товчлуурууд
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📊 Дүн харах"):
                st.info(f"Таны оноо: {st.session_state.last_score}")
        with col2:
            if st.button("❌ Алдаа шалгах"):
                st.warning("Таны алдсан асуултууд энд харагдана (Бэлтгэгдэж байна).")
        with col3:
            if st.button("💡 Бодолт харах"):
                st.write("### Бодолтын хэсэг:")
                st.latex(r"x = \sqrt{15^2 - 9^2} = 12")
        
        if st.button("🔙 Буцах"):
            del st.session_state.current_test
            st.rerun()

    # 4. Шалгалт өгөх явц
    else:
        test = st.session_state.current_test
        remaining = (40 * 60) - (time.time() - st.session_state.test_start_time)

        if remaining > 0:
            mins, secs = divmod(int(remaining), 60)
            st.markdown(f"<h2 style='text-align:center; color:red;'>🕒 {mins:02d}:{secs:02d}</h2>", unsafe_allow_html=True)
            
            with st.form("test_form"):
                # Жишээ асуулт
                q1 = st.radio("1. Тэгш өнцөгт △ABC-ийн ∠C=90° бол sinA харьцааг нэрлэнэ үү.", ["AC/AB", "BC/AB", "BC/AC", "AC/BC"], index=None)
                
                if st.form_submit_button("Шалгалтыг дуусгах"):
                    # Оноо бодох
                    score = 1 if q1 == "BC/AB" else 0
                    st.session_state.last_score = score
                    st.session_state.test_finished = True
                    st.rerun()
        else:
            st.session_state.test_finished = True
            st.rerun()
