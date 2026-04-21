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

# 2. ДИЗАЙН (CSS)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    [data-testid="stSidebar"] { background-color: #0b4ab1 !important; min-width: 260px !important; }
    .sidebar-title { color: white; text-align: center; font-size: 45px; font-weight: bold; padding: 20px 0; margin-bottom: 10px; }
    .goal-box { background: white; padding: 25px; border-radius: 20px; border: 1px solid #f0f2f6; border-left: 10px solid #0b4ab1; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .main-header { color: #0b4ab1; font-size: 45px; font-weight: 800; margin-bottom: 5px; line-height: 0.95 !important; }
    
    /* Нүүр хуудасны том товчлуурууд */
    div.stButton > button[key^="btn_"] {
        width: 100% !important;
        height: 190px !important;
        border-radius: 25px !important;
        border: 1px solid #f0f0f0 !important;
        background: #fdfdfd !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s ease-in-out !important;
    }
    div.stButton > button[key^="btn_"] p { font-size: 22px !important; font-weight: bold !important; color: #0b4ab1 !important; }

    /* Шалгах товч (Даалгаврын сан) */
    div.stButton > button[key^="check_"] {
        width: 120px !important;
        height: 45px !important;
        font-size: 16px !important;
        border-radius: 10px !important;
    }

    /* Сорилын A, B, C, D товчлуурууд */
    div[data-testid="column"] button[key^="q_btn_"] {
        width: 50px !important;
        height: 40px !important;
        min-width: 50px !important;
        padding: 0px !important;
    }

    .math-card { background: white; padding: 25px; border-radius: 15px; border: 1px solid #e0e0e0; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Цэс)
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    menu_options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил"]
    current_index = menu_options.index(st.session_state.selected_menu) if st.session_state.selected_menu in menu_options else 0
    selected = option_menu(
        menu_title=None, options=menu_options,
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        default_index=current_index,
        styles={"container": {"background-color": "#0b4ab1", "padding": "0"}, "icon": {"color": "white", "font-size": "18px"}, "nav-link": {"font-size": "16px", "color": "white", "margin": "5px 0px", "padding": "10px 15px", "text-align": "left", "font-weight": "500"}, "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)", "font-weight": "bold"}}
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
        st.markdown('<div class="goal-box"><div class="main-header">Математикийн ертөнцөд тавтай морил!</div><div style="font-size: 19px; line-height: 1.4; color: #444; text-align: justify; text-indent: 20px;">Сонирхолтой цахим хичээл, баялаг бодлогын сангаар дамжуулан математик сэтгэлгээгээ бие даан хөгжүүлж, ирээдүйн амжилтынхаа суурийг өнөөдөр тавихад тань бид туслах болно. Хамтдаа суралцаж, хамтдаа хөгжицгөөе!</div></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1], gap="medium")
    with c1:
        if st.button("📺\n\nЦахим контент", key="btn_1"): st.session_state.selected_menu = "Цахим контент"; st.rerun()
    with c2:
        if st.button("📚\n\nДаалгаврын сан", key="btn_2"): st.session_state.selected_menu = "Даалгаврын сан"; st.rerun()
    with c3:
        if st.button("📝\n\nСорил", key="btn_3"): st.session_state.selected_menu = "Сорил"; st.rerun()

# 5. ЦАХИМ КОНТЕНТ
elif st.session_state.selected_menu == "Цахим контент":
    st.markdown("<h1 style='color: #0b4ab1;'>📺 Цахим хичээлүүд</h1>", unsafe_allow_html=True)
    st.write("Доорх хичээлүүдийг үзэж мэдлэгээ баталгаажуулаарай.")
    st.video("https://www.youtube.com/watch?v=your_video_id")

# 6. ДААЛГАВРЫН САН
elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown("<h3 style='text-align: center; color: #0b4ab1;'>📚 Бодлогын сан</h3>", unsafe_allow_html=True)
    units = ["Тоон олонлог, зэрэг, язгуур, тоог жиших, тоймлох", "Харьцаа, пропорц, процент", "Алгебрын илэрхийлэл, тэгшитгэл, тэнцэтгэл биш", "Дараалал, функц", "Өнцөг, дүрс, байгуулалт", "Байршил, хөдөлгөөн, хувиргалт", "Хэмжигдэхүүн", "Магадлал, статистик"]
    col_u, col_l = st.columns([0.6, 0.4])
    with col_u: u_choice = st.selectbox("Сэдэв сонгох:", units)
    with col_l: l_choice = st.radio("Түвшин:", ["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"], horizontal=True)

    u_idx = units.index(u_choice) + 1
    levels = {"Мэдлэг ойлголт": 1, "Чадвар": 2, "Хэрэглээ": 3}
    f_path = f"task_{u_idx}_{levels[l_choice]}.xlsx"
    st.divider()

    if os.path.exists(f_path):
        try:
            df_tasks = pd.read_excel(f_path)
            for idx, row in df_tasks.iterrows():
                with st.container():
                    st.markdown(f"#### 📝 Бодлого {idx+1}")
                    st.markdown(smart_math_render(row['Асуулт']))
                    user_ans = st.radio(f"Хариу сонгох ({idx+1}):", ["A", "B", "C", "D"], key=f"t_{u_idx}_{idx}", horizontal=True, label_visibility="collapsed")
                    if st.button(f"Шалгах {idx+1}", key=f"check_{idx}"):
                        correct_ans = str(row['Хариу']).strip().upper()
                        if user_ans == correct_ans: st.success(f"✅ Зөв!")
                        else: 
                            st.error(f"❌ Буруу. Зөв хариу: {correct_ans}")
                            if 'Бодолт' in row and pd.notna(row['Бодолт']):
                                with st.expander("Бодолт харах"): st.markdown(smart_math_render(row['Бодолт']))
                st.write("---")
        except Exception as e: st.error(f"Алдаа: {e}")
    else: st.warning(f"Файл олдсонгүй: {f_path}")

# 7. СОРИЛ (ШИНЭЧЛЭГДСЭН ХЭСЭГ)
elif st.session_state.selected_menu == "Сорил":
    if 'quiz_active' not in st.session_state: st.session_state.quiz_active = False
    if 'quiz_finished' not in st.session_state: st.session_state.quiz_finished = False

    # --- ШАТ 1: ЖАГСААЛТ ---
    if not st.session_state.quiz_active and not st.session_state.quiz_finished:
        st.markdown("<h3 style='text-align: center; color: #0b4ab1;'>📝 Онлайн сорил, шалгалт</h3>", unsafe_allow_html=True)
        st.markdown("""
            <div style='background-color: #0b4ab1; color: white; padding: 10px; border-radius: 8px; display: flex; font-weight: bold; margin-bottom: 10px;'>
                <div style='width: 10%; text-align: center;'>#</div><div style='width: 60%;'>Сорилын нэр</div><div style='width: 30%; text-align: center;'>Хувилбар</div>
            </div>
        """, unsafe_allow_html=True)

        quiz_units = ["Тоон олонлог, зэрэг, язгуур, тоог жиших, тоймлох", "Харьцаа, пропорц, процент", "Алгебрын илэрхийлэл, тэгшитгэл, тэнцэтгэл биш", "Дараалал, функц", "Өнцөг, дүрс, байгуулалт", "Байршил, хөдөлгөөн, хувиргалт", "Хэмжигдэхүүн", "Магадлал, статистик"]

        for i, name in enumerate(quiz_units):
            col_n, col_v = st.columns([0.7, 0.3])
            col_n.markdown(f"<div style='padding: 12px 5px; border-bottom: 1px solid #eee;'>{i+1}. {name}</div>", unsafe_allow_html=True)
            with col_v:
                v_cols = st.columns(4)
                for j, v in enumerate(["A", "B", "C", "D"]):
                    if v_cols[j].button(v, key=f"q_btn_{i}_{v}"):
                        st.session_state.quiz_file = f"quiz_{i+1}_{v}.xlsx"
                        st.session_state.quiz_active = True
                        st.session_state.start_time = time.time()
                        st.rerun()

    # --- ШАТ 2: СОРИЛ БОДОХ ---
    elif st.session_state.quiz_active:
        remaining = max(0, 2400 - int(time.time() - st.session_state.start_time))
        c_head, c_timer = st.columns([4, 1])
        if c_head.button("⬅️ Буцах"): st.session_state.quiz_active = False; st.rerun()
        mins, secs = divmod(remaining, 60)
        c_timer.error(f"⏳ {mins:02d}:{secs:02d}")

        if os.path.exists(st.session_state.quiz_file):
            df_q = pd.read_excel(st.session_state.quiz_file)
            with st.form("quiz_form"):
                user_answers = {}
                for idx, row in df_q.iterrows():
                    st.markdown(f"**Бодлого {idx+1}:**")
                    st.markdown(smart_math_render(row['Асуулт']))
                    user_answers[idx] = st.radio(f"Сонголт {idx}:", ["A", "B", "C", "D"], key=f"active_q_{idx}", horizontal=True, label_visibility="collapsed")
                    st.write("---")
                if st.form_submit_button("🏁 Дуусгах"):
                    st.session_state.quiz_results = user_answers
                    st.session_state.quiz_active = False
                    st.session_state.quiz_finished = True
                    st.rerun()
        else: st.error("Файл олдсонгүй."); st.session_state.quiz_active = False

    # --- ШАТ 3: ҮР ДҮН ---
    elif st.session_state.quiz_finished:
        st.markdown("<h3 style='text-align: center; color: #0b4ab1;'>📊 Сорилын дүн</h3>", unsafe_allow_html=True)
        df_q = pd.read_excel(st.session_state.quiz_file)
        correct_count = sum(1 for idx, row in df_q.iterrows() if st.session_state.quiz_results.get(idx) == str(row['Хариу']).strip().upper())
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Нийт", len(df_q)); c2.metric("Зөв", correct_count); c3.metric("Хувь", f"{(correct_count/len(df_q))*100:.1f}%")
        
        st.divider()
        for idx, row in df_q.iterrows():
            u_ans = st.session_state.quiz_results.get(idx)
            c_ans = str(row['Хариу']).strip().upper()
            with st.expander(f"Бодлого {idx+1}: {'✅' if u_ans == c_ans else '❌'}"):
                st.markdown(smart_math_render(row['Асуулт']))
                st.write(f"Таны хариулт: {u_ans} | Зөв хариулт: {c_ans}")
                if 'Бодолт' in row and pd.notna(row['Бодолт']): st.info(f"**Бодолт:** {row['Бодолт']}")

        if st.button("🏠 Цэс рүү буцах"): st.session_state.quiz_finished = False; st.rerun()

# 8. БУСАД ЦЭСҮҮД
elif st.session_state.selected_menu == "Клубын мэдээлэл":
    st.markdown("<h1 style='color: #0b4ab1;'>👥 Математикийн клуб</h1>", unsafe_allow_html=True)
elif st.session_state.selected_menu == "Хүүхдийн хүмүүжил":
    st.markdown("<h1 style='color: #0b4ab1;'>❤️ Хүүхдийн хүмүүжил, зөвлөгөө</h1>", unsafe_allow_html=True)
