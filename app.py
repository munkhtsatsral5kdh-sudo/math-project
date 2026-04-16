import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import time
from streamlit_autorefresh import st_autorefresh
import pandas as pd

# 1. Сонгогдсон цэсийг санах ойд хадгалах
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Нүүр хуудас"
if 'test_started' not in st.session_state:
    st.session_state.test_started = False

# 2. Вэбсайтын ерөнхий тохиргоо
st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# 3. ДИЗАЙН (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #004aad !important; min-width: 300px !important; }
    .sidebar-title { color: #ffffff !important; text-align: center; font-size: 40px !important; font-weight: bold; padding: 20px 0; border-bottom: 2px solid rgba(255,255,255,0.3); margin-bottom: 20px; }
    .main-header { color: #004aad !important; font-size: 45px !important; font-weight: 900; text-align: center; margin-bottom: 20px; }
    .goal-text { font-size: 22px !important; color: #333; line-height: 1.6; background: white; padding: 30px; border-left: 15px solid #004aad; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .custom-card { background: white; border-radius: 25px; padding: 30px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 1px solid #eee; height: 250px; }
    .card-icon { font-size: 50px; margin-bottom: 10px; }
    .card-title { color: #004aad; font-size: 22px; font-weight: bold; }
    .problem-text { font-family: 'Times New Roman', serif; font-size: 21px; line-height: 1.6; color: #1a1a1a; }
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
    col1, col2 = st.columns([1, 1.5], gap="large")
    with col1:
        if os.path.exists("logo.gif"):
            with open("logo.gif", "rb") as f:
                data = f.read()
                data_url = base64.b64encode(data).decode("utf-8")
            st.markdown(f'<img src="data:image/gif;base64,{data_url}" width="100%">', unsafe_allow_html=True)
        else:
            st.info("Математикийн ертөнц")
    with col2:
        st.markdown('<p class="main-header" style="text-align:left;">Бидний зорилго</p>', unsafe_allow_html=True)
        st.markdown('<div class="goal-text">Математикийн ертөнцөөр хамтдаа аялж, сонирхолтой цахим хичээл, бодлогын сангаар дамжуулан өөрийн мэдлэг чадвараа бие даан ахиулж, ирээдүйн амжилтынхаа эхлэлийг өнөөдөр тавьцгаая!</div>', unsafe_allow_html=True)

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
                        
                        # Асуултын текстийг цэвэрлэх
                        raw_q = str(row['Асуулт'])
                        # A, B, C, D сонголтууд текстийн дотор байгаа бол тэдгээрийг арилгаж зөвхөн асуултыг үлдээнэ
                        q_only = raw_q.split("A.")[0].split("A)")[0].strip()
                        st.markdown(f'<div class="problem-text">{q_only}</div>', unsafe_allow_html=True)
                        
                        # Сонгох хэлбэр (Radio button)
                        choice = st.radio(
                            "Хариултаа сонгоно уу:",
                            ["Сонгох", "A", "B", "C", "D"],
                            key=f"radio_{i}",
                            horizontal=True
                        )
                        
                        if st.button(f"🔍 Шалгах", key=f"btn_{i}"):
                            if choice == "Сонгох":
                                st.warning("Хариултаа сонгоно уу!")
                            elif choice.strip().upper() == str(row['Хариу']).strip().upper():
                                st.success("Зөв! ✅ Баяр хүргэе!")
                                st.balloons() # Бөмбөлөг хөөргөх хэсэг 🎈
                            else:
                                st.error(f"Буруу байна. ❌ Зөв хариу: {row['Хариу']}")
                        
                        if pd.notnull(row['Бодолт']):
                            with st.expander("💡 Тайлабар харах"):
                                st.info(str(row['Бодолт']))
                        st.write("---")
        except Exception as e:
            st.error(f"Алдаа: {e}")

# --- СОРИЛ ХЭСЭГ ---
elif st.session_state.selected_menu == "Сорил":
    st.markdown('<p class="main-header">📝 Сорил</p>', unsafe_allow_html=True)
    st.info("Сорилтын хэсэг бэлтгэгдэж байна.")

# Бусад цэсүүд...
else:
    st.markdown(f'<p class="main-header">{st.session_state.selected_menu}</p>', unsafe_allow_html=True)
    st.info("Тус хэсэг удахгүй нэмэгдэнэ.")
