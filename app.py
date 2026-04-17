import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import pandas as pd
import time

# 1. Сайтын ерөнхий тохиргоо
st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# --- СИСТЕМ: ЦЭСНИЙ УДИРДЛАГА ---
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Нүүр хуудас"

# УХААЛАГ МАТЕМАТИК ТАНИГЧ
def smart_math_render(text):
    if not isinstance(text, str): return str(text)
    if ('\\' in text or '^' in text or '/' in text) and '$' not in text:
        clean_text = text.replace('\\displaystyle', '').strip()
        text = f"$\\displaystyle {clean_text}$"
    return text

# 2. ДИЗАЙН (ТУС БҮРТ НЬ ТОХИРУУЛАХ БОЛОМЖТОЙ CSS)
st.markdown("""
    <style>
    /* ҮНДСЭН ГРИД */
    .stApp { background-color: white; }
    [data-testid="stSidebar"] { background-color: #0b4ab1 !important; min-width: 260px !important; }
    .sidebar-title { color: white; text-align: center; font-size: 45px; font-weight: bold; padding: 20px 0; }
    
    /* 1. НҮҮР ХУУДАСНЫ ТОМ ТОВЧЛУУРУУД (btn_1, btn_2, btn_3) */
    div.stButton > button[key^="btn_"] {
        width: 100% !important;
        height: 250px !important;
        border-radius: 25px !important;
        background: #fdfdfd !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05) !important;
        border: 1px solid #f0f0f0 !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }
    div.stButton > button[key^="btn_"] p {
        font-size: 24px !important; /* Нүүр хуудасны текстийн хэмжээ */
        font-weight: bold !important;
        color: #0b4ab1 !important;
    }

    /* 2. ДААЛГАВРЫН САНГИЙН "ШАЛГАХ" ТОВЧ (check_) */
    div.stButton > button[key^="check_"] {
        width: 140px !important;
        height: 45px !important;
        font-size: 16px !important; /* Шалгах товчны текстийн хэмжээ */
        background-color: #28a745 !important;
        color: white !important;
        border-radius: 10px !important;
        margin-top: 10px !important;
    }

    /* 3. СОРИЛ ХЭСГИЙН A, B, C, D СОНГОХ ТОВЧ (q_) */
    div.stButton > button[key^="q_"] {
        width: 55px !important;
        height: 45px !important;
        min-width: 55px !important;
        background-color: white !important;
        border: 1px solid #0b4ab1 !important;
        color: #0b4ab1 !important;
        font-weight: bold !important;
        font-size: 18px !important; /* A, B, C, D үсгийн хэмжээ */
    }

    /* АСУУЛТЫН ТЕКСТИЙН ХЭМЖЭЭ */
    .question-text {
        font-size: 20px !important;
        font-weight: 500;
        color: #333;
        margin-bottom: 15px;
    }
    
    .main-header { color: #0b4ab1; font-size: 45px; font-weight: 800; line-height: 1.1; }
    .goal-box { background: white; padding: 25px; border-radius: 20px; border-left: 10px solid #0b4ab1; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    menu_options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил"]
    selected = option_menu(
        menu_title=None, options=menu_options,
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        default_index=0,
        styles={
            "container": {"background-color": "#0b4ab1"},
            "nav-link": {"color": "white", "font-size": "16px", "text-align": "left"},
            "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)"}
        }
    )
    if selected != st.session_state.selected_menu:
        st.session_state.selected_menu = selected
        st.rerun()

# 4. НҮҮР ХУУДАС
if st.session_state.selected_menu == "Нүүр хуудас":
    col1, col2 = st.columns([1, 1.2], gap="large")
    with col1:
        if os.path.exists("logo.gif"):
            with open("logo.gif", "rb") as f: data_url = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(f'<img src="data:image/gif;base64,{data_url}" style="width: 100%; border-radius: 20px;">', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="goal-box"><div class="main-header">Математикийн ертөнцөд тавтай морил!</div><div style="font-size: 19px; line-height: 1.4; color: #444; margin-top:15px;">Хамтдаа суралцаж, хамтдаа хөгжицгөөе!</div></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1: 
        if st.button("📺\n\nЦахим контент", key="btn_1"): st.session_state.selected_menu = "Цахим контент"; st.rerun()
    with c2: 
        if st.button("📚\n\nДаалгаврын сан", key="btn_2"): st.session_state.selected_menu = "Даалгаврын сан"; st.rerun()
    with c3: 
        if st.button("📝\n\nСорил", key="btn_3"): st.session_state.selected_menu = "Сорил"; st.rerun()

# 5. ДААЛГАВРЫН САН
elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown("<h3 style='text-align: center; color: #0b4ab1;'>📚 Бодлогын сан</h3>", unsafe_allow_html=True)
    units = ["Тоон олонлог, зэрэг, язгуур, тоог жиших, тоймлох", "Харьцаа, пропорц, процент", "Алгебрын илэрхийлэл, тэгшитгэл, тэнцэтгэл биш", "Дараалал, функц", "Өнцөг, дүрс, байгуулалт", "Байршил, хөдөлгөөн, хувиргалт", "Хэмжигдэхүүн", "Магадлал, статистик"]
    
    col_u, col_l = st.columns([0.6, 0.4])
    u_choice = col_u.selectbox("Сэдэв сонгох:", units)
    l_choice = col_l.radio("Түвшин:", ["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"], horizontal=True)

    u_idx = units.index(u_choice) + 1
    l_idx = {"Мэдлэг ойлголт": 1, "Чадвар": 2, "Хэрэглээ": 3}[l_choice]
    f_path = f"task_{u_idx}_{l_idx}.xlsx"

    if os.path.exists(f_path):
        df = pd.read_excel(f_path)
        for idx, row in df.iterrows():
            st.markdown(f"<div class='question-text'>Бодлого {idx+1}:</div>", unsafe_allow_html=True)
            st.markdown(smart_math_render(row['Асуулт']))
            ans = st.radio(f"Сонгох {idx}:", ["A", "B", "C", "D"], key=f"t_ans_{u_idx}_{idx}", horizontal=True, label_visibility="collapsed")
            if st.button(f"Шалгах {idx+1}", key=f"check_{idx}"):
                if str(ans) == str(row['Хариу']).strip().upper(): st.success("✅ Зөв!")
                else: st.error(f"❌ Буруу. Зөв хариу: {row['Хариу']}")
            st.write("---")
    else: st.warning("Файл олдсонгүй.")

# 6. СОРИЛ
elif st.session_state.selected_menu == "Сорил":
    if 'quiz_active' not in st.session_state: st.session_state.quiz_active = False
    
    if not st.session_state.quiz_active:
        st.markdown("<h3 style='text-align: center; color: #0b4ab1;'>📝 Онлайн сорил</h3>", unsafe_allow_html=True)
        # Хүснэгтэн загвар
        st.markdown("<div style='background-color: #343a40; color: white; padding: 10px; display: flex;'> <div style='width: 70%;'>Сорилын нэр</div> <div style='width: 30%; text-align: center;'>Хувилбар</div> </div>", unsafe_allow_html=True)
        
        quiz_list = ["Тоон олонлог...", "Харьцаа...", "Алгебр...", "Дараалал...", "Өнцөг...", "Байршил...", "Хэмжигдэхүүн...", "Магадлал..."]
        for i, name in enumerate(quiz_list):
            c_name, c_btns = st.columns([0.7, 0.3])
            c_name.write(f"{i+1}. {name}")
            with c_btns:
                v_cols = st.columns(4)
                for j, v in enumerate(["A", "B", "C", "D"]):
                    # СОРИЛЫН ТОВЧЛУУР (q_ түлхүүртэй)
                    if v_cols[j].button(v, key=f"q_{i}_{v}"):
                        st.session_state.quiz_file = f"quiz_{i+1}_{v}.xlsx"
                        st.session_state.quiz_active = True
                        st.session_state.start_time = time.time()
                        st.rerun()
    else:
        # Сорил бодох хэсэг
        st.write(f"Одоо бодож буй файл: {st.session_state.quiz_file}")
        if st.button("⬅️ Буцах", key="check_back"): 
            st.session_state.quiz_active = False
            st.rerun()

# БУСАД ЦЭСҮҮД
else:
    st.markdown(f"<h1>{st.session_state.selected_menu}</h1>", unsafe_allow_html=True)
    st.info("Удахгүй мэдээлэл нэмэгдэнэ.")
