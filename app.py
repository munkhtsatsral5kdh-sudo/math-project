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
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

# Сэдвүүдийн жагсаалт (Бүх хэсэгт ашиглагдана)
UNITS = [
    "Тоон олонлог, зэрэг, язгуур", "Харьцаа, пропорц, процент",
    "Алгебрын илэрхийлэл, тэгшитгэл", "Дараалал, функц",
    "Өнцөг, дүрс, байгуулалт", "Байршил, хөдөлгөөн",
    "Хэмжигдэхүүн", "Магадлал, статистик"
]

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
    div.stButton > button { border-radius: 12px !important; transition: all 0.3s ease-in-out !important; }
    .math-card { background: white; padding: 20px; border-radius: 15px; border: 1px solid #e0e0e0; margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
    .timer-container { position: sticky; top: 0; background: #ff4b4b; color: white; padding: 10px; border-radius: 12px; text-align: center; font-size: 22px; font-weight: bold; z-index: 999; margin-bottom: 20px; }
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
        styles={"container": {"background-color": "#0b4ab1"}, "nav-link": {"font-size": "16px", "color": "white"}, "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)"}}
    )
    if selected != st.session_state.selected_menu:
        st.session_state.selected_menu = selected
        st.session_state.quiz_active = False
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
    st.markdown("<h1 style='color: #0b4ab1;'>📺 Цахим хичээлүүд</h1>")
    st.video("https://www.youtube.com/watch?v=your_video_id")

# 6. ДААЛГАВРЫН САН (24 файл: Түвшин бүрт 100 тест)
elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown("<h3 style='text-align: center; color: #0b4ab1;'>📚 Бие даан ажиллах даалгаврын сан</h3>", unsafe_allow_html=True)
    col_u, col_l = st.columns([2, 1])
    with col_u: u_choice = st.selectbox("Сэдэв сонгох:", UNITS)
    with col_l: l_choice = st.selectbox("Түвшин:", ["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"])
    
    u_idx = UNITS.index(u_choice) + 1
    levels = {"Мэдлэг ойлголт": 1, "Чадвар": 2, "Хэрэглээ": 3}
    f_path = f"task_{u_idx}_{levels[l_choice]}.xlsx" # Нэршил: task_1_1.xlsx
    
    if os.path.exists(f_path):
        df_tasks = pd.read_excel(f_path)
        st.info(f"📍 {u_choice} | Түвшин: {l_choice} ({len(df_tasks)} даалгавар)")
        for idx, row in df_tasks.iterrows():
            with st.container():
                st.markdown(f'<div class="math-card">', unsafe_allow_html=True)
                st.markdown(f"**Даалгавар {idx+1}:**")
                st.markdown(smart_math_render(row['Асуулт']))
                with st.expander("Хариуг шалгах"):
                    u_ans = st.radio(f"Сонгох:", ["A", "B", "C", "D"], key=f"t_{u_idx}_{idx}", horizontal=True)
                    if st.button("Шалгах", key=f"b_{u_idx}_{idx}"):
                        if u_ans == str(row['Хариу']).strip().upper(): st.success("Зөв! ✅")
                        else: 
                            st.error(f"Буруу. Зөв хариу: {row['Хариу']}")
                            if 'Бодолт' in row: st.info(f"**Бодолт:** {row['Бодолт']}")
                st.markdown('</div>', unsafe_allow_html=True)
    else: st.warning(f"Файл олдсонгүй: {f_path}")

# 7. СОРИЛ (32 файл: 8 сэдэв x 4 хувилбар)
elif st.session_state.selected_menu == "Сорил":
    st.markdown("<h3 style='text-align: center; color: #0b4ab1;'>📝 Онлайн сорил, шалгалт</h3>", unsafe_allow_html=True)
    if not st.session_state.quiz_active:
        st.markdown("<div style='background-color:#343a40; color:white; padding:8px; border-radius:5px; display:flex;'> <div style='width:5%;'>#</div> <div style='width:55%;'>Сорилын нэр</div> <div style='width:40%; text-align:center;'>Хувилбарууд</div> </div>", unsafe_allow_html=True)
        for i, name in enumerate(UNITS):
            c1, c2 = st.columns([0.6, 0.4])
            c1.write(f"**{i+1}.** {name}")
            with c2:
                v_cols = st.columns(4)
                for j, v in enumerate(["A", "B", "C", "D"]):
                    if v_cols[j].button(v, key=f"q_btn_{i}_{v}"):
                        st.session_state.u_num, st.session_state.u_name, st.session_state.variant = i+1, name, v
                        st.session_state.quiz_active, st.session_state.start_time = True, time.time()
                        st.rerun()
            st.divider()
    else:
        rem = max(0, (40 * 60) - int(time.time() - st.session_state.start_time))
        st.markdown(f'<div class="timer-container">⏳ Үлдсэн хугацаа: {rem//60:02d}:{rem%60:02d}</div>', unsafe_allow_html=True)
        if st.button("⬅️ Буцах"): st.session_state.quiz_active = False; st.rerun()
        
        f_path = f"quiz_{st.session_state.u_num}_{st.session_state.variant}.xlsx" # Нэршил: quiz_1_A.xlsx
        if os.path.exists(f_path):
            df_q = pd.read_excel(f_path).head(15).reset_index()
            with st.form("quiz_engine"):
                ans_map = {}
                for idx, row in df_q.iterrows():
                    st.markdown(f"**Асуулт {idx+1}:**")
                    st.markdown(smart_math_render(row['Асуул?']))
                    ans_map[idx] = st.radio("Хариу:", ["A", "B", "C", "D"], key=f"qz_{idx}", horizontal=True, label_visibility="collapsed")
                    st.write("---")
                if st.form_submit_button("🏁 Дуусгах") or rem <= 0:
                    st.session_state.quiz_active = False
                    score = sum(1 for idx, row in df_q.iterrows() if ans_map[idx] == str(row['Хариу']).strip().upper())
                    st.success(f"### 🎉 Таны оноо: {score} / {len(df_q)} ({(score/len(df_q))*100:.1f}%)")
                    for idx, row in df_q.iterrows():
                        with st.expander(f"Асуулт {idx+1}: {'✅' if ans_map[idx] == str(row['Хариу']).strip().upper() else '❌'}"):
                            st.write(f"Зөв хариу: **{row['Хариу']}**")
                            if 'Бодолт' in row: st.info(f"**Бодолт:** {row['Бодолт']}")
                    st.stop()
        else: st.error(f"Файл олдсонгүй: {f_path}")
        if rem > 0: time.sleep(1); st.rerun()

# 8 & 9. БУСАД
elif st.session_state.selected_menu == "Клубын мэдээлэл": st.markdown("<h1>👥 Клуб</h1>", unsafe_allow_html=True)
elif st.session_state.selected_menu == "Хүүхдийн хүмүүжил": st.markdown("<h1>❤️ Хүмүүжил</h1>", unsafe_allow_html=True)
