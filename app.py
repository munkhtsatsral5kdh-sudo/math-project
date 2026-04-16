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
    st.markdown("<h2 style='text-align: center; color: #0b4ab1;'>📝 Онлайн сорил, шалгалт</h2>", unsafe_allow_html=True)
    
    # Сэдвийн нэрс
    units = [
        "Тоон олонлог, зэрэг, язгуур", "Харьцаа, пропорц, процент",
        "Алгебрын илэрхийлэл, тэгшитгэл", "Дараалал, функц",
        "Өнцөг, дүрс, байгуулалт", "Байршил, хөдөлгөөн",
        "Хэмжигдэхүүн", "Магадлал, статистик"
    ]

    # Системийн төлөв
    if 'quiz_page' not in st.session_state: st.session_state.quiz_page = "list"
    if 'current_unit' not in st.session_state: st.session_state.current_unit = None
    if 'current_variant' not in st.session_state: st.session_state.current_variant = None

    # --- 1. ЖАГСААЛТ (image_bfe462.jpg загвар) ---
    if st.session_state.quiz_page == "list":
        st.markdown("<div style='background:#343a40; color:white; padding:10px; border-radius:5px; display:flex; font-weight:bold;'><div style='width:10%;'>#</div><div style='width:60%;'>Сорилын нэр</div><div style='width:30%; text-align:center;'>Төлөв</div></div>", unsafe_allow_html=True)
        for i, name in enumerate(units):
            col1, col2, col3 = st.columns([0.5, 6, 3])
            col1.write(f"**{i+1}**")
            if col2.button(f"➔ IX анги | {name}", key=f"unit_link_{i}", use_container_width=True):
                st.session_state.current_unit = name
                st.session_state.quiz_page = "variant_select" # Хувилбар сонгох руу
                st.rerun()
            col3.markdown("<div style='text-align:center; color:green;'>Нээлттэй</div>", unsafe_allow_html=True)
            st.markdown("<hr style='margin:2px;'>", unsafe_allow_html=True)

    # --- 2. ХУВИЛБАР СОНГОХ (image_bff2a5.png загварын дагуу) ---
    elif st.session_state.quiz_page == "variant_select":
        if st.button("⬅️ Буцах"):
            st.session_state.quiz_page = "list"; st.rerun()
        
        st.markdown(f"<h3 style='text-align:center; color:#0b4ab1;'>{st.session_state.current_unit}</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;'>Шалгалтын хувилбараа сонгоно уу:</p>", unsafe_allow_html=True)
        
        # 4 Хувилбарыг товчлуур хэлбэрээр харуулах
        v_cols = st.columns(4)
        v_names = ["Хувилбар А", "Хувилбар Б", "Хувилбар В", "Хувилбар Г"]
        for idx, v_name in enumerate(v_names):
            if v_cols[idx].button(v_name, use_container_width=True, type="secondary"):
                st.session_state.current_variant = v_name
                st.session_state.quiz_page = "info"; st.rerun()

    # --- 3. СОРИЛ ЭХЛЭХ МЭДЭЭЛЭЛ (image_bff2a5.png загвар) ---
    elif st.session_state.quiz_page == "info":
        if st.button("⬅️ Хувилбар солих"):
            st.session_state.quiz_page = "variant_select"; st.rerun()
            
        st.markdown(f"<h2 style='text-align:center;'>{st.session_state.current_variant}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; color:gray;'>Сэдэв: {st.session_state.current_unit}</p>", unsafe_allow_html=True)
        
        col_start = st.columns([1, 2, 1])
        with col_start[1]:
            # Тэр том ногоон товчлуур
            if st.button("🚀 СОРИЛ ЭХЛЭХ", type="primary", use_container_width=True):
                st.session_state.quiz_page = "active"; st.session_state.show_mode = "test"; st.rerun()
            
            # Доорх жижиг товчлуурууд
            s1, s2, s3 = st.columns(3)
            if s1.button("📊 Дүн"): st.toast("Дүн байхгүй")
            if s2.button("❌ Алдаа"): st.session_state.quiz_page = "active"; st.session_state.show_mode = "error"; st.rerun()
            if s3.button("📖 Бодолт"): st.session_state.quiz_page = "active"; st.session_state.show_mode = "solution"; st.rerun()

    # --- 4. ИДЭВХТЭЙ СОРИЛ ---
    elif st.session_state.quiz_page == "active":
        if st.button("⬅️ Зогсоох"):
            st.session_state.quiz_page = "info"; st.rerun()
        
        st.info(f"📍 {st.session_state.current_unit} | {st.session_state.current_variant}")

        if os.path.exists("data_bank.xlsx"):
            df = pd.read_excel("data_bank.xlsx")
            # Шүүлтүүр: Нэгжийн дугаар болон Хувилбар (А, Б, В, Г)
            unit_num = units.index(st.session_state.current_unit) + 1
            variant_letter = st.session_state.current_variant.split(" ")[-1] # "А", "Б" г.м
            
            # Excel-д 'Хувилбар' багана байх ёстой
            q_df = df[(df['Нэгж'].astype(str).str.contains(str(unit_num))) & (df['Хувилбар'] == variant_letter)]
            
            if q_df.empty:
                st.warning("Энэ хувилбарт бодлого ороогүй байна.")
            else:
                for idx, row in q_df.iterrows():
                    st.markdown(smart_math_render(row['Асуулт']))
                    st.radio("Хариулт:", ["A", "B", "C", "D"], key=f"q_{idx}", horizontal=True)
                    if st.session_state.show_mode in ["error", "solution"]:
                        st.success(f"Зөв хариу: {row['Хариу']}")
                        with st.expander("Бодолт харах"): st.write(row.get('Тайлбар', 'Байхгүй'))
                    st.write("---")
# 8. КЛУБЫН МЭДЭЭЛЭЛ
elif st.session_state.selected_menu == "Клубын мэдээлэл":
    st.markdown("<h1 style='color: #0b4ab1;'>👥 Математикийн клуб</h1>", unsafe_allow_html=True)
    st.write("Манай клубын үйл ажиллагаа, бүртгэл энд байна.")

# 9. ХҮҮХДИЙН ХҮМҮҮЖИЛ
elif st.session_state.selected_menu == "Хүүхдийн хүмүүжил":
    st.markdown("<h1 style='color: #0b4ab1;'>❤️ Хүүхдийн хүмүүжил, зөвлөгөө</h1>", unsafe_allow_html=True)
    st.info("Хүүхдээ хэрхэн хөгжүүлэх талаарх багшийн зөвлөгөөнүүд.")
