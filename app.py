import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import pandas as pd
import time

# 1. Сайтын ерөнхий тохиргоо
st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

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

# 2. ДИЗАЙН (Товчлууруудыг яг ижил өндөр, урттай болгох CSS)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    [data-testid="stSidebar"] { background-color: #0b4ab1 !important; min-width: 260px !important; }
    .sidebar-title { color: white; text-align: center; font-size: 45px; font-weight: bold; padding: 20px 0; }
    .goal-box { background: white; padding: 25px; border-radius: 20px; border: 1px solid #f0f2f6; border-left: 10px solid #0b4ab1; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .main-header { color: #0b4ab1; font-size: 45px; font-weight: 800; margin-bottom: 5px; line-height: 0.95 !important; }
    
    /* НҮҮР ХУУДАСНЫ 3 ТОВЧЛУУРЫГ ЯГ ИЖИЛ БОЛГОХ */
    .home-btns div.stButton > button {
        width: 100% !important;
        aspect-ratio: 1 / 0.8 !important; /* Урт, өндрийн харьцааг ижил болгоно */
        height: 220px !important; 
        border-radius: 25px !important;
        background: #fdfdfd !important;
        border: 1px solid #f0f0f0 !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }
    .home-btns div.stButton > button p { font-size: 22px !important; font-weight: bold !important; color: #0b4ab1 !important; }

    /* ШАЛГАХ ТОВЧ (Жижиг хэвээр нь үлдээх) */
    .stForm div.stButton > button {
        width: 130px !important;
        height: 45px !important;
        border-radius: 10px !important;
    }
    
    .math-card { background: white; padding: 25px; border-radius: 15px; border: 1px solid #e0e0e0; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Цэс)
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Нүүр хуудас"

with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    menu_options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил"]
    selected = option_menu(
        menu_title=None, options=menu_options,
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        default_index=0,
        styles={"nav-link": {"color": "white"}, "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)"}}
    )
    st.session_state.selected_menu = selected

# 4. НҮҮР ХУУДАС
if st.session_state.selected_menu == "Нүүр хуудас":
    col1, col2 = st.columns([1, 1.2], gap="large")
    with col1:
        if os.path.exists("logo.gif"):
            with open("logo.gif", "rb") as f: data_url = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(f'<img src="data:image/gif;base64,{data_url}" style="width: 100%; border-radius: 20px;">', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="goal-box"><div class="main-header">Математикийн ертөнцөд тавтай морил!</div><div style="font-size: 19px; color: #444; text-align: justify;">Сонирхолтой цахим хичээл, баялаг бодлогын сангаар дамжуулан математик сэтгэлгээгээ хөгжүүлж, хамтдаа хөгжицгөөе!</div></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="home-btns">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1: 
        if st.button("📺\n\nЦахим контент", key="h1"): st.session_state.selected_menu = "Цахим контент"; st.rerun()
    with c2: 
        if st.button("📚\n\nДаалгаврын сан", key="h2"): st.session_state.selected_menu = "Даалгаврын сан"; st.rerun()
    with c3: 
        if st.button("📝\n\nСорил", key="h3"): st.session_state.selected_menu = "Сорил"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 5. ДААЛГАВРЫН САН (Зураг харуулдаг болгов)
elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown("<h2 style='text-align: center; color: #0b4ab1;'>📚 Бодлогын сан</h2>", unsafe_allow_html=True)
    units = ["Тоон олонлог...", "Харьцаа...", "Алгебр...", "Дараалал...", "Өнцөг...", "Байршил...", "Хэмжигдэхүүн", "Статистик"]
    
    sc1, sc2 = st.columns([0.6, 0.4])
    u_choice = sc1.selectbox("Сэдэв сонгох:", units)
    l_choice = sc2.radio("Түвшин:", ["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"], horizontal=True)

    # Алдааг засахын тулд толь бичгийг салгаж бичив
    u_idx = units.index(u_choice) + 1
    levels_map = {"Мэдлэг ойлголт": 1, "Чадвар": 2, "Хэрэглээ": 3}
    l_idx = levels_map[l_choice]
    f_path = f"task_{u_idx}_{l_idx}.xlsx"

    if os.path.exists(f_path):
        df = pd.read_excel(f_path)
        for idx, row in df.iterrows():
            st.markdown('<div class="math-card">', unsafe_allow_html=True)
            st.markdown(f"#### 📝 Бодлого {idx+1}")
            st.markdown(smart_math_render(row['Асуулт']))
            
            # Зураг харуулах хэсэг (Зөвхөн байвал)
            if 'Зураг' in row and pd.notna(row['Зураг']):
                img_path = os.path.join("images", str(row['Зураг']))
                if os.path.exists(img_path): st.image(img_path, width=400)

            with st.form(key=f"form_{u_idx}_{l_idx}_{idx}"):
                ans = st.radio("Хариу сонгох:", ["A", "B", "C", "D"], key=f"ans_{idx}", horizontal=True)
                if st.form_submit_button("Шалгах"):
                    correct = str(row['Хариу']).strip().upper()
                    if ans == correct: st.success("Зөв! ✅")
                    else: st.error(f"Буруу. Зөв хариу: {correct}")
            st.markdown('</div>', unsafe_allow_html=True)
    else: st.warning(f"⚠️ {f_path} файл олдсонгүй.")

# 6. СОРИЛ (Таны анхны кодоор сэргээв)
elif st.session_state.selected_menu == "Сорил":
    if 'quiz_active' not in st.session_state: st.session_state.quiz_active = False
    
    if not st.session_state.quiz_active:
        st.markdown("<h3 style='text-align: center; color: #0b4ab1;'>📝 Онлайн сорил</h3>", unsafe_allow_html=True)
        quiz_units = ["Тоон олонлог...", "Харьцаа...", "Алгебр...", "Дараалал...", "Өнцөг...", "Байршил...", "Хэмжигдэхүүн", "Статистик"]
        for i, name in enumerate(quiz_units):
            c_n, c_v = st.columns([0.7, 0.3])
            c_n.markdown(f"<div style='padding:12px 0; border-bottom:1px solid #eee;'>{i+1}. {name}</div>", unsafe_allow_html=True)
            v_cols = c_v.columns(4)
            for j, v in enumerate(["A", "B", "C", "D"]):
                if v_cols[j].button(v, key=f"q_{i}_{v}"):
                    st.session_state.quiz_file = f"quiz_{i+1}_{v}.xlsx"
                    st.session_state.quiz_active = True
                    st.session_state.start_time = time.time()
                    st.rerun()
    else:
        # Сорил өгөх хэсэг
        remaining = max(0, 2400 - int(time.time() - st.session_state.start_time))
        if st.button("⬅️ Гарах"): st.session_state.quiz_active = False; st.rerun()
        
        mins, secs = divmod(remaining, 60)
        st.error(f"⏳ Үлдсэн хугацаа: {mins:02d}:{secs:02d}")

        if os.path.exists(st.session_state.quiz_file):
            df_q = pd.read_excel(st.session_state.quiz_file)
            with st.form("quiz_form"):
                for idx, row in df_q.iterrows():
                    st.markdown(f"**Бодлого {idx+1}:**")
                    st.markdown(smart_math_render(row['Асуулт']))
                    if 'Зураг' in row and pd.notna(row['Зураг']):
                        img_path = os.path.join("images", str(row['Зураг']))
                        if os.path.exists(img_path): st.image(img_path, width=400)
                    st.radio("Хариу:", ["A", "B", "C", "D"], key=f"quiz_ans_{idx}", horizontal=True)
                    st.divider()
                if st.form_submit_button("🏁 Дуусгах"):
                    st.success("Сорил дууслаа!"); st.session_state.quiz_active = False; st.rerun()
        if remaining > 0: time.sleep(1); st.rerun()

# Бусад хэсэг
elif st.session_state.selected_menu == "Цахим контент":
    st.video("https://www.youtube.com/watch?v=your_video_id")
