import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import time
import pandas as pd
import re
from streamlit_autorefresh import st_autorefresh

# 1. СИСТЕМ ТӨЛӨВ - Тогтвортой ажиллагаа
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Нүүр хуудас"
if 'test_started' not in st.session_state:
    st.session_state.test_started = False

st.set_page_config(page_title="Математикийн багш", page_icon="📐", layout="wide")

# 2. ТӨГС ДИЗАЙН (Таны зургууд дээрх яг тэр өнгөнүүд)
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    
    /* Цэсний хэсэг: Яг зураг дээрх тэр цайвардуу гүн цэнхэр */
    [data-testid="stSidebar"] { 
        background-color: #1a3c6d !important; 
        min-width: 290px !important; 
    }
    
    .sidebar-title { 
        color: #ffffff !important; 
        text-align: center; 
        font-size: 30px !important; 
        font-weight: bold; 
        padding: 25px 0; 
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Зорилго хэсэг: Тэгшлэлт + Догол мөр (Маш цэвэрхэн) */
    .goal-box {
        background: #ffffff; 
        padding: 35px; 
        border-radius: 4px; 
        border-top: 5px solid #1a3c6d;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-top: 20px;
    }
    .goal-text { 
        font-size: 21px !important; 
        color: #333; 
        line-height: 2.0; 
        text-align: justify; 
        text-indent: 55px; 
        font-family: 'Times New Roman', serif;
    }

    /* Сорилтын товчлуурууд: Дөрвөлжин загвар */
    .stButton>button {
        border-radius: 4px !important;
        font-weight: bold !important;
        height: 45px !important;
        border: none !important;
    }

    /* Математик бодлогын карт */
    .math-card {
        background: white; 
        padding: 30px; 
        border-radius: 8px; 
        border: 1px solid #e0e0e0;
        margin-bottom: 25px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Цэс - Өнгөний нарийн тохиргоотой)
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    
    menu_options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил"]
    
    selected = option_menu(None, menu_options, 
                           icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'], 
                           default_index=0,
                           styles={
                               "container": {"background-color": "#1a3c6d", "padding": "0px"},
                               "nav-link": {"color": "#cbd5e0", "font-size": "17px", "text-align": "left", "margin":"12px", "font-weight": "400"},
                               "nav-link-selected": {"background-color": "#2d5a9e", "color": "white", "font-weight": "600"},
                           })
    
    if selected != st.session_state.selected_menu:
        st.session_state.selected_menu = selected
        st.rerun()

# 4. MATH FORMATTER (Excel-ийн бодлогуудыг LaTeX-ээр гоё харуулах)
def render_math(text):
    if not isinstance(text, str): return
    # A. B. C. D. форматлах
    formatted = re.sub(r'([A-D]\.)', r'\n\n**\1**', text)
    # Томьёог таньж LaTeX болгох
    if any(c in text for c in ['^', '_', '/', '\\', '{', '=', '+', '-']):
        st.latex(formatted.replace('**', ''))
    else:
        st.markdown(f'<div style="font-size:20px;">{formatted}</div>', unsafe_allow_html=True)

# 5. ХУУДАСНУУД

if st.session_state.selected_menu == "Нүүр хуудас":
    col1, col2 = st.columns([1, 1.8], gap="large")
    with col1:
        if os.path.exists("logo.gif"):
            with open("logo.gif", "rb") as f:
                st.markdown(f'<img src="data:image/gif;base64,{base64.b64encode(f.read()).decode()}" width="100%">', unsafe_allow_html=True)
        st.markdown('<h2 style="color:#28a745; text-align:center; font-weight:bold;">МАТЕМАТИК БАГШ</h2>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<h1 style="color:#1a3c6d; border-bottom: 3px solid #28a745; display: inline-block;">Бидний зорилго</h1>', unsafe_allow_html=True)
        st.markdown(f'<div class="goal-box"><p class="goal-text">Математикийн ертөнцөөр хамтдаа аялж, сонирхолтой цахим хичээл, бодлогын сангаар дамжуулан өөрийн мэдлэг чадвараа бие даан ахиулж, ирээдүйн амжилтынхаа эхлэлийг өнөөдөр тавьцгаая! Бид сурагч бүрт математик сэтгэлгээг хялбар бөгөөд сонирхолтой байдлаар хүргэхийг зорьж байна.</p></div>', unsafe_allow_html=True)

    st.write("###")
    # Нүүр хуудасны 3 том карт
    c1, c2, c3 = st.columns(3)
    main_items = [("📺", "Цахим контент"), ("📚", "Даалгаврын сан"), ("📝", "Сорил")]
    for i, (icon, title) in enumerate(main_items):
        with [c1, c2, c3][i]:
            st.markdown(f'<div style="background:white; padding:40px; border-radius:10px; text-align:center; border: 1px solid #eee; box-shadow:0 4px 10px rgba(0,0,0,0.03);"><h1>{icon}</h1><h3>{title}</h3></div>', unsafe_allow_html=True)
            if st.button(f"Орох", key=f"h_btn_{i}", use_container_width=True):
                st.session_state.selected_menu = title
                st.rerun()

elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown('<h1 style="color:#1a3c6d; text-align:center;">📚 Даалгаврын сан</h1>', unsafe_allow_html=True)
    if os.path.exists("data_bank.xlsx"):
        df = pd.read_excel("data_bank.xlsx")
        unit = st.selectbox("Хичээлийн сэдэв:", df['Нэгж'].unique())
        t1, t2, t3 = st.tabs(["🔹 Мэдлэг ойлголт", "🔹 Чадвар", "🔹 Хэрэглээ"])
        
        for idx, lvl in enumerate(["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"]):
            with [t1, t2, t3][idx]:
                f_df = df[(df['Нэгж'] == unit) & (df['Түвшин'] == lvl)]
                for i, row in f_df.iterrows():
                    st.markdown('<div class="math-card">', unsafe_allow_html=True)
                    st.write(f"**Асуулт {i+1}**")
                    render_math(row['Асуулт'])
                    
                    ans = st.radio("Хариулт сонгох:", ["A", "B", "C", "D"], key=f"q_{lvl}_{i}", horizontal=True)
                    if st.button("Хариу шалгах", key=f"b_{lvl}_{i}"):
                        if str(ans).strip().upper() == str(row['Хариу']).strip().upper():
                            st.success("Зөв байна! ✅"); st.balloons()
                        else: st.error(f"Буруу. Зөв хариу: {row['Хариу']}")
                    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.selected_menu == "Сорил":
    st.markdown('<h1 style="color:#1a3c6d; text-align:center;">📝 Онлайн сорил</h1>', unsafe_allow_html=True)
    if not st.session_state.test_started:
        for i in range(1, 9):
            with st.expander(f"📌 Үнэлгээний нэгж {i}"):
                v_cols = st.columns(4)
                for j, var in enumerate(['A', 'B', 'C', 'D']):
                    if v_cols[j].button(f"{var} хувилбар", key=f"var_{i}_{var}"):
                        st.session_state.active_unit = f"Нэгж {i} - {var} хувилбар"
                
                if st.session_state.get('active_unit') and f"Нэгж {i}" in st.session_state.active_unit:
                    st.markdown(f"--- \n **Сонгосон:** `{st.session_state.active_unit}`")
                    b1, b2, b3, b4 = st.columns(4)
                    # Өнгөтэй товчлуурууд
                    if b1.button("🟢 ЭХЛЭХ", key=f"st_{i}", use_container_width=True):
                        st.session_state.test_started = True
                        st.session_state.start_time = time.time()
                        st.rerun()
                    b2.button("🔵 ДҮН", key=f"re_{i}", use_container_width=True)
                    b3.button("⚪ АЛДАА", key=f"er_{i}", use_container_width=True)
                    b4.button("🔴 БОДОЛТ", key=f"so_{i}", use_container_width=True)
    else:
        st_autorefresh(interval=1000, key="quiz_timer")
        rem = (40 * 60) - (time.time() - st.session_state.start_time)
        if rem <= 0:
            st.error("⏰ Хугацаа дууслаа!"); st.session_state.test_started = False
        else:
            m, s = divmod(int(rem), 60)
            st.sidebar.markdown(f'<div style="background-color:#d9534f; padding:20px; color:white; border-radius:4px; text-align:center;"><h2>⏱️ {m:02d}:{s:02d}</h2></div>', unsafe_allow_html=True)
            st.subheader(st.session_state.active_unit)
            if st.button("🏁 СОРИЛ ДУУСГАХ", use_container_width=True):
                st.session_state.test_started = False
                st.rerun()
