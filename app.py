import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import time
import pandas as pd
import re
from streamlit_autorefresh import st_autorefresh

# 1. State Management
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Нүүр хуудас"
if 'test_started' not in st.session_state:
    st.session_state.test_started = False

st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# 2. ТӨГС ДИЗАЙН (Зураг дээрх өнгө, товчлуурын загвар)
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    
    /* Цэсний хэсэг: Яг тэр гүн цэнхэр өнгө */
    [data-testid="stSidebar"] { 
        background-color: #002b5b !important; 
        min-width: 300px !important; 
    }
    .sidebar-title { 
        color: #ffffff !important; 
        text-align: center; 
        font-size: 35px !important; 
        font-weight: bold; 
        padding: 25px 0; 
        border-bottom: 2px solid rgba(255,255,255,0.1);
    }
    
    /* Зорилго хэсэг: Догол мөр + Хоёр талын зай */
    .goal-box {
        background: white; 
        padding: 35px; 
        border-radius: 15px; 
        border-left: 12px solid #002b5b;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    }
    .goal-text { 
        font-size: 22px !important; 
        color: #1f1f1f; 
        line-height: 1.9; 
        text-align: justify; 
        text-indent: 60px; 
        margin: 0;
    }
    
    /* Сорилтын 4 өнгөтэй товчлуур */
    .stButton>button { border-radius: 8px !important; font-weight: bold !important; height: 50px !important; }
    
    /* Математик бодлогын цэгцтэй харагдац */
    .math-card {
        background: white; 
        padding: 30px; 
        border-radius: 20px; 
        border: 1px solid #e0e0e0;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил төлөвшил МХБ"]
    
    selected = option_menu(None, options, 
                           icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'], 
                           default_index=options.index(st.session_state.selected_menu),
                           styles={
                               "container": {"background-color": "#002b5b", "padding": "10px"},
                               "nav-link": {"color": "white", "font-size": "18px", "text-align": "left", "margin":"8px", "--hover-color": "#004080"},
                               "nav-link-selected": {"background-color": "#0056b3", "font-weight": "bold"},
                           })
    if selected != st.session_state.selected_menu:
        st.session_state.selected_menu = selected
        st.rerun()

# 4. ФУНКЦ: Excel-ийн бичвэрийг цэвэрлэж LaTeX болгох
def clean_and_display(text):
    if not isinstance(text, str): return text
    # Сонголтуудын өмнө мөр шилжүүлэг нэмэх
    text = re.sub(r'([A-D]\.)', r'\n\n**\1**', text)
    # Хэрэв текст дотор $ байхгүй ч математик тэмдэгт байвал LaTeX орчинд оруулна
    if any(c in text for c in ['^', '_', '/', '\\', '{']):
        st.latex(text.replace('**', ''))
    else:
        st.markdown(f'<div style="font-size:20px;">{text}</div>', unsafe_allow_html=True)

# 5. CONTENT
if st.session_state.selected_menu == "Нүүр хуудас":
    c1, c2 = st.columns([1, 1.8], gap="large")
    with c1:
        if os.path.exists("logo.gif"):
            with open("logo.gif", "rb") as f:
                st.markdown(f'<img src="data:image/gif;base64,{base64.b64encode(f.read()).decode()}" width="100%">', unsafe_allow_html=True)
        st.markdown('<h1 style="color:#28a745; text-align:center; font-weight:900;">МАТЕМАТИК<br>БАГШИЙН ТУСЛАХ</h1>', unsafe_allow_html=True)
    
    with c2:
        st.markdown('<h1 style="color:#002b5b; margin-bottom:20px;">Бидний зорилго</h1>', unsafe_allow_html=True)
        st.markdown(f'<div class="goal-box"><p class="goal-text">Математикийн ертөнцөөр хамтдаа аялж, сонирхолтой цахим хичээл, бодлогын сангаар дамжуулан өөрийн мэдлэг чадвараа бие даан ахиулж, ирээдүйн амжилтынхаа эхлэлийг өнөөдөр тавьцгаая! Бид сурагч бүрт математик сэтгэлгээг хялбар бөгөөд сонирхолтой байдлаар хүргэхийг зорьж байна.</p></div>', unsafe_allow_html=True)

    st.write("---")
    # 3 Том интерактив цонх
    cols = st.columns(3)
    cards = [("📺", "Цахим контент"), ("📚", "Даалгаврын сан"), ("📝", "Сорил")]
    for i, (icon, title) in enumerate(cards):
        with cols[i]:
            st.markdown(f'<div style="background:white; padding:35px; border-radius:20px; text-align:center; box-shadow:0 10px 20px rgba(0,0,0,0.05);"><h1>{icon}</h1><h2>{title}</h2></div>', unsafe_allow_html=True)
            if st.button(f"{title} нээх ➡️", key=f"main_btn_{i}", use_container_width=True):
                st.session_state.selected_menu = title
                st.rerun()

elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown('<p class="main-header">📚 Даалгаврын сан</p>', unsafe_allow_html=True)
    if os.path.exists("data_bank.xlsx"):
        df = pd.read_excel("data_bank.xlsx")
        unit = st.selectbox("Сэдэв сонгох:", df['Нэгж'].unique())
        tabs = st.tabs(["🧠 Мэдлэг ойлголт", "🛠️ Чадвар", "🎯 Хэрэглээ"])
        
        for idx, lvl in enumerate(["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"]):
            with tabs[idx]:
                f_df = df[(df['Нэгж'] == unit) & (df['Түвшин'] == lvl)]
                for i, row in f_df.iterrows():
                    st.markdown('<div class="math-card">', unsafe_allow_html=True)
                    st.markdown(f"### 💠 Бодлого {i+1}")
                    clean_and_display(row['Асуулт'])
                    
                    ans = st.radio("Хариулт:", ["Сонгох", "A", "B", "C", "D"], key=f"r_{lvl}_{i}", horizontal=True)
                    if st.button("Шалгах ✅", key=f"c_{lvl}_{i}"):
                        if ans.strip().upper() == str(row['Хариу']).strip().upper():
                            st.success("Маш сайн! Зөв байна."); st.balloons()
                        else: st.error(f"Буруу байна. Зөв хариулт: {row['Хариу']}")
                    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.selected_menu == "Сорил":
    st.markdown('<p class="main-header">📝 Онлайн сорилтын систем</p>', unsafe_allow_html=True)
    if not st.session_state.test_started:
        for i in range(1, 9):
            with st.expander(f"💎 Үнэлгээний нэгж {i}"):
                v_cols = st.columns(4)
                for j, var in enumerate(['A', 'B', 'C', 'D']):
                    if v_cols[j].button(f"{var} хувилбар", key=f"v_{i}_{var}"):
                        st.session_state.active_unit = f"Нэгж {i} - {var}"
                
                if st.session_state.get('active_unit') and f"Нэгж {i}" in st.session_state.active_unit:
                    st.write(f"👉 **Сонгосон:** {st.session_state.active_unit}")
                    # ЗУРАГ ДЭЭРХ 4 ӨНГӨТЭЙ ТОВЧЛУУР
                    b1, b2, b3, b4 = st.columns(4)
                    if b1.button("🟢 ЭХЛЭХ", key=f"start_{i}", use_container_width=True):
                        st.session_state.test_started = True
                        st.session_state.start_time = time.time()
                        st.rerun()
                    if b2.button("🔵 ДҮН", key=f"res_{i}", use_container_width=True): st.info("Удахгүй...")
                    if b3.button("⚪ АЛДАА", key=f"err_{i}", use_container_width=True): st.info("Удахгүй...")
                    if b4.button("🔴 БОДОЛТ", key=f"sol_{i}", use_container_width=True): st.info("Удахгүй...")
    else:
        st_autorefresh(interval=1000, key="quiz_timer")
        rem = (40 * 60) - (time.time() - st.session_state.start_time)
        if rem <= 0:
            st.error("⏰ Хугацаа дууслаа!"); st.session_state.test_started = False
        else:
            m, s = divmod(int(rem), 60)
            st.sidebar.markdown(f'<div style="background-color:#ff4b4b; padding:20px; border-radius:10px; color:white; text-align:center;"><h2>⏱️ {m:02d}:{s:02d}</h2></div>', unsafe_allow_html=True)
            st.subheader(st.session_state.active_unit)
            if st.button("🏁 СОРИЛ ДУУСГАХ"):
                st.session_state.test_started = False
                st.rerun()
