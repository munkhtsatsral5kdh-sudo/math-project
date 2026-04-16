import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import time
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# 1. Сонгогдсон цэсийг санах ойд хадгалах
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Нүүр хуудас"
if 'test_started' not in st.session_state:
    st.session_state.test_started = False

# 2. Вэбсайтын ерөнхий тохиргоо
st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# 3. ДИЗАЙН (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #004aad !important; min-width: 300px !important; }
    .sidebar-title { color: #ffffff !important; text-align: center; font-size: 40px !important; font-weight: bold; padding: 20px 0; border-bottom: 2px solid rgba(255,255,255,0.3); margin-bottom: 20px; }
    .main-header { color: #004aad !important; font-size: 45px !important; font-weight: 900; text-align: center; margin-bottom: 30px; }
    .goal-text { font-size: 22px !important; color: #333; line-height: 1.6; background: white; padding: 30px; border-left: 15px solid #004aad; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .custom-card { background: white; border-radius: 25px; padding: 30px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 1px solid #eee; height: 260px; margin-bottom: 20px; }
    .card-icon { font-size: 50px; margin-bottom: 10px; }
    .card-title { color: #004aad; font-size: 22px; font-weight: bold; margin-bottom: 10px; }
    .problem-text { font-family: 'Times New Roman', serif; font-size: 21px; line-height: 1.8; color: #1a1a1a; margin-bottom: 20px; white-space: pre-line; }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR (Цэс)
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил төлөвшил МХБ"]
    selected = option_menu(None, options, icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'], 
                           default_index=options.index(st.session_state.selected_menu), key='menu_widget',
                           styles={"container": {"background-color": "#004aad"}, "nav-link": {"color": "white", "font-weight": "bold"}})
    st.session_state.selected_menu = selected

# --- НҮҮР ХУУДАС ---
if st.session_state.selected_menu == "Нүүр хуудас":
    col1, col2 = st.columns([1, 1.5], gap="large")
    with col1:
        if os.path.exists("logo.gif"):
            with open("logo.gif", "rb") as f:
                data_url = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(f'<img src="data:image/gif;base64,{data_url}" width="100%">', unsafe_allow_html=True)
    with col2:
        st.markdown('<p class="main-header" style="text-align:left;">Бидний зорилго</p>', unsafe_allow_html=True)
        st.markdown('<div class="goal-text">Математикийн ертөнцөөр хамтдаа аялж, сонирхолтой цахим хичээл, бодлогын сангаар дамжуулан өөрийн мэдлэг чадвараа бие даан ахиулж, ирээдүйн амжилтынхаа эхлэлийг өнөөдөр тавьцгаая!</div>', unsafe_allow_html=True)
    
    st.write("###")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="custom-card"><div class="card-icon">📚</div><div class="card-title">Баялаг сан</div><p>6-12-р ангийн бүх сэдвийг хамарсан даалгаврын сан</p></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="custom-card"><div class="card-icon">🎯</div><div class="card-title">Бие даах чадвар</div><p>Өөрийгөө сорих, алдаагаа засах бүрэн боломж</p></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="custom-card"><div class="card-icon">🚀</div><div class="card-title">Ирээдүйн амжилт</div><p>Математик сэтгэлгээг хөгжүүлж, ирээдүйдээ хөрөнгө оруулалт хийх</p></div>', unsafe_allow_html=True)

# --- ДААЛГАВРЫН САН (Түвшингээр ангилдаг хэсэг) ---
elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown('<p class="main-header">📚 Даалгаврын сан</p>', unsafe_allow_html=True)
    if os.path.exists("data_bank.xlsx"):
        df = pd.read_excel("data_bank.xlsx")
        units = df['Нэгж'].unique()
        
        selected_unit = st.selectbox("Нэгж сонгох:", units)
        
        # 3 Түвшинг Tab хэлбэрээр харуулах (Мэдлэг, Чадвар, Хэрэглээ)
        tab1, tab2, tab3 = st.tabs(["🧠 Мэдлэг ойлголт", "🛠️ Чадвар", "🎯 Хэрэглээ"])
        
        levels = {"Мэдлэг ойлголт": tab1, "Чадвар": tab2, "Хэрэглээ": tab3}
        
        for level_name, tab in levels.items():
            with tab:
                # Тухайн нэгж болон түвшинд тохирох бодлогуудыг шүүх
                filtered_df = df[(df['Нэгж'] == selected_unit) & (df['Түвшин'] == level_name)]
                
                if filtered_df.empty:
                    st.info(f"Энэ түвшинд бодлого хараахан ороогүй байна.")
                else:
                    for i, row in filtered_df.iterrows():
                        st.markdown(f"#### 💠 Бодлого {i+1}:")
                        q_raw = str(row['Асуулт']).replace("A.", "\n\n**A.**").replace("B.", "\n\n**B.**").replace("C.", "\n\n**C.**").replace("D.", "\n\n**D.**")
                        st.markdown(f'<div class="problem-text">{q_raw}</div>', unsafe_allow_html=True)
                        
                        choice = st.radio("Хариултаа сонгоно уу:", ["Сонгох", "A", "B", "C", "D"], key=f"r_{i}", horizontal=True)
                        
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            if st.button("🔍 Шалгах", key=f"b_{i}"):
                                if choice == "Сонгох": st.warning("Хариултаа сонгоно уу.")
                                elif choice.strip().upper() == str(row['Хариу']).strip().upper():
                                    st.success("Зөв! ✅")
                                    st.balloons()
                                else: st.error(f"Буруу. Зөв: {row['Хариу']}")
                        with col2:
                            if pd.notnull(row['Бодолт']):
                                with st.expander("💡 Тайлабар харах"): st.info(str(row['Бодолт']))
                        st.write("---")

# --- СОРИЛ (Таны эх код хэвээрээ) ---
elif st.session_state.selected_menu == "Сорил":
    st.markdown('<p class="main-header">📝 Онлайн сорилтын систем</p>', unsafe_allow_html=True)
    if not st.session_state.test_started:
        units = [f"Үнэлгээний нэгж {i}" for i in range(1, 9)]
        for i, unit_name in enumerate(units, 1):
            with st.expander(f"🔹 {unit_name}"):
                cols = st.columns(4)
                for j, var in enumerate(['A', 'B', 'C', 'D']):
                    if cols[j].button(f"{var} хувилбар", key=f"quiz_btn_{i}_{var}"):
                        st.session_state.active_unit = f"{unit_name} - {var} хувилбар"
                        st.session_state.show_options = True
                if st.session_state.get('show_options') and st.session_state.active_unit.startswith(unit_name):
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        if st.button("🟢 Эхлэх", key=f"start_{i}"):
                            st.session_state.test_started = True
                            st.session_state.start_time = time.time()
                            st.rerun()
                    with c2: st.button("🔵 Дүн", key=f"res_{i}")
                    with c3: st.button("⚪ Алдаа", key=f"err_{i}")
                    with c4: st.button("🔴 Бодолт", key=f"sol_{i}")
    else:
        st_autorefresh(interval=1000, key="quiz_refresh")
        remaining = (40 * 60) - (time.time() - st.session_state.start_time)
        if remaining <= 0:
            st.error("⏰ Хугацаа дууслаа!")
            st.session_state.test_started = False
        else:
            mins, secs = divmod(int(remaining), 60)
            st.sidebar.markdown(f'<div style="background-color:#ff4b4b;padding:15px;border-radius:15px;text-align:center;color:white;"><h3>⏱️ {mins:02d}:{secs:02d}</h3></div>', unsafe_allow_html=True)
            st.subheader(st.session_state.active_unit)
            if st.button("✅ Сорил дуусгах"):
                st.session_state.test_started = False
                st.rerun()

else:
    st.markdown(f'<p class="main-header">{st.session_state.selected_menu}</p>', unsafe_allow_html=True)
    st.info("Тун удахгүй...")
