import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import pandas as pd
import time

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

# 2. ДИЗАЙН (Товчлуурын ангилал)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    [data-testid="stSidebar"] { background-color: #0b4ab1 !important; min-width: 260px !important; }
    .sidebar-title { color: white; text-align: center; font-size: 45px; font-weight: bold; padding: 20px 0; margin-bottom: 10px; }
    .goal-box { background: white; padding: 25px; border-radius: 20px; border: 1px solid #f0f2f6; border-left: 10px solid #0b4ab1; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .main-header { color: #0b4ab1; font-size: 45px; font-weight: 800; margin-bottom: 5px; line-height: 0.95 !important; }
    
    /* НҮҮР ХУУДАСНЫ ТОМ ТОВЧЛУУРУУД */
    .home-btn-container div.stButton > button { width: 100% !important; height: 160px !important; border-radius: 20px !important; border: 1px solid #f0f0f0 !important; background: #fdfdfd !important; box-shadow: 0 8px 20px rgba(0,0,0,0.05) !important; display: flex !important; flex-direction: column !important; align-items: center !important; justify-content: center !important; }
    .home-btn-container div.stButton > button p { font-size: 20px !important; font-weight: bold !important; color: #0b4ab1 !important; }
    
    /* СОРИЛЫН ЖИЖИГ ТОВЧЛУУРУУД */
    .quiz-btn-grid div.stButton > button { width: 100% !important; height: 40px !important; border-radius: 8px !important; padding: 0px !important; background-color: #f8f9fa !important; border: 1px solid #dee2e6 !important; }
    .quiz-btn-grid div.stButton > button p { font-size: 16px !important; color: #333 !important; }

    .math-card { background: white; padding: 25px; border-radius: 15px; border: 1px solid #e0e0e0; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Цэс)
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    menu_options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил"]
    try:
        current_index = menu_options.index(st.session_state.selected_menu)
    except:
        current_index = 0
    selected = option_menu(
        menu_title=None, options=menu_options,
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        default_index=current_index,
        styles={"container": {"background-color": "#0b4ab1", "padding": "0"}, "icon": {"color": "white", "font-size": "18px"}, "nav-link": {"font-size": "16px", "color": "white", "margin": "5px 0px", "padding": "10px 15px", "text-align": "left", "font-weight": "500"}, "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)", "font-weight": "bold"}}
    )
    if selected != st.session_state.selected_menu:
        st.session_state.selected_menu = selected
        st.rerun()

# --- ХУУДАСНУУД ---

# 4. НҮҮР ХУУДАС
if st.session_state.selected_menu == "Нүүр хуудас":
    col1, col2 = st.columns([1, 1.2], gap="large")
    with col1:
        if os.path.exists("logo.gif"):
            with open("logo.gif", "rb") as f: data_url = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(f'<img src="data:image/gif;base64,{data_url}" style="width: 100%; border-radius: 20px;">', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="goal-box"><div class="main-header">Математикийн ертөнцөд тавтай морил!</div><div style="font-size: 19px; line-height: 1.4; color: #444; text-align: justify; text-indent: 20px;">Сонирхолтой цахим хичээл, баялаг бодлогын сангаар дамжуулан математик сэтгэлгээгээ бие даан хөгжүүлж, ирээдүйн амжилтынхаа суурийг өнөөдөр тавихад тань бид туслах болно.</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="home-btn-container">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        if st.button("📺\n\nЦахим контент", key="h_btn1"): st.session_state.selected_menu = "Цахим контент"; st.rerun()
    with c2:
        if st.button("📚\n\nДаалгаврын сан", key="h_btn2"): st.session_state.selected_menu = "Даалгаврын сан"; st.rerun()
    with c3:
        if st.button("📝\n\nСорил", key="h_btn3"): st.session_state.selected_menu = "Сорил"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 6. ДААЛГАВРЫН САН (Бүрэн сэргээсэн хэсэг)
elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown("<h1 style='color: #0b4ab1; text-align: center;'>📚 Бодлогын сан</h1>", unsafe_allow_html=True)
    if os.path.exists("data_bank.xlsx"):
        df = pd.read_excel("data_bank.xlsx")
        sc1, sc2 = st.columns(2)
        with sc1: unit = st.selectbox("Сэдэв сонгох:", df['Нэгж'].unique())
        with sc2: level = st.radio("Түвшин:", ["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"], horizontal=True)
        
        f_df = df[(df['Нэгж'] == unit) & (df['Түвшин'] == level)]
        if f_df.empty: st.info("Энэ хэсэгт бодлого хараахан ороогүй байна.")
        else:
            for i, row in f_df.iterrows():
                with st.form(key=f"db_form_{i}"):
                    st.markdown('<div class="math-card">', unsafe_allow_html=True)
                    st.markdown(f"### 📝 Бодлого {i+1}")
                    st.markdown(smart_math_render(row['Асуулт']))
                    ans = st.radio("Хариу сонгох:", ["A", "B", "C", "D"], key=f"db_ans_{i}", horizontal=True)
                    if st.form_submit_button("Шалгах"):
                        correct = str(row['Хариу']).strip().upper()
                        if ans == correct: st.success("Зөв! ✅"); st.balloons()
                        else: st.error(f"Буруу байна. Зөв хариу: {correct}")
                    st.markdown('</div>', unsafe_allow_html=True)
    else: st.warning("data_bank.xlsx файл олдсонгүй.")

# 7. СОРИЛ (Хугацаа гүйдэг + Жижиг товчлуур)
elif st.session_state.selected_menu == "Сорил":
    st.markdown("<h3 style='text-align: center; color: #0b4ab1;'>📝 Онлайн сорил, шалгалт</h3>", unsafe_allow_html=True)
    units = ["Тоон олонлог, зэрэг, язгуур", "Харьцаа, пропорц, процент", "Алгебрын илэрхийлэл, тэгшитгэл", "Дараалал, функц", "Өнцөг, дүрс, байгуулалт", "Байршил, хөдөлгөөн", "Хэмжигдэхүүн", "Магадлал, статистик"]

    if 'quiz_active' not in st.session_state: st.session_state.quiz_active = False

    if not st.session_state.quiz_active:
        st.markdown("<div style='background-color: #343a40; color: white; padding: 10px; border-radius: 5px; display: flex; font-size: 14px; font-weight: bold;'><div style='width: 5%;'>#</div><div style='width: 60%;'>Сорилын нэр (IX анги)</div><div style='width: 35%; text-align: center;'>Хувилбарууд</div></div>", unsafe_allow_html=True)
        for i, name in enumerate(units):
            col_n, col_v = st.columns([0.65, 0.35])
            col_n.write(f"**{i+1}.** {name}")
            with col_v:
                st.markdown('<div class="quiz-btn-grid">', unsafe_allow_html=True)
                v1, v2, v3, v4 = st.columns(4)
                if v1.button("A", key=f"qA_{i}"): st.session_state.u_name=name; st.session_state.var="A"; st.session_state.quiz_active=True; st.session_state.start_t=time.time(); st.rerun()
                if v2.button("B", key=f"qB_{i}"): st.session_state.u_name=name; st.session_state.var="B"; st.session_state.quiz_active=True; st.session_state.start_t=time.time(); st.rerun()
                if v3.button("C", key=f"qC_{i}"): st.session_state.u_name=name; st.session_state.var="C"; st.session_state.quiz_active=True; st.session_state.start_t=time.time(); st.rerun()
                if v4.button("D", key=f"qD_{i}"): st.session_state.u_name=name; st.session_state.var="D"; st.session_state.quiz_active=True; st.session_state.start_t=time.time(); st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<hr style='margin: 0; opacity: 0.1;'>", unsafe_allow_html=True)
    else:
        elapsed = int(time.time() - st.session_state.start_t)
        rem = max(0, 2400 - elapsed)
        mm, ss = divmod(rem, 60)
        c_b, c_t = st.columns([5, 1])
        if c_b.button("⬅️ Гарах"): st.session_state.quiz_active = False; st.rerun()
        c_t.error(f"⏳ {mm:02d}:{ss:02d}")
        
        st.info(f"📍 {st.session_state.u_name} | Хувилбар {st.session_state.var}")
        if os.path.exists("data_bank.xlsx"):
            df = pd.read_excel("data_bank.xlsx")
            u_idx = units.index(st.session_state.u_name) + 1
            q_df = df[(df['Нэгж'].astype(str).str.contains(str(u_idx))) & (df['Хувилбар'] == st.session_state.var)] if 'Хувилбар' in df.columns else df[df['Нэгж'].astype(str).str.contains(str(u_idx))].head(5)
            for idx, row in q_df.iterrows():
                st.markdown(smart_math_render(row['Асуулт']))
                st.radio("Хариу:", ["A", "B", "C", "D"], key=f"qz_q_{idx}", horizontal=True)
                st.write("---")
            if st.button("🏁 Дуусгах", use_container_width=True): st.success("Дууслаа!"); st.session_state.quiz_active = False; st.rerun()
        if rem > 0: time.sleep(1); st.rerun()

# БУСАД ЦЭСҮҮД
elif st.session_state.selected_menu == "Цахим контент":
    st.markdown("<h1 style='color: #0b4ab1;'>📺 Цахим хичээлүүд</h1>", unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=your_video_id")
elif st.session_state.selected_menu == "Клубын мэдээлэл":
    st.markdown("<h1 style='color: #0b4ab1;'>👥 Математикийн клуб</h1>", unsafe_allow_html=True)
elif st.session_state.selected_menu == "Хүүхдийн хүмүүжил":
    st.markdown("<h1 style='color: #0b4ab1;'>❤️ Хүүхдийн хүмүүжил, зөвлөгөө</h1>", unsafe_allow_html=True)
