import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64

# 1. Сонгогдсон цэсийг санах ойд хадгалах (Энэ нь гацалтаас сэргийлнэ)
if 'menu_option' not in st.session_state:
    st.session_state.menu_option = "Нүүр хуудас"

# 2. Вэбсайтын тохиргоо
st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# 3. ДИЗАЙН (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #004aad !important; min-width: 300px !important; }
    .sidebar-title { color: #ffffff !important; text-align: center; font-size: 40px !important; font-weight: bold; padding: 20px 0; border-bottom: 2px solid rgba(255,255,255,0.3); margin-bottom: 20px; }
    .main-header { color: #004aad !important; font-size: 50px !important; font-weight: 900; text-align: center; margin-bottom: 20px; }
    .goal-text { font-size: 22px !important; color: #333; line-height: 1.6; background: white; padding: 30px; border-left: 15px solid #004aad; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .custom-card { background: white; border-radius: 25px; padding: 30px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 1px solid #eee; height: 250px; }
    .card-icon { font-size: 50px; margin-bottom: 10px; }
    .card-title { color: #004aad; font-size: 22px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR (Цэс)
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None, 
        options=["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил төлөвшил МХБ"],
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        default_index=0, # Анх ороход Нүүр хуудас харагдана
        styles={
            "container": {"background-color": "#004aad"},
            "nav-link": {"color": "white", "font-weight": "bold"},
            "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)"},
        }
    )

# 5. ХУУДАСНУУД
# --- НҮҮР ХУУДАС ---
if selected == "Нүүр хуудас":
    col1, col2 = st.columns([1, 1.5], gap="large")
    with col1:
        # Лого оруулах хэсэг
        if os.path.exists("logo.gif"):
            with open("logo.gif", "rb") as f:
                data = f.read()
                data_url = base64.b64encode(data).decode("utf-8")
            st.markdown(f'<img src="data:image/gif;base64,{data_url}" width="100%">', unsafe_allow_html=True)
    with col2:
        st.markdown('<p class="main-header" style="text-align:left;">Бидний зорилго</p>', unsafe_allow_html=True)
        st.markdown('<div class="goal-text">Математикийн ертөнцөөр хамтдаа аялж, сонирхолтой цахим хичээл, бодлогын сангаар дамжуулан өөрийн мэдлэг чадвараа бие даан ахиулж, ирээдүйн амжилтынхаа эхлэлийг өнөөдөр тавьцгаая!</div>', unsafe_allow_html=True)

    st.write("---")
    
    # Картууд
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="custom-card"><div class="card-icon">📺</div><div class="card-title">Цахим контент</div></div>', unsafe_allow_html=True)
        st.button("Үзэх", key="btn1")
    with c2:
        st.markdown('<div class="custom-card"><div class="card-icon">📚</div><div class="card-title">Даалгаврын сан</div></div>', unsafe_allow_html=True)
        st.button("Нээх", key="btn2")
    with c3:
        st.markdown('<div class="custom-card"><div class="card-icon">📝</div><div class="card-title">Сорил</div></div>', unsafe_allow_html=True)
        st.button("Эхлэх", key="btn3")

# --- СОРИЛ ХЭСЭГ ---
elif selected == "Сорил":
    st.markdown('<p class="main-header">📝 Онлайн сорилтын систем</p>', unsafe_allow_html=True)
    
    units = [
        "Үнэлгээний нэгж 1. Тоон олонлог, зэрэг, язгуур, тоог жиших, тоймлох",
        "Үнэлгээний нэгж 2. Харьцаа, пропорц, процент",
        "Үнэлгээний нэгж 3. Алгебрын илэрхийлэл, тэгшитгэл, тэнцэтгэл биш",
        "Үнэлгээний нэгж 4. Дараалал, функц",
        "Үнэлгээний нэгж 5. Өнцөг, дүрс, байгуулалт",
        "Үнэлгээний нэгж 6. Байршил, хөдөлгөөн, хувиргалт",
        "Үнэлгээний нэгж 7. Хэмжигдэхүүн",
        "Үнэлгээний нэгж 8. Магадлал, статистик"
    ]

    for i, unit_name in enumerate(units, 1):
        with st.expander(f"🔹 {unit_name}"):
            cols = st.columns(4)
            for j, var in enumerate(['A', 'B', 'C', 'D']):
                cols[j].button(f"{var} хувилбар", key=f"q_{i}_{var}")

else:
    st.write(f"### {selected} хуудас бэлтгэгдэж байна.")
