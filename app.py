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

# 2. ДИЗАЙН (CSS ШИНЭЧЛЭЛ)
st.markdown("""
    <style>
    /* Ерөнхий үсгийн хэмжээг томруулах */
    html, body, [class*="st-"] {
        font-size: 19px !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .stApp { background-color: white; }
    [data-testid="stSidebar"] { background-color: #0b4ab1 !important; min-width: 260px !important; }
    .sidebar-title { color: white; text-align: center; font-size: 40px; font-weight: bold; padding: 20px 0; }
    
    /* Нүүр хуудасны хайрцаг */
    .goal-box { 
        background: white; 
        padding: 40px; 
        border-radius: 25px; 
        border: 1px solid #f0f2f6; 
        border-left: 12px solid #0b4ab1; 
        box-shadow: 0 15px 35px rgba(0,0,0,0.07); 
    }
    .main-header { color: #0b4ab1; font-size: 45px; font-weight: 800; margin-bottom: 20px; line-height: 1.2; }
    .main-text { font-size: 22px !important; line-height: 1.7; color: #333; text-align: justify; }

    /* НҮҮР ХУУДАСНЫ 3 ТОМ ТОВЧЛУУР */
    div.stButton > button {
        width: 100% !important;
        min-height: 200px !important; 
        border-radius: 30px !important;
        border: 2px solid #f0f2f6 !important;
        background: linear-gradient(145deg, #ffffff, #f8f9fa) !important;
        box-shadow: 8px 8px 20px #dee2e6, -8px -8px 20px #ffffff !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s ease-in-out !important;
    }
    
    div.stButton > button:hover {
        transform: translateY(-10px) !important;
        border-color: #0b4ab1 !important;
        box-shadow: 0 15px 30px rgba(11, 74, 177, 0.15) !important;
    }

    div.stButton > button p {
        font-size: 26px !important;
        font-weight: 800 !important;
        color: #0b4ab1 !important;
        margin-top: 15px !important;
    }

    /* СОРИЛЫН A, B, C, D ТОВЧНУУДЫГ НЭГ ШУГАМАНД ЦЭГЦЛЭХ */
    [data-testid="stHorizontalBlock"] .stButton > button {
        min-height: 45px !important;
        height: 45px !important;
        width: 100% !important;
        max-width: 55px !important;
        border-radius: 12px !important;
        padding: 0 !important;
        background: #f8f9fa !important;
        box-shadow: 2px 2px 5px #d1d9e6 !important;
        margin: 0 auto !important;
    }
    
    [data-testid="stHorizontalBlock"] .stButton > button p {
        font-size: 18px !important;
        margin-top: 0 !important;
        font-weight: bold !important;
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
        styles={
            "container": {"background-color": "#0b4ab1", "padding": "0"},
            "icon": {"color": "white", "font-size": "22px"}, 
            "nav-link": {"font-size": "18px", "color": "white", "text-align": "left", "margin": "8px 0px"},
            "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)", "font-weight": "bold"}
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
        st.markdown(f"""
            <div class="goal-box">
                <div class="main-header">Математикийн ертөнцөд тавтай морил!</div>
                <div class="main-text">
                    Сонирхолтой цахим хичээл, баялаг бодлогын сангаар дамжуулан математик сэтгэлгээгээ бие даан хөгжүүлж, 
                    ирээдүйн амжилтынхаа суурийг өнөөдөр тавихад тань бид туслах болно. 
                    <b>Хамтдаа суралцаж, хамтдаа хөгжицгөөе!</b>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1], gap="large")
    with c1:
        if st.button("📺\nЦахим контент", key="btn_1"): st.session_state.selected_menu = "Цахим контент"; st.rerun()
    with c2:
        if st.button("📚\nДаалгаврын сан", key="btn_2"): st.session_state.selected_menu = "Даалгаврын сан"; st.rerun()
    with c3:
        if st.button("📝\nСорил", key="btn_3"): st.session_state.selected_menu = "Сорил"; st.rerun()

# 5. ЦАХИМ КОНТЕНТ
elif st.session_state.selected_menu == "Цахим контент":
    st.markdown("<h1 style='color: #0b4ab1;'>📺 Цахим хичээлүүд</h1>", unsafe_allow_html=True)
    st.write("Доорх хичээлүүдийг үзэж мэдлэгээ баталгаажуулаарай.")
    st.video("https://www.youtube.com/watch?v=your_video_id")

# 6. ДААЛГАВРЫН САН
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

# 7. СОРИЛ
elif st.session_state.selected_menu == "Сорил":
    st.markdown("<h2 style='text-align: center; color: #0b4ab1;'>📝 Онлайн сорил, шалгалт</h2>", unsafe_allow_html=True)
    units = ["Тоон олонлог, зэрэг, язгуур", "Харьцаа, пропорц, процент", "Алгебрын илэрхийлэл, тэгшитгэл", "Дараалал, функц", "Өнцөг, дүрс, байгуулалт", "Байршил, хөдөлгөөн", "Хэмжигдэхүүн", "Магадлал, статистик"]
    
    if 'quiz_active' not in st.session_state: st.session_state.quiz_active = False

    if not st.session_state.quiz_active:
        # Хүснэгтийн толгой
        st.markdown("""
            <div style='background-color: #343a40; color: white; padding: 15px; border-radius: 12px; display: flex; align-items: center; font-weight: bold; margin-bottom: 10px;'>
                <div style='width: 65%; padding-left: 15px; font-size: 20px;'>Сорилын нэр (IX анги)</div>
                <div style='width: 35%; text-align: center; font-size: 20px;'>Хувилбарууд</div>
            </div>
        """, unsafe_allow_html=True)

        for i, name in enumerate(units):
            row_c1, row_c2 = st.columns([0.65, 0.35])
            with row_c1:
                st.markdown(f"<div style='padding: 12px; font-size: 20px;'><b>{i+1}.</b> {name}</div>", unsafe_allow_html=True)
            with row_c2:
                # Товчлууруудыг gap="small" тохиргоогоор маш цэгцтэй зэрэгцүүлэв
                v_cols = st.columns(4, gap="small")
                for idx, var in enumerate(["A", "B", "C", "D"]):
                    if v_cols[idx].button(var, key=f"v{var}_{i}"):
                        st.session_state.unit_name = name; st.session_state.variant = var; st.session_state.quiz_active = True; st.rerun()
            st.markdown("<hr style='margin: 0; opacity: 0.1;'>", unsafe_allow_html=True)
    else:
        if st.button("⬅️ Буцах"): st.session_state.quiz_active = False; st.rerun()
        st.info(f"📍 {st.session_state.unit_name} | Хувилбар {st.session_state.variant}")

# 8. КЛУБ
elif st.session_state.selected_menu == "Клубын мэдээлэл":
    st.markdown("<h1 style='color: #0b4ab1;'>👥 Математикийн клуб</h1>", unsafe_allow_html=True)

# 9. ХҮҮХДИЙН ХҮМҮҮЖИЛ
elif st.session_state.selected_menu == "Хүүхдийн хүмүүжил":
    st.markdown("<h1 style='color: #0b4ab1;'>❤️ Хүүхдийн хүмүүжил, зөвлөгөө</h1>", unsafe_allow_html=True)
