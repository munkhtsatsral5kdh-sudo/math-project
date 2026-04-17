import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import pandas as pd
import time

# 1. Сайтын ерөнхий тохиргоо
st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# --- УХААЛАГ МАТЕМАТИК ТАНИГЧ ---
def smart_math_render(text):
    if not isinstance(text, str): return str(text)
    for label in ['A.', 'B.', 'C.', 'D.']:
        if label in text:
            text = text.replace(label, f'\n\n**{label}**')
    if ('\\' in text or '^' in text or '/' in text) and '$' not in text:
        clean_text = text.replace('\\displaystyle', '').strip()
        text = f"$\\displaystyle {clean_text}$"
    return text

# --- ДИЗАЙН (Товчлуурууд ижил хэмжээтэй) ---
st.markdown("""
    <style>
    .stApp { background-color: white; }
    [data-testid="stSidebar"] { background-color: #0b4ab1 !important; min-width: 260px !important; }
    .sidebar-title { color: white; text-align: center; font-size: 45px; font-weight: bold; padding: 20px 0; }
    
    /* Нүүр хуудасны 3 товчлуур (Ижил хэмжээ + Гоо зүй) */
    .home-btns div.stButton > button {
        width: 100% !important;
        height: 200px !important; /* Тогтмол өндөр */
        border-radius: 25px !important;
        background: #fdfdfd !important;
        border: 1px solid #f0f0f0 !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s ease-in-out !important;
    }
    .home-btns div.stButton > button:hover { transform: translateY(-5px); border-color: #0b4ab1 !important; }
    .home-btns div.stButton > button p { font-size: 22px !important; font-weight: bold !important; color: #0b4ab1 !important; }

    /* Шалгах товчлуурын тусдаа дизайн */
    .check-btn div.stButton > button {
        width: 120px !important;
        height: 45px !important;
        font-size: 16px !important;
        border-radius: 10px !important;
        margin: 10px 0;
    }
    
    .math-card { background: white; padding: 25px; border-radius: 15px; border: 1px solid #e0e0e0; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- ЦЭСНИЙ УДИРДЛАГА ---
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Нүүр хуудас"

with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    menu_options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил"]
    current_index = menu_options.index(st.session_state.selected_menu) if st.session_state.selected_menu in menu_options else 0
    selected = option_menu(
        menu_title=None, options=menu_options,
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        default_index=current_index,
        styles={"container": {"background-color": "#0b4ab1"}, "nav-link": {"color": "white"}, "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)"}}
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
        st.markdown('<div class="goal-box" style="padding:25px; border-radius:20px; border-left:10px solid #0b4ab1; box-shadow:0 10px 30px rgba(0,0,0,0.05);"><h1 style="color:#0b4ab1;">Математикийн ертөнцөд тавтай морил!</h1><p style="font-size:19px; color:#444;">Сонирхолтой цахим хичээл, баялаг бодлогын сангаар дамжуулан математик сэтгэлгээгээ хөгжүүлэхэд тань бид туслах болно.</p></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="home-btns">', unsafe_allow_html=True) # Дизайныг хэрэглэх класс
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1: 
        if st.button("📺\n\nЦахим контент", key="h1"): st.session_state.selected_menu = "Цахим контент"; st.rerun()
    with c2: 
        if st.button("📚\n\nДаалгаврын сан", key="h2"): st.session_state.selected_menu = "Даалгаврын сан"; st.rerun()
    with c3: 
        if st.button("📝\n\nСорил", key="h3"): st.session_state.selected_menu = "Сорил"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 5. ДААЛГАВРЫН САН (Алдаа засагдсан хувилбар)
elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown("<h2 style='text-align: center; color: #0b4ab1;'>📚 Бодлогын сан</h2>", unsafe_allow_html=True)
    units = ["Тоон олонлог, зэрэг, язгуур, тоог жиших, тоймлох", "Харьцаа, пропорц, процент", "Алгебрын илэрхийлэл, тэгшитгэл, тэнцэтгэл биш", "Дараалал, функц", "Өнцөг, дүрс, байгуулалт", "Байршил, хөдөлгөөн, хувиргалт", "Хэмжигдэхүүн", "Магадлал, статистик"]
    
    sc1, sc2 = st.columns([0.6, 0.4])
    u_choice = sc1.selectbox("Сэдэв сонгох:", units)
    l_choice = sc2.radio("Түвшин:", ["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"], horizontal=True)

    # Алдааг засахын тулд f-string-ээс толь бичгийг салгаж бичив
    u_idx = units.index(u_choice) + 1
    levels_dict = {"Мэдлэг ойлголт": 1, "Чадвар": 2, "Хэрэглээ": 3}
    l_idx = levels_dict[l_choice]
    f_path = f"task_{u_idx}_{l_idx}.xlsx"

    if os.path.exists(f_path):
        df = pd.read_excel(f_path)
        for idx, row in df.iterrows():
            st.markdown('<div class="math-card">', unsafe_allow_html=True)
            st.markdown(f"#### 📝 Бодлого {idx+1}")
            st.markdown(smart_math_render(row['Асуулт']))
            
            # Зураг харуулах (images/ хавтсанд зургаа хийгээрэй)
            if 'Зураг' in row and pd.notna(row['Зураг']):
                img_path = os.path.join("images", str(row['Зураг']))
                if os.path.exists(img_path): st.image(img_path, width=400)
            
            with st.form(key=f"form_{u_idx}_{l_idx}_{idx}"):
                ans = st.radio("Хариу:", ["A", "B", "C", "D"], key=f"ans_{idx}", horizontal=True)
                st.markdown('<div class="check-btn">', unsafe_allow_html=True)
                if st.form_submit_button("Шалгах"):
                    correct = str(row['Хариу']).strip().upper()
                    if ans == correct: st.success("Зөв! ✅")
                    else: st.error(f"Буруу. Зөв хариу: {correct}")
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else: st.warning(f"⚠️ {f_path} файл олдсонгүй.")

# Сорил болон бусад хэсэг таны анхны кодоор үргэлжилнэ...
elif st.session_state.selected_menu == "Сорил":
    st.write("Сорил хэсэг...")
elif st.session_state.selected_menu == "Цахим контент":
    st.video("https://www.youtube.com/watch?v=your_video_id")
