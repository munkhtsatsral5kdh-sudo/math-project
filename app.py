import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64

# 1. Сайтын ерөнхий тохиргоо
st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# 2. ДИЗАЙН (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #004aad !important; min-width: 300px !important; }
    .sidebar-title { color: #ffffff !important; text-align: center; font-size: 40px !important; font-weight: bold; padding: 20px 0; border-bottom: 2px solid rgba(255,255,255,0.3); }
    .main-header { color: #004aad !important; font-size: 55px !important; font-weight: 900; margin-bottom: 15px; }
    .goal-text { font-size: 24px !important; color: #333; line-height: 1.6; background: white; padding: 35px; border-left: 15px solid #004aad; border-radius: 15px; text-align: justify; }
    .content-card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px; border-top: 5px solid #004aad; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None, 
        options=["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил"],
        icons=['house', 'play-btn', 'book', 'pencil-square'],
        default_index=0,
        styles={"nav-link": {"font-size": "17px", "color": "white", "font-weight": "bold"}, "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)"}}
    )

# 4. АГУУЛГА
if selected == "Нүүр хуудас":
    col1, col2 = st.columns([1, 1.4])
    with col1:
        logo_path = "logo.gif" 
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                data = f.read()
                data_url = base64.b64encode(data).decode("utf-8")
            st.markdown(f'<img src="data:image/gif;base64,{data_url}" width="100%">', unsafe_allow_html=True)
    with col2:
        st.markdown('<p class="main-header">Бидний зорилго</p>', unsafe_allow_html=True)
        st.markdown('<div class="goal-text">Есдүгээр ангийн математикийн ертөнцөөр хамтдаа аялж, сонирхолтой цахим хичээл, бодлогын сангаар дамжуулан өөрийн мэдлэг чадвараа бие даан ахиулж, ирээдүйн амжилтынхаа эхлэлийг өнөөдөр тавьцгаая!</div>', unsafe_allow_html=True)

elif selected == "Цахим контент":
    st.markdown("<h1 style='color: #004aad;'>📺 Видео хичээлүүд</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.subheader("1. Рационал тоо")
            # Жишээ видео холбоос (YouTube-ийн дурын хичээл тавьж болно)
            st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") 
            st.write("Энэ хичээлээр рационал тоон олонлог болон түүний чанарыг үзнэ.")
            st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        with st.container():
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.subheader("2. Алгебрын илэрхийлэл")
            st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            st.write("Ижил төстэй гишүүдийг эмхэтгэх, хаалт задлах аргад суралцана.")
            st.markdown('</div>', unsafe_allow_html=True)

elif selected == "Даалгаврын сан":
    st.markdown("<h1 style='color: #004aad;'>📚 Бодлогын сан</h1>", unsafe_allow_html=True)
    st.info("Удахгүй бодлогын файлууд нэмэгдэнэ.")

elif selected == "Сорил":
    st.markdown("<h1 style='color: #004aad;'>📝 Өөрийгөө сориорой</h1>", unsafe_allow_html=True)
    st.write("Доорх асуултад хариулаад 'Шалгах' товчийг дараарай.")
    
    q1 = st.radio("1. (-5) + 8 = ?", [3, -3, 13, -13])
    if st.button("Шалгах"):
        if q1 == 3:
            st.success("Зөв байна! Баяр хүргэе. 🎉")
        else:
            st.error("Буруу байна, дахин оролдоорой. ❌")
