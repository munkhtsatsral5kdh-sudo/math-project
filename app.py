import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import time
import pandas as pd
import re
from streamlit_autorefresh import st_autorefresh

# 1. СИСТЕМ ТӨЛӨВ
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Нүүр хуудас"
if 'test_started' not in st.session_state:
    st.session_state.test_started = False

st.set_page_config(page_title="Математикийн багш", page_icon="📐", layout="wide")

# 2. ТАНЫ ЗУРАГ ДЭЭРХ ШИГ ӨНГӨ БОЛОН ДИЗАЙН (CSS)
st.markdown("""
    <style>
    /* Ерөнхий дэвсгэр өнгө */
    .stApp { background-color: #f4f7f9; }
    
    /* Цэсний хэсэг - Яг зураг дээрх өнгө */
    [data-testid="stSidebar"] { 
        background-color: #0b2447 !important; 
        min-width: 280px !important; 
    }
    
    /* Цэсний гарчиг */
    .sidebar-title { 
        color: #ffffff !important; 
        text-align: center; 
        font-size: 32px !important; 
        font-weight: 800; 
        padding: 30px 0; 
        letter-spacing: 2px;
    }
    
    /* Зорилго хэсэг - Тэгшлэлт ба Догол мөр */
    .goal-box {
        background: #ffffff; 
        padding: 30px; 
        border-radius: 12px; 
        border-left: 10px solid #19376d;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        margin-top: 20px;
    }
    .goal-text { 
        font-size: 20px !important; 
        color: #2c3333; 
        line-height: 1.8; 
        text-align: justify;    /* Хоёр талыг тэгшлэх */
        text-indent: 50px;      /* Догол мөр авах */
        margin: 0;
    }

    /* Сорилтын товчлуурууд - Өнгө өнгөөрөө */
    .btn-green { background-color: #28a745 !important; color: white !important; }
    .btn-blue { background-color: #007bff !important; color: white !important; }
    .btn-gray { background-color: #6c757d !important; color: white !important; }
    .btn-red { background-color: #dc3545 !important; color: white !important; }

    /* Математик бодлогын карт */
    .math-card {
        background: white; 
        padding: 25px; 
        border-radius: 15px; 
        border: 1px solid #e0e0e0;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Цэс)
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    
    # Зураг дээрх цэсүүдийг яг ижил дарааллаар
    menu_options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил"]
    
    selected = option_menu(None, menu_options, 
                           icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'], 
                           default_index=0,
                           styles={
                               "container": {"background-color": "#0b2447", "padding": "5px"},
                               "nav-link": {"color": "#a5c0dd", "font-size": "17px", "text-align": "left", "margin":"10px"},
                               "nav-link-selected": {"background-color": "#19376d", "color": "white", "font-weight": "bold"},
                           })
    
    if selected != st.session_state.selected_menu:
        st.session_state.selected_menu = selected
        st.rerun()

# 4. EXCEL-ЭЭС УНШИХ ФУНКЦ (Ухаалаг форматлагч)
def show_math_question(text):
    if not isinstance(text, str): return
    # Сонголтуудыг (A., B., C., D.) дараагийн мөр рүү шилжүүлж тодоор харуулах
    formatted = re.sub(r'([A-D]\.)', r'\n\n**\1**', text)
    st.markdown(formatted)

# 5. ХУУДАСНЫ АГУУЛГА

if st.session_state.selected_menu == "Нүүр хуудас":
    col1, col2 = st.columns([1, 1.8], gap="large")
    with col1:
        if os.path.exists("logo.gif"):
            with open("logo.gif", "rb") as f:
                st.markdown(f'<img src="data:image/gif;base64,{base64.b64encode(f.read()).decode()}" width="100%">', unsafe_allow_html=True)
        st.markdown('<h2 style="color:#28a745; text-align:center;">МАТЕМАТИК БАГШ</h2>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<h1 style="color:#0b2447;">Бидний зорилго</h1>', unsafe_allow_html=True)
        st.markdown(f'<div class="goal-box"><p class="goal-text">Математикийн ертөнцөөр хамтдаа аялж, сонирхолтой цахим хичээл, бодлогын сангаар дамжуулан өөрийн мэдлэг чадвараа бие даан ахиулж, ирээдүйн амжилтынхаа эхлэлийг өнөөдөр тавьцгаая! Бид сурагч бүрт математик сэтгэлгээг хялбар бөгөөд сонирхолтой байдлаар хүргэхийг зорьж байна.</p></div>', unsafe_allow_html=True)

    st.write("---")
    # Нүүр хуудасны 3 том товчлуур
    c1, c2, c3 = st.columns(3)
    main_btns = [("📺", "Цахим контент"), ("📚", "Даалгаврын сан"), ("📝", "Сорил")]
    for i, (icon, title) in enumerate(main_btns):
        with [c1, c2, c3][i]:
            st.markdown(f'<div style="background:white; padding:30px; border-radius:20px; text-align:center; box-shadow:0 10px 20px rgba(0,0,0,0.05);"><h1>{icon}</h1><h3>{title}</h3></div>', unsafe_allow_html=True)
            if st.button(f"{title} руу орох", key=f"home_btn_{i}", use_container_width=True):
                st.session_state.selected_menu = title
                st.rerun()

elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown('<h1 style="color:#0b2447; text-align:center;">📚 Даалгаврын сан</h1>', unsafe_allow_html=True)
    if os.path.exists("data_bank.xlsx"):
        df = pd.read_excel("data_bank.xlsx")
        unit = st.selectbox("Сэдвийн нэр сонгох:", df['Нэгж'].unique())
        tabs = st.tabs(["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"])
        
        for idx, lvl in enumerate(["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"]):
            with tabs[idx]:
                f_df = df[(df['Нэгж'] == unit) & (df['Түвшин'] == lvl)]
                for i, row in f_df.iterrows():
                    with st.container():
                        st.markdown('<div class="math-card">', unsafe_allow_html=True)
                        st.write(f"**Бодлого {i+1}**")
                        show_math_question(row['Асуулт'])
                        
                        ans = st.radio("Хариу:", ["A", "B", "C", "D"], key=f"ans_{lvl}_{i}", horizontal=True)
                        if st.button("Шалгах", key=f"chk_{lvl}_{i}"):
                            if str(ans).strip().upper() == str(row['Хариу']).strip().upper():
                                st.success("Зөв! ✅"); st.balloons()
                            else: st.error(f"Буруу байна. Зөв хариу: {row['Хариу']}")
                        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.selected_menu == "Сорил":
    st.markdown('<h1 style="color:#0b2447; text-align:center;">📝 Онлайн сорил</h1>', unsafe_allow_html=True)
    if not st.session_state.test_started:
        for i in range(1, 9):
            with st.expander(f"🔹 Үнэлгээний нэгж {i}"):
                st.write("Хувилбар сонгоно уу:")
                v_cols = st.columns(4)
                for j, var in enumerate(['A', 'B', 'C', 'D']):
                    if v_cols[j].button(f"{var} хувилбар", key=f"v_{i}_{var}"):
                        st.session_state.active_unit = f"Нэгж {i} - {var} хувилбар"
                
                if st.session_state.get('active_unit') and f"Нэгж {i}" in st.session_state.active_unit:
                    st.info(f"Сонгосон: {st.session_state.active_unit}")
                    # 4 ӨНГӨТЭЙ ТОВЧЛУУР (Яг зураг дээрх шиг)
                    b1, b2, b3, b4 = st.columns(4)
                    if b1.button("🟢 ЭХЛЭХ", key=f"start_{i}", use_container_width=True):
                        st.session_state.test_started = True
                        st.session_state.start_time = time.time()
                        st.rerun()
                    b2.button("🔵 ДҮН", key=f"res_{i}", use_container_width=True)
                    b3.button("⚪ АЛДАА", key=f"err_{i}", use_container_width=True)
                    b4.button("🔴 БОДОЛТ", key=f"sol_{i}", use_container_width=True)
    else:
        st_autorefresh(interval=1000, key="timer")
        rem = (40 * 60) - (time.time() - st.session_state.start_time)
        if rem <= 0:
            st.error("⏰ Хугацаа дууслаа!"); st.session_state.test_started = False
        else:
            m, s = divmod(int(rem), 60)
            st.sidebar.markdown(f'<div style="background-color:#ff4b4b; padding:20px; color:white; border-radius:10px; text-align:center;"><h2>⏱️ {m:02d}:{s:02d}</h2></div>', unsafe_allow_html=True)
            st.subheader(st.session_state.active_unit)
            if st.button("🏁 СОРИЛ ДУУСГАХ"):
                st.session_state.test_started = False
                st.rerun()
                
