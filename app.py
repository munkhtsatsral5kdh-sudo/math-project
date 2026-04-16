import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import time
from streamlit_autorefresh import st_autorefresh
import pandas as pd

# 1. Санах ойн тохиргоо
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Нүүр хуудас"
if 'test_started' not in st.session_state:
    st.session_state.test_started = False

# 2. Вэбсайтын ерөнхий тохиргоо
st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# 3. ДИЗАЙН (CSS) - Өмнөх загварыг хадгалав
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #004aad !important; min-width: 300px !important; }
    .sidebar-title { color: #ffffff !important; text-align: center; font-size: 40px !important; font-weight: bold; padding: 20px 0; border-bottom: 2px solid rgba(255,255,255,0.3); margin-bottom: 20px; }
    .main-header { color: #004aad !important; font-size: 45px !important; font-weight: 900; text-align: center; margin-bottom: 20px; }
    .goal-text { font-size: 22px !important; color: #333; line-height: 1.6; background: white; padding: 30px; border-left: 15px solid #004aad; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    /* Бодлогын текстийн фонт */
    .problem-text { font-family: 'Times New Roman', serif; font-size: 22px; line-height: 1.8; color: #1a1a1a; white-space: pre-wrap; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR (Цэс)
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил төлөвшил МХБ"]
    
    try:
        current_index = options.index(st.session_state.selected_menu)
    except:
        current_index = 0
    
    selected = option_menu(
        menu_title=None, 
        options=options,
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        default_index=current_index,
        key='menu_widget',
        styles={
            "container": {"background-color": "#004aad"},
            "nav-link": {"color": "white", "font-weight": "bold"},
            "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)"},
        }
    )
    st.session_state.selected_menu = selected

# --- НҮҮР ХУУДАС ---
if st.session_state.selected_menu == "Нүүр хуудас":
    st.markdown('<p class="main-header">Бидний зорилго</p>', unsafe_allow_html=True)
    st.markdown('<div class="goal-text">Математикийн ертөнцөөр хамтдаа аялж, сонирхолтой цахим хичээл, бодлогын сангаар дамжуулан өөрийн мэдлэг чадвараа бие даан ахиулж, амжилтын эхлэлийг тавьцгаая!</div>', unsafe_allow_html=True)

# --- ДААЛГАВРЫН САН (Шинэчлэгдсэн) ---
elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown('<p class="main-header">📚 Даалгаврын сан</p>', unsafe_allow_html=True)
    if not os.path.exists("data_bank.xlsx"):
        st.error("data_bank.xlsx файл олдсонгүй!")
    else:
        try:
            df = pd.read_excel("data_bank.xlsx")
            unique_units = df['Нэгж'].unique()
            for unit in unique_units:
                with st.expander(f"🔹 {unit}", expanded=True):
                    unit_df = df[df['Нэгж'] == unit]
                    for i, row in unit_df.iterrows():
                        st.markdown(f"### 💠 Бодлого {i+1}:")
                        
                        # Текстийг LaTeX биш, ердийн хэлбэрээр харуулах
                        raw_q = str(row['Асуулт'])
                        formatted_q = raw_q.replace("A.", "\n\n**A.**").replace("B.", "\n\n**B.**").replace("C.", "\n\n**C.**").replace("D.", "\n\n**D.**")
                        
                        st.markdown(f'<div class="problem-text">{formatted_q}</div>', unsafe_allow_html=True)
                        
                        # Сонгох хэлбэр
                        choice = st.radio(
                            "Хариултаа сонгоно уу:",
                            ["Сонгох", "A", "B", "C", "D"],
                            key=f"radio_db_{i}",
                            horizontal=True
                        )
                        
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            if st.button(f"🔍 Шалгах", key=f"check_db_{i}"):
                                if choice == "Сонгох":
                                    st.warning("Хариултаа сонгоно уу!")
                                elif choice.strip().upper() == str(row['Хариу']).strip().upper():
                                    st.success("Зөв! ✅")
                                    st.balloons() # Зөв хариулахад бөмбөлөг хөөрнө 🎈
                                else:
                                    st.error(f"Буруу. Зөв: {row['Хариу']}")
                        with col2:
                            if pd.notnull(row['Бодолт']):
                                with st.expander("💡 Тайлабар харах"):
                                    st.info(str(row['Бодолт']))
                        st.write("---")
        except Exception as e:
            st.error(f"Алдаа: {e}")

# --- СОРИЛ ХЭСЭГ ---
elif st.session_state.selected_menu == "Сорил":
    st.markdown('<p class="main-header">📝 Онлайн сорил</p>', unsafe_allow_html=True)
    st.info("Сорилтын систем бэлтгэгдэж байна.")

# Бусад цэсүүд
else:
    st.markdown(f'<p class="main-header">{st.session_state.selected_menu}</p>', unsafe_allow_html=True)
    st.info("Тун удахгүй...")
