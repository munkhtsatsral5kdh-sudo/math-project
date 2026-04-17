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

# 2. ДИЗАЙН
st.markdown("""
    <style>
    .stApp { background-color: white; }
    [data-testid="stSidebar"] { background-color: #0b4ab1 !important; min-width: 260px !important; }
    .sidebar-title { color: white; text-align: center; font-size: 45px; font-weight: bold; padding: 20px 0; margin-bottom: 10px; }
    .goal-box { background: white; padding: 25px; border-radius: 20px; border: 1px solid #f0f2f6; border-left: 10px solid #0b4ab1; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .main-header { color: #0b4ab1; font-size: 45px; font-weight: 800; margin-bottom: 5px; line-height: 0.95 !important; }
    div.stElementContainer:has(button[key^="home_btn_"]) button {
        width: 100% !important; height: 180px !important; border-radius: 25px !important;
        border: 1px solid #f0f0f0 !important; background: #fdfdfd !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05) !important; display: flex !important;
        flex-direction: column !important; align-items: center !important; justify-content: center !important;
    }
    div.stElementContainer:has(button[key^="home_btn_"]) button p { font-size: 22px !important; font-weight: bold !important; color: #0b4ab1 !important; }
    .math-card { background: white; padding: 25px; border-radius: 15px; border: 1px solid #e0e0e0; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.02); }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Цэс)
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    menu_options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил"]
    current_idx = menu_options.index(st.session_state.selected_menu) if st.session_state.selected_menu in menu_options else 0
    selected = option_menu(
        menu_title=None, options=menu_options,
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        default_index=current_idx,
        styles={"container": {"background-color": "#0b4ab1"}, "nav-link": {"color": "white"}, "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)"}}
    )
    if selected != st.session_state.selected_menu:
        st.session_state.selected_menu = selected
        st.rerun()

# 4. НҮҮР ХУУДАС
if st.session_state.selected_menu == "Нүүр хуудас":
    col1, col2 = st.columns([1, 1.2], gap="large")
    with col1:
        if os.path.exists("logo.gif"):
            with open("logo.gif", "rb") as f: data_url = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(f'<img src="data:image/gif;base64,{data_url}" style="width: 100%; border-radius: 20px;">', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="goal-box"><div class="main-header">Математикийн ертөнцөд тавтай морил!</div><div style="font-size: 19px; line-height: 1.4; color: #444; text-align: justify; text-indent: 20px;">Хамтдаа суралцаж, хамтдаа хөгжицгөөе!</div></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        if st.button("📺\n\nЦахим контент", key="home_btn_1"): st.session_state.selected_menu = "Цахим контент"; st.rerun()
    with c2:
        if st.button("📚\n\nДаалгаврын сан", key="home_btn_2"): st.session_state.selected_menu = "Даалгаврын сан"; st.rerun()
    with c3:
        if st.button("📝\n\nСорил", key="home_btn_3"): st.session_state.selected_menu = "Сорил"; st.rerun()

# 5. ДААЛГАВРЫН САН
elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown("<h3 style='text-align: center; color: #0b4ab1;'>📚 Бодлогын сан</h3>", unsafe_allow_html=True)
    units = ["Тоон олонлог", "Харьцаа", "Алгебр", "Дараалал", "Өнцөг", "Байршил", "Хэмжигдэхүүн", "Магадлал"]
    col_u, col_l = st.columns([0.6, 0.4])
    with col_u: u_choice = st.selectbox("Сэдэв сонгох:", units)
    with col_l: l_choice = st.radio("Түвшин:", ["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"], horizontal=True)
    
    u_idx = units.index(u_choice) + 1
    levels_map = {"Мэдлэг ойлголт": 1, "Чадвар": 2, "Хэрэглээ": 3}
    f_path = f"task_{u_idx}_{levels_map[l_choice]}.xlsx"
    
    if os.path.exists(f_path):
        df_tasks = pd.read_excel(f_path)
        for idx, row in df_tasks.iterrows():
            st.markdown('<div class="math-card">', unsafe_allow_html=True)
            st.markdown(f"#### 📝 Бодлого {idx+1}")
            st.markdown(smart_math_render(row['Асуулт']))
            user_ans = st.radio(f"Хариу:", ["A", "B", "C", "D"], key=f"t_{u_idx}_{idx}", horizontal=True)
            if st.button(f"Шалгах {idx+1}"):
                correct = str(row['Хариу']).strip().upper()
                if user_ans == correct: st.success("✅ Зөв!")
                else: st.error(f"❌ Буруу. Зөв хариу: {correct}")
            st.markdown('</div>', unsafe_allow_html=True)
    else: st.warning(f"⚠️ {f_path} файл олдсонгүй.")

# 6. СОРИЛ (ЗАСАГДСАН ХУВИЛБАР)
elif st.session_state.selected_menu == "Сорил":
    if 'quiz_active' not in st.session_state: st.session_state.quiz_active = False
    if 'start_time' not in st.session_state: st.session_state.start_time = None
    if 'submitted' not in st.session_state: st.session_state.submitted = False

    if not st.session_state.quiz_active:
        st.markdown("<h3 style='text-align: center; color: #0b4ab1;'>📝 Онлайн шалгалт (40 минут)</h3>", unsafe_allow_html=True)
        with st.container():
            st.info("Бүртгүүлээд 'Эхлүүлэх' товч дарснаар цаг тоолж эхэлнэ.")
            c1, c2 = st.columns(2)
            with c1:
                s_school = st.text_input("Сургууль:", key="std_school")
                s_class = st.text_input("Анги:", key="std_class")
            with c2:
                s_name = st.text_input("Нэр:", key="std_name")
                topic_list = ["Тоон олонлог", "Харьцаа", "Алгебр", "Дараалал", "Өнцөг", "Байршил", "Хэмжигдэхүүн", "Магадлал"]
                s_topic = st.selectbox("Сэдэв:", range(len(topic_list)), format_func=lambda x: f"{x+1}. {topic_list[x]}")
                s_ver = st.selectbox("Хувилбар:", ["A", "B", "C", "D"])

        if st.button("🚀 Шалгалт эхлүүлэх"):
            if s_school and s_class and s_name:
                st.session_state.quiz_file = f"quiz_{s_topic + 1}_{s_ver.lower()}.xlsx"
                st.session_state.quiz_active = True
                st.session_state.start_time = time.time()
                st.session_state.submitted = False
                st.rerun()
            else: st.error("⚠️ Мэдээллээ бүрэн бөглөнө үү!")

    elif st.session_state.quiz_active and not st.session_state.submitted:
        rem = (40 * 60) - (time.time() - st.session_state.start_time)
        if rem <= 0:
            st.error("⏰ Хугацаа дууслаа!")
            rem = 0
        
        m, s = divmod(int(rem), 60)
        st.sidebar.metric("⏳ Үлдсэн хугацаа", f"{m:02d}:{s:02d}")

        if os.path.exists(st.session_state.quiz_file):
            df_q = pd.read_excel(st.session_state.quiz_file)
            with st.form("quiz_form"):
                st.write(f"✍️ Сурагч: {st.session_state.std_name}")
                for idx, row in df_q.iterrows():
                    if pd.isna(row['Асуулт']): continue
                    st.markdown(f"#### {idx+1}. {smart_math_render(row['Асуулт'])}")
                    if idx < 12: st.radio("Сонгох:", ["A", "B", "C", "D"], key=f"ans_{idx}", horizontal=True)
                    else: st.text_input("Хариу бичих:", key=f"ans_{idx}")
                
                if st.form_submit_button("🏁 Дуусгах"):
                    st.session_state.submitted = True
                    st.rerun()
        else:
            st.error("Файл олдсонгүй."); st.button("Буцах", on_click=lambda: setattr(st.session_state, 'quiz_active', False))

    elif st.session_state.submitted:
        df_q = pd.read_excel(st.session_state.quiz_file)
        score = 0
        ans_list = []
        for i, r in df_q.iterrows():
            u_ans = str(st.session_state.get(f"ans_{i}", "")).strip().upper()
            if u_ans == str(r['Хариу']).strip().upper(): score += 1
            ans_list.append(f"Б{i+1}:{u_ans}")
        
        st.success(f"🎊 {st.session_state.std_name}, та {score} оноо авлаа!")
        # Энд ТАНИЙ_ФОРМ_ID-г өөрийнхөөрөө солино
        form_link = f"https://docs.google.com/forms/d/e/ТАНИЙ_ФОРМ_ID/viewform?entry.1={st.session_state.std_name}&entry.2={st.session_state.std_class}&entry.3={score}&entry.4={', '.join(ans_list)}"
        st.markdown(f"### [✅ БАГШ РУУ ДҮНГ ИЛГЭЭХ]({form_link})")
        if st.button("Нүүр хуудас"):
            st.session_state.quiz_active = False
            st.session_state.submitted = False
            st.rerun()

# 7. БУСАД ХЭСЭГ
elif st.session_state.selected_menu == "Цахим контент":
    st.markdown("<h1 style='color: #0b4ab1;'>📺 Цахим хичээлүүд</h1>", unsafe_allow_html=True)
elif st.session_state.selected_menu == "Клубын мэдээлэл":
    st.markdown("<h1 style='color: #0b4ab1;'>👥 Клуб</h1>", unsafe_allow_html=True)
elif st.session_state.selected_menu == "Хүүхдийн хүмүүжил":
    st.markdown("<h1 style='color: #0b4ab1;'>❤️ Зөвлөгөө</h1>", unsafe_allow_html=True)
