import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import pandas as pd
import re

# 1. Сайтын ерөнхий тохиргоо
st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# --- СИСТЕМ: ЦЭСНИЙ УДИРДЛАГА ---
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Нүүр хуудас"

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

# 2. ДИЗАЙН (Засварласан CSS)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    
    /* ХАЖУУГИЙН ЦЭС - Өргөнийг багасгасан */
    [data-testid="stSidebar"] { 
        background-color: #0b4ab1 !important; 
        min-width: 250px !important;
        max-width: 250px !important;
    }
    
    /* "ЦЭС" гарчиг - ТОМ болгосон (45px) */
    .sidebar-title { 
        color: white; text-align: center; font-size: 45px; font-weight: bold; 
        padding: 20px 0; margin-bottom: 0px;
        letter-spacing: 2px;
    }

    /* "Бидний зорилго" хайрцаг */
    .goal-box {
        background: white; padding: 25px; border-radius: 20px;
        border: 1px solid #f0f2f6;
        border-left: 10px solid #0b4ab1; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    
    /* ГАРЧИГ - Мөр хоорондын зай бага */
    .main-header { 
        color: #0b4ab1; 
        font-size: 45px; 
        font-weight: 800; 
        margin-bottom: 10px;
        line-height: 1.1; 
    }

    /* Төв хэсгийн 3 товчлуур - ДӨРВӨЛЖИН болгохын тулд өндрийг багасгав */
    div.stButton > button {
        width: 100% !important; 
        height: 200px !important;  /* 280-г 200 болгож багасгав */
        border-radius: 25px !important; 
        border: 1px solid #f0f0f0 !important;
        background: #fdfdfd !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 10px !important;
        transition: all 0.3s ease-in-out !important;
    }

    div.stButton > button p {
        font-size: 20px !important; /* Текстийг жаахан багасгав */
        font-weight: bold !important;
        color: #0b4ab1 !important;
        line-height: 1.2 !important;
    }

    div.stButton > button:hover {
        transform: translateY(-8px) !important;
        box-shadow: 0 15px 40px rgba(0,74,177,0.15) !important;
        border: 1px solid #0b4ab1 !important;
    }

    .math-card {
        background: white; padding: 25px; border-radius: 15px;
        border: 1px solid #e0e0e0; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Цэс)
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    
    menu_options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил"]
    current_index = menu_options.index(st.session_state.selected_menu) if st.session_state.selected_menu in menu_options else 0

    selected = option_menu(
        menu_title=None, 
        options=menu_options,
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        default_index=current_index,
        styles={
            "container": {"background-color": "#0b4ab1", "padding": "0"},
            "icon": {"color": "white", "font-size": "18px"}, 
            "nav-link": {
                "font-size": "14px",  /* Текстийг жижиг болгосон */
                "color": "white", 
                "font-family": "Arial", 
                "font-weight": "normal", 
                "margin": "5px", 
                "text-align": "left"
            },
            "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)", "font-weight": "bold"},
        }
    )
    if selected != st.session_state.selected_menu:
        st.session_state.selected_menu = selected
        st.rerun()

# 4. НҮҮР ХУУДАС
if st.session_state.selected_menu == "Нүүр хуудас":
    col1, col2 = st.columns([1, 1.2], gap="large")
    with col1:
        if os.path.exists("logo.gif"):
            with open("logo.gif", "rb") as f:
                data_url = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(f'<img src="data:image/gif;base64,{data_url}" style="width: 100%; border-radius: 20px;">', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="goal-box">
                <div class="main-header">Математикийн ертөнцөд тавтай морил!</div>
                <div style="
                    font-size: 19px; 
                    line-height: 1.4; 
                    color: #444; 
                    text-align: justify; 
                    text-indent: 20px;
                    font-family: 'Arial', sans-serif;
                ">Сонирхолтой цахим хичээл, баялаг бодлогын сангаар дамжуулан математик сэтгэлгээгээ бие даан хөгжүүлж, ирээдүйн амжилтынхаа суурийг өнөөдөр тавихад тань бид туслах болно. Хамтдаа суралцаж, хамтдаа хөгжицгөөе!</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1], gap="medium")
    
    with c1:
        if st.button("📺\n\nЦахим контент", key="btn_1"):
            st.session_state.selected_menu = "Цахим контент"
            st.rerun()
            
    with c2:
        if st.button("📚\n\nДаалгаврын сан", key="btn_2"):
            st.session_state.selected_menu = "Даалгаврын сан"
            st.rerun()
            
    with c3:
        if st.button("📝\n\nСорил", key="btn_3"):
            st.session_state.selected_menu = "Сорил"
            st.rerun()

# 5. ДААЛГАВРЫН САН
elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown("<h1 style='color: #0b4ab1; text-align: center;'>📚 Бодлогын сан</h1>", unsafe_allow_html=True)
    
    if os.path.exists("data_bank.xlsx"):
        df = pd.read_excel("data_bank.xlsx")
        sc1, sc2 = st.columns(2)
        with sc1:
            unit = st.selectbox("Сэдэв сонгох:", df['Нэгж'].unique())
        with sc2:
            level = st.radio("Түвшин:", ["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"], horizontal=True)
            
        f_df = df[(df['Нэгж'] == unit) & (df['Түвшин'] == level)]
        
        if f_df.empty:
            st.info("Энэ хэсэгт бодлого хараахан ороогүй байна.")
        else:
            for i, row in f_df.iterrows():
                with st.form(key=f"form_{i}"):
                    st.markdown('<div class="math-card">', unsafe_allow_html=True)
                    st.markdown(f"### 📝 Бодлого {i+1}")
                    st.markdown(smart_math_render(row['Асуулт']))
                    ans = st.radio("Хариу сонгох:", ["A", "B", "C", "D"], key=f"ans_{i}", horizontal=True)
                    submit = st.form_submit_button("Шалгах")
                    
                    if submit:
                        correct = str(row['Хариу']).strip().upper()
                        if ans == correct:
                            st.success("Зөв! ✅")
                            st.balloons()
                        else:
                            st.error(f"Буруу байна. Зөв хариу: {correct}")
                    st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("data_bank.xlsx файл олдсонгүй.")

else:
    st.markdown(f"<h1 style='color: #0b4ab1; text-align: center; margin-top: 50px;'>{st.session_state.selected_menu}</h1>", unsafe_allow_html=True)
    st.info("Энэ хэсэг удахгүй нэмэгдэнэ.")
