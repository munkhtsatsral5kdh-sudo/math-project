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

def smart_math_render(text):
    if not isinstance(text, str): return str(text)
    if ('\\' in text or '^' in text or '/' in text) and '$' not in text:
        clean_text = text.replace('\\displaystyle', '').strip()
        text = f"$\\displaystyle {clean_text}$"
    return text

# 2. ДИЗАЙН (ХЭСЭГ ТУС БҮРТ ЗОРИУЛСАН CSS)
st.markdown("""
    <style>
    /* ҮНДСЭН ГРИД */
    .stApp { background-color: white; }
    [data-testid="stSidebar"] { background-color: #0b4ab1 !important; }
    
    /* [1] НҮҮР ХУУДАСНЫ 3 ТОМ ТОВЧЛУУР (btn_1, btn_2, btn_3) */
    div.stButton > button[key^="btn_"] {
        width: 100% !important;
        height: 250px !important; /* Өндөр */
        border-radius: 20px !important;
        background: #fdfdfd !important;
        border: 1px solid #0b4ab1 !important;
    }
    div.stButton > button[key^="btn_"] p {
        font-size: 26px !important; /* Үсгийн хэмжээ */
        font-weight: bold !important;
        color: #0b4ab1 !important;
    }

    /* [2] ДААЛГАВРЫН САНГИЙН "ШАЛГАХ" ТОВЧ (check_) */
    div.stButton > button[key^="check_"] {
        width: 130px !important; /* Нарийн */
        height: 40px !important; /* Намхан */
        font-size: 15px !important;
        background-color: #28a745 !important;
        color: white !important;
        border-radius: 8px !important;
    }

    /* [3] СОРИЛЫН A, B, C, D ТОВЧ (q_btn_) */
    div.stButton > button[key^="q_btn_"] {
        width: 50px !important;
        height: 40px !important;
        min-width: 50px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 5px !important;
    }

    /* [4] ТЕКСТИЙН ХЭМЖЭЭНҮҮД */
    .unit-title { font-size: 22px !important; font-weight: bold; color: #333; }
    .question-box { font-size: 19px !important; line-height: 1.6; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR
with st.sidebar:
    st.markdown('<p style="color:white; font-size:40px; text-align:center; font-weight:bold;">ЦЭС</p>', unsafe_allow_html=True)
    menu_options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил"]
    selected = option_menu(None, menu_options, icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'], default_index=0)
    if selected != st.session_state.selected_menu:
        st.session_state.selected_menu = selected
        st.rerun()

# 4. НҮҮР ХУУДАС
if st.session_state.selected_menu == "Нүүр хуудас":
    st.markdown('<div style="background:white; padding:30px; border-radius:20px; border-left:10px solid #0b4ab1; box-shadow: 0 10px 30px rgba(0,0,0,0.05);"><h1 style="color:#0b4ab1;">Математикийн ертөнцөд тавтай морил!</h1></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("📺\n\nЦахим контент", key="btn_1"): st.session_state.selected_menu = "Цахим контент"; st.rerun()
    with c2: 
        if st.button("📚\n\nДаалгаврын сан", key="btn_2"): st.session_state.selected_menu = "Даалгаврын сан"; st.rerun()
    with c3: 
        if st.button("📝\n\nСорил", key="btn_3"): st.session_state.selected_menu = "Сорил"; st.rerun()

# 5. ДААЛГАВРЫН САН
elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown("<h2 style='text-align:center;'>📚 Даалгаврын сан</h2>", unsafe_allow_html=True)
    units = ["Тоон олонлог", "Харьцаа", "Алгебр", "Дараалал", "Өнцөг", "Байршил", "Хэмжигдэхүүн", "Статистик"]
    col_u, col_l = st.columns([0.6, 0.4])
    u_choice = col_u.selectbox("Сэдэв сонгох:", units)
    l_choice = col_l.radio("Түвшин:", ["Мэдлэг", "Чадвар", "Хэрэглээ"], horizontal=True)
    
    u_idx = units.index(u_choice) + 1
    l_idx = {"Мэдлэг": 1, "Чадвар": 2, "Хэрэглээ": 3}[l_choice]
    f_path = f"task_{u_idx}_{l_idx}.xlsx"

    if os.path.exists(f_path):
        df = pd.read_excel(f_path)
        for idx, row in df.iterrows():
            st.markdown(f"<div class='unit-title'>Бодлого {idx+1}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='question-box'>{smart_math_render(row['Асуулт'])}</div>", unsafe_allow_html=True)
            ans = st.radio(f"Хариу {idx}", ["A", "B", "C", "D"], key=f"t_{u_idx}_{idx}", horizontal=True, label_visibility="collapsed")
            if st.button(f"Шалгах {idx+1}", key=f"check_{idx}"):
                if str(ans) == str(row['Хариу']).strip().upper(): st.success("Зөв!")
                else: st.error(f"Буруу. Зөв хариу: {row['Хариу']}")
            st.write("---")
    else: st.warning("Файл олдсонгүй.")

# 6. СОРИЛ
elif st.session_state.selected_menu == "Сорил":
    st.markdown("<h2 style='text-align:center;'>📝 Онлайн сорил</h2>", unsafe_allow_html=True)
    quiz_units = ["Нэгж 1", "Нэгж 2", "Нэгж 3", "Нэгж 4", "Нэгж 5", "Нэгж 6", "Нэгж 7", "Нэгж 8"]
    
    st.markdown("<div style='background:#343a40; color:white; padding:10px; display:flex; font-weight:bold;'><div style='width:70%'>Сэдэв</div><div style='width:30%; text-align:center'>Хувилбар</div></div>", unsafe_allow_html=True)
    
    for i, name in enumerate(quiz_units):
        c_n, c_v = st.columns([0.7, 0.3])
        c_n.write(f"{i+1}. {name}")
        with c_v:
            v_cols = st.columns(4)
            for j, v in enumerate(["A", "B", "C", "D"]):
                if v_cols[j].button(v, key=f"q_btn_{i}_{v}"):
                    st.info(f"Сонголоо: {name} - {v}")

# БУСАД
else:
    st.title(st.session_state.selected_menu)
    st.info("Удахгүй мэдээлэл орно.")
