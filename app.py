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

# УХААЛАГ МАТЕМАТИК ТАНИГЧ (LaTeX болон томьёог зөв харуулах)
def smart_math_render(text):
    if not isinstance(text, str): return str(text)
    # Сонголтуудыг шинэ мөрөнд гаргах
    for label in ['A.', 'B.', 'C.', 'D.']:
        if label in text:
            text = text.replace(label, f'\n\n**{label}**')
    # Томьёо байвал LaTeX хэлбэрт оруулах
    if ('\\' in text or '^' in text or '/' in text) and '$' not in text:
        clean_text = text.replace('\\displaystyle', '').strip()
        text = f"$\\displaystyle {clean_text}$"
    return text

# 2. ДИЗАЙН (CSS)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    [data-testid="stSidebar"] { background-color: #0b4ab1 !important; min-width: 260px !important; }
    .sidebar-title { color: white; text-align: center; font-size: 40px; font-weight: bold; padding: 10px 0; }
    .goal-box { background: white; padding: 25px; border-radius: 20px; border-left: 10px solid #0b4ab1; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    /* Сонголтын товчлууруудыг дөрвөлжин болгох */
    div[data-testid="column"] button { width: 55px !important; height: 45px !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Цэс)
with st.sidebar:
    st.markdown('<p class="sidebar-title">МАТЕМАТИК</p>', unsafe_allow_html=True)
    menu_options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл"]
    selected = option_menu(
        menu_title=None, options=menu_options,
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people'],
        default_index=menu_options.index(st.session_state.selected_menu),
        styles={"nav-link": {"color": "white", "font-size": "16px"}, "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)"}}
    )
    if selected != st.session_state.selected_menu:
        st.session_state.selected_menu = selected
        st.rerun()

# --- НҮҮР ХУУДАС ---
if st.session_state.selected_menu == "Нүүр хуудас":
    st.markdown('<div class="goal-box"><h1>Сайн байна уу?</h1><p>Математик сургалтын системд тавтай морил.</p></div>', unsafe_allow_html=True)

