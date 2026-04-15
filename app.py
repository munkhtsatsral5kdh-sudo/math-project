import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import time

# 1. Төлөв хадгалах
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Нүүр хуудас"
if 'test_started' not in st.session_state:
    st.session_state.test_started = False

st.set_page_config(page_title="Математикийн багшийн туслах", layout="wide")

# 2. ДИЗАЙН (Өмнөх цэнхэр загвар)
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #004aad !important; }
    .sidebar-title { color: #ffffff; text-align: center; font-size: 35px; font-weight: bold; padding: 20px 0; border-bottom: 1px solid rgba(255,255,255,0.2); }
    .main-header { color: #004aad; font-size: 45px; font-weight: 900; text-align: center; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил төлөвшил МХБ"]
    selected = option_menu(
        menu_title=None, 
        options=options,
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        default_index=options.index(st.session_state.selected_menu),
        key='menu_widget'
    )
    st.session_state.selected_menu = selected

# 4. ХУУДАСНУУД
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
                st.session_state.show_options = True
            
            if st.session_state.get('show_options'):
                st.write("---")
                cols = st.columns(4)
                if cols[0].button("🟢 Сорил эхлэх"):
                    st.session_state.test_started = True
                    st.session_state.start_time = time.time()
                    st.rerun()
                cols[1].button("🔵 Дүн харах")
                cols[2].button("⚪ Алдаа шалгах")
                cols[3].button("🔴 Бодолт")

    else:
        # СОРИЛЫН ЯВЦ (ЯГ 40 МИНУТ)
        remaining = (40 * 60) - (time.time() - st.session_state.start_time)
        if remaining <= 0:
            st.error("⏰ Хугацаа дууслаа!")
            st.session_state.test_started = False
        else:
            mins, secs = divmod(int(remaining), 60)
            st.sidebar.metric("⏱️ Үлдсэн хугацаа", f"{mins:02d}:{secs:02d}")
            st.subheader("Үнэлгээний нэгж 5: Өнцөг, дүрс, байгуулалт (А хувилбар)")

            # БҮХ 15 АСУУЛТ (PDF-ийн дагуу)
            q1 = st.radio("1. Тэгш өнцөгт ABC гурвалжны ∠C=90° бол sinA харьцааг нэрлэнэ үү?", ["AC/AB", "BC/AB", "BC/AC", "AC/BC"], key="q1")
            q2 = st.radio("2. Гурвалжны медианууд огтлолцлын цэгээрээ оройгоос тоолбол ямар харьцаагаар хуваагддаг вэ?", ["1:1", "1:2", "2:1", "3:1"], key="q2")
            q3 = st.radio("3. Гурвалжны дундаж шугам нь суурьтайгаа параллель бөгөөд урт нь суурийнхаа ... -тай тэнцүү байдаг.", ["Хагастай", "Гуравны нэгтэй", "Хоёр дахин их", "Тэнцүү"], key="q3")
            q4 = st.radio("4. Тэгш өнцөгт гурвалжны катетууд 9 см ба 12 см бол гипотенузыг ол?", ["13 см", "15 см", "17 см", "20 см"], key="q4")
            q5 = st.radio("5. Тойргийн төвөөс хөвчид буусан перпендикуляр нь уг хөвчийг хэрхэн хуваадаг вэ?", ["2:1 харьцаагаар", "Хагаслан хуваана", "Гурав хуваана", "Хуваахгүй"], key="q5")
            q6 = st.radio("6. cos 60°-ын утгыг ол.", ["1/2", "√2/2", "√3/2", "1"], key="q6")
            q7 = st.radio("7. sin 30°-ын утгыг ол.", ["1/2", "√2/2", "√3/2", "1"], key="q7")
            q8 = st.radio("8. Пифагорын теоремоор аль нь зөв бэ? (a, b - катет, c - гипотенуз)", ["a²+b²=c²", "a²+c²=b²", "b²+c²=a²", "a+b=c"], key="q8")
            q9 = st.radio("9. Дугуйн талбайг олох томъёо аль нь вэ?", ["2πr", "πr²", "πd", "2πr²"], key="q9")
            q10 = st.radio("10. Гурвалжны дотоод өнцгүүдийн нийлбэр хэд вэ?", ["90°", "180°", "270°", "360°"], key="q10")
            q11 = st.radio("11. Адил хажуут гурвалжны оройн өнцөг 40° бол суурийн өнцгийг ол.", ["40°", "70°", "80°", "140°"], key="q11")
            q12 = st.radio("12. Тойргийн уртыг олох томъёо аль нь вэ?", ["πr²", "2πr", "πd²", "2πd"], key="q12")
            
            st.write("---")
            st.write("### Нөхөх даалгавар")
            n13 = st.text_input("13. Тойргийн радиус 15 см, төвөөс хөвч хүртэл 9 см бол хөвчний урт хэд вэ?")
            n14 = st.text_input("14. Тэгш өнцөгт гурвалжны нэг өнцөг 30° бол түүний эсрэг орших катет гипотенузын ...-тэй тэнцүү.")
            n15 = st.text_input("15. sin²α + cos²α = ?")

            if st.button("Сорил дуусгах"):
                st.session_state.test_started = False
                st.success("Сорил дууслаа. Баярлалаа!")
                st.rerun()

else:
    st.markdown(f'<p class="main-header">{st.session_state.selected_menu}</p>', unsafe_allow_html=True)
    st.write("Энэ хэсэг удахгүй нэмэгдэнэ.")
