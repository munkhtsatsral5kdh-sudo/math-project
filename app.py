import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import pandas as pd

# 1. Сайтын ерөнхий тохиргоо (Хамгийн дээд талд)
st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# --- СИСТЕМ: ЦЭСНИЙ УДИРДЛАГА (Session State) ---
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Нүүр хуудас"

# УХААЛАГ МАТЕМАТИК ТАНИГЧ (LaTeX засагч)
def smart_math_render(text):
    if not isinstance(text, str): return str(text)
    # Сонголтуудыг шинэ мөрөнд гаргах
    for label in ['A.', 'B.', 'C.', 'D.']:
        if label in text:
            text = text.replace(label, f'\n\n**{label}**')
    
    # Хэрэв LaTeX тэмдэгт байгаад $ тэмдэг байхгүй бол нэмэх
    if ('\\' in text or '^' in text or '/' in text) and '$' not in text:
        clean_text = text.replace('\\displaystyle', '').strip()
        text = f"$\\displaystyle {clean_text}$"
    return text

# 2. ДИЗАЙН (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    [data-testid="stSidebar"] { background-color: #004aad !important; }
    .sidebar-title { color: white; text-align: center; font-size: 32px; font-weight: bold; padding: 20px 0; border-bottom: 1px solid rgba(255,255,255,0.2); }
    
    .goal-box {
        background: white; padding: 40px; border-radius: 20px;
        border-left: 10px solid #004aad; box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    }
    .main-header { color: #004aad; font-size: 45px; font-weight: 800; margin-bottom: 20px; }
    
    /* Товчлуурын загвар */
    div.stButton > button {
        width: 100%; border-radius: 20px; border: none; background: white;
        padding: 40px 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        transition: all 0.3s ease; height: 200px; color: #004aad; font-weight: bold;
        white-space: pre-line; /* Шинэ мөр авах боломжтой болгох */
    }
    div.stButton > button:hover {
        transform: translateY(-5px); border: 1px solid #004aad;
        box-shadow: 0 15px 35px rgba(0,74,173,0.1);
    }
    
    .math-card {
        background: white; padding: 25px; border-radius: 15px;
        border: 1px solid #e0e0e0; margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Цэс)
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    # Индексийг автоматаар олох
    menu_options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил"]
    current_index = menu_options.index(st.session_state.selected_menu)
    
    selected = option_menu(
        menu_title=None, 
        options=menu_options,
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        default_index=current_index,
        styles={
            "container": {"background-color": "#004aad", "padding": "0"},
            "icon": {"color": "white", "font-size": "20px"}, 
            "nav-link": {"font-size": "17px", "color": "white", "font-family": "Arial", "font-weight": "bold", "margin": "5px"},
            "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)"},
        }
    )
    # Цэс солигдсон эсэхийг шалгах
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
            st.markdown(f'<img src="data:image/gif;base64,{data_url}" width="100%">', unsafe_allow_html=True)
        else:
            st.info("Logo.gif олдсонгүй.")
    
    with col2:
        st.markdown(f"""
            <div class="goal-box">
                <div class="main-header">Бидний зорилго</div>
                <div style="font-size: 22px; line-height: 1.6; color: #444;">
                    Математикийн ертөнцөөр хамтдаа аялж, сонирхолтой цахим хичээл, 
                    бодлогын сангаар дамжуулан өөрийн мэдлэг чадвараа бие даан ахиулж, 
                    ирээдүйн амжилтынхаа эхлэлийг өнөөдөр тавьцгаая!
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="medium")
    
    if c1.button("📺\n\nЦахим контент\n\nҮзэх", key="btn_1"):
        st.session_state.selected_menu = "Цахим контент"
        st.rerun()
    if c2.button("📚\n\nДаалгаврын сан\n\nНээх", key="btn_2"):
        st.session_state.selected_menu = "Даалгаврын сан"
        st.rerun()
    if c3.button("📝\n\nСорил\n\nЭхлэх", key="btn_3"):
        st.session_state.selected_menu = "Сорил"
        st.rerun()

# 5. ДААЛГАВРЫН САН
elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown("<h1 style='color: #004aad; text-align: center;'>📚 Бодлогын сан</h1>", unsafe_allow_html=True)
    
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
                # Form ашиглах нь товчлуур дарахад хуудас дахин ачаалж хариу алга болохоос сэргийлнэ
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

# Бусад цэсүүд
else:
    st.markdown(f"<h1 style='color: #004aad; text-align: center; margin-top: 50px;'>{st.session_state.selected_menu}</h1>", unsafe_allow_html=True)
    st.info("Энэ хэсэг удахгүй нэмэгдэнэ.")
