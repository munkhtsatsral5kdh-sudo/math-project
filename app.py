import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import time
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# 1. Сонгогдсон цэсийг санах ойд маш баттай хадгалах
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Нүүр хуудас"
if 'test_started' not in st.session_state:
    st.session_state.test_started = False

# 2. Вэбсайтын ерөнхий тохиргоо
st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# 3. ДИЗАЙН (CSS) - Харагдах байдал маш чухал
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #004aad !important; min-width: 280px !important; }
    .main-header { color: #004aad !important; font-size: 45px !important; font-weight: 900; text-align: center; margin-bottom: 25px; }
    .goal-text { font-size: 20px !important; color: #333; line-height: 1.6; background: white; padding: 25px; border-left: 10px solid #004aad; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
    /* Нүүр хуудасны 3 цонхны загвар */
    .custom-card { background: white; border-radius: 20px; padding: 25px; text-align: center; box-shadow: 0 10px 20px rgba(0,0,0,0.08); border: 1px solid #eee; height: 230px; margin-bottom: 15px; }
    .card-icon { font-size: 45px; margin-bottom: 10px; }
    .card-title { color: #004aad; font-size: 22px; font-weight: bold; margin-bottom: 10px; }
    .problem-text { font-family: 'Times New Roman', serif; font-size: 21px; line-height: 1.8; color: #1a1a1a; white-space: pre-wrap; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR (Цэс) - Гацалтыг засах логик
with st.sidebar:
    st.markdown('<p style="color:white; font-size:35px; font-weight:bold; text-align:center; padding: 20px 0;">ЦЭС</p>', unsafe_allow_html=True)
    options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил төлөвшил МХБ"]
    
    # Session state-тэй холбож, тогтвортой ажиллуулах
    selected = option_menu(None, options, 
                           icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'], 
                           default_index=options.index(st.session_state.selected_menu),
                           key='nav_menu_main')
    
    # Хэрэв хэрэглэгч цэс дээр дарвал session_state-ийг шинэчилнэ
    if selected != st.session_state.selected_menu:
        st.session_state.selected_menu = selected
        st.rerun()

# 5. ХУУДАСНУУД

# --- НҮҮР ХУУДАС (3 Том Цонхтой) ---
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

    st.write("---")
    # Гурван цонх (Interactive Buttons)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="custom-card"><div class="card-icon">📺</div><div class="card-title">Цахим контент</div><p>Видео хичээлүүд үзэх</p></div>', unsafe_allow_html=True)
        if st.button("Хичээл үзэх ➡️", key="btn_to_content", use_container_width=True):
            st.session_state.selected_menu = "Цахим контент"
            st.rerun()
    with c2:
        st.markdown('<div class="custom-card"><div class="card-icon">📚</div><div class="card-title">Даалгаврын сан</div><p>Түвшингээр бодлого бодох</p></div>', unsafe_allow_html=True)
        if st.button("Сан руу орох ➡️", key="btn_to_bank", use_container_width=True):
            st.session_state.selected_menu = "Даалгаврын сан"
            st.rerun()
    with c3:
        st.markdown('<div class="custom-card"><div class="card-icon">📝</div><div class="card-title">Сорил</div><p>Өөрийгөө сорьж шалгах</p></div>', unsafe_allow_html=True)
        if st.button("Сорил эхлэх ➡️", key="btn_to_test", use_container_width=True):
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
                    st.info(f"Энэ хэсэгт одоогоор бодлого ороогүй байна.")
                else:
                    for i, row in f_df.iterrows():
                        st.markdown(f"#### 💠 Бодлого {i+1}:")
                        # Асуултын бичиглэлийг засах
                        q_fmt = str(row['Асуулт']).replace("A.", "\n**A.**").replace("B.", "\n**B.**").replace("C.", "\n**C.**").replace("D.", "\n**D.**")
                        st.markdown(f'<div class="problem-text">{q_fmt}</div>', unsafe_allow_html=True)
                        
                        ans = st.radio("Сонголт:", ["Сонгох", "A", "B", "C", "D"], key=f"ans_{lvl_name}_{i}", horizontal=True)
                        
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            if st.button("Шалгах", key=f"chk_{lvl_name}_{i}"):
                                if ans == "Сонгох": st.warning("Хариултаа сонгоно уу.")
                                elif str(ans).strip().upper() == str(row['Хариу']).strip().upper():
                                    st.success("Зөв! ✅"); st.balloons()
                                else: st.error(f"Буруу. Зөв: {row['Хариу']}")
                        with col2:
                            if pd.notnull(row['Бодолт']):
                                with st.expander("💡 Тайлбар харах"): st.info(str(row['Бодолт']))
                        st.write("---")

# --- СОРИЛ (Тоолууртай хэсэг) ---
elif st.session_state.selected_menu == "Сорил":
    st.markdown('<p class="main-header">📝 Онлайн сорилтын систем</p>', unsafe_allow_html=True)
    if not st.session_state.test_started:
        units = [f"Үнэлгээний нэгж {i}" for i in range(1, 9)]
        for i, unit_name in enumerate(units, 1):
            with st.expander(f"🔹 {unit_name}"):
                cols = st.columns(4)
                for j, var in enumerate(['A', 'B', 'C', 'D']):
                    if cols[j].button(f"{var} хувилбар", key=f"q_btn_{i}_{var}"):
                        st.session_state.active_unit = f"{unit_name} - {var} хувилбар"
                        st.session_state.show_options = True
                
                if st.session_state.get('show_options') and st.session_state.active_unit.startswith(unit_name):
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        if st.button("🟢 Эхлэх", key=f"s_start_{i}"):
                            st.session_state.test_started = True
                            st.session_state.start_time = time.time()
                            st.rerun()
    else:
        st_autorefresh(interval=1000, key="quiz_refresh")
        rem = (40 * 60) - (time.time() - st.session_state.start_time)
        if rem <= 0:
            st.error("⏰ Хугацаа дууслаа!")
            st.session_state.test_started = False
        else:
            m, s = divmod(int(rem), 60)
            st.sidebar.markdown(f'<div style="background-color:#ff4b4b;padding:15px;border-radius:10px;text-align:center;color:white;"><h3>⏱️ {m:02d}:{s:02d}</h3>Үлдсэн хугацаа</div>', unsafe_allow_html=True)
            st.subheader(st.session_state.active_unit)
            if st.button("✅ Сорил дуусгах"):
                st.session_state.test_started = False
                st.rerun()

# --- БУСАД ---
else:
    st.markdown(f'<p class="main-header">{st.session_state.selected_menu}</p>', unsafe_allow_html=True)
    st.info("Бэлтгэгдэж байна...")
