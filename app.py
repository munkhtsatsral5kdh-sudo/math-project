import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64

# 1. Вэбсайтын үндсэн тохиргоо
st.set_page_config(
    page_title="Математикийн цахим хичээл", 
    page_icon="📐", 
    layout="wide"
)

# 2. ДИЗАЙН (CSS) - Сайтыг илүү үзэмжтэй болгох хэсэг
st.markdown("""
    <style>
    /* Үндсэн фонт болон өнгө */
    .stApp { background-color: #f4f7f6; }
    
    /* Sidebar-ийн загвар */
    [data-testid="stSidebar"] { 
        background-color: #004aad !important; 
        min-width: 280px !important; 
    }
    .sidebar-title { 
        color: #ffffff !important; 
        text-align: center; 
        font-size: 28px !important; 
        font-weight: bold; 
        padding: 20px 0; 
        border-bottom: 1px solid rgba(255,255,255,0.2);
    }

    /* Гарчигны загвар */
    .main-header { 
        color: #004aad; 
        font-size: 45px !important; 
        font-weight: 800; 
        text-align: center;
        margin-bottom: 30px;
    }

    /* Контент картын загвар */
    .content-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        border-top: 8px solid #004aad;
        transition: transform 0.3s;
    }
    .content-card:hover {
        transform: translateY(-5px);
    }
    
    /* Зорилго хэсэг */
    .goal-box {
        background: white;
        padding: 40px;
        border-radius: 20px;
        border-left: 15px solid #ffca28;
        font-size: 22px !important;
        line-height: 1.8;
        color: #2c3e50;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ХАЖУУГИЙН ЦЭС (SIDEBAR)
with st.sidebar:
    st.markdown('<p class="sidebar-title">МАТЕМАТИК IX</p>', unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None, 
        options=["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил"],
        icons=['house-fill', 'play-circle-fill', 'file-earmark-text-fill', 'check2-square'],
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "transparent"},
            "icon": {"color": "#ffca28", "font-size": "20px"}, 
            "nav-link": {"font-size": "18px", "color": "white", "text-align": "left", "margin":"5px", "font-weight": "normal"},
            "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)", "font-weight": "bold", "border-radius": "10px"},
        }
    )

# 4. ХУУДАСНУУДЫН АГУУЛГА
if selected == "Нүүр хуудас":
    st.markdown('<p class="main-header">Математикийн ертөнцөд тавтай морил</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.2], gap="large")
    
    with col1:
        # Лого харуулах хэсэг
        logo_path = "logo.gif"
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                data = f.read()
                data_url = base64.b64encode(data).decode("utf-8")
            st.markdown(f'<img src="data:image/gif;base64,{data_url}" width="100%" style="border-radius: 20px;">', unsafe_allow_html=True)
        else:
            st.info("Лого оруулах бол 'logo.gif' нэрээр GitHub-д хуулна уу.")

    with col2:
        st.markdown('<div class="goal-box"><b>Бидний зорилго:</b><br>Есдүгээр ангийн математикийн хичээлийг илүү сонирхолтой, ойлгомжтой байдлаар сурагчдад хүргэх, бие даан суралцах боломжийг бүрдүүлэхэд оршино. Та эндээс видео хичээл үзэж, даалгавар ажиллаж, өөрийгөө сорих боломжтой.</div>', unsafe_allow_html=True)

elif selected == "Цахим контент":
    st.markdown('<p class="main-header">📺 Цахим видео хичээлүүд</p>', unsafe_allow_html=True)
    
    # Хичээлүүдийг 2 баганаар харуулах
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("🔹 1. Рационал тоо")
        # ЭНД ӨӨРИЙН YOUTUBE ЛИНКИЙГ ТАВИАРАЙ
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") 
        st.write("**Агуулга:** Рационал тоон олонлог, жиших, үйлдлүүд.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("🔹 3. Пропорц ба харьцаа")
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        st.write("**Агуулга:** Харьцааг ашиглан бодлого бодох аргачлал.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("🔹 2. Алгебрын илэрхийлэл")
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        st.write("**Агуулга:** Олон гишүүнтийг үржигдэхүүн болгон задлах.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("🔹 4. Тэгшитгэл ба тэнцэтгэл биш")
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        st.write("**Агуулга:** Шугаман тэгшитгэл болон систем тэгшитгэл.")
        st.markdown('</div>', unsafe_allow_html=True)

elif selected == "Даалгаврын сан":
    st.markdown('<p class="main-header">📚 Бие даан ажиллах даалгавар</p>', unsafe_allow_html=True)
    st.info("Хичээл бүрт тохирсон PDF даалгавруудыг эндээс татаж аваарай.")
    
    # Жишээ татах товч
    st.write("### 📄 1-р бүлэг: Рационал тоо")
    st.button("Даалгавар татах (PDF)")

elif selected == "Сорил":
    st.markdown('<p class="main-header">📝 Өөрийгөө сориорой</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.write("### Асуулт 1")
    answer1 = st.radio("(-2) * (-3) + 4 үйлдлийн хариу хэд вэ?", [1, 10, -2, 6])
    
    if st.button("Хариуг шалгах"):
        if answer1 == 10:
            st.success("Зөв байна! Мундаг байна. ✨")
        else:
            st.error("Буруу байна, дахин бодоод үзээрэй. 🧐")
    st.markdown('</div>', unsafe_allow_html=True)
