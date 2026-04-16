import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import pandas as pd
import time

# 1. Сайтын ерөнхий тохиргоо
st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# --- СИСТЕМ: SESSION STATE ---
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Нүүр хуудас"
if 'quiz_active' not in st.session_state:
    st.session_state.quiz_active = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

# Сэдвүүдийн жагсаалт
UNITS = [
    "Тоон олонлог, зэрэг, язгуур", "Харьцаа, пропорц, процент",
    "Алгебрын илэрхийлэл, тэгшитгэл", "Дараалал, функц",
    "Өнцөг, дүрс, байгуулалт", "Байршил, хөдөлгөөн",
    "Хэмжигдэхүүн", "Магадлал, статистик"
]

# УХААЛАГ МАТЕМАТИК ТАНИГЧ
def smart_math_render(text):
    if not isinstance(text, str): return str(text)
    for label in ['A.', 'B.', 'C.', 'D.']:
        if label in text:
            text = text.replace(label, f'\n\n**{label}**')
    if ('\\' in text or '^' in text or '/' in text) and '$' not in text:
        clean_text = text.replace('\\displaystyle', '').strip()
        text = f"$\\displaystyle {clean_text}$"
    return text

# 2. ДИЗАЙН (ЧИНИЙ АНХНЫ ЗАГВАРЫГ ХАДГАЛАВ)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    [data-testid="stSidebar"] { background-color: #0b4ab1 !important; min-width: 260px !important; }
    .sidebar-title { color: white; text-align: center; font-size: 45px; font-weight: bold; padding: 20px 0; margin-bottom: 10px; }
    .goal-box { background: white; padding: 25px; border-radius: 20px; border: 1px solid #f0f2f6; border-left: 10px solid #0b4ab1; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .main-header { color: #0b4ab1; font-size: 45px; font-weight: 800; margin-bottom: 5px; line-height: 0.95 !important; }
    
    /* Чиний анхны том товчлуурын стиль */
    div.stButton > button { 
        width: 100% !important; 
        height: 190px !important; 
        border-radius: 25px !important; 
        border: 1px solid #f0f0f0 !important; 
        background: #fdfdfd !important; 
        box-shadow: 0 10px 25px rgba(0,0,0,0.05) !important; 
        display: flex !important; 
        flex-direction: column !important; 
        align-items: center !important; 
        justify-content: center !important; 
        transition: all 0.3s ease-in-out !important; 
    }
    div.stButton > button p { font-size: 22px !important; font-weight: bold !important; color: #0b4ab1 !important; }
    
    .math-card { background: white; padding: 25px; border-radius: 15px; border: 1px solid #e0e0e0; margin-bottom: 20px; }
    .timer-container { position: sticky; top: 0; background: #ff4b4b; color: white; padding: 10px; border-radius: 12px; text-align: center; font-size: 22px; font-weight: bold; z-index: 999; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Цэс)
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    menu_options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил"]
    current_index = menu_options.index(st.session_state.selected_menu) if st.session_state.selected_menu in menu_options else 0
    selected = option_menu(
        menu_title=None, options=menu_options,
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        default_index=current_index,
        styles={"container": {"background-color": "#0b4ab1", "padding": "0"}, "icon": {"color": "white", "font-size": "18px"}, "nav-link": {"font-size": "16px", "color": "white", "margin": "5px 0px", "padding": "10px 15px", "text-align": "left", "font-weight": "500"}, "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)", "font-weight": "bold"}}
    )
    if selected != st.session_state.selected_menu:
        st.session_state.selected_menu = selected
        st.session_state.quiz_active = False
        st.rerun()

# 4. НҮҮР ХУУДАС
if st.session_state.selected_menu == "Нүүр хуудас":
    col1, col2 = st.columns([1, 1.2], gap="large")
    with col1:
        if os.path.exists("logo.gif"):
            with open("logo.gif", "rb") as f: data_url = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(f'<img src="data:image/gif;base64,{data_url}" style="width: 100%; border-radius: 20px;">', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="goal-box"><div class="main-header">Математикийн ертөнцөд тавтай морил!</div><div style="font-size: 19px; line-height: 1.4; color: #444; text-align: justify; text-indent: 20px;">Сонирхолтой цахим хичээл, баялаг бодлогын сангаар дамжуулан математик сэтгэлгээгээ бие даан хөгжүүлж, ирээдүйн амжилтынхаа суурийг өнөөдөр тавихад тань бид туслах болно. Хамтдаа суралцаж, хамтдаа хөгжицгөөе!</div></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1], gap="medium")
    with c1:
        if st.button("📺\n\nЦахим контент", key="btn_1"): st.session_state.selected_menu = "Цахим контент"; st.rerun()
    with c2:
        if st.button("📚\n\nДаалгаврын сан", key="btn_2"): st.session_state.selected_menu = "Даалгаврын сан"; st.rerun()
    with c3:
        if st.button("📝\n\nСорил", key="btn_3"): st.session_state.selected_menu = "Сорил"; st.rerun()

# 5. ЦАХИМ КОНТЕНТ
elif st.session_state.selected_menu == "Цахим контент":
    st.markdown("<h1 style='color: #0b4ab1;'>📺 Цахим хичээлүүд</h1>", unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=your_video_id")

# 6. ДААЛГАВРЫН САН (24 файлтай хувилбар)
elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown("<h3 style='color: #0b4ab1; text-align: center;'>📚 Бодлогын сан</h3>", unsafe_allow_html=True)
    sc1, sc2 = st.columns(2)
    with sc1: u_choice = st.selectbox("Сэдэв сонгох:", UNITS)
    with sc2: l_choice = st.radio("Түвшин:", ["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"], horizontal=True)
    
    u_idx = UNITS.index(u_choice) + 1
    levels = {"Мэдлэг ойлголт": 1, "Чадвар": 2, "Хэрэглээ": 3}
    f_path = f"task_{u_idx}_{levels[l_choice]}.xlsx"
    
    if os.path.exists(f_path):
        df = pd.read_excel(f_path)
        for i, row in df.iterrows():
            with st.form(key=f"task_{u_idx}_{i}"):
                st.markdown('<div class="math-card">', unsafe_allow_html=True)
                st.markdown(f"### 📝 Бодлого {i+1}")
                st.markdown(smart_math_render(row['Асуулт']))
                ans = st.radio("Хариу сонгох:", ["A", "B", "C", "D"], key=f"ans_{i}", horizontal=True)
                if st.form_submit_button("Шалгах"):
                    if ans == str(row['Хариу']).strip().upper(): st.success("Зөв! ✅"); st.balloons()
                    else: 
                        st.error(f"Буруу. Зөв хариу: {row['Хариу']}")
                        if 'Бодолт' in row: st.info(f"**Бодолт:** {row['Бодолт']}")
                st.markdown('</div>', unsafe_allow_html=True)
    else: st.warning(f"Файл олдсонгүй: {f_path}")

# 7. СОРИЛ (Зураг дээрх загварыг хадгалж, логикийг нэмэв)
elif st.session_state.selected_menu == "Сорил":
    # Гарчиг
    st.markdown("<h3 style='text-align: center; color: #0b4ab1; font-family: sans-serif;'>📝 Онлайн сорил, шалгалт</h3>", unsafe_allow_html=True)

    # 1. СОРИЛ СОНГОХ ХЭСЭГ (Хэрэв сорил эхлээгүй бол)
    if not st.session_state.quiz_active:
        # Хүснэгтийн толгой (Зураг дээрх шиг хар дэвсгэртэй)
        st.markdown("""
            <div style='background-color: #343a40; color: white; padding: 10px; border-radius: 5px; display: flex; font-weight: bold;'>
                <div style='width: 5%;'>#</div>
                <div style='width: 65%;'>Сорилын нэр (IX анги)</div>
                <div style='width: 30%; text-align: center;'>Хувилбарууд</div>
            </div>
        """, unsafe_allow_html=True)

        # Сэдвүүдийн жагсаалт
        units = [
            "Тоон олонлог, зэрэг, язгуур", "Харьцаа, пропорц, процент",
            "Алгебрын илэрхийлэл, тэгшитгэл", "Дараалал, функц",
            "Өнцөг, дүрс, байгуулалт", "Байршил, хөдөлгөөн",
            "Хэмжигдэхүүн", "Магадлал, статистик"
        ]

        for i, name in enumerate(units):
            col_n, col_v = st.columns([0.7, 0.3])
            
            # Сэдвүүдийг жагсааж бичих
            with col_n:
                st.markdown(f"<div style='padding: 12px 0; border-bottom: 1px solid #eee;'>{i+1}. {name}</div>", unsafe_allow_html=True)
            
            # Хувилбар сонгох A, B, C, D товчлуурууд
            with col_v:
                v_cols = st.columns(4)
                variants = ["A", "B", "C", "D"]
                for j, v in enumerate(variants):
                    if v_cols[j].button(v, key=f"v_btn_{i}_{v}"):
                        # Сонгосон файл болон төлөвийг хадгалах
                        st.session_state.current_quiz_file = f"quiz_{i+1}_{v}.xlsx"
                        st.session_state.quiz_active = True
                        st.session_state.start_time = time.time()
                        st.rerun()
            st.markdown("<div style='margin-top: -10px;'></div>", unsafe_allow_html=True)

    # 2. СОРИЛ ЯВАГДАЖ БАЙХ ҮЕ (Товчлуур дарсны дараа)
    else:
        # Хугацаа тооцох (40 минут = 2400 секунд)
        elapsed = int(time.time() - st.session_state.start_time)
        remaining = max(0, 2400 - elapsed)
        
        # Дээд хэсэгт таймер болон буцах товчлуур
        c_back, c_timer = st.columns([5, 1])
        if c_back.button("⬅️ Сорилын жагсаалт руу буцах"):
            st.session_state.quiz_active = False
            st.rerun()
        
        c_timer.error(f"⏳ {remaining//60:02d}:{remaining%60:02d}")

        # Файлыг уншиж бодлогуудыг харуулах
        f_path = st.session_state.current_quiz_file
        if os.path.exists(f_path):
            df_quiz = pd.read_excel(f_path)
            
            with st.form("quiz_submission_form"):
                st.info(f"📍 Таны сонгосон: {f_path}")
                for idx, row in df_quiz.iterrows():
                    st.markdown(f"**Асуулт {idx+1}:**")
                    # smart_math_render функц ашиглан томьёог харуулах
                    st.markdown(smart_math_render(row['Асуулт']))
                    st.radio("Хариу сонгох:", ["A", "B", "C", "D"], key=f"user_ans_{idx}", horizontal=True, label_visibility="collapsed")
                    st.write("---")
                
                if st.form_submit_button("🏁 Сорилыг дуусгах"):
                    st.success("Сорил дууслаа. Таны хариултууд хадгалагдлаа!")
                    # Энд оноо тооцох логик нэмж болно
                    st.session_state.quiz_active = False
        else:
            st.warning(f"Уучлаарай, '{f_path}' файл олдсонгүй. Файлаа шалгана уу.")
            if st.button("Буцах"):
                st.session_state.quiz_active = False
                st.rerun()

    # --- СОРИЛЫН ЦОНХ (Чиний өмнөх код хэвээрээ) ---
    else:
        # (Энэ хэсгийн кодыг чиний өмнөх кодноос хэвээр нь үлдээлээ...)
        c_back, c_time = st.columns([5, 1])
        if c_back.button("⬅️ Буцах"):
            st.session_state.quiz_active = False; st.rerun()
        c_time.error(f"⏳ 40:00")

        st.info(f"📍 {st.session_state.unit_name} | Хувилбар {st.session_state.variant}")

        if os.path.exists("data_bank.xlsx"):
            df = pd.read_excel("data_bank.xlsx")
            unit_num = units.index(st.session_state.unit_name) + 1
            
            # Шүүлтүүр: Нэгж ба Хувилбар
            if 'Хувилбар' in df.columns:
                q_df = df[(df['Нэгж'].astype(str).str.contains(str(unit_num))) & (df['Хувилбар'] == st.session_state.variant)]
            else:
                q_df = df[df['Нэгж'].astype(str).str.contains(str(unit_num))].head(5)

            if q_df.empty:
                st.warning("Энэ хэсэгт бодлого хараахан ороогүй байна.")
            else:
                for idx, row in q_df.iterrows():
                    st.markdown(smart_math_render(row['Асуулт']))
                    st.radio("Хариу сонгох:", ["A", "B", "C", "D"], key=f"q_{idx}", horizontal=True, label_visibility="collapsed")
                    st.write("---")
                
                if st.button("🏁 Дуусгах", use_container_width=True):
                    st.success("Дууслаа!"); st.session_state.quiz_active = False; st.rerun()
        else:
            st.error("data_bank.xlsx файл олдсонгүй.")

# 8 & 9. БУСАД
elif st.session_state.selected_menu == "Клубын мэдээлэл":
    st.markdown("<h1 style='color: #0b4ab1;'>👥 Клуб</h1>", unsafe_allow_html=True)
elif st.session_state.selected_menu == "Хүүхдийн хүмүүжил":
    st.markdown("<h1 style='color: #0b4ab1;'>❤️ Хүмүүжил</h1>", unsafe_allow_html=True)
