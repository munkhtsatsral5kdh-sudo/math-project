import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import time
import pandas as pd
import re
from streamlit_autorefresh import st_autorefresh

# 1. СИСТЕМ ТӨЛӨВ
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Нүүр хуудас"
if 'test_started' not in st.session_state:
    st.session_state.test_started = False

st.set_page_config(page_title="Математик Багш", page_icon="📐", layout="wide")

# 2. УХААЛАГ МАТЕМАТИК ТАНИГЧ (2400 бодлогыг автоматаар бутархай болгоно)
def smart_math_render(text):
    if not isinstance(text, str): return text
    
    # LaTeX тэмдэглэгээг таних (\sqrt, \frac, ^, \mathbb г.м)
    special_chars = ['\\', '^', '_', '{', '}']
    if any(char in text for char in special_chars) and '$' not in text:
        text = f"$ {text} $"
    
    # Энгийн 1/3 гэсэн бичиглэлийг LaTeX бутархай болгох
    if '/' in text and '$' not in text:
        text = re.sub(r'(\d+)/(\d+)', r' $\\frac{\1}{\2}$ ', text)
        
    return text

# 3. ДИЗАЙН (Өнгө болон загвар)
st.markdown("""
    <style>
    .stApp { background-color: #eef2f6 !important; }
    [data-testid="stSidebar"] { background-color: #1a3a5f !important; min-width: 280px !important; }
    .sidebar-title { color: white; text-align: center; font-size: 26px; font-weight: bold; padding: 20px 0; border-bottom: 1px solid rgba(255,255,255,0.1); }
    .goal-box { background: white; padding: 35px; border-radius: 4px; border-top: 6px solid #1a3a5f; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-top: 20px; }
    .goal-text { font-size: 20px; color: #333; line-height: 1.9; text-align: justify; text-indent: 50px; font-family: 'Times New Roman', serif; }
    .math-card { background: white; padding: 30px; border-radius: 8px; border: 1px solid #dee2e6; margin-bottom: 25px; box-shadow: 0 2px 8px rgba(0,0,0,0.02); }
    .stButton>button { border-radius: 4px !important; font-weight: 600 !important; height: 45px !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR (Цэс)
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    menu_options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил"]
    selected = option_menu(None, menu_options, 
                           icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'], 
                           default_index=menu_options.index(st.session_state.selected_menu),
                           styles={"container": {"background-color": "#1a3a5f"}, "nav-link": {"color": "#adb5bd", "font-size": "16px"}, "nav-link-selected": {"background-color": "#2c4e7a", "color": "white"}})
    if selected != st.session_state.selected_menu:
        st.session_state.selected_menu = selected
        st.rerun()

# 5. НҮҮР ХУУДАС
if st.session_state.selected_menu == "Нүүр хуудас":
    c1, c2 = st.columns([1, 1.8], gap="large")
    with c1: st.markdown('<h2 style="color:#28a745; text-align:center;">МАТЕМАТИК БАГШ</h2>', unsafe_allow_html=True)
    with c2:
        st.markdown('<h1 style="color:#1a3a5f;">Бидний зорилго</h1>', unsafe_allow_html=True)
        st.markdown(f'<div class="goal-box"><p class="goal-text">Математикийн ертөнцөөр хамтдаа аялж, сонирхолтой цахим хичээл, бодлогын сангаар дамжуулан өөрийн мэдлэг чадвараа бие даан ахиулж, ирээдүйн амжилтынхаа эхлэлийг өнөөдөр тавьцгаая!</p></div>', unsafe_allow_html=True)

# 6. ДААЛГАВРЫН САН
elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown('<h1 style="color:#1a3a5f; text-align:center;">📚 Даалгаврын сан</h1>', unsafe_allow_html=True)
    if os.path.exists("data_bank.xlsx"):
        df = pd.read_excel("data_bank.xlsx")
        unit = st.selectbox("Сэдэв сонгох:", df['Нэгж'].unique())
        tabs = st.tabs(["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"])
        
        for idx, lvl in enumerate(["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"]):
            with tabs[idx]:
                f_df = df[(df['Нэгж'] == unit) & (df['Түвшин'] == lvl)]
                for i, row in f_df.iterrows():
                    st.markdown('<div class="math-card">', unsafe_allow_html=True)
                    st.write(f"**Бодлого {i+1}**")
                    
                    # 1. Асуулт болон сонголтуудыг нэг дор харуулах
                    st.markdown(smart_math_render(row['Асуулт']))
                    
                    # 2. Хариулт сонгох хэсэг (KeyError-оос сэргийлж багана шалгахгүй)
                    ans = st.radio("Хариу сонгох:", ["A", "B", "C", "D"], key=f"ans_{lvl}_{i}", horizontal=True)
                    
                    # 3. Шалгах товчлуур
                    if st.button("Шалгах", key=f"chk_{lvl}_{i}"):
                        correct_ans = str(row['Хариу']).strip().upper()
                        if str(ans).strip().upper() == correct_ans:
                            st.success("Зөв! ✅"); st.balloons()
                        else: 
                            st.error(f"Буруу. Зөв хариу: {correct_ans}")
                    st.markdown('</div>', unsafe_allow_html=True)
