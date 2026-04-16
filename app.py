import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import time
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
    .main-header { color: #004aad !important; font-size: 50px !important; font-weight: 900; text-align: center; margin-bottom: 20px; }
    .goal-text { font-size: 22px !important; color: #333; line-height: 1.6; background: white; padding: 30px; border-left: 15px solid #004aad; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .custom-card { background: white; border-radius: 25px; padding: 30px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 1px solid #eee; height: 250px; }
    .card-icon { font-size: 50px; margin-bottom: 10px; }
    .card-title { color: #004aad; font-size: 22px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR (Цэс)
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил төлөвшил МХБ"]
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
        else:
            st.warning("logo.gif олдсонгүй")
            
    with col2:
        st.markdown('<p class="main-header" style="text-align:left;">Бидний зорилго</p>', unsafe_allow_html=True)
        st.markdown('<div class="goal-text">Математикийн ертөнцөөр хамтдаа аялж, сонирхолтой цахим хичээл, бодлогын сангаар дамжуулан өөрийн мэдлэг чадвараа бие даан ахиулж, ирээдүйн амжилтынхаа эхлэлийг өнөөдөр тавьцгаая!</div>', unsafe_allow_html=True)

    st.write("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="custom-card"><div class="card-icon">📺</div><div class="card-title">Цахим контент</div></div>', unsafe_allow_html=True)
        if st.button("Үзэх", key="go_content"):
            st.session_state.selected_menu = "Цахим контент"
            st.rerun()
    with c2:
        st.markdown('<div class="custom-card"><div class="card-icon">📚</div><div class="card-title">Даалгаврын сан</div></div>', unsafe_allow_html=True)
        if st.button("Нээх", key="go_bank"):
            st.session_state.selected_menu = "Даалгаврын сан"
            st.rerun()
    with c3:
        st.markdown('<div class="custom-card"><div class="card-icon">📝</div><div class="card-title">Сорил</div></div>', unsafe_allow_html=True)
        if st.button("Эхлэх", key="go_quiz"):
            st.session_state.selected_menu = "Сорил"
            st.rerun()

# --- СОРИЛ ХЭСЭГ ---
elif st.session_state.selected_menu == "Сорил":
    st.markdown('<p class="main-header">📝 Онлайн сорилтын систем</p>', unsafe_allow_html=True)
    
    if not st.session_state.test_started:
        units = [
            "Үнэлгээний нэгж 1. Тоон олонлог, зэрэг, язгуур, тоог жиших, тоймлох",
            "Үнэлгээний нэгж 2. Харьцаа, пропорц, процент",
            "Үнэлгээний нэгж 3. Алгебрын илэрхийлэл, тэгшитгэл, тэнцэтгэл биш",
            "Үнэлгээний нэгж 4. Дараалал, функц",
            "Үнэлгээний нэгж 5. Өнцөг, дүрс, байгуулалт",
            "Үнэлгээний нэгж 6. Байршил, хөдөлгөөн, хувиргалт",
            "Үнэлгээний нэгж 7. Хэмжигдэхүүн",
            "Үнэлгээний нэгж 8. Магадлал, статистик"
        ]

        for i, unit_name in enumerate(units, 1):
            with st.expander(f"🔹 {unit_name}"):
                cols = st.columns(4)
                for j, var in enumerate(['A', 'B', 'C', 'D']):
                    if cols[j].button(f"{var} хувилбар", key=f"btn_{i}_{var}"):
                        st.session_state.active_unit = f"{unit_name} - {var} хувилбар"
                        st.session_state.show_options = True
                
                if st.session_state.get('show_options') and unit_name in st.session_state.get('active_unit', ''):
                    st.write("---")
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        if st.button("🟢 Сорил эхлэх", key=f"start_{i}"):
                            st.session_state.test_started = True
                            st.session_state.start_time = time.time()
                            st.rerun()
                    with c2: st.button("🔵 Дүн харах", key=f"res_{i}")
                    with c3: st.button("⚪ Алдаа шалгах", key=f"chk_{i}")
                    with c4: st.button("🔴 Бодолт", key=f"sol_{i}")
   # --- СОРИЛ ХЭСЭГ ---
elif st.session_state.selected_menu == "Сорил":
    st.markdown('<p class="main-header">📝 Онлайн сорилтын систем</p>', unsafe_allow_html=True)
    
    if not st.session_state.test_started:
        units = [
            "Үнэлгээний нэгж 1. Тоон олонлог, зэрэг, язгуур, тоог жиших, тоймлох",
            "Үнэлгээний нэгж 2. Харьцаа, пропорц, процент",
            "Үнэлгээний нэгж 3. Алгебрын илэрхийлэл, тэгшитгэл, тэнцэтгэл биш",
            "Үнэлгээний нэгж 4. Дараалал, функц",
            "Үнэлгээний нэгж 5. Өнцөг, дүрс, байгуулалт",
            "Үнэлгээний нэгж 6. Байршил, хөдөлгөөн, хувиргалт",
            "Үнэлгээний нэгж 7. Хэмжигдэхүүн",
            "Үнэлгээний нэгж 8. Магадлал, статистик"
        ]

        for i, unit_name in enumerate(units, 1):
            with st.expander(f"🔹 {unit_name}"):
                cols = st.columns(4)
                for j, var in enumerate(['A', 'B', 'C', 'D']):
                    if cols[j].button(f"{var} хувилбар", key=f"btn_{i}_{var}"):
                        st.session_state.active_unit = f"{unit_name} - {var} хувилбар"
                        st.session_state.show_options = True
                
                if st.session_state.get('show_options') and unit_name in st.session_state.get('active_unit', ''):
                    st.write("---")
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        if st.button("🟢 Сорил эхлэх", key=f"start_{i}"):
                            st.session_state.test_started = True
                            st.session_state.start_time = time.time()
                            st.rerun()
                    with c2: st.button("🔵 Дүн харах", key=f"res_{i}")
                    with c3: st.button("⚪ Алдаа шалгах", key=f"chk_{i}")
                    with c4: st.button("🔴 Бодолт", key=f"sol_{i}")
    
    else:
            st_autorefresh(interval=1000, key="quizrefresh")
            remaining = (40 * 60) - (time.time() - st.session_state.start_time)
if remaining <= 0:
                st.error("⏰ Хугацаа дууслаа!")
                st.session_state.test_started = False
                if st.button("Буцах"):
                    st.rerun()
            else:
                mins, secs = divmod(int(remaining), 60)
                st.sidebar.markdown(f"""
                    <div style="background-color: #ff4b4b; padding: 10px; border-radius: 10px; text-align: center; margin-top: 20px;">
                        <h2 style="color: white; margin: 0;">⏱️ {mins:02d}:{secs:02d}</h2>
                        <p style="color: white; margin: 0;">Үлдсэн хугацаа</p>
                    </div>
                """, unsafe_allow_html=True)

                st.subheader(st.session_state.active_unit)
                st.write("---")
                
                # Сорил дуусгах товч
                if st.button("✅ Сорил дуусгах"):
                    st.session_state.test_started = False
                    st.rerun()
    # --- ДААЛГАВРЫН САН ---
    elif st.session_state.selected_menu == "Даалгаврын сан":
        import pandas as pd
        st.markdown('<p class="main-header">📚 Даалгаврын сан</p>', unsafe_allow_html=True)
        try:
            df = pd.read_excel("data_bank.xlsx")
            for unit_name in ["Нэгж 1"]:
                with st.expander(f"🔹 {unit_name}", expanded=True):
                    unit_df = df[df['Нэгж'] == unit_name]
                    for i, row in unit_df.iterrows():
                        st.markdown(f"#### 🔹 Бодлого {i+1}:")
                        
                        # Текстийг автоматаар шинэ мөрөнд шилжүүлэх (A, B, C, D-г доош нь цувуулна)
                        raw_q = str(row['Асуулт'])
                        q_text = raw_q.replace("A.", "\n\nA.").replace("B.", "\n\nB.").replace("C.", "\n\nC.").replace("D.", "\n\nD.")
                        st.markdown(q_text)
                        
                        # Хариу оруулах
                        u_ans = st.text_input(f"Хариу (A, B, C, D):", key=f"q_{i}", placeholder="Жишээ нь: A")
                        c1, c2 = st.columns([1, 4])
                        with c1:
                            if st.button(f"🔍 Шалгах", key=f"b_{i}"):
                                if str(u_ans).strip().upper() == str(row['Хариу']).strip().upper():
                                    st.success("Зөв! ✅")
                                else:
                                    st.error(f"Буруу. Зөв хариу: {row['Хариу']}")
                        with c2:
                            if pd.notnull(row['Бодолт']):
                                with st.expander("💡 Тайлбар харах"):
                                    st.info(str(row['Бодолт']))
                        st.write("---")
            st.markdown("<style>.stMarkdown p {font-family:'Times New Roman'; font-size:18px; line-height:1.8;}</style>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Алдаа гарлаа: {e}")
                                with st.expander("💡 Тайлбар харах"):
                                    st.info(str(row['Бодолт']))
                        st.write("---")
            st.markdown("<style>.stMarkdown p {font-family:'Times New Roman'; font-size:18px; line-height:1.8;}</style>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Алдаа гарлаа: {e}")

    elif st.session_state.selected_menu == "Цахим контент":
        st.markdown('<p class="main-header">📺 Цахим контент</p>', unsafe_allow_html=True)
        st.info("Видео хичээлүүд бэлтгэгдэж байна.")

    elif st.session_state.selected_menu == "Клубын мэдээлэл":
        st.markdown('<p class="main-header">🏢 Клубын мэдээлэл</p>', unsafe_allow_html=True)
        st.info("Математикийн клубын мэдээлэл.")

    elif st.session_state.selected_menu == "Хүүхдийн хүмүүжил төлөвшил МХБ":
        st.markdown('<p class="main-header">❤️ Хүмүүжил төлөвшил</p>', unsafe_allow_html=True)
        st.info("Зөвлөгөө мэдээлэл.")
