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
    cards = [
        {"icon": "📺", "title": "Цахим контент", "desc": "Видео хичээл болон интерактив материалууд"},
        {"icon": "📚", "title": "Даалгаврын сан", "desc": "Өөрийгөө сорих бодлого, дасгалууд"},
        {"icon": "📝", "title": "Сорил", "desc": "Мэдлэгээ шалгах онлайн шалгалтууд"}
    ]
    for i, col in enumerate([c1, c2, c3]):
        with col:
            st.markdown(f'<div class="custom-card"><div class="card-icon">{cards[i]["icon"]}</div><div class="card-title">{cards[i]["title"]}</div><p style="color:#777; font-size:15px; margin-top:10px;">{cards[i]["desc"]}</p></div>', unsafe_allow_html=True)

elif selected == "Сорил":
    import time
    from streamlit_autorefresh import st_autorefresh

    # Секунд бүр хуудсыг шинэчлэх (requirements.txt-д streamlit-autorefresh нэмсэн байх шаардлагатай)
    st_autorefresh(interval=1000, key="timer_refresh")

    st.markdown('<p class="main-header" style="text-align: center;">📝 Онлайн сорилтын систем</p>', unsafe_allow_html=True)

    # 1. Сорил сонгогдоогүй үед жагсаалтыг харуулах
    if 'current_test' not in st.session_state:
        st.write("### 📋 Үнэлгээний нэгжүүд")
        
        # 8 нэгжийн жагсаалт
        units = [
            "Үнэлгээний нэгж 1. Тоон олонлог, зэрэг, язгуур",
            "Үнэлгээний нэгж 2. Харьцаа, пропорц, процент",
            "Үнэлгээний нэгж 3. Алгебрын илэрхийлэл",
            "Үнэлгээний нэгж 4. Дараалал, функц",
            "Үнэлгээний нэгж 5. Өнцөг, дүрс, байгуулалт",
            "Үнэлгээний нэгж 6. Байршил, хөдөлгөөн, хувиргалт",
            "Үнэлгээний нэгж 7. Хэмжигдэхүүн",
            "Үнэлгээний нэгж 8. Магадлал, статистик"
        ]

        for i, unit_name in enumerate(units, 1):
            with st.expander(f"🔹 {unit_name}"):
                st.write("Аль хувилбарыг бөглөх вэ?")
                col1, col2, col3, col4 = st.columns(4)
                
                # Хувилбар бүрт "Эхлэх" товчлуур
                for j, variant in enumerate(['A', 'B', 'C', 'D']):
                    with [col1, col2, col3, col4][j]:
                        if st.button(f"{variant} хувилбар", key=f"btn_{i}_{variant}"):
                            st.session_state.current_test = {"unit": i, "variant": variant, "name": unit_name}
                            st.session_state.test_start_time = time.time()
                            st.rerun()

    # 2. Шалгалт өгөх явц
    else:
        test = st.session_state.current_test
        elapsed = time.time() - st.session_state.test_start_time
        total_time = 40 * 60 # 40 минут
        remaining = total_time - elapsed

        if remaining > 0:
            mins, secs = divmod(int(remaining), 60)
            
            # Толгой хэсэг: Нэр болон Хугацаа
            st.info(f"📖 {test['name']} | **{test['variant']} ХУВИЛБАР**")
            st.markdown(f"""
                <div style="text-align: center; background-color: #1e1e1e; padding: 10px; border-radius: 10px; border: 2px solid #ffca28;">
                    <h2 style="margin:0; color: white;">🕒 Үлдсэн хугацаа: <span style="color: #ff4b4b;">{mins:02d}:{secs:02d}</span></h2>
                </div>
            """, unsafe_allow_html=True)

            # Асуултуудыг Нэгж ба Хувилбараар ялгаж харуулах
            if test['unit'] == 5 and test['variant'] == 'A':
                with st.form("variant_a_form"):
                    st.write("### I ХЭСЭГ. СОНГОХ ДААЛГАВАР")
                    # PDF-ээс авсан асуултууд
                    q1 = st.radio("1. Тэгш өнцөгт △ABC-ийн ∠C=90° бол sinA харьцааг нэрлэнэ үү.", ["AC/AB", "BC/AB", "BC/AC", "AC/BC"], index=None)
                    # ... бусад асуултууд ...
                    
                    if st.form_submit_button("Шалгалтыг дуусгах"):
                        st.balloons()
                        st.success("Шалгалт дууслаа!")
                        time.sleep(2)
                        del st.session_state.current_test
                        st.rerun()
            else:
                st.warning(f"Уучлаарай, {test['unit']}-р нэгжийн {test['variant']} хувилбарын асуултууд хараахан ороогүй байна.")
                if st.button("Буцах"):
                    del st.session_state.current_test
                    st.rerun()
        else:
            st.error("⌛ Хугацаа дууслаа!")
            if st.button("Цэс рүү буцах"):
                del st.session_state.current_test
                st.rerun()
            if st.button("Сорил руу буцах"):
                del st.session_state.current_test
                st.rerun()
