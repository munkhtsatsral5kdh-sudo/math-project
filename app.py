import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import time

# Төлөв хадгалах
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Нүүр хуудас"
if 'test_started' not in st.session_state:
    st.session_state.test_started = False

st.set_page_config(page_title="Математикийн багшийн туслах", layout="wide")

# ДИЗАЙН
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #004aad !important; }
    .sidebar-title { color: #ffffff; text-align: center; font-size: 35px; font-weight: bold; padding: 20px 0; }
    .main-header { color: #004aad; font-size: 45px; font-weight: 900; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None, 
        options=["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил төлөвшил МХБ"],
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        default_index=["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил төлөвшил МХБ"].index(st.session_state.selected_menu),
        key='menu_widget'
    )
    st.session_state.selected_menu = selected

# ХУУДАСНУУД
if st.session_state.selected_menu == "Нүүр хуудас":
    col1, col2 = st.columns([1, 1.5])
    with col1:
        if os.path.exists("logo.gif"):
            with open("logo.gif", "rb") as f:
                st.markdown(f'<img src="data:image/gif;base64,{base64.b64encode(f.read()).decode()}" width="100%">', unsafe_allow_html=True)
    with col2:
        st.markdown('<p class="main-header" style="text-align:left;">Бидний зорилго</p>', unsafe_allow_html=True)
        st.write("Математикийн ертөнцөөр хамтдаа аялж, мэдлэг чадвараа ахиулцгаая!")

elif st.session_state.selected_menu == "Сорил":
    if not st.session_state.test_started:
        st.markdown('<p class="main-header">📝 Онлайн сорилтын систем</p>', unsafe_allow_html=True)
        with st.expander("🔹 Үнэлгээний нэгж 5. Өнцөг, дүрс, байгуулалт"):
            c1, c2, c3, c4 = st.columns(4)
            if c1.button("A хувилбар"):
                st.session_state.active_test = "Нэгж 5 - А хувилбар"
                st.session_state.show_options = True
            
            if st.session_state.get('show_options'):
                st.write("---")
                cols = st.columns(4)
                if cols[0].button("🟢 Сорил эхлэх"):
                    st.session_state.test_started = True
                    st.session_state.start_time = time.time()
                    st.rerun()

    else:
        # СОРИЛЫН ЯВЦ (40 МИНУТ)
        remaining = (40 * 60) - (time.time() - st.session_state.start_time)
        if remaining <= 0:
            st.error("⏰ Хугацаа дууслаа!")
            st.session_state.test_started = False
        else:
            mins, secs = divmod(int(remaining), 60)
            st.sidebar.metric("⏱️ Үлдсэн хугацаа", f"{mins:02d}:{secs:02d}")
            st.subheader("Үнэлгээний нэгж 5: Өнцөг, дүрс, байгуулалт")

            # PDF-ээс авсан асуултууд
            q1 = st.radio("1. Тэгш өнцөгт ABC гурвалжны ∠C=90° бол sinA харьцааг нэрлэнэ үү?", ["AC/AB", "BC/AB", "BC/AC", "AC/BC"]) # [cite: 3, 4, 9]
            q2 = st.radio("2. Гурвалжны медианууд огтлолцлын цэгээрээ оройгоос тоолбол ямар харьцаагаар хуваагддаг вэ?", ["1:1", "1:2", "2:1", "3:1"]) # [cite: 4, 5, 10, 13]
            q4 = st.radio("4. Тэгш өнцөгт гурвалжны катетууд 9 см ба 12 см бол гипотенузыг ол?", ["13 см", "15 см", "17 см", "20 см"]) # [cite: 21, 23]
            q5 = st.radio("5. Тойргийн төвөөс хөвчид буусан перпендикуляр нь уг хөвчийг хэрхэн хуваадаг вэ?", ["2:1 харьцаагаар", "Хагаслан хуваана", "Гурав хуваана", "Хуваахгүй"]) # [cite: 25, 27]
            
            st.write("---")
            st.write("### Нөхөх даалгавар")
            st.write("13. Тойргийн радиус 15 см, төвөөс хөвч хүртэл 9 см бол:") # [cite: 75, 76]
            ans13 = st.text_input("Хөвчийг хагаслан хуваах хэрчмийн урт (ab):") # [cite: 77]

            if st.button("Сорил дуусгах"):
                st.session_state.test_started = False
                st.success("Амжилттай дууслаа!")
                st.rerun()