# --- СОРИЛ (Таны Excel файлын бүтэцтэй холбосон хэсэг) ---
elif st.session_state.selected_menu == "Сорил":
    if 'quiz_active' not in st.session_state: st.session_state.quiz_active = False
    if 'quiz_finished' not in st.session_state: st.session_state.quiz_finished = False

    # 1. Мэдээлэл бөглөх хэсэг
    if not st.session_state.quiz_active and not st.session_state.quiz_finished:
        st.subheader("📝 Сурагчийн бүртгэл")
        c1, c2, c3 = st.columns(3)
        std_school = c1.text_input("Сургууль (Жишээ нь: 1-р сургууль):")
        std_name = c2.text_input("Сурагчийн нэр:")
        std_class = c3.selectbox("Анги:", ["9а", "9б", "9в", "9г", "Бусад"])
        
        st.divider()
        st.write("📖 **Хувилбараа сонгоод сорилыг эхлүүлнэ үү:**")
        
        # Хувилбаруудын нэрс (Таны Excel нэрс: quiz_1_A.xlsx гэх мэт)
        quiz_names = ["Тоон олонлог", "Харьцаа, пропорц", "Алгебрын илэрхийлэл", "Дараалал, функц", "Өнцөг, дүрс", "Байршил, хөдөлгөөн", "Хэмжигдэхүүн", "Статистик"]
        
        for i, name in enumerate(quiz_names):
            col1, col2 = st.columns([0.7, 0.3])
            col1.write(f"**{i+1}. {name}**")
            v_cols = col2.columns(4)
            for j, v in enumerate(["A", "B", "C", "D"]):
                if v_cols[j].button(v, key=f"btn_{i}_{v}"):
                    if std_name and std_school:
                        st.session_state.std_name = std_name
                        st.session_state.std_school = std_school
                        st.session_state.std_class = std_class
                        st.session_state.quiz_file = f"quiz_{i+1}_{v}.xlsx"
                        st.session_state.quiz_active = True
                        st.session_state.start_time = time.time()
                        st.rerun()
                    else: st.warning("⚠️ Сургууль болон Нэрээ оруулна уу!")

    # 2. Шалгалт явагдаж байгаа үе
    elif st.session_state.quiz_active:
        remaining = max(0, 2400 - int(time.time() - st.session_state.start_time)) # 40 минут
        mins, secs = divmod(remaining, 60)
        st.error(f"⏳ Үлдсэн хугацаа: {mins:02d}:{secs:02d}")

        if os.path.exists(st.session_state.quiz_file):
            df_q = pd.read_excel(st.session_state.quiz_file)
            with st.form("quiz_form"):
                user_answers = {}
                for idx, row in df_q.iterrows():
                    # ТАНЫ EXCEL: 'Оноо' баганаас оноог уншина
                    pts = row['Оноо'] if 'Оноо' in row and pd.notna(row['Оноо']) else 1
                    st.markdown(f"**Бодлого {idx+1} ({pts} оноо):**")
                    st.markdown(smart_math_render(row['Асуулт']))
                    user_answers[idx] = st.radio("Сонгох:", ["A", "B", "C", "D"], key=f"ans_{idx}", horizontal=True)
                
                if st.form_submit_button("🏁 Дуусгах"):
                    st.session_state.results = user_answers
                    st.session_state.quiz_active = False
                    st.session_state.quiz_finished = True
                    st.rerun()
        if remaining > 0: time.sleep(1); st.rerun()

    # 3. Дүнгийн хэсэг
    elif st.session_state.quiz_finished:
        df_q = pd.read_excel(st.session_state.quiz_file)
        earned = 0
        total = 0
        log = []

        for idx, row in df_q.iterrows():
            pts = row['Оноо'] if 'Оноо' in row and pd.notna(row['Оноо']) else 1
            total += pts
            u_ans = st.session_state.results[idx]
            c_ans = str(row['Хариу']).strip().upper() # ТАНЫ EXCEL: 'Хариу' багана
            
            if u_ans == c_ans: earned += pts
            log.append(f"Б{idx+1}:{u_ans}")

        st.balloons()
        st.success(f"📊 {st.session_state.std_name}, та {total} онооноос {earned} оноо авлаа.")

        # Google Form холбоос (Сургуулийн мэдээлэлтэй)
        base_url = "https://docs.google.com/forms/d/e/1FAIpQLSeM9y7SN_kMvo0KfZZgt1A1_UM01mbm18s2cAizZQzGZtKfhw/formResponse"
        params = (
            f"?entry.1163331065={st.session_state.std_name} ({st.session_state.std_school})"
            f"&entry.589452758={st.session_state.std_class}"
            f"&entry.599767365={earned}/{total}"
            f"&entry.1997083807={', '.join(log)}"
            f"&submit=Submit"
        )
        st.markdown(f'<a href="{base_url + params}" target="_blank" style="text-decoration:none;"><div style="background-color:#28a745;color:white;padding:15px;border-radius:10px;text-align:center;font-weight:bold;">✅ БАГШ РУУ ДҮНГ ИЛГЭЭХ</div></a>', unsafe_allow_html=True)
        
        with st.expander("Бодолт харах"):
            for idx, row in df_q.iterrows():
                st.write(f"**Бодлого {idx+1}:**")
                if 'Бодолт' in row: st.markdown(smart_math_render(row['Бодолт'])) # ТАНЫ EXCEL: 'Бодолт' багана
        
        if st.button("Дахин сорил өгөх"):
            st.session_state.quiz_finished = False; st.rerun()

# Бусад цэс (Хоосон үлдээв)
elif st.session_state.selected_menu == "Цахим контент": st.write("📺 Хичээлүүд")
elif st.session_state.selected_menu == "Даалгаврын сан": st.write("📚 Бодлогууд")
