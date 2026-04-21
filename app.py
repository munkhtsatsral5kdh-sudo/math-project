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
    
    /* Сорил хэсгийн A, B, C, D товчлууруудыг жижиг дөрвөлжин болгох */
    div[data-testid="column"] button {
        width: 50px !important;
        height: 40px !important;
        min-width: 50px !important;
        padding: 0px !important;
    }
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

# 5. ЦАХИМ КОНТЕНТ
elif st.session_state.selected_menu == "Цахим контент":
    st.markdown("<h1 style='color: #0b4ab1;'>📺 Цахим хичээлүүд</h1>", unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=your_video_id")

# 6. ДААЛГАВРЫН САН
elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown("<h3 style='text-align: center; color: #0b4ab1;'>📚 Бодлогын сан</h3>", unsafe_allow_html=True)
    units = ["Тоон олонлог, зэрэг, язгуур, тоог жиших, тоймлох", "Харьцаа, пропорц, процент", "Алгебрын илэрхийлэл, тэгшитгэл, тэнцэтгэл биш", "Дараалал, функц", "Өнцөг, дүрс, байгуулалт", "Байршил, хөдөлгөөн, хувиргалт", "Хэмжигдэхүүн", "Магадлал, статистик"]
    col_u, col_l = st.columns([0.6, 0.4])
    with col_u: u_choice = st.selectbox("Сэдэв сонгох:", units)
    with col_l: l_choice = st.radio("Түвшин:", ["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"], horizontal=True)
    
    levels_map = {"Мэдлэг ойлголт": 1, "Чадвар": 2, "Хэрэглээ": 3}
    f_path = f"task_{units.index(u_choice) + 1}_{levels_map[l_choice]}.xlsx"
    
    if os.path.exists(f_path):
        df_tasks = pd.read_excel(f_path)
        for idx, row in df_tasks.iterrows():
            st.markdown(f"#### 📝 Бодлого {idx+1}")
            st.markdown(smart_math_render(row['Асуулт']))
            user_ans = st.radio(f"Хариу сонгох ({idx+1}):", ["A", "B", "C", "D"], key=f"t_{idx}", horizontal=True)
            if st.button(f"Шалгах {idx+1}", key=f"c_{idx}"):
                correct = str(row['Хариу']).strip().upper()
                if user_ans == correct: st.success(f"✅ Зөв!")
                else: 
                    st.error(f"❌ Буруу. Зөв хариу: {correct}")
                    if 'Бодолт' in row and pd.notna(row['Бодолт']):
                        with st.expander("Бодолт харах"): st.markdown(smart_math_render(row['Бодолт']))
            st.divider()

# 7. СОРИЛ
elif st.session_state.selected_menu == "Сорил":
    if 'quiz_active' not in st.session_state: st.session_state.quiz_active = False
    if 'quiz_finished' not in st.session_state: st.session_state.quiz_finished = False

    if not st.session_state.quiz_active and not st.session_state.quiz_finished:
        st.markdown("<h3 style='text-align: center; color: #0b4ab1;'>📝 Онлайн сорил, шалгалт</h3>", unsafe_allow_html=True)
        col_name, col_class = st.columns(2)
        with col_name: std_name = st.text_input("Сурагчийн нэр:", key="std_name_input")
        with col_class: std_class = st.selectbox("Анги:", ["9а", "9б", "9в", "9г"], key="std_class_input")
        
        st.markdown("""<div style='background-color: #343a40; color: white; padding: 10px; border-radius: 5px; display: flex; font-weight: bold;'><div style='width: 10%;'>#</div><div style='width: 60%;'>Сорилын нэр (IX анги)</div><div style='width: 30%; text-align: center;'>Хувилбарууд</div></div>""", unsafe_allow_html=True)
        quiz_units = ["Тоон олонлог, зэрэг, язгуур, тоог жиших, тоймлох", "Харьцаа, пропорц, процент", "Алгебрын илэрхийлэл, тэгшитгэл, тэнцэтгэл биш", "Дараалал, функц", "Өнцөг, дүрс, байгуулалт", "Байршил, хөдөлгөөн, хувиргалт", "Хэмжигдэхүүн", "Магадлал, статистик"]
        for i, name in enumerate(quiz_units):
            col_n, col_v = st.columns([0.7, 0.3])
            col_n.markdown(f"<div style='padding: 15px 0; border-bottom: 1px solid #eee;'>{i+1}. {name}</div>", unsafe_allow_html=True)
            with col_v:
                v_cols = st.columns(4)
                for j, v in enumerate(["A", "B", "C", "D"]):
                    if v_cols[j].button(v, key=f"q_{i}_{v}"):
                        if std_name:
                            st.session_state.std_name = std_name
                            st.session_state.std_class = std_class
                            st.session_state.quiz_file = f"quiz_{i+1}_{v}.xlsx"
                            st.session_state.quiz_active = True
                            st.session_state.start_time = time.time()
                            st.rerun()
                        else: st.warning("Нэрээ оруулна уу!")

    elif st.session_state.quiz_active:
        remaining = max(0, 2400 - int(time.time() - st.session_state.start_time))
        mins, secs = divmod(remaining, 60)
        st.error(f"⏳ Үлдсэн хугацаа: {mins:02d}:{secs:02d}")
        if os.path.exists(st.session_state.quiz_file):
            df_q = pd.read_excel(st.session_state.quiz_file)
            with st.form("quiz_form"):
                user_answers = {}
                for idx, row in df_q.iterrows():
                    st.markdown(f"**Бодлого {idx+1}:**")
                    st.markdown(smart_math_render(row['Асуулт']))
                    user_answers[idx] = st.radio("Сонгох:", ["A", "B", "C", "D"], key=f"ans_{idx}", horizontal=True)
                if st.form_submit_button("🏁 Дуусгах"):
                    st.session_state.results = user_answers
                    st.session_state.quiz_active = False
                    st.session_state.quiz_finished = True
                    st.rerun()
        if remaining > 0: time.sleep(1); st.rerun()

    elif st.session_state.quiz_finished:
        df_q = pd.read_excel(st.session_state.quiz_file)
        correct_count = 0
        ans_log = []
        for idx, row in df_q.iterrows():
            u_ans = st.session_state.results[idx]
            c_ans = str(row['Хариу']).strip().upper()
            if u_ans == c_ans: correct_count += 1
            ans_log.append(f"Б{idx+1}:{u_ans}")
        
        st.balloons()
        st.success(f"📊 {st.session_state.get('std_name', 'Сурагч')}, та {len(df_q)}-аас {correct_count} оноо авлаа.")

        # GOOGLE FORM ИЛГЭЭХ
        base_url = "https://docs.google.com/forms/d/e/1FAIpQLSeM9y7SN_kMvo0KfZZgt1A1_UM01mbm18s2cAizZQzGZtKfhw/formResponse"
        params = f"?entry.1163331065={st.session_state.std_name}&entry.589452758={st.session_state.std_class}&entry.599767365={correct_count}&entry.1997083807={', '.join(ans_log)}&submit=Submit"
        
        st.markdown(f"""<a href="{base_url + params}" target="_blank" style="text-decoration: none;"><div style="background-color: #28a745; color: white; padding: 15px; border-radius: 10px; text-align: center; font-size: 20px; font-weight: bold;">✅ БАГШ РУУ ДҮНГ ИЛГЭЭХ (ЭНД ДАРНА УУ)</div></a>""", unsafe_allow_html=True)
        
        with st.expander("Алдаа болон бодолт хянах"):
            for idx, row in df_q.iterrows():
                u_ans = st.session_state.results[idx]
                c_ans = str(row['Хариу']).strip().upper()
                st.write(f"Бодлого {idx+1}: {'✅ Зөв' if u_ans == c_ans else '❌ Буруу'}")
                if 'Бодолт' in row: st.markdown(smart_math_render(row['Бодолт']))
        
        if st.button("Дахин сорил өгөх"):
            st.session_state.quiz_finished = False
            st.rerun()

# 8 & 9. БУСАД ЦЭС
elif st.session_state.selected_menu == "Клубын мэдээлэл":
    st.markdown("<h1 style='color: #0b4ab1;'>👥 Математикийн клуб</h1>", unsafe_allow_html=True)
elif st.session_state.selected_menu == "Хүүхдийн хүмүүжил":
    st.markdown("<h1 style='color: #0b4ab1;'>❤️ Хүүхдийн хүмүүжил</h1>", unsafe_allow_html=True)
