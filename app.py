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

st.set_page_config(page_title="Математик Багш", page_icon="📐", layout="wide")

# 2. ТАНЫ ИЛГЭЭСЭН ЗУРАГ ДЭЭРХ СУУРЬ ӨНГӨ (CSS)
st.markdown(f"""
    <style>
    /* Суурь өнгө - Таны зураг дээрх цайвар сааралдуу цэнхэр */
    .stApp {{ 
        background-color: #eef2f6 !important; 
    }}
    
    /* Хажуугийн цэс - Гүн цэнхэр */
    [data-testid="stSidebar"] {{ 
        background-color: #1e3a5f !important; 
        min-width: 280px !important; 
    }}
    
    .sidebar-title {{ 
        color: #ffffff !important; 
        text-align: center; 
        font-size: 28px !important; 
        font-weight: bold; 
        padding: 25px 0; 
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }}
    
    /* Зорилго хэсэг - Цагаан дэвсгэр, Тэгшлэлт, Догол мөр */
    .goal-box {{
        background: #ffffff; 
        padding: 35px; 
        border-radius: 8px; 
        border-left: 8px solid #1e3a5f;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-top: 20px;
    }}
    .goal-text {{ 
        font-size: 20px !important; 
        color: #2c3e50; 
        line-height: 1.8; 
        text-align: justify; 
        text-indent: 50px; 
    }}

    /* Сорилтын товчлуурууд */
    .stButton>button {{
        border-radius: 6px !important;
        font-weight: 600 !important;
        height: 45px !important;
    }}
    
    /* Бодлогын карт */
    .math-card {{
        background: white; 
        padding: 25px; 
        border-radius: 12px; 
        border: 1px solid #d1d9e6;
        margin-bottom: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    menu_options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил"]
    
    selected = option_menu(None, menu_options, 
                           icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'], 
                           default_index=0,
                           styles={
                               "container": {"background-color": "#1e3a5f", "padding": "0px"},
                               "nav-link": {"color": "#cbd5e0", "font-size": "17px", "text-align": "left", "margin":"10px"},
                               "nav-link-selected": {"background-color": "#334e68", "color": "white"},
                           })
    if selected != st.session_state.selected_menu:
        st.session_state.selected_menu = selected
        st.rerun()

# 4. EXCEL-ИЙН БИЧИГЛЭЛИЙГ ЦЭГЦЛЭХ
def render_question(text):
    if not isinstance(text, str): return
    # A. B. C. D. шилжүүлэг
    formatted = re.sub(r'([A-D]\.)', r'\n\n**\1**', text)
    st.markdown(f'<div style="font-size:19px;">{formatted}</div>', unsafe_allow_html=True)

# 5. ХУУДАСНУУД
if st.session_state.selected_menu == "Нүүр хуудас":
    c1, c2 = st.columns([1, 1.8], gap="large")
    with c1:
        if os.path.exists("logo.gif"):
            with open("logo.gif", "rb") as f:
                st.markdown(f'<img src="data:image/gif;base64,{base64.b64encode(f.read()).decode()}" width="100%">', unsafe_allow_html=True)
        st.markdown('<h2 style="color:#2ecc71; text-align:center; font-weight:bold;">МАТЕМАТИК БАГШ</h2>', unsafe_allow_html=True)
    
    with c2:
        st.markdown('<h1 style="color:#1e3a5f;">Бидний зорилго</h1>', unsafe_allow_html=True)
        st.markdown(f'<div class="goal-box"><p class="goal-text">Математикийн ертөнцөөр хамтдаа аялж, сонирхолтой цахим хичээл, бодлогын сангаар дамжуулан өөрийн мэдлэг чадвараа бие даан ахиулж, ирээдүйн амжилтынхаа эхлэлийг өнөөдөр тавьцгаая! Бид сурагч бүрт математик сэтгэлгээг хялбар бөгөөд сонирхолтой байдлаар хүргэхийг зорьж байна.</p></div>', unsafe_allow_html=True)

    st.write("---")
    # Нүүр хуудасны 3 том карт
    cols = st.columns(3)
    items = [("📺", "Цахим контент"), ("📚", "Даалгаврын сан"), ("📝", "Сорил")]
    for i, (icon, title) in enumerate(items):
        with cols[i]:
            st.markdown(f'<div style="background:white; padding:35px; border-radius:15px; text-align:center; border: 1px solid #d1d9e6;"><h1>{icon}</h1><h3>{title}</h3></div>', unsafe_allow_html=True)
            if st.button(f"Орох ➡️", key=f"home_{i}", use_container_width=True):
                st.session_state.selected_menu = title
                st.rerun()

elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown('<h1 style="color:#1e3a5f; text-align:center;">📚 Даалгаврын сан</h1>', unsafe_allow_html=True)
    if os.path.exists("data_bank.xlsx"):
        df = pd.read_excel("data_bank.xlsx")
        unit = st.selectbox("Сэдэв сонгох:", df['Нэгж'].unique())
        t1, t2, t3 = st.tabs(["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"])
        
        for idx, lvl in enumerate(["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"]):
            with [t1, t2, t3][idx]:
                f_df = df[(df['Нэгж'] == unit) & (df['Түвшин'] == lvl)]
                for i, row in f_df.iterrows():
                    st.markdown('<div class="math-card">', unsafe_allow_html=True)
                    st.write(f"**Бодлого {i+1}**")
                    render_question(row['Асуулт'])
                    
                    ans = st.radio("Сонголт:", ["A", "B", "C", "D"], key=f"q_{lvl}_{i}", horizontal=True)
                    if st.button("Шалгах", key=f"b_{lvl}_{i}"):
                        if str(ans).strip().upper() == str(row['Хариу']).strip().upper():
                            st.success("Зөв! ✅"); st.balloons()
                        else: st.error(f"Буруу. Зөв: {row['Хариу']}")
                    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.selected_menu == "Сорил":
    st.markdown('<h1 style="color:#1e3a5f; text-align:center;">📝 Онлайн сорил</h1>', unsafe_allow_html=True)
    if not st.session_state.test_started:
        for i in range(1, 9):
            with st.expander(f"📌 Үнэлгээний нэгж {i}"):
                v_cols = st.columns(4)
                for j, var in enumerate(['A', 'B', 'C', 'D']):
                    if v_cols[j].button(f"{var} хувилбар", key=f"v_{i}_{var}"):
                        st.session_state.active_unit = f"Нэгж {i} - {var} хувилбар"
                
                if st.session_state.get('active_unit') and f"Нэгж {i}" in st.session_state.active_unit:
                    st.write(f"**Сонгосон:** {st.session_state.active_unit}")
                    b1, b2, b3, b4 = st.columns(4)
                    if b1.button("🟢 ЭХЛЭХ", key=f"st_{i}", use_container_width=True):
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
            st.sidebar.markdown(f'<div style="background-color:#d9534f; padding:20px; color:white; border-radius:8px; text-align:center;"><h2>⏱️ {m:02d}:{s:02d}</h2></div>', unsafe_allow_html=True)
            st.subheader(st.session_state.active_unit)
            if st.button("🏁 СОРИЛ ДУУСГАХ"):
                st.session_state.test_started = False
                st.rerun()
