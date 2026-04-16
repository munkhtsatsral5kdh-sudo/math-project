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

# 2. ДИЗАЙН (Шинэчлэгдсэн: Товчлуурнууд цэгцтэй болсон)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    [data-testid="stSidebar"] { background-color: #0b4ab1 !important; min-width: 260px !important; }
    .sidebar-title { color: white; text-align: center; font-size: 40px; font-weight: bold; padding: 10px 0; }
    /* Нүүр хуудасны том товч */
    .home-btn button { height: 180px !important; border-radius: 20px !important; }
    /* Сорилын жижиг товч */
    div.stButton > button { border-radius: 8px !important; height: auto !important; padding: 5px 10px !important; }
    .table-header { background-color: #343a40; color: white; padding: 10px; border-radius: 5px; display: flex; font-weight: bold; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Цэс) - Алдааг зассан хувилбар
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Нүүр хуудас"

with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    menu_options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил"]
    
    # default_index-ийг илүү найдвартай тодорхойлох
    try:
        current_idx = menu_options.index(st.session_state.selected_menu)
    except:
        current_idx = 0

    selected = option_menu(
        menu_title=None, options=menu_options,
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        default_index=current_idx,
        styles={"container": {"background-color": "#0b4ab1", "padding": "0"}, 
                "nav-link": {"color": "white", "font-size": "16px", "text-align": "left"},
                "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)"}}
    )
    if selected != st.session_state.selected_menu:
        st.session_state.selected_menu = selected
        st.rerun()

# 4. НҮҮР ХУУДАС
if st.session_state.selected_menu == "Нүүр хуудас":
    st.markdown("### 👋 Сайн байна уу?")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="home-btn">', unsafe_allow_html=True)
        if st.button("📺\n\nЦахим контент", key="h_btn1", use_container_width=True): 
            st.session_state.selected_menu = "Цахим контент"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="home-btn">', unsafe_allow_html=True)
        if st.button("📚\n\nДаалгаврын сан", key="h_btn2", use_container_width=True): 
            st.session_state.selected_menu = "Даалгаврын сан"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="home-btn">', unsafe_allow_html=True)
        if st.button("📝\n\nСорил", key="h_btn3", use_container_width=True): 
            st.session_state.selected_menu = "Сорил"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# 7. СОРИЛ (Шинэчлэгдсэн: Секундээр гүйдэг цаг + 4 хувилбар)
elif st.session_state.selected_menu == "Сорил":
    st.markdown("<h2 style='text-align: center; color: #0b4ab1;'>📝 Онлайн сорил, шалгалт</h2>", unsafe_allow_html=True)
    
    units = ["Тоон олонлог, зэрэг, язгуур", "Харьцаа, пропорц, процент", "Алгебрын илэрхийлэл, тэгшитгэл", "Дараалал, функц", "Өнцөг, дүрс, байгуулалт", "Байршил, хөдөлгөөн", "Хэмжигдэхүүн", "Магадлал, статистик"]

    if 'quiz_active' not in st.session_state: st.session_state.quiz_active = False

    if not st.session_state.quiz_active:
        st.markdown("<div class='table-header'><div style='width:5%;'>#</div><div style='width:65%;'>Сорилын нэр (IX анги)</div><div style='width:30%; text-align:center;'>Хувилбар</div></div>", unsafe_allow_html=True)
        for i, name in enumerate(units):
            c_name, c_vars = st.columns([0.7, 0.3])
            c_name.write(f"**{i+1}.** {name}")
            with c_vars:
                v_cols = st.columns(4)
                for j, v_letter in enumerate(["A", "B", "C", "D"]):
                    if v_cols[j].button(v_letter, key=f"v{v_letter}_{i}"):
                        st.session_state.quiz_active = True
                        st.session_state.u_name = name
                        st.session_state.var = v_letter
                        st.session_state.start_time = time.time()
                        st.rerun()
            st.markdown("<hr style='margin: 2px;'>", unsafe_allow_html=True)
    else:
        # --- БОДИТ ЦАГ ХЭМЖИГЧ ---
        elapsed = int(time.time() - st.session_state.start_time)
        remaining = max(0, 2400 - elapsed) # 40 минут
        mins, secs = divmod(remaining, 60)
        
        c_head, c_time = st.columns([5, 1])
        if c_head.button("⬅️ Гарах"): st.session_state.quiz_active = False; st.rerun()
        c_time.error(f"⏳ {mins:02d}:{secs:02d}")

        st.subheader(f"📍 {st.session_state.u_name} | Хувилбар {st.session_state.var}")
        st.info("Сорилын бодлогууд энд харагдана. Excel-ээс өгөгдөл унших хэсгийг энд нэмж болно.")
        
        if remaining > 0:
            time.sleep(1) # 1 секунд хүлээгээд шинэчилнэ
            st.rerun()
