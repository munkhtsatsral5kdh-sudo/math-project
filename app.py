import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import time

# 1. Сонгогдсон төлөвүүдийг санах (Гацалтаас сэргийлнэ)
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Нүүр хуудас"
if 'test_started' not in st.session_state:
    st.session_state.test_started = False

st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# 2. ДИЗАЙН (Өөрчлөгдөөгүй, таны хүссэн цэнхэр загвар)
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #004aad !important; min-width: 300px !important; }
    .sidebar-title { color: #ffffff !important; text-align: center; font-size: 40px !important; font-weight: bold; padding: 20px 0; border-bottom: 2px solid rgba(255,255,255,0.3); margin-bottom: 20px; }
    .main-header { color: #004aad !important; font-size: 50px !important; font-weight: 900; text-align: center; margin-bottom: 20px; }
    .goal-text { font-size: 22px !important; color: #333; line-height: 1.6; background: white; padding: 30px; border-left: 15px solid #004aad; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .custom-card { background: white; border-radius: 25px; padding: 30px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 1px solid #eee; height: 250px; }
    .card-title { color: #004aad; font-size: 22px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил төлөвшил МХБ"]
    current_index = options.index(st.session_state.selected_menu)
    
    selected = option_menu(
        menu_title=None, 
        options=options,
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        default_index=current_index,
        key='menu_widget',
        styles={"container": {"background-color": "#004aad"}, "nav-link": {"color": "white", "font-weight": "bold"}, "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)"}}
    )
    st.session_state.selected_menu = selected

# 4. ХУУДАСНУУД
if st.session_state.selected_menu == "Нүүр хуудас":
    col1, col2 = st.columns([1, 1.5], gap="large")
    with col1:
        if os.path.exists("logo.gif"):
            with open("logo.gif", "rb") as f:
                data = f.read()
                st.markdown(f'<img src="data:image/gif;base64,{base64.b64encode(data).decode()}" width="100%">', unsafe_allow_html=True)
    with col2:
        st.markdown('<p class="main-header" style="text-align:left;">Бидний зорилго</p>', unsafe_allow_html=True)
        st.markdown('<div class="goal-text">Математикийн ертөнцөөр хамтдаа аялж, сонирхолтой цахим хичээл...</div>', unsafe_allow_html=True)
    
    # "Эхлэх" товч Сорил руу үсэрнэ
    st.write("---")
    c1, c2, c3 = st.columns(3)
    with c3:
        st.markdown('<div class="custom-card"><div style="font-size:50px;">📝</div><div class="card-title">Сорил</div></div>', unsafe_allow_html=True)
        if st.button("Эхлэх", key="jump_to_test"):
            st.session_state.selected_menu = "Сорил"
            st.rerun()

elif st.session_state.selected_menu == "Сорил":
    st.markdown('<p class="main-header">📝 Онлайн сорилтын систем</p>', unsafe_allow_html=True)
    
    if not st.session_state.test_started:
        # 8 нэгж харуулах
        units = [f"Үнэлгээний нэгж {i}" for i in range(1, 9)]
        for i, unit in enumerate(units, 1):
            with st.expander(f"🔹 {unit}"):
                cols = st.columns(4)
                for j, var in enumerate(['A', 'B', 'C', 'D']):
                    if cols[j].button(f"{var} хувилбар", key=f"v_{i}_{var}"):
                        st.session_state.active_unit = f"{unit} - {var} хувилбар"
                        st.session_state.show_controls = True
                
                if st.session_state.get('show_controls') and unit in st.session_state.active_unit:
                    st.write("---")
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        if st.button("🟢 Сорил эхлэх", key=f"start_{i}"):
                            st.session_state.test_started = True
                            st.session_state.start_time = time.time()
                            st.rerun()
                    with c2: st.button("🔵 Дүн харах", key=f"res_{i}")
                    with c3: st.button("⚪ Алдаа шалгах", key=f"chk_{i}")
                    with c4: st.button("🔴 Бодолт", key=f"sol_{i}")

    else:
        # СОРИЛ ЯВЖ БАЙХ ҮЕ (40 МИНУТ)
        time_limit = 40 * 60 # 40 минут
        elapsed = time.time() - st.session_state.start_time
        remaining = time_limit - elapsed

        if remaining <= 0:
            st.error("⏰ Хугацаа дууслаа!")
            st.session_state.test_started = False
        else:
            mins, secs = divmod(int(remaining), 60)
            st.sidebar.metric("⏱️ Үлдсэн хугацаа", f"{mins:02d}:{secs:02d}")
            
            st.subheader(st.session_state.active_unit)
            st.write("1. Тэгш өнцөгт $\triangle ABC$-ийн $\angle C=90^{\circ}$ бол $\sin A$ харьцааг нэрлэнэ үү.")
            st.radio("Хариулт:", ["A. AC/AB", "B. BC/AB", "C. BC/AC", "D. AC/BC"])
            
            if st.button("Сорил дуусгах"):
                st.session_state.test_started = False
                st.rerun()
