import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import time
from streamlit_autorefresh import st_autorefresh
import pandas as pd

# 1. Санах ойн тохиргоо (Таны эх код)
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Нүүр хуудас"
if 'test_started' not in st.session_state:
    st.session_state.test_started = False

# 2. Вэбсайтын ерөнхий тохиргоо
st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# 3. ДИЗАЙН (CSS - Таны эх кодыг хэвээр үлдээв)
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #004aad !important; min-width: 300px !important; }
    .sidebar-title { color: #ffffff !important; text-align: center; font-size: 40px !important; font-weight: bold; padding: 20px 0; border-bottom: 2px solid rgba(255,255,255,0.3); margin-bottom: 20px; }
    .main-header { color: #004aad !important; font-size: 50px !important; font-weight: 900; text-align: center; margin-bottom: 20px; }
    .goal-text { font-size: 22px !important; color: #333; line-height: 1.6; background: white; padding: 30px; border-left: 15px solid #004aad; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .problem-text { font-family: 'Times New Roman', serif; font-size: 22px; line-height: 1.8; color: #1a1a1a; white-space: pre-wrap; }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR (Цэс - Таны эх код)
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил төлөвшил МХБ"]
    
    current_index = 0
    if st.session_state.selected_menu in options:
        current_index = options.index(st.session_state.selected_menu)
    
    selected = option_menu(
        menu_title=None, 
        options=options,
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        default_index=current_index,
        key='menu_widget',
        styles={
            "container": {"background-color": "#004aad"},
            "nav-link": {"color": "white", "font-weight": "bold"},
            "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)"},
        }
    )
    st.session_state.selected_menu = selected

# 5. ХУУДАСНУУДЫН УДИРДЛАГА

# --- НҮҮР ХУУДАС ---
if st.session_state.selected_menu == "Нүүр хуудас":
    col1, col2 = st.columns([1, 1.5], gap="large")
    with col1:
        if os.path.exists("logo.gif"):
            with open("logo.gif", "rb") as f:
                data = f.read()
                data_url = base64.b64encode(data).decode("utf-8")
            st.markdown(f'<img src="data:image/gif;base64,{data_url}" width="100%">', unsafe_allow_html=True)
    with col2:
        st.markdown('<p class="main-header" style="text-align:left;">Бидний зорилго</p>', unsafe_allow_html=True)
        st.markdown('<div class="goal-text">Математикийн ертөнцөөр хамтдаа аялж, сонирхолтой цахим хичээл, бодлогын сангаар дамжуулан өөрийн мэдлэг чадвараа бие даан ахиулж, амжилтын эхлэлийг тавьцгаая!</div>', unsafe_allow_html=True)

# --- СОРИЛ ХЭСЭГ (Яг таны эх код хэвээрээ) ---
elif st.session_state.selected_menu == "Сорил":
    st.markdown('<p class="main-header">📝 Онлайн сорилтын систем</p>', unsafe_allow_html=True)
    if not st.session_state.test_started:
        units = ["Үнэлгээний нэгж 1", "Үнэлгээний нэгж 2", "Үнэлгээний нэгж 3", "Үнэлгээний нэгж 4", "Үнэлгээний нэгж 5", "Үнэлгээний нэгж 6", "Үнэлгээний нэгж 7", "Үнэлгээний нэгж 8"]
        for i, unit_name in enumerate(units, 1):
            with st.expander(f"🔹 {unit_name}"):
                cols = st.columns(4)
                for j, var in enumerate(['A', 'B', 'C', 'D']):
                    if cols[j].button(f"{var} хувилбар", key=f"btn_u_{i}_{var}"):
                        st.session_state.active_unit = f"{unit_name} - {var} хувилбар"
                        st.session_state.show_options = True
                
                if st.session_state.get('show_options') and st.session_state.active_unit.startswith(unit_name):
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        if st.button("🟢 Эхлэх", key=f"start_q_{i}"):
                            st.session_state.test_started = True
                            st.session_state.start_time = time.time()
                            st.rerun()
                    with c2: st.button("🔵 Дүн", key=f"res_{i}")
                    with c3: st.button("⚪ Алдаа", key=f"err_{i}")
                    with c4: st.button("🔴 Бодолт", key=f"sol_{i}")
    else:
        st_autorefresh(interval=1000, key="quiz_ref")
        remaining = (40 * 60) - (time.time() - st.session_state.start_time)
        if remaining <= 0:
            st.error("⏰ Хугацаа дууслаа!")
            st.session_state.test_started = False
        else:
            mins, secs = divmod(int(remaining), 60)
            st.sidebar.markdown(f'<div style="background-color:#ff4b4b;padding:10px;border-radius:10px;text-align:center;color:white;"><h2>⏱️ {mins:02d}:{secs:02d}</h2>Үлдсэн хугацаа</div>', unsafe_allow_html=True)
            st.subheader(st.session_state.active_unit)
            if st.button("✅ Сорил дуусгах"):
                st.session_state.test_started = False
                st.rerun()

# --- ДААЛГАВРЫН САН (Текст зассан + Сонгодог товчлуур + Бөмбөлөг) ---
elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown('<p class="main-header">📚 Даалгаврын сан</p>', unsafe_allow_html=True)
    if os.path.exists("data_bank.xlsx"):
        try:
            df = pd.read_excel("data_bank.xlsx")
            for unit in df['Нэгж'].unique():
                with st.expander(f"🔹 {unit}", expanded=True):
                    unit_df = df[df['Нэгж'] == unit]
                    for i, row in unit_df.iterrows():
                        st.markdown(f"### 💠 Бодлого {i+1}:")
                        # Текстийн бичиглэлийг засах
                        q_text = str(row['Асуулт']).replace("A.", "\n\n**A.**").replace("B.", "\n\n**B.**").replace("C.", "\n\n**C.**").replace("D.", "\n\n**D.**")
                        st.markdown(f'<div class="problem-text">{q_text}</div>', unsafe_allow_html=True)
                        
                        # Хариулт сонгох хэсэг
                        choice = st.radio("Хариултаа сонгоно уу:", ["Сонгох", "A", "B", "C", "D"], key=f"db_r_{i}", horizontal=True)
                        
                        if st.button(f"🔍 Шалгах", key=f"db_b_{i}"):
                            if choice == "Сонгох":
                                st.warning("Хариултаа сонгоно уу!")
                            elif choice.strip().upper() == str(row['Хариу']).strip().upper():
                                st.success("Зөв! ✅ Баяр хүргэе!")
                                st.balloons()
                            else:
                                st.error(f"Буруу. Зөв хариу: {row['Хариу']}")
                        
                        if pd.notnull(row['Бодолт']):
                            with st.expander("💡 Тайлабар харах"):
                                st.info(str(row['Бодолт']))
                        st.write("---")
        except Exception as e:
            st.error(f"Алдаа: {e}")

# --- БУСАД ---
elif st.session_state.selected_menu == "Цахим контент":
    st.info("Цахим хичээлүүд.")
elif st.session_state.selected_menu == "Клубын мэдээлэл":
    st.info("Клубын мэдээлэл.")
elif st.session_state.selected_menu == "Хүүхдийн хүмүүжил төлөвшил МХБ":
    st.info("Зөвлөгөө.")
