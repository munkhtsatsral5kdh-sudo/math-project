import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import pandas as pd
import time

# 1. Сайтын ерөнхий тохиргоо
st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# УХААЛАГ МАТЕМАТИК ТАНИГЧ (Үндсэн логик хэвээрээ)
def smart_math_render(text):
    if not isinstance(text, str): return str(text)
    # Сонголтуудыг салгах
    for label in ['A.', 'B.', 'C.', 'D.']:
        if label in text:
            text = text.replace(label, f'\n\n**{label}** ')
    
    # Томьёо таних
    if ('\\' in text or '^' in text or '/' in text) and '$' not in text:
        clean_text = text.replace('\\displaystyle', '').strip()
        text = f"$\\displaystyle {clean_text}$"
    return text

# Зураг харуулах туслах функц
def show_problem_content(row):
    # Текст харуулах
    st.markdown(smart_math_render(row['Асуулт']))
    # Зураг харуулах (Хэрэв 'Зураг' багана байгаа бөгөөд утгатай бол)
    if 'Зураг' in row and pd.notna(row['Зураг']):
        img_name = str(row['Зураг']).strip()
        img_path = os.path.join("images", img_name)
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=False, width=450)

# 2. ДИЗАЙН (Нүүр хуудасны 3 товчлуурыг ижил хэмжээтэй болгох)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    [data-testid="stSidebar"] { background-color: #0b4ab1 !important; min-width: 260px !important; }
    .sidebar-title { color: white; text-align: center; font-size: 40px; font-weight: bold; padding: 20px 0; }
    
    /* НҮҮР ХУУДАСНЫ ТОМ ТОВЧЛУУРУУД */
    .home-btns div.stButton > button {
        width: 100% !important;
        height: 200px !important;
        border-radius: 25px !important;
        background: #fdfdfd !important;
        border: 1px solid #f0f0f0 !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05) !important;
        transition: 0.3s;
    }
    .home-btns div.stButton > button:hover { transform: translateY(-5px); border-color: #0b4ab1 !important; }
    .home-btns div.stButton > button p { font-size: 22px !important; font-weight: bold !important; color: #0b4ab1 !important; }

    /* БОДЛОГЫН КАРТ */
    .math-card { 
        background: white; padding: 25px; border-radius: 15px; 
        border: 1px solid #e0e0e0; margin-bottom: 20px;
    }

    /* ШАЛГАХ ТОВЧ (Жижиг хэвээр үлдээх) */
    .check-btn div.stButton > button {
        width: 120px !important; height: 45px !important;
        border-radius: 10px !important; font-size: 16px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Цэс)
if 'selected_menu' not in st.session_state: st.session_state.selected_menu = "Нүүр хуудас"
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None, options=["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил"],
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        default_index=0, styles={"nav-link": {"color": "white"}, "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)"}}
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
        st.markdown('<div class="goal-box" style="background: white; padding: 25px; border-radius: 20px; border-left: 10px solid #0b4ab1; box-shadow: 0 10px 30px rgba(0,0,0,0.05);"><h1 style="color: #0b4ab1;">Математикийн ертөнцөд тавтай морил!</h1><p style="font-size: 19px; color: #444; text-align: justify;">Сонирхолтой цахим хичээл, баялаг бодлогын сангаар дамжуулан математик сэтгэлгээгээ хөгжүүлэхэд тань тусална.</p></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="home-btns">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1: 
        if st.button("📺\n\nЦахим контент"): st.session_state.selected_menu = "Цахим контент"; st.rerun()
    with c2: 
        if st.button("📚\n\nДаалгаврын сан"): st.session_state.selected_menu = "Даалгаврын сан"; st.rerun()
    with c3: 
        if st.button("📝\n\nСорил"): st.session_state.selected_menu = "Сорил"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 5. ДААЛГАВРЫН САН
elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown("<h2 style='text-align: center; color: #0b4ab1;'>📚 Бодлогын сан</h2>", unsafe_allow_html=True)
    units = ["Тоон олонлог, зэрэг, язгуур, тоог жиших, тоймлох", "Харьцаа, пропорц, процент", "Алгебрын илэрхийлэл, тэгшитгэл, тэнцэтгэл биш", "Дараалал, функц", "Өнцөг, дүрс, байгуулалт", "Байршил, хөдөлгөөн, хувиргалт", "Хэмжигдэхүүн", "Магадлал, статистик"]
    
    sc1, sc2 = st.columns([0.6, 0.4])
    u_choice = sc1.selectbox("Сэдэв сонгох:", units)
    l_choice = sc2.radio("Түвшин:", ["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"], horizontal=True)

    # АЛДАА ГАРСАН ХЭСГИЙГ ЗАСАВ:
    u_idx = units.index(u_choice) + 1
    level_map = {"Мэдлэг ойлголт": 1, "Чадвар": 2, "Хэрэглээ": 3}
    l_idx = level_map[l_choice]
    f_path = f"task_{u_idx}_{l_idx}.xlsx"

    if os.path.exists(f_path):
        df = pd.read_excel(f_path)
        for idx, row in df.iterrows():
            st.markdown('<div class="math-card">', unsafe_allow_html=True)
            st.markdown(f"#### 📝 Бодлого {idx+1}")
            show_problem_content(row) # Текст + Зураг харуулна
            
            with st.form(key=f"task_{u_idx}_{l_idx}_{idx}"):
                ans = st.radio("Хариу сонгох:", ["A", "B", "C", "D"], key=f"ans_{idx}", horizontal=True)
                st.markdown('<div class="check-btn">', unsafe_allow_html=True)
                if st.form_submit_button("Шалгах"):
                    correct = str(row['Хариу']).strip().upper()
                    if ans == correct: st.success("Зөв! ✅")
                    else: 
                        st.error(f"Буруу. Зөв хариу: {correct}")
                        if 'Бодолт' in row and pd.notna(row['Бодолт']):
                            with st.expander("Бодолт харах"): st.markdown(smart_math_render(row['Бодолт']))
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else: st.warning(f"⚠️ {f_path} файл олдсонгүй.")

# 6. СОРИЛ
elif st.session_state.selected_menu == "Сорил":
    if 'quiz_active' not in st.session_state: st.session_state.quiz_active = False
    
    if not st.session_state.quiz_active:
        st.markdown("<h3 style='text-align: center; color: #0b4ab1;'>📝 Онлайн сорил</h3>", unsafe_allow_html=True)
        # Сорилын хүснэгт (Таны өмнөх код хэвээрээ)
        quiz_units = ["Тоон олонлог...", "Харьцаа...", "Алгебр...", "Дараалал...", "Өнцөг...", "Байршил...", "Хэмжигдэхүүн", "Статистик"]
        for i, name in enumerate(quiz_units):
            c_n, c_v = st.columns([0.7, 0.3])
            c_n.write(f"{i+1}. {name}")
            v_cols = c_v.columns(4)
            for j, v in enumerate(["A", "B", "C", "D"]):
                if v_cols[j].button(v, key=f"qbtn_{i}_{v}"):
                    st.session_state.quiz_file = f"quiz_{i+1}_{v}.xlsx"
                    st.session_state.quiz_active = True
                    st.session_state.start_time = time.time()
                    st.rerun()
    else:
        # Сорил өгөх хэсэг
        remaining = max(0, 2400 - int(time.time() - st.session_state.start_time))
        if st.button("⬅️ Буцах"): st.session_state.quiz_active = False; st.rerun()
        
        if os.path.exists(st.session_state.quiz_file):
            df_q = pd.read_excel(st.session_state.quiz_file)
            with st.form("quiz_run"):
                for idx, row in df_q.iterrows():
                    st.write(f"**Бодлого {idx+1}:**")
                    show_problem_content(row) # Сорил дээр ч зураг харагдана
                    st.radio("Сонгох:", ["A", "B", "C", "D"], key=f"run_{idx}", horizontal=True)
                    st.divider()
                if st.form_submit_button("🏁 Дуусгах"):
                    st.success("Сорил дууслаа!"); st.session_state.quiz_active = False; st.rerun()
        
        if remaining > 0: time.sleep(1); st.rerun()

# Бусад хэсгүүд (Цахим контент гэх мэт) таны үндсэн кодоор үргэлжилнэ.
