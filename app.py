import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import pandas as pd
import time

# 1. Сайтын ерөнхий тохиргоо
st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# --- СИСТЕМ: ХЭРЭГЛЭГЧИЙН ТӨЛӨВ ХАДГАЛАХ ---
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Нүүр хуудас"
if 'quiz_active' not in st.session_state:
    st.session_state.quiz_active = False

# УХААЛАГ МАТЕМАТИК ТАНИГЧ (Томьёо харуулах)
def smart_math_render(text):
    if not isinstance(text, str): return str(text)
    if ('\\' in text or '^' in text or '/' in text) and '$' not in text:
        return f"$\\displaystyle {text.replace('\\\\displaystyle', '').strip()}$"
    return text

# 2. ДИЗАЙН (ЧИНИЙ АНХНЫ ЗАГВАР ЯГ ХЭВЭЭРЭЭ)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    [data-testid="stSidebar"] { background-color: #0b4ab1 !important; min-width: 250px !important; }
    .sidebar-title { color: white; text-align: center; font-size: 45px; font-weight: bold; padding: 20px 0; }
    
    /* Нүүр хуудасны цагаан том товчлуурууд */
    div.stButton > button {
        width: 100% !important;
        height: 200px !important;
        border-radius: 25px !important;
        background: white !important;
        border: 1px solid #f0f2f6 !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05) !important;
        color: #0b4ab1 !important;
        font-size: 20px !important;
        font-weight: bold !important;
    }
    
    /* Сорил хэсгийн хар толгой */
    .quiz-header {
        background-color: #343a40;
        color: white;
        padding: 10px;
        border-radius: 5px;
        display: flex;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (ЦЭС)
with st.sidebar:
    st.markdown('<p class="sidebar-title">цэс</p>', unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None,
        options=["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил"],
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        default_index=0,
        styles={
            "container": {"background-color": "#0b4ab1"},
            "nav-link": {"color": "white", "font-size": "14px", "text-align": "left", "font-family": "sans-serif"},
            "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)"},
        }
    )
    st.session_state.selected_menu = selected

# 4. НҮҮР ХУУДАС
if st.session_state.selected_menu == "Нүүр хуудас":
    col1, col2 = st.columns([1, 1.2])
    with col1:
        if os.path.exists("logo.gif"): st.image("logo.gif")
    with col2:
        st.markdown('<h1 style="color: #0b4ab1;">Математикийн багшийн туслах</h1>', unsafe_allow_html=True)
        st.write("Сонирхолтой цахим хичээл, баялаг бодлогын сангаар дамжуулан математик сэтгэлгээгээ хөгжүүлээрэй.")

    st.write("---")
    c1, c2, c3 = st.columns(3)
    if c1.button("📺\n\nЦахим контент"): st.session_state.selected_menu = "Цахим контент"; st.rerun()
    if c2.button("📚\n\nДаалгаврын сан"): st.session_state.selected_menu = "Даалгаврын сан"; st.rerun()
    if c3.button("📝\n\nСорил"): st.session_state.selected_menu = "Сорил"; st.rerun()

# 5. ДААЛГАВРЫН САН (24 ФАЙЛ)
elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown("<h3 style='text-align:center; color:#0b4ab1;'>📚 Бодлогын сан</h3>", unsafe_allow_html=True)
    units = ["Тоон олонлог", "Харьцаа", "Алгебр", "Дараалал", "Дүрс", "Байршил", "Хэмжигдэхүүн", "Статистик"]
    col_u, col_l = st.columns(2)
    u_choice = col_u.selectbox("Сэдэв сонгох:", units)
    l_choice = col_l.radio("Түвшин:", ["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"], horizontal=True)
    
    u_idx = units.index(u_choice) + 1
    l_idx = {"Мэдлэг ойлголт": 1, "Чадвар": 2, "Хэрэглээ": 3}[l_choice]
    f_path = f"task_{u_idx}_{l_idx}.xlsx"
    
    if os.path.exists(f_path):
        df = pd.read_excel(f_path)
        for i, row in df.iterrows():
            with st.expander(f"Бодлого {i+1}"):
                st.markdown(smart_math_render(row['Асуулт']))
                st.radio("Хариу:", ["A", "B", "C", "D"], key=f"t_{u_idx}_{i}", horizontal=True)
    else: st.warning(f"'{f_path}' файл олдсонгүй.")

# 6. СОРИЛ (32 ФАЙЛ - ЗУРАГ ДЭЭРХ ЗАГВАР ХЭВЭЭРЭЭ)
elif st.session_state.selected_menu == "Сорил":
    if not st.session_state.quiz_active:
        st.markdown("<h3 style='text-align: center; color: #0b4ab1;'>📝 Онлайн сорил, шалгалт</h3>", unsafe_allow_html=True)
        st.markdown('<div class="quiz-header"><div style="width:5%">#</div><div style="width:65%">Сорилын нэр</div><div style="width:30%; text-align:center;">Хувилбарууд</div></div>', unsafe_allow_html=True)
        
        quiz_names = ["Тоон олонлог, зэрэг, язгуур", "Харьцаа, пропорц, процент", "Алгебрын илэрхийлэл", "Дараалал, функц", "Өнцөг, дүрс", "Байршил, хөдөлгөөн", "Хэмжигдэхүүн", "Магадлал, статистик"]
        
        for i, name in enumerate(quiz_names):
            col_n, col_v = st.columns([0.7, 0.3])
            col_n.write(f"**{i+1}.** {name}")
            with col_v:
                v_cols = st.columns(4)
                for j, v in enumerate(["A", "B", "C", "D"]):
                    if v_cols[j].button(v, key=f"q_{i}_{v}"):
                        st.session_state.quiz_file = f"quiz_{i+1}_{v}.xlsx"
                        st.session_state.quiz_active = True
                        st.session_state.start_time = time.time()
                        st.rerun()
            st.divider()
    else:
        # Сорил эхэлсэн үе
        rem = max(0, 2400 - int(time.time() - st.session_state.start_time))
        st.error(f"⏳ Үлдсэн хугацаа: {rem//60:02d}:{rem%60:02d}")
        if st.button("⬅️ Буцах"): st.session_state.quiz_active = False; st.rerun()

        if os.path.exists(st.session_state.quiz_file):
            df_q = pd.read_excel(st.session_state.quiz_file)
            for idx, row in df_q.iterrows():
                st.write(f"**{idx+1}.**", smart_math_render(row['Асуулт']))
                st.radio("Сонгох:", ["A", "B", "C", "D"], key=f"qz_{idx}", horizontal=True)
            if st.button("Дуусгах"):
                st.balloons(); st.session_state.quiz_active = False; st.rerun()
        else: st.error("Сорилын файл олдсонгүй.")

# БУСАД
else:
    st.write(f"### {st.session_state.selected_menu}")
    st.info("Энэ хэсэг удахгүй нэмэгдэнэ.")
