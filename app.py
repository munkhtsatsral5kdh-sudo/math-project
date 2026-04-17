import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import pandas as pd
import time

# 1. Сайтын ерөнхий тохиргоо
st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# --- СИСТЕМ: SESSION STATE ---
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Нүүр хуудас"
if 'quiz_active' not in st.session_state:
    st.session_state.quiz_active = False
if 'quiz_finished' not in st.session_state:
    st.session_state.quiz_finished = False

# УХААЛАГ МАТЕМАТИК ТАНИГЧ
def smart_math_render(text):
    if not isinstance(text, str): return str(text)
    if ('\\' in text or '^' in text or '/' in text) and '$' not in text:
        clean_text = text.replace('\\displaystyle', '').strip()
        return f"$\\displaystyle {clean_text}$"
    return text

# 2. ДИЗАЙН (БҮХ CSS ЗАСВАРУУД)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    [data-testid="stSidebar"] { background-color: #0b4ab1 !important; min-width: 260px !important; }
    .sidebar-title { color: white; text-align: center; font-size: 45px; font-weight: bold; padding: 20px 0; }
    .goal-box { background: white; padding: 25px; border-radius: 20px; border: 1px solid #f0f2f6; border-left: 10px solid #0b4ab1; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .main-header { color: #0b4ab1; font-size: 45px; font-weight: 800; line-height: 0.95 !important; }

    /* НҮҮР ХУУДАСНЫ 3 ТОМ ТОВЧЛУУРЫГ ИЖИЛ ХЭМЖЭЭТЭЙ БОЛГОХ */
    div.stButton > button[key^="btn_"] {
        width: 100% !important;
        height: 200px !important;
        border-radius: 25px !important;
        border: 1px solid #f0f0f0 !important;
        background: #fdfdfd !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }
    div.stButton > button[key^="btn_"] p {
        font-size: 22px !important;
        font-weight: bold !important;
        color: #0b4ab1 !important;
    }

    /* "ШАЛГАХ" ТОВЧИЙГ ЖИЖИГСГЭХ */
    div.stButton > button[key^="check_"] {
        width: 120px !important;
        height: 40px !important;
        font-size: 14px !important;
        margin: 0 auto !important;
        display: block !important;
        border-radius: 10px !important;
    }

    /* СОРИЛЫН A, B, C, D ТОВЧИЙГ ЖИЖИГ ДӨРВӨЛЖИН БОЛГОХ */
    div.stButton > button[key^="q_btn_"] {
        width: 50px !important;
        height: 40px !important;
        min-width: 50px !important;
        padding: 0px !important;
        background-color: white !important;
        border: 1px solid #ddd !important;
        color: #0b4ab1 !important;
    }

    /* Хүснэгтийн толгой */
    .quiz-header {
        background-color: #343a40;
        color: white;
        padding: 12px;
        border-radius: 5px;
        display: flex;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    menu_options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил"]
    selected = option_menu(
        menu_title=None, options=menu_options,
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        default_index=0,
        styles={
            "container": {"background-color": "#0b4ab1"},
            "nav-link": {"color": "white", "font-size": "16px", "text-align": "left"},
            "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)"}
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
            with open("logo.gif", "rb") as f: data_url = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(f'<img src="data:image/gif;base64,{data_url}" style="width: 100%; border-radius: 20px;">', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="goal-box"><div class="main-header">Математикийн ертөнцөд тавтай морил!</div><div style="font-size: 19px; line-height: 1.4; color: #444; text-align: justify; text-indent: 20px; margin-top:15px;">Сонирхолтой цахим хичээл, баялаг бодлогын сангаар дамжуулан математик сэтгэлгээгээ бие даан хөгжүүлж, ирээдүйн амжилтынхаа суурийг өнөөдөр тавихад тань бид туслах болно.</div></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1: 
        if st.button("📺\n\nЦахим контент", key="btn_1"): st.session_state.selected_menu = "Цахим контент"; st.rerun()
    with c2: 
        if st.button("📚\n\nДаалгаврын сан", key="btn_2"): st.session_state.selected_menu = "Даалгаврын сан"; st.rerun()
    with c3: 
        if st.button("📝\n\nСорил", key="btn_3"): st.session_state.selected_menu = "Сорил"; st.rerun()

# 5. ДААЛГАВРЫН САН
elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown("<h3 style='text-align: center; color: #0b4ab1;'>📚 Даалгаврын сан</h3>", unsafe_allow_html=True)
    units = ["Тоон олонлог, зэрэг, язгуур, тоог жиших, тоймлох", "Харьцаа, пропорц, процент", "Алгебрын илэрхийлэл, тэгшитгэл, тэнцэтгэл биш", "Дараалал, функц", "Өнцөг, дүрс, байгуулалт", "Байршил, хөдөлгөөн, хувиргалт", "Хэмжигдэхүүн", "Магадлал, статистик"]
    
    col_u, col_l = st.columns([0.6, 0.4])
    u_choice = col_u.selectbox("Сэдэв сонгох:", units)
    l_choice = col_l.radio("Түвшин:", ["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"], horizontal=True)
    
    u_idx = units.index(u_choice) + 1
    l_idx = {"Мэдлэг ойлголт": 1, "Чадвар": 2, "Хэрэглээ": 3}[l_choice]
    f_path = f"task_{u_idx}_{l_idx}.xlsx"

    st.divider()
    if os.path.exists(f_path):
        df = pd.read_excel(f_path)
        for idx, row in df.iterrows():
            st.markdown(f"**Бодлого {idx+1}:**")
            st.markdown(smart_math_render(row['Асуулт']))
            ans = st.radio(f"Хариу {idx}:", ["A", "B", "C", "D"], key=f"t_ans_{u_idx}_{idx}", horizontal=True, label_visibility="collapsed")
            if st.button(f"Шалгах {idx+1}", key=f"check_{idx}"):
                correct = str(row['Хариу']).strip().upper()
                if ans == correct: st.success("✅ Зөв!")
                else: 
                    st.error(f"❌ Буруу. Зөв хариу: {correct}")
                    if 'Бодолт' in row and pd.notna(row['Бодолт']):
                        with st.expander("Бодолт харах"): st.markdown(smart_math_render(row['Бодолт']))
            st.write("---")
    else: st.warning("Файл олдсонгүй.")

# 6. СОРИЛ
elif st.session_state.selected_menu == "Сорил":
    if not st.session_state.quiz_active and not st.session_state.quiz_finished:
        st.markdown("<h3 style='text-align: center; color: #0b4ab1;'>📝 Онлайн сорил, шалгалт</h3>", unsafe_allow_html=True)
        st.markdown('<div class="quiz-header"><div style="width:5%">#</div><div style="width:65%">Сорилын нэр (IX анги)</div><div style="width:30%; text-align:center;">Хувилбарууд</div></div>', unsafe_allow_html=True)
        
        quiz_units = ["Тоон олонлог, зэрэг, язгуур, тоог жиших, тоймлох", "Харьцаа, пропорц, процент", "Алгебрын илэрхийлэл, тэгшитгэл, тэнцэтгэл биш", "Дараалал, функц", "Өнцөг, дүрс, байгуулалт", "Байршил, хөдөлгөөн, хувиргалт", "Хэмжигдэхүүн", "Магадлал, статистик"]
        
        for i, name in enumerate(quiz_units):
            col_n, col_v = st.columns([0.7, 0.3])
            col_n.markdown(f"<div style='padding: 12px 0; border-bottom: 1px solid #eee;'>{i+1}. {name}</div>", unsafe_allow_html=True)
            with col_v:
                v_cols = st.columns(4)
                for j, v in enumerate(["A", "B", "C", "D"]):
                    if v_cols[j].button(v, key=f"q_btn_{i}_{v}"):
                        st.session_state.quiz_file = f"quiz_{i+1}_{v}.xlsx"
                        st.session_state.quiz_active = True
                        st.session_state.start_time = time.time()
                        st.rerun()

    elif st.session_state.quiz_active:
        remaining = max(0, 2400 - int(time.time() - st.session_state.start_time))
        c_back, c_timer = st.columns([5, 1])
        if c_back.button("⬅️ Буцах"): st.session_state.quiz_active = False; st.rerun()
        mins, secs = divmod(remaining, 60)
        c_timer.error(f"⏳ {mins:02d}:{secs:02d}")

        if os.path.exists(st.session_state.quiz_file):
            df_q = pd.read_excel(st.session_state.quiz_file)
            with st.form("q_form"):
                u_ans = {}
                for idx, row in df_q.iterrows():
                    st.markdown(f"**Бодлого {idx+1}:**")
                    st.markdown(smart_math_render(row['Асуулт']))
                    u_ans[idx] = st.radio(f"s_{idx}", ["A", "B", "C", "D"], key=f"qz_{idx}", horizontal=True, label_visibility="collapsed")
                    st.write("---")
                if st.form_submit_button("🏁 Дуусгах"):
                    st.session_state.results = u_ans
                    st.session_state.quiz_active = False
                    st.session_state.quiz_finished = True
                    st.rerun()
        if remaining > 0: time.sleep(1); st.rerun()

    elif st.session_state.quiz_finished:
        st.success("Сорил дууслаа!")
        df_q = pd.read_excel(st.session_state.quiz_file)
        corrects = sum(1 for idx, row in df_q.iterrows() if str(st.session_state.results[idx]) == str(row['Хариу']).strip().upper())
        st.metric("Таны оноо", f"{corrects}/{len(df_q)} ({corrects/len(df_q)*100:.1f}%)")
        for idx, row in df_q.iterrows():
            with st.expander(f"Бодлого {idx+1}"):
                st.markdown(smart_math_render(row['Асуулт']))
                st.write(f"Таны хариулт: {st.session_state.results[idx]} | Зөв хариулт: {row['Хариу']}")
                if 'Бодолт' in row: st.info(f"Бодолт: {row['Бодолт']}")
        if st.button("Дахин эхлэх"): st.session_state.quiz_finished = False; st.rerun()

# БУСАД ЦЭСҮҮД
else:
    st.markdown(f"<h1 style='color: #0b4ab1;'>{st.session_state.selected_menu}</h1>", unsafe_allow_html=True)
    st.info("Энэ хэсэг удахгүй нэмэгдэнэ.")
