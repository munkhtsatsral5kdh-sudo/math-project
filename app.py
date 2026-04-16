import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import time
import pandas as pd
import re
from streamlit_autorefresh import st_autorefresh

# 1. Тохиргоо
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Нүүр хуудас"
if 'test_started' not in st.session_state:
    st.session_state.test_started = False

st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# 2. ДИЗАЙН (Цэсний өнгө болон Математик бичиглэлийн CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #003366 !important; min-width: 280px !important; }
    .sidebar-title { color: white !important; font-size: 30px !important; font-weight: bold; text-align: center; padding: 20px 0; border-bottom: 1px solid rgba(255,255,255,0.1); }
    
    .main-header { color: #003366 !important; font-size: 40px !important; font-weight: 900; text-align: center; }
    
    .goal-text { 
        font-size: 19px !important; color: #333; line-height: 1.8; background: white; 
        padding: 25px; border-left: 8px solid #003366; border-radius: 10px; 
        text-align: justify; text-indent: 40px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    /* Бодлогын хэсэг - Математик бичиглэлд зориулав */
    .problem-box { 
        background: white; padding: 25px; border-radius: 15px; 
        border: 1px solid #dee2e6; margin-bottom: 25px; 
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    .math-text { font-size: 20px !important; line-height: 1.6; }
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
                               "container": {"background-color": "#003366"},
                               "nav-link": {"color": "white", "font-size": "16px", "text-align": "left", "margin":"5px"},
                               "nav-link-selected": {"background-color": "#0056b3"},
                           })
    if selected != st.session_state.selected_menu:
        st.session_state.selected_menu = selected
        st.rerun()

# 4. ФУНКЦ: Excel-ийн бичвэрийг цэгцлэх (A. B. C. D. форматлах)
def format_math_question(text):
    if not isinstance(text, str): return text
    # Сонголтуудын өмнө мөр шилжүүлэг нэмэх
    text = re.sub(r'([A-D]\.)', r'\n\n**\1**', text)
    return text

# 5. ХУУДАСНУУД
if st.session_state.selected_menu == "Нүүр хуудас":
    c1, c2 = st.columns([1, 1.5])
    with c1:
        if os.path.exists("logo.gif"):
            with open("logo.gif", "rb") as f:
                st.markdown(f'<img src="data:image/gif;base64,{base64.b64encode(f.read()).decode()}" width="100%">', unsafe_allow_html=True)
        st.markdown('<h2 style="color:#00c04b; text-align:center;">МАТЕМАТИК БАГШИЙН ТУСЛАХ</h2>', unsafe_allow_html=True)
    with c2:
        st.markdown('<p class="main-header" style="text-align:left;">Бидний зорилго</p>', unsafe_allow_html=True)
        st.markdown('<div class="goal-text">Математикийн ертөнцөөр хамтдаа аялж, сонирхолтой цахим хичээл, бодлогын сангаар дамжуулан өөрийн мэдлэг чадвараа бие даан ахиулж, ирээдүйн амжилтынхаа эхлэлийг өнөөдөр тавьцгаая! Бид сурагч бүрт математик сэтгэлгээг хялбар бөгөөд сонирхолтой байдлаар хүргэхийг зорьж байна.</div>', unsafe_allow_html=True)
    
    st.write("###")
    cols = st.columns(3)
    titles = [("📺", "Цахим контент"), ("📚", "Даалгаврын сан"), ("📝", "Сорил")]
    for i, (icon, title) in enumerate(titles):
        with cols[i]:
            st.markdown(f'<div style="background:white; padding:25px; border-radius:15px; text-align:center; box-shadow:0 4px 10px rgba(0,0,0,0.05);"><h2>{icon}</h2><h3>{title}</h3></div>', unsafe_allow_html=True)
            if st.button(f"{title} руу орох", key=f"nav_{i}", use_container_width=True):
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
                if f_df.empty:
                    st.info("Энэ хэсэгт бодлого ороогүй байна.")
                else:
                    for i, row in f_df.iterrows():
                        st.markdown(f'<div class="problem-box">', unsafe_allow_html=True)
                        st.markdown(f"#### 💠 Бодлого {i+1}")
                        
                        # Excel-ээс уншсан асуултыг форматлах
                        formatted_q = format_math_question(row['Асуулт'])
                        
                        # Хэрэв текст дотор $ тэмдэг байвал LaTeX-ээр харуулна
                        if '$' in str(formatted_q):
                            st.latex(formatted_q.replace('$', ''))
                        else:
                            st.markdown(formatted_q)
                        
                        ans = st.radio("Хариулт сонгох:", ["Сонгох", "A", "B", "C", "D"], key=f"ans_{lvl}_{i}", horizontal=True)
                        
                        c1, c2 = st.columns([1, 4])
                        with c1:
                            if st.button("Шалгах", key=f"chk_{lvl}_{i}"):
                                if ans == "Сонгох": st.warning("Хариу сонгоно уу.")
                                elif str(ans).strip().upper() == str(row['Хариу']).strip().upper():
                                    st.success("Зөв! ✅"); st.balloons()
                                else: st.error(f"Буруу. Зөв: {row['Хариу']}")
                        with c2:
                            if pd.notnull(row['Бодолт']):
                                with st.expander("💡 Бодолт харах"): st.write(row['Бодолт'])
                        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.selected_menu == "Сорил":
    st.markdown('<p class="main-header">📝 Онлайн сорилтын систем</p>', unsafe_allow_html=True)
    if not st.session_state.test_started:
        for i in range(1, 9):
            with st.expander(f"🔹 Үнэлгээний нэгж {i}"):
                v_cols = st.columns(4)
                for j, var in enumerate(['A', 'B', 'C', 'D']):
                    if v_cols[j].button(f"{var} хувилбар", key=f"var_{i}_{var}"):
                        st.session_state.active_unit = f"Үнэлгээний нэгж {i} - {var} хувилбар"
                
                if st.session_state.get('active_unit') and f"нэгж {i}" in st.session_state.active_unit.lower():
                    st.success(f"Сонгосон: {st.session_state.active_unit}")
                    b1, b2, b3, b4 = st.columns(4)
                    if b1.button("🟢 Эхлэх", key=f"s_{i}", use_container_width=True):
                        st.session_state.test_started = True
                        st.session_state.start_time = time.time()
                        st.rerun()
                    b2.button("🔵 Дүн", key=f"r_{i}", use_container_width=True)
                    b3.button("⚪ Алдаа", key=f"e_{i}", use_container_width=True)
                    b4.button("🔴 Бодолт", key=f"sol_{i}", use_container_width=True)
    else:
        st_autorefresh(interval=1000, key="timer")
        rem = (40 * 60) - (time.time() - st.session_state.start_time)
        if rem <= 0:
            st.error("⏰ Хугацаа дууслаа!"); st.session_state.test_started = False
        else:
            m, s = divmod(int(rem), 60)
            st.sidebar.metric("⏱️ Үлдсэн хугацаа", f"{m:02d}:{s:02d}")
            st.subheader(st.session_state.active_unit)
            if st.button("✅ Сорил дуусгах"):
                st.session_state.test_started = False
                st.rerun()
