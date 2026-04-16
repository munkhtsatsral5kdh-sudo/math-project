import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import pandas as pd
import re

# 1. Сайтын ерөнхий тохиргоо
st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# --- СИСТЕМ: ЦЭСНИЙ УДИРДЛАГА ---
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Нүүр хуудас"

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

# 2. ДИЗАЙН (ШИНЭЧЛЭГДСЭН CSS)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    [data-testid="stSidebar"] { background-color: #0b4ab1 !important; min-width: 260px !important; }
    .sidebar-title { color: white; text-align: center; font-size: 45px; font-weight: bold; padding: 20px 0; margin-bottom: 10px; }
    
    /* Зорилго хайрцаг */
    .goal-box { background: white; padding: 30px; border-radius: 20px; border: 1px solid #f0f2f6; border-left: 10px solid #0b4ab1; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .main-header { color: #0b4ab1; font-size: 40px; font-weight: 800; margin-bottom: 15px; line-height: 1.1 !important; }
    
    /* НҮҮР ХУУДАСНЫ ТОМ ТОВЧЛУУРУУД */
    div.stButton > button {
        width: 100% !important;
        min-height: 180px !important; 
        border-radius: 25px !important;
        border: 2px solid #f0f2f6 !important;
        background: linear-gradient(145deg, #ffffff, #f5f7fa) !important;
        box-shadow: 5px 5px 15px #d1d9e6, -5px -5px 15px #ffffff !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s ease !important;
        white-space: pre-wrap !important;
    }
    
    div.stButton > button:hover {
        transform: translateY(-8px) !important;
        border-color: #0b4ab1 !important;
        box-shadow: 0 12px 25px rgba(11, 74, 177, 0.12) !important;
    }

    div.stButton > button p {
        font-size: 22px !important;
        font-weight: 700 !important;
        color: #0b4ab1 !important;
        margin-top: 10px !important;
    }

    /* СОРИЛ ХЭСГИЙН ЖИЖИГ ТОВЧНУУД (A, B, C, D) */
    [data-testid="stHorizontalBlock"] div.stButton > button {
        min-height: 45px !important;
        height: 45px !important;
        border-radius: 12px !important;
        margin: 2px 0 !important;
        background: white !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
    }
    
    [data-testid="stHorizontalBlock"] div.stButton > button p {
        font-size: 16px !important;
        margin-top: 0 !important;
    }

    .math-card { background: white; padding: 25px; border-radius: 15px; border: 1px solid #e0e0e0; margin-bottom: 20px; }
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
        st.rerun()

# 4. НҮҮР ХУУДАС
if st.session_state.selected_menu == "Нүүр хуудас":
    col1, col2 = st.columns([1, 1.2], gap="large")
    with col1:
        if os.path.exists("logo.gif"):
            with open("logo.gif", "rb") as f: data_url = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(f'<img src="data:image/gif;base64,{data_url}" style="width: 100%; border-radius: 20px;">', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="goal-box"><div class="main-header">Математикийн ертөнцөд тавтай морил!</div><div style="font-size: 19px; line-height: 1.5; color: #444; text-align: justify;">Сонирхолтой цахим хичээл, баялаг бодлогын сангаар дамжуулан математик сэтгэлгээгээ бие даан хөгжүүлж, ирээдүйн амжилтынхаа суурийг өнөөдөр тавихад тань бид туслах болно. Хамтдаа суралцаж, хамтдаа хөгжицгөөе!</div></div>', unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1], gap="medium")
    with c1:
        if st.button("📺\nЦахим контент", key="btn_1", use_container_width=True): 
            st.session_state.selected_menu = "Цахим контент"; st.rerun()
    with c2:
        if st.button("📚\nДаалгаврын сан", key="btn_2", use_container_width=True): 
            st.session_state.selected_menu = "Даалгаврын сан"; st.rerun()
    with c3:
        if st.button("📝\nСорил", key="btn_3", use_container_width=True): 
            st.session_state.selected_menu = "Сорил"; st.rerun()

# 5. ЦАХИМ КОНТЕНТ (ХЭВЭЭРЭЭ)
elif st.session_state.selected_menu == "Цахим контент":
    st.markdown("<h1 style='color: #0b4ab1;'>📺 Цахим хичээлүүд</h1>", unsafe_allow_html=True)
    st.write("Доорх хичээлүүдийг үзэж мэдлэгээ баталгаажуулаарай.")
    st.video("https://www.youtube.com/watch?v=your_video_id")

# 6. ДААЛГАВРЫН САН (ХЭВЭЭРЭЭ)
elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown("<h1 style='color: #0b4ab1; text-align: center;'>📚 Бодлогын сан</h1>", unsafe_allow_html=True)
    if os.path.exists("data_bank.xlsx"):
        df = pd.read_excel("data_bank.xlsx")
        sc1, sc2 = st.columns(2)
        with sc1: unit = st.selectbox("Сэдэв сонгох:", df['Нэгж'].unique())
        with sc2: level = st.radio("Түвшин:", ["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"], horizontal=True)
        f_df = df[(df['Нэгж'] == unit) & (df['Түвшин'] == level)]
        if f_df.empty: st.info("Энэ хэсэгт бодлого хараахан ороогүй байна.")
        else:
            for i, row in f_df.iterrows():
                with st.form(key=f"form_{i}"):
                    st.markdown('<div class="math-card">', unsafe_allow_html=True)
                    st.markdown(f"### 📝 Бодлого {i+1}"); st.markdown(smart_math_render(row['Асуулт']))
                    ans = st.radio("Хариу сонгох:", ["A", "B", "C", "D"], key=f"ans_{i}", horizontal=True)
                    if st.form_submit_button("Шалгах"):
                        correct = str(row['Хариу']).strip().upper()
                        if ans == correct: st.success("Зөв! ✅"); st.balloons()
                        else: st.error(f"Буруу байна. Зөв хариу: {correct}")
                    st.markdown('</div>', unsafe_allow_html=True)
    else: st.warning("data_bank.xlsx файл олдсонгүй.")

# 7. СОРИЛ (ХЭВЭЭРЭЭ - Дизайн нь CSS-ээр зохицуулагдсан)
elif st.session_state.selected_menu == "Сорил":
    st.markdown("<h3 style='text-align: center; color: #0b4ab1;'>📝 Онлайн сорил, шалгалт</h3>", unsafe_allow_html=True)
    units = ["Тоон олонлог, зэрэг, язгуур", "Харьцаа, пропорц, процент", "Алгебрын илэрхийлэл, тэгшитгэл", "Дараалал, функц", "Өнцөг, дүрс, байгуулалт", "Байршил, хөдөлгөөн", "Хэмжигдэхүүн", "Магадлал, статистик"]
    if 'quiz_active' not in st.session_state: st.session_state.quiz_active = False

    if not st.session_state.quiz_active:
        st.markdown("""<div style='background-color: #343a40; color: white; padding: 10px; border-radius: 10px; display: flex; font-size: 14px;'><div style='width: 5%;'>#</div><div style='width: 50%;'>Сорилын нэр (IX анги)</div><div style='width: 45%; text-align: center;'>Хувилбарууд</div></div>""", unsafe_allow_html=True)
        for i, name in enumerate(units):
            col_name, col_vars = st.columns([0.55, 0.45])
            with col_name: st.write(f"**{i+1}.** {name}")
            with col_vars:
                v1, v2, v3, v4 = st.columns(4)
                if v1.button("A", key=f"vA_{i}"): st.session_state.unit_name = name; st.session_state.variant = "A"; st.session_state.quiz_active = True; st.rerun()
                if v2.button("B", key=f"vB_{i}"): st.session_state.unit_name = name; st.session_state.variant = "B"; st.session_state.quiz_active = True; st.rerun()
                if v3.button("C", key=f"vC_{i}"): st.session_state.unit_name = name; st.session_state.variant = "C"; st.session_state.quiz_active = True; st.rerun()
                if v4.button("D", key=f"vD_{i}"): st.session_state.unit_name = name; st.session_state.variant = "D"; st.session_state.quiz_active = True; st.rerun()
            st.markdown("<hr style='margin: 0; opacity: 0.1;'>", unsafe_allow_html=True)
    else:
        c_back, c_time = st.columns([5, 1])
        if c_back.button("⬅️ Буцах"): st.session_state.quiz_active = False; st.rerun()
        c_time.error(f"⏳ 40:00")
        st.info(f"📍 {st.session_state.unit_name} | Хувилбар {st.session_state.variant}")
        # Сорилын логик хэвээрээ... (код товчлох үүднээс энд үлдээв)

# 8 болон 9-р хэсэг (Клуб, Хүмүүжил) хэвээрээ...
elif st.session_state.selected_menu == "Клубын мэдээлэл":
    st.markdown("<h1 style='color: #0b4ab1;'>👥 Математикийн клуб</h1>", unsafe_allow_html=True)
elif st.session_state.selected_menu == "Хүүхдийн хүмүүжил":
    st.markdown("<h1 style='color: #0b4ab1;'>❤️ Хүүхдийн хүмүүжил, зөвлөгөө</h1>", unsafe_allow_html=True)
