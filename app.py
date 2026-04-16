import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import time
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# 1. Санах ойн тохиргоо
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Нүүр хуудас"
if 'test_started' not in st.session_state:
    st.session_state.test_started = False

st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# 2. ДИЗАЙН (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #004aad !important; min-width: 250px !important; }
    .main-header { color: #004aad !important; font-size: 45px !important; font-weight: 900; text-align: center; margin-bottom: 20px; }
    .goal-text { font-size: 20px !important; color: #333; line-height: 1.6; background: white; padding: 25px; border-left: 10px solid #004aad; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
    /* Картын дизайн */
    .custom-card { background: white; border-radius: 20px; padding: 30px; text-align: center; box-shadow: 0 10px 20px rgba(0,0,0,0.05); border: 1px solid #eee; height: 220px; }
    .problem-text { font-family: 'Times New Roman', serif; font-size: 21px; line-height: 1.8; color: #1a1a1a; white-space: pre-wrap; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Цэс)
with st.sidebar:
    st.markdown('<p style="color:white; font-size:35px; font-weight:bold; text-align:center; padding: 20px 0;">ЦЭС</p>', unsafe_allow_html=True)
    options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил төлөвшил МХБ"]
    
    # Сонгогдсон индексийг олох
    try:
        current_idx = options.index(st.session_state.selected_menu)
    except:
        current_idx = 0

    selected = option_menu(None, options, 
                           icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'], 
                           default_index=current_idx,
                           key='main_nav')
    st.session_state.selected_menu = selected

# --- НҮҮР ХУУДАС (3 Цонхтой) ---
if st.session_state.selected_menu == "Нүүр хуудас":
    col1, col2 = st.columns([1, 1.5], gap="large")
    with col1:
        if os.path.exists("logo.gif"):
            with open("logo.gif", "rb") as f:
                data_url = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(f'<img src="data:image/gif;base64,{data_url}" width="100%">', unsafe_allow_html=True)
        st.markdown('<h2 style="color:#00c04b; text-align:center; font-weight:bold;">МАТЕМАТИК<br>БАГШИЙН ТУСЛАХ</h2>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<p class="main-header" style="text-align:left;">Бидний зорилго</p>', unsafe_allow_html=True)
        st.markdown('<div class="goal-text">Математикийн ертөнцөөр хамтдаа аялж, сонирхолтой цахим хичээл, бодлогын сангаар дамжуулан өөрийн мэдлэг чадвараа бие даан ахиулж, ирээдүйн амжилтынхаа эхлэлийг өнөөдөр тавьцгаая!</div>', unsafe_allow_html=True)

    st.write("###")
    # 3 Хэсэг (Картууд товчлууртай)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="custom-card"><h2>📺</h2><h3>Цахим контент</h3><p>Видео хичээл үзэх</p></div>', unsafe_allow_html=True)
        if st.button("Үзэх ➡️", key="btn_content", use_container_width=True):
            st.session_state.selected_menu = "Цахим контент"
            st.rerun()
    with c2:
        st.markdown('<div class="custom-card"><h2>📚</h2><h3>Даалгаврын сан</h3><p>Түвшингээр бодох</p></div>', unsafe_allow_html=True)
        if st.button("Орох ➡️", key="btn_bank", use_container_width=True):
            st.session_state.selected_menu = "Даалгаврын сан"
            st.rerun()
    with c3:
        st.markdown('<div class="custom-card"><h2>📝</h2><h3>Сорил</h3><p>Өөрийгөө сорих</p></div>', unsafe_allow_html=True)
        if st.button("Эхлэх ➡️", key="btn_test", use_container_width=True):
            st.session_state.selected_menu = "Сорил"
            st.rerun()

# --- ДААЛГАВРЫН САН (3 Түвшинтэй) ---
elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown('<p class="main-header">📚 Даалгаврын сан</p>', unsafe_allow_html=True)
    if os.path.exists("data_bank.xlsx"):
        df = pd.read_excel("data_bank.xlsx")
        units = df['Нэгж'].unique()
        selected_unit = st.selectbox("Сэдэв сонгох:", units)
        
        tab1, tab2, tab3 = st.tabs(["🧠 Мэдлэг ойлголт", "🛠️ Чадвар", "🎯 Хэрэглээ"])
        levels = {"Мэдлэг ойлголт": tab1, "Чадвар": tab2, "Хэрэглээ": tab3}
        
        for lvl_name, tab in levels.items():
            with tab:
                f_df = df[(df['Нэгж'] == selected_unit) & (df['Түвшин'] == lvl_name)]
                if f_df.empty:
                    st.info(f"'{lvl_name}' түвшинд бодлого хараахан ороогүй байна.")
                else:
                    for i, row in f_df.iterrows():
                        st.markdown(f"#### 💠 Бодлого {i+1}:")
                        q_text = str(row['Асуулт']).replace("A.", "\n\n**A.**").replace("B.", "\n\n**B.**").replace("C.", "\n\n**C.**").replace("D.", "\n\n**D.**")
                        st.markdown(f'<div class="problem-text">{q_text}</div>', unsafe_allow_html=True)
                        
                        ans = st.radio("Хариулт сонгох:", ["Сонгох", "A", "B", "C", "D"], key=f"radio_{i}_{lvl_name}", horizontal=True)
                        
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            if st.button("Шалгах", key=f"btn_{i}_{lvl_name}"):
                                if ans == "Сонгох": st.warning("Хариу сонгоно уу")
                                elif ans.strip().upper() == str(row['Хариу']).strip().upper():
                                    st.success("Зөв! ✅"); st.balloons()
                                else: st.error(f"Буруу. Зөв: {row['Хариу']}")
                        with col2:
                            if pd.notnull(row['Бодолт']):
                                with st.expander("💡 Тайлабар харах"): st.info(str(row['Бодолт']))
                        st.write("---")

# --- СОРИЛ (Таны эх код дээрх тоолуур) ---
elif st.session_state.selected_menu == "Сорил":
    st.markdown('<p class="main-header">📝 Онлайн сорилтын систем</p>', unsafe_allow_html=True)
    if not st.session_state.test_started:
        units = [f"Үнэлгээний нэгж {i}" for i in range(1, 9)]
        for i, unit_name in enumerate(units, 1):
            with st.expander(f"🔹 {unit_name}"):
                cols = st.columns(4)
                for j, var in enumerate(['A', 'B', 'C', 'D']):
                    if cols[j].button(f"{var} хувилбар", key=f"s_btn_{i}_{var}"):
                        st.session_state.active_unit = f"{unit_name} - {var} хувилбар"
                        st.session_state.show_options = True
                if st.session_state.get('show_options') and st.session_state.active_unit.startswith(unit_name):
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        if st.button("🟢 Эхлэх", key=f"start_{i}"):
                            st.session_state.test_started = True
                            st.session_state.start_time = time.time()
                            st.rerun()
    else:
        st_autorefresh(interval=1000, key="quiz_refresh")
        remaining = (40 * 60) - (time.time() - st.session_state.start_time)
        if remaining <= 0:
            st.error("⏰ Хугацаа дууслаа!")
            st.session_state.test_started = False
        else:
            mins, secs = divmod(int(remaining), 60)
            st.sidebar.markdown(f'<div style="background-color:#ff4b4b;padding:15px;border-radius:10px;text-align:center;color:white;"><h3>⏱️ {mins:02d}:{secs:02d}</h3></div>', unsafe_allow_html=True)
            st.subheader(st.session_state.active_unit)
            if st.button("✅ Сорил дуусгах"):
                st.session_state.test_started = False
                st.rerun()
else:
    st.info(f"{st.session_state.selected_menu} хэсэг удахгүй нэмэгдэнэ.")
