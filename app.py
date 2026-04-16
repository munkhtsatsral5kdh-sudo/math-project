import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import pandas as pd
import re

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

# 6. ДААЛГАВРЫН САН
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
                with st.form(key=f"form_{i}"):
                    st.markdown('<div class="math-card">', unsafe_allow_html=True)
                    st.markdown(f"### 📝 Бодлого {i+1}"); st.markdown(smart_math_render(row['Асуулт']))
                    ans = st.radio("Хариу сонгох:", ["A", "B", "C", "D"], key=f"ans_{i}", horizontal=True)
                    if st.form_submit_button("Шалгах"):
                        correct = str(row['Хариу']).strip().upper()
                        if ans == correct: st.success("Зөв! ✅"); st.balloons()
                        else: st.error(f"Буруу байна. Зөв хариу: {correct}")
                    st.markdown('</div>', unsafe_allow_html=True)
    else: st.warning("data_bank.xlsx файл олдсонгүй.")

# 7. СОРИЛ
elif st.session_state.selected_menu == "Сорил":
    st.markdown("<h2 style='text-align: center; color: #0b4ab1;'>📝 Математикийн Онлайн Сорил</h2>", unsafe_allow_html=True)
    
    # Сэдвийн нэрс (Зураг дээрх 8 нэгж)
    units = [
        "Тоон олонлог, зэрэг, язгуур", "Харьцаа, пропорц, процент",
        "Алгебрын илэрхийлэл, тэгшитгэл", "Дараалал, функц",
        "Өнцөг, дүрс, байгуулалт", "Байршил, хөдөлгөөн",
        "Хэмжигдэхүүн", "Магадлал, статистик"
    ]

    # Системийн төлөв хадгалах
    if 'quiz_page' not in st.session_state: st.session_state.quiz_page = "list"
    if 'current_unit' not in st.session_state: st.session_state.current_unit = None
    if 'show_mode' not in st.session_state: st.session_state.show_mode = "test"

    # --- 1. ЖАГСААЛТ ХАРАГДАХ (image_bfe462.jpg загвар) ---
    if st.session_state.quiz_page == "list":
        st.markdown("<div style='background:#f8f9fa; padding:10px; border-radius:5px; font-weight:bold; display:flex; justify-content:space-between;'><div># Сорилын нэр</div><div style='margin-right:150px;'>Удирдах хэсэг</div></div>", unsafe_allow_html=True)
        st.write("")

        for i, unit_name in enumerate(units):
            col_name, col_btns = st.columns([2, 2])
            with col_name:
                st.write(f"**{i+1}.** IX анги | {unit_name}")
            with col_btns:
                b1, b2, b3, b4 = st.columns(4)
                if b1.button("🚀 Эхлэх", key=f"start_{i}"):
                    st.session_state.current_unit = unit_name
                    st.session_state.quiz_page = "active"; st.session_state.show_mode = "test"; st.rerun()
                if b2.button("📊 Дүн", key=f"score_{i}"):
                    st.toast("Дүн хараахан гараагүй")
                if b3.button("❌ Алдаа", key=f"err_{i}"):
                    st.session_state.current_unit = unit_name
                    st.session_state.quiz_page = "active"; st.session_state.show_mode = "error"; st.rerun()
                if b4.button("📖 Бодолт", key=f"sol_{i}"):
                    st.session_state.current_unit = unit_name
                    st.session_state.quiz_page = "active"; st.session_state.show_mode = "solution"; st.rerun()
            st.markdown("<hr style='margin:2px;'>", unsafe_allow_html=True)

    # --- 2. ИДЭВХТЭЙ СОРИЛЫН ЦОНХ (4 хувилбартай) ---
    elif st.session_state.quiz_page == "active":
        c_head, c_time = st.columns([5, 1])
        if c_head.button("⬅️ Буцах"):
            st.session_state.quiz_page = "list"; st.rerun()
        c_time.markdown("<div style='background:black; color:red; padding:5px; text-align:center; border-radius:5px; font-weight:bold;'>⏳ 40:00</div>", unsafe_allow_html=True)
        
        st.info(f"📍 Сэдэв: {st.session_state.current_unit}")

        if os.path.exists("data_bank.xlsx"):
            df = pd.read_excel("data_bank.xlsx")
            # Excel-ийн 'Нэгж' баганаас харгалзах дугаараар шүүх
            unit_idx = units.index(st.session_state.current_unit) + 1
            q_df = df[df['Нэгж'].astype(str).str.contains(str(unit_idx))].head(5)

            if q_df.empty:
                st.warning("Энэ нэгжид бодлого хараахан ороогүй байна.")
            else:
                for idx, row in q_df.iterrows():
                    st.markdown(smart_math_render(row['Асуулт'])) #
                    
                    # 4 ХУВИЛБАРТАЙ СОНГОЛТ (A, B, C, D)
                    st.radio(f"Хариулт сонгох {idx}:", ["A", "B", "C", "D"], key=f"quiz_opt_{idx}", horizontal=True, label_visibility="collapsed")
                    
                    # Алдаа болон Бодолт харах үед тайлбар гарна
                    if st.session_state.show_mode in ["error", "solution"]:
                        st.success(f"Зөв хариу: {row['Хариу']}")
                        with st.expander("📖 Зөв бодолт харах"):
                            st.write(row.get('Тайлбар', 'Бодолт ороогүй байна.'))
                    st.write("---")
                
                if st.session_state.show_mode == "test":
                    if st.button("🏁 Шалгалт дуусгах", use_container_width=True):
                        st.balloons(); st.session_state.quiz_page = "list"; st.rerun()
# 8. КЛУБЫН МЭДЭЭЛЭЛ
elif st.session_state.selected_menu == "Клубын мэдээлэл":
    st.markdown("<h1 style='color: #0b4ab1;'>👥 Математикийн клуб</h1>", unsafe_allow_html=True)
    st.write("Манай клубын үйл ажиллагаа, бүртгэл энд байна.")

# 9. ХҮҮХДИЙН ХҮМҮҮЖИЛ
elif st.session_state.selected_menu == "Хүүхдийн хүмүүжил":
    st.markdown("<h1 style='color: #0b4ab1;'>❤️ Хүүхдийн хүмүүжил, зөвлөгөө</h1>", unsafe_allow_html=True)
    st.info("Хүүхдээ хэрхэн хөгжүүлэх талаарх багшийн зөвлөгөөнүүд.")
