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

# 1. МАТЕМАТИК БИЧИГЛЭЛИЙГ САЙЖРУУЛСАН ТАНИГЧ
def smart_math_render(text):
    if not isinstance(text, str): return str(text)
    for label in ['A.', 'B.', 'C.', 'D.']:
        if label in text:
            text = text.replace(label, f'\n\n**{label}**')
    keywords = ['\\', '^', '_', '/', '{', '}']
    is_math = any(kw in text for kw in keywords)
    if is_math and '$' not in text:
        clean_text = text.replace('\\displaystyle', '').strip()
        return f"$\\displaystyle {clean_text}$"
    return text

# 2. ДИЗАЙН (CSS)
st.markdown("""
    <style>
    .stApp { background-color: white; }
    [data-testid="stSidebar"] { background-color: #0b4ab1 !important; min-width: 260px !important; }
    .sidebar-title { color: white; text-align: center; font-size: 45px; font-weight: bold; padding: 20px 0; }
    .goal-box { background: white; padding: 25px; border-radius: 20px; border: 1px solid #f0f2f6; border-left: 10px solid #0b4ab1; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .main-header { color: #0b4ab1; font-size: 45px; font-weight: 800; line-height: 0.95 !important; }
    div.stButton > button[key^="btn_"] {
        width: 100% !important; height: 190px !important;
        border-radius: 25px !important; background: #fdfdfd !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05) !important;
        display: flex !important; flex-direction: column !important;
        align-items: center !important; justify-content: center !important;
    }
    div.stButton > button[key^="btn_"] p { font-size: 22px !important; font-weight: bold !important; color: #0b4ab1 !important; }
    div[data-testid="column"] button[key^="q_btn_"] {
        width: 50px !important; height: 40px !important; min-width: 50px !important; padding: 0px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Цэс)
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    menu_options = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил"]
    selected = option_menu(
        menu_title=None, options=menu_options,
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        default_index=menu_options.index(st.session_state.selected_menu) if st.session_state.selected_menu in menu_options else 0,
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
        st.markdown('<div class="goal-box"><div class="main-header">Математикийн ертөнцөд тавтай морил!</div><div style="font-size: 19px; color: #444; text-align: justify;">Сонирхолтой цахим хичээл, баялаг бодлогын сангаар дамжуулан математик сэтгэлгээгээ бие даан хөгжүүлж, ирээдүйн амжилтынхаа суурийг өнөөдөр тавихад тань бид туслах болно.</div></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("📺\n\nЦахим контент", key="btn_1"): st.session_state.selected_menu = "Цахим контент"; st.rerun()
    if c2.button("📚\n\nДаалгаврын сан", key="btn_2"): st.session_state.selected_menu = "Даалгаврын сан"; st.rerun()
    if c3.button("📝\n\nСорил", key="btn_3"): st.session_state.selected_menu = "Сорил"; st.rerun()

# 5. ЦАХИМ КОНТЕНТ (ШИНЭЧЛЭГДСЭН - Өөрийн бичлэг оруулах)
elif st.session_state.selected_menu == "Цахим контент":
    st.markdown("<h1 style='color: #0b4ab1;'>📺 Миний хийсэн хичээлүүд</h1>", unsafe_allow_html=True)
    
    # Хичээлийн сонголтууд
    video_option = st.selectbox("Үзэх хичээлээ сонгоно уу:", ["Хичээл 1", "Хичээл 2"])
    
    if video_option == "Хичээл 1":
        if os.path.exists("video1.mp4"): # video1.mp4 гэсэн файл байгаа эсэхийг шалгана
            st.video("video1.mp4")
        else:
            st.warning("Бичлэгийн файл (video1.mp4) олдсонгүй.")
            
    elif video_option == "Хичээл 2":
        if os.path.exists("video2.mp4"):
            st.video("video2.mp4")
        else:
            st.warning("Бичлэгийн файл (video2.mp4) олдсонгүй.")

# 6. ДААЛГАВРЫН САН
elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown("<h3 style='text-align: center; color: #0b4ab1;'>📚 Бодлогын сан</h3>", unsafe_allow_html=True)
    units = ["Тоон олонлог, зэрэг, язгуур, тоог жиших, тоймлох", "Харьцаа, пропорц, процент", "Алгебрын илэрхийлэл, тэгшитгэл, тэнцэтгэл биш", "Дараалал, функц", "Өнцөг, дүрс, байгуулалт", "Байршил, хөдөлгөөн, хувиргалт", "Хэмжигдэхүүн", "Магадлал, статистик"]
    col_u, col_l = st.columns([0.6, 0.4])
    u_choice = col_u.selectbox("Сэдэв сонгох:", units)
    l_choice = col_l.radio("Түвшин:", ["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"], horizontal=True)
    u_idx, levels = units.index(u_choice) + 1, {"Мэдлэг ойлголт": 1, "Чадвар": 2, "Хэрэглээ": 3}
    f_path = f"task_{u_idx}_{levels[l_choice]}.xlsx"
    if os.path.exists(f_path):
        df_tasks = pd.read_excel(f_path)
        for idx, row in df_tasks.iterrows():
            st.markdown(f"#### 📝 Бодлого {idx+1}")
            st.markdown(smart_math_render(row['Асуулт']))
            user_ans = st.radio(f"Хариу ({idx+1}):", ["A", "B", "C", "D"], key=f"t_{u_idx}_{idx}", horizontal=True, label_visibility="collapsed")
            if st.button(f"Шалгах {idx+1}", key=f"check_{idx}"):
                c_ans = str(row['Хариу']).strip().upper()
                if user_ans == c_ans: st.success("✅ Зөв!")
                else: 
                    st.error(f"❌ Буруу. Зөв хариу: {c_ans}")
                    if 'Бодолт' in row and pd.notna(row['Бодолт']):
                        with st.expander("Бодолт харах"): st.markdown(smart_math_render(row['Бодолт']))
            st.write("---")

# 7. СОРИЛ
elif st.session_state.selected_menu == "Сорил":
    if 'quiz_active' not in st.session_state: st.session_state.quiz_active = False
    if 'quiz_finished' not in st.session_state: st.session_state.quiz_finished = False

    if not st.session_state.quiz_active and not st.session_state.quiz_finished:
        st.markdown("<h3 style='text-align: center; color: #0b4ab1;'>📝 Онлайн сорилын бүртгэл</h3>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        s_school = col1.text_input("Сургууль:")
        s_name = col2.text_input("Овог нэр:")
        s_class = col3.text_input("Анги:")
        st.divider()
        quiz_units = ["Тоон олонлог, зэрэг, язгуур, тоог жиших, тоймлох", "Харьцаа, пропорц, процент", "Алгебрын илэрхийлэл, тэгшитгэл, тэнцэтгэл биш", "Дараалал, функц", "Өнцөг, дүрс, байгуулалт", "Байршил, хөдөлгөөн, хувиргалт", "Хэмжигдэхүүн", "Магадлал, статистик"]
        for i, name in enumerate(quiz_units):
            col_n, col_v = st.columns([0.7, 0.3])
            col_n.markdown(f"<div style='padding: 12px 0; border-bottom: 1px solid #eee;'>{i+1}. {name}</div>", unsafe_allow_html=True)
            with col_v:
                v_cols = st.columns(4)
                for j, v in enumerate(["A", "B", "C", "D"]):
                    if v_cols[j].button(v, key=f"q_btn_{i}_{v}"):
                        if s_school and s_name and s_class:
                            st.session_state.std_info = {"school": s_school, "name": s_name, "class": s_class}
                            st.session_state.quiz_file = f"quiz_{i+1}_{v}.xlsx"
                            st.session_state.quiz_active = True
                            st.session_state.start_time = time.time()
                            st.rerun()
                        else: st.warning("⚠️ Мэдээллээ бүрэн бөглөнө үү!")

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
                    user_answers[idx] = st.radio(f"Хариу {idx}", ["A", "B", "C", "D"], key=f"aq_{idx}", horizontal=True, label_visibility="collapsed")
                    st.write("---")
                if st.form_submit_button("🏁 Дуусгах") or remaining <= 0:
                    st.session_state.quiz_results = user_answers
                    st.session_state.quiz_active = False
                    st.session_state.quiz_finished = True
                    st.rerun()
        if remaining > 0: time.sleep(1); st.rerun()

    elif st.session_state.quiz_finished:
        df_q = pd.read_excel(st.session_state.quiz_file)
        total_score, max_score, log = 0, 0, []
        for idx, row in df_q.iterrows():
            u_ans = st.session_state.quiz_results.get(idx)
            c_ans = str(row['Хариу']).strip().upper()
            pts = float(row['Оноо']) if 'Оноо' in row and pd.notna(row['Оноо']) else 1.0
            max_score += pts
            if u_ans == c_ans: total_score += pts
            log.append(f"Б{idx+1}:{u_ans}")
        st.balloons()
        st.markdown(f"""<div style='text-align: center; padding: 30px; border: 2px solid #0b4ab1; border-radius: 20px;'>
                <h2 style='color: #0b4ab1;'>{st.session_state.std_info['name']}</h2>
                <h1 style='font-size: 72px; color: #0b4ab1;'>{total_score:g} / {max_score:g}</h1></div>""", unsafe_allow_html=True)
        g_url = "https://docs.google.com/forms/d/e/1FAIpQLSeM9y7SN_kMvo0KfZZgt1A1_UM01mbm18s2cAizZQzGZtKfhw/formResponse"
        p = f"?entry.1163331065={st.session_state.std_info['name']} ({st.session_state.std_info['school']})&entry.589452758={st.session_state.std_info['class']}&entry.599767365={total_score}/{max_score}&entry.1997083807={', '.join(log)}&submit=Submit"
        st.markdown(f'<a href="{g_url + p}" target="_blank" style="text-decoration:none;"><div style="background-color:#28a745;color:white;padding:18px;border-radius:12px;text-align:center;font-weight:bold;margin-top:20px;">🚀 БАГШ РУУ ДҮНГ ИЛГЭЭХ</div></a>', unsafe_allow_html=True)
        if st.button("🏠 Нүүр хуудас"): 
            st.session_state.quiz_finished = False
            st.session_state.selected_menu = "Нүүр хуудас"
            st.rerun()

# 8. КЛУБЫН МЭДЭЭЛЭЛ (ШИНЭЧЛЭГДСЭН - Зураг оруулах)
# 8. КЛУБЫН МЭДЭЭЛЭЛ (ШИНЭЧЛЭГДСЭН)
elif st.session_state.selected_menu == "Клубын мэдээлэл":
    st.markdown("<h1 style='color: #0b4ab1; text-align: center;'>👥 Математикийн клуб</h1>", unsafe_allow_html=True)
    
    # Текстэн мэдээлэл оруулах хэсэг
    st.markdown("""
    <div style='background-color: #f0f5ff; padding: 20px; border-radius: 15px; border-left: 5px solid #0b4ab1; margin-bottom: 20px;'>
        <h3>Манай клубын танилцуулга:</h3>
        <p style='font-size: 18px;'>
           "NextGen Robotics" клуб нь ирээдүйн технологийн салбарын түүчээ болох хүсэл эрмэлзэлтэй, инженерчлэл болон програмчлалын хорхойтнуудын нэгдэл юм. Бид зөвхөн робот угсраад зогсохгүй, орчин үеийн хиймэл оюун ухаан (AI) болон технологийн хөгжлийг эх хэл дээрээ судалж, бүтээлчээр сэтгэхийг эрхэмлэдэг.Манай баг хамт олон хүүхэд залуусын сониуч занг хөгжүүлж, тэднийг ирээдүйн "дижитал иргэн" болоход нь туслах зорилготой нэгэн гэр бүл шиг дотно орчныг бүрдүүлсэн билээ.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Хоёр баганаар зураг болон бичлэг харуулах
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📸 Клубын зураг")
        if os.path.exists("club_photo.jpg"):
            st.image("club_photo.jpg", caption="Клубын үйл ажиллагаа", use_container_width=True)
        else:
            st.info("Бидэнд одоогоор зураг байхгүй байна. (club_photo.jpg файлыг хийнэ үү)")

    with col2:
        st.subheader("🎥 Клубын үйл ажиллагаа")
        if os.path.exists("club_video.mp4"):
            st.video("club_video.mp4")
        else:
            st.info("Клубын бичлэг ороогүй байна. (club_video.mp4 файлыг хийнэ үү)")

    # Нэмэлт мэдээлэл (текст)
    st.divider()
    st.markdown("#### ✨ Клубын амжилтаас")
    st.write("- 2025 оны Эрдэнэ сумын математикийн олимпиадад 9а ангийн сурагч Б.Тэмүүлэн дэд байр, 8а ангийн сурагч О.Хонгорзул дэд байр, Р.Энхчимэг гутгаар байр ")
    st.write("- Логик паззлын уралдаанд 6а ангийн сурагч С.Цэнгүүнжаргал тусгай байрт орсон амжилттай байна.0")

# 9. ХҮҮХДИЙН ХҮМҮҮЖИЛ
elif st.session_state.selected_menu == "Хүүхдийн хүмүүжил":
    st.markdown("<h1 style='color: #0b4ab1;'>❤️ Зөвлөгөө</h1>", unsafe_allow_html=True)
