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
    div.stButton { width: 100% !important; }
    div.stButton > button { width: 100% !important; height: 190px !important; border-radius: 25px !important; border: 1px solid #f0f0f0 !important; background: #fdfdfd !important; box-shadow: 0 10px 25px rgba(0,0,0,0.05) !important; display: flex !important; flex-direction: column !important; align-items: center !important; justify-content: center !important; transition: all 0.3s ease-in-out !important; }
    div.stButton > button p { font-size: 22px !important; font-weight: bold !important; color: #0b4ab1 !important; }
    .math-card { background: white; padding: 25px; border-radius: 15px; border: 1px solid #e0e0e0; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)
st.markdown("""
    <style>
    /* "Шалгах" товчийг жижиг болгох */
    div.stButton > button {
        width: 120px !important;  /* Өргөнийг нь багасгав */
        height: 45px !important;   /* Өндрийг нь тогтмол болгов */
        font-size: 16px !important;
        margin: 0 auto;
        display: block;
        border-radius: 10px !important;
    }

    /* Сорил хэсгийн A, B, C, D товчлууруудыг жижиг дөрвөлжин болгох */
    div[data-testid="column"] button {
        width: 50px !important;
        height: 40px !important;
        min-width: 50px !important;
        padding: 0px !important;
    }

    /* Радио товчлуур (сонгох дугуй)-ын хэмжээг тохируулах */
    div[data-testid="stMarkdownContainer"] p {
        font-size: 18px !important;
    }
    
    /* Сорил болон Даалгаврын сангийн асуултын текстийг цэгцлэх */
    .stRadio > label {
        font-size: 16px !important;
        font-weight: bold;
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
        if st.button("📺\n\nЦахим контент", key="btn_1", use_container_width=True): st.session_state.selected_menu = "Цахим контент"; st.rerun()
    with c2:
        if st.button("📚\n\nДаалгаврын сан", key="btn_2", use_container_width=True): st.session_state.selected_menu = "Даалгаврын сан"; st.rerun()
    with c3:
        if st.button("📝\n\nСорил", key="btn_3", use_container_width=True): st.session_state.selected_menu = "Сорил"; st.rerun()

# 5. ЦАХИМ КОНТЕНТ
elif st.session_state.selected_menu == "Цахим контент":
    st.markdown("<h1 style='color: #0b4ab1;'>📺 Цахим хичээлүүд</h1>", unsafe_allow_html=True)
    # Энд чи видеогоо оруулна
    st.write("Доорх хичээлүүдийг үзэж мэдлэгээ баталгаажуулаарай.")
    st.video("https://www.youtube.com/watch?v=your_video_id") # Жишээ видео

# 5. ДААЛГАВРЫН САН (24 ФАЙЛТАЙ ХҮСНЭГТЭН ЗАГВАР)
elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown("<h3 style='text-align: center; color: #0b4ab1;'>📚 Бодлогын сан</h3>", unsafe_allow_html=True)
    
    # Таны илгээсэн яг тэр нэрс
    units = [
        "Тоон олонлог, зэрэг, язгуур, тоог жиших, тоймлох",
        "Харьцаа, пропорц, процент",
        "Алгебрын илэрхийлэл, тэгшитгэл, тэнцэтгэл биш",
        "Дараалал, функц",
        "Өнцөг, дүрс, байгуулалт",
        "Байршил, хөдөлгөөн, хувиргалт",
        "Хэмжигдэхүүн",
        "Магадлал, статистик"
    ]
    
    # Сэдэв болон Түвшин сонгох (Зураг дээрх шиг)
    col_u, col_l = st.columns([0.6, 0.4])
    with col_u:
        u_choice = st.selectbox("Сэдэв сонгох:", units)
    with col_l:
        l_choice = st.radio("Түвшин:", ["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"], horizontal=True)

    # Файлын нэр үүсгэх (Нэгж_Түвшин.xlsx)
    u_idx = units.index(u_choice) + 1
    levels = {"Мэдлэг ойлголт": 1, "Чадвар": 2, "Хэрэглээ": 3}
    l_idx = levels[l_choice]
    f_path = f"task_{u_idx}_{l_idx}.xlsx"

    st.divider()

    # Excel файлыг уншиж бодлогуудыг харуулах
    if os.path.exists(f_path):
        try:
            df_tasks = pd.read_excel(f_path)
            st.success(f"📍 {u_choice} - {l_choice} түвшний {len(df_tasks)} бодлого олдлоо.")
            
            for idx, row in df_tasks.iterrows():
                # Бодлого бүрийг цэвэрхэн хайрцагт харуулах
                with st.container():
                    st.markdown(f"#### 📝 Бодлого {idx+1}")
                    st.markdown(smart_math_render(row['Асуулт']))
                    
                    # Хариулт сонгох хэсэг
                    user_ans = st.radio(f"Хариу сонгох ({idx+1}):", ["A", "B", "C", "D"], 
                                       key=f"task_ans_{u_idx}_{l_idx}_{idx}", 
                                       horizontal=True, label_visibility="collapsed")
                    
                    # Шалгах товчлуур
                    if st.button(f"Шалгах {idx+1}", key=f"check_{idx}"):
                        correct_ans = str(row['Хариу']).strip().upper()
                        if user_ans == correct_ans:
                            st.success(f"✅ Зөв! (Хариу: {correct_ans})")
                        else:
                            st.error(f"❌ Буруу. Зөв хариу: {correct_ans}")
                            if 'Бодолт' in row and pd.notna(row['Бодолт']):
                                with st.expander("Бодолт харах"):
                                    st.markdown(smart_math_render(row['Бодолт']))
                st.write("---")
        except Exception as e:
            st.error(f"Файл уншихад алдаа гарлаа: {e}")
    else:
        st.warning(f"⚠️ '{f_path}' файл олдсонгүй. Файлаа системд байршуулна уу.")
# 7. СОРИЛ (Оноо, Алдаа, Бодолттой хувилбар)
elif st.session_state.selected_menu == "Сорил":
    # Шаардлагатай session_state-уудыг үүсгэх
    if 'quiz_active' not in st.session_state: st.session_state.quiz_active = False
    if 'quiz_finished' not in st.session_state: st.session_state.quiz_finished = False

    # --- 1-Р ШАТ: ЖАГСААЛТ ХАРАГДАХ ХЭСЭГ ---
    if not st.session_state.quiz_active and not st.session_state.quiz_finished:
        st.markdown("<h3 style='text-align: center; color: #0b4ab1;'>📝 Онлайн сорил, шалгалт</h3>", unsafe_allow_html=True)
        st.markdown("""
            <div style='background-color: #343a40; color: white; padding: 10px; border-radius: 5px; display: flex; font-weight: bold;'>
                <div style='width: 5%;'>#</div><div style='width: 65%;'>Сорилын нэр (IX анги)</div><div style='width: 30%; text-align: center;'>Хувилбарууд</div>
            </div>
        """, unsafe_allow_html=True)

        quiz_units = [
            "Тоон олонлог, зэрэг, язгуур, тоог жиших, тоймлох", "Харьцаа, пропорц, процент",
            "Алгебрын илэрхийлэл, тэгшитгэл, тэнцэтгэл биш", "Дараалал, функц",
            "Өнцөг, дүрс, байгуулалт", "Байршил, хөдөлгөөн, хувиргалт",
            "Хэмжигдэхүүн", "Магадлал, статистик"
        ]

        for i, name in enumerate(quiz_units):
            col_n, col_v = st.columns([0.7, 0.3])
            col_n.markdown(f"<div style='padding: 15px 0; border-bottom: 1px solid #eee;'>{i+1}. {name}</div>", unsafe_allow_html=True)
            with col_v:
                v_cols = st.columns(4)
                for j, v in enumerate(["A", "B", "C", "D"]):
                    if v_cols[j].button(v, key=f"q_{i}_{v}"):
                        st.session_state.quiz_file = f"quiz_{i+1}_{v}.xlsx"
                        st.session_state.quiz_active = True
                        st.session_state.start_time = time.time()
                        st.rerun()

    # --- 2-Р ШАТ: СОРИЛ БОДОЖ БАЙХ ҮЕ ---
    elif st.session_state.quiz_active:
        remaining = max(0, 2400 - int(time.time() - st.session_state.start_time))
        c_back, c_timer = st.columns([5, 1])
        if c_back.button("⬅️ Жагсаалт руу буцах"):
            st.session_state.quiz_active = False; st.rerun()
        
        mins, secs = divmod(remaining, 60)
        c_timer.error(f"⏳ {mins:02d}:{secs:02d}")

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

    # --- 3-Р ШАТ: ОНОО, АЛДАА, БОДОЛТ ХАРАХ ХЭСЭГ ---
    elif st.session_state.quiz_finished:
        st.markdown("<h3 style='text-align: center; color: #0b4ab1;'>📊 Сорилын дүн</h3>", unsafe_allow_html=True)
        df_q = pd.read_excel(st.session_state.quiz_file)
        
        # Оноо тооцох
        correct_count = 0
        for idx, row in df_q.iterrows():
            if str(st.session_state.results[idx]) == str(row['Хариу']).strip().upper():
                correct_count += 1
        
        score_percent = (correct_count / len(df_q)) * 100
        
        # Онооны самбар
        c1, c2, c3 = st.columns(3)
        c1.metric("Нийт асуулт", len(df_q))
        c2.metric("Зөв хариулсан", correct_count)
        c3.metric("Гүйцэтгэл", f"{score_percent:.1f}%")

        st.divider()

        # Алдаа болон Бодолт хянах
        st.subheader("📝 Алдаа болон Бодолт хянах")
        for idx, row in df_q.iterrows():
            user_ans = st.session_state.results[idx]
            correct_ans = str(row['Хариу']).strip().upper()
            
            with st.expander(f"Бодлого {idx+1}: {'✅ Зөв' if user_ans == correct_ans else '❌ Буруу'}"):
                st.markdown(smart_math_render(row['Асуулт']))
                st.write(f"**Таны хариулт:** {user_ans}")
                st.write(f"**Зөв хариулт:** {correct_ans}")
                
                if 'Бодолт' in row and pd.notna(row['Бодолт']):
                    st.info("**Бодолт:**")
                    st.markdown(smart_math_render(row['Бодолт']))
                else:
                    st.warning("Энэ бодлогод тайлбар оруулаагүй байна.")

        if st.button("Дахин сорил өгөх"):
            st.session_state.quiz_finished = False
            st.rerun()
# 8. КЛУБЫН МЭДЭЭЛЭЛ
elif st.session_state.selected_menu == "Клубын мэдээлэл":
    st.markdown("<h1 style='color: #0b4ab1;'>👥 Математикийн клуб</h1>", unsafe_allow_html=True)
    st.write("Манай клубын үйл ажиллагаа, бүртгэл энд байна.")

# 9. ХҮҮХДИЙН ХҮМҮҮЖИЛ
elif st.session_state.selected_menu == "Хүүхдийн хүмүүжил":
    st.markdown("<h1 style='color: #0b4ab1;'>❤️ Хүүхдийн хүмүүжил, зөвлөгөө</h1>", unsafe_allow_html=True)
    st.info("Хүүхдээ хэрхэн хөгжүүлэх талаарх багшийн зөвлөгөөнүүд.")
