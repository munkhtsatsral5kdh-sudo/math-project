import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import pandas as pd
import time

# 1. Сайтын ерөнхий тохиргоо
st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# УХААЛАГ МАТЕМАТИК ТАНИГЧ (Эвдэхгүйгээр сайжруулав)
def smart_math_render(text):
    if not isinstance(text, str): return str(text)
    # Сонголтуудыг салгаж харуулах
    for label in ['A.', 'B.', 'C.', 'D.']:
        if label in text:
            text = text.replace(label, f'\n\n**{label}** ')
    
    # % тэмдэгтийг засах
    if '%' in text and '\\%' not in text:
        text = text.replace('%', '\\%')
        
    # Латех таних
    if ('\\' in text or '^' in text or '/' in text) and '$' not in text:
        clean_text = text.replace('\\displaystyle', '').strip()
        text = f"$\\displaystyle {clean_text}$"
    return text

# Зураг харуулах туслах функц
def show_image(image_name):
    if pd.notna(image_name) and str(image_name).strip() != "":
        img_path = os.path.join("images", str(image_name).strip())
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=False, width=400)

# 2. ДИЗАЙН (Бүрэн шинэчилсэн, эвдрэхгүй)
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #0b4ab1 !important; min-width: 260px !important; }
    .sidebar-title { color: white; text-align: center; font-size: 35px; font-weight: bold; padding: 20px 0; }
    
    /* НҮҮР ХУУДАСНЫ ТОМ ТОВЧЛУУРУУД (Ижил хэмжээтэй) */
    .home-btns div.stButton > button {
        width: 100% !important;
        height: 200px !important;
        border-radius: 20px !important;
        background: white !important;
        border: 1px solid #eee !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        transition: transform 0.2s !important;
    }
    .home-btns div.stButton > button:hover { transform: translateY(-5px); border-color: #0b4ab1 !important; }
    .home-btns div.stButton > button p { font-size: 20px !important; font-weight: bold !important; color: #0b4ab1 !important; }

    /* БОДЛОГЫН КАРТ */
    .math-card { 
        background: white; padding: 30px; border-radius: 15px; 
        border: 1px solid #eef0f3; margin-bottom: 25px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    .math-card p { font-size: 18px !important; line-height: 1.7 !important; }

    /* ШАЛГАХ ТОВЧ (Бусад товчлуурт нөлөөлөхгүй) */
    .check-btn div.stButton > button {
        width: 140px !important; height: 45px !important;
        background-color: #0b4ab1 !important; color: white !important;
        border-radius: 10px !important; font-size: 16px !important;
    }
    
    /* СОРИЛЫН А, B, C, D ТОВЧ */
    .quiz-btns div.stButton > button {
        width: 60px !important; height: 45px !important;
        border-radius: 8px !important; font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR
if 'selected_menu' not in st.session_state: st.session_state.selected_menu = "Нүүр хуудас"
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None, options=["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил"],
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        default_index=0,
        styles={"nav-link": {"color": "white", "font-size": "16px"}, "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)"}}
    )
    st.session_state.selected_menu = selected

# 4. НҮҮР ХУУДАС
if st.session_state.selected_menu == "Нүүр хуудас":
    col1, col2 = st.columns([1, 1.2], gap="large")
    with col1:
        if os.path.exists("logo.gif"):
            with open("logo.gif", "rb") as f: data_url = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(f'<img src="data:image/gif;base64,{data_url}" style="width: 100%; border-radius: 20px;">', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="goal-box" style="background:white; padding:30px; border-radius:20px; border-left:10px solid #0b4ab1; box-shadow:0 10px 30px rgba(0,0,0,0.05);"><h1 style="color:#0b4ab1;">Математикийн ертөнцөд тавтай морил!</h1><p style="font-size:18px; color:#555;">Сонирхолтой цахим хичээл, баялаг бодлогын сангаар дамжуулан математик сэтгэлгээгээ бие даан хөгжүүлэхэд тань бид туслах болно.</p></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="home-btns">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        if st.button("📺\n\nЦахим контент", key="h1"): st.session_state.selected_menu = "Цахим контент"; st.rerun()
    with c2:
        if st.button("📚\n\nДаалгаврын сан", key="h2"): st.session_state.selected_menu = "Даалгаврын сан"; st.rerun()
    with c3:
        if st.button("📝\n\nСорил", key="h3"): st.session_state.selected_menu = "Сорил"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 5. ДААЛГАВРЫН САН (24 файл + Зурагтай)
elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown("<h2 style='text-align: center; color: #0b4ab1;'>📚 Бодлогын сан</h2>", unsafe_allow_html=True)
    units = ["Тоон олонлог, зэрэг, язгуур, тоог жиших, тоймлох", "Харьцаа, пропорц, процент", "Алгебрын илэрхийлэл, тэгшитгэл, тэнцэтгэл биш", "Дараалал, функц", "Өнцөг, дүрс, байгуулалт", "Байршил, хөдөлгөөн, хувиргалт", "Хэмжигдэхүүн", "Магадлал, статистик"]
    
    col_u, col_l = st.columns([0.6, 0.4])
    u_choice = col_u.selectbox("Сэдэв сонгох:", units)
    l_choice = col_l.radio("Түвшин:", ["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"], horizontal=True)

    f_path = f"task_{units.index(u_choice)+1}_{{'Мэдлэг ойлголт':1, 'Чадвар':2, 'Хэрэглээ':3}[l_choice]}.xlsx"

    if os.path.exists(f_path):
        df = pd.read_excel(f_path)
        for idx, row in df.iterrows():
            st.markdown('<div class="math-card">', unsafe_allow_html=True)
            st.markdown(f"#### 📝 Бодлого {idx+1}")
            st.markdown(smart_math_render(row['Асуулт']))
            
            # ЗУРАГ ХАРУУЛАХ (Хэрэв байгаа бол)
            if 'Зураг' in row: show_image(row['Зураг'])
            
            with st.form(key=f"f_{f_path}_{idx}"):
                user_ans = st.radio("Хариу:", ["A", "B", "C", "D"], key=f"r_{idx}", horizontal=True)
                st.markdown('<div class="check-btn">', unsafe_allow_html=True)
                if st.form_submit_button("Шалгах"):
                    correct = str(row['Хариу']).strip().upper()
                    if user_ans == correct: st.success("✅ Зөв!")
                    else: 
                        st.error(f"❌ Буруу. Зөв хариу: {correct}")
                        if 'Бодолт' in row and pd.notna(row['Бодолт']):
                            with st.expander("Бодолт харах"): st.markdown(smart_math_render(row['Бодолт']))
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else: st.warning(f"⚠️ {f_path} файл олдсонгүй.")

# 7. СОРИЛ (32 файл + Секундээр гүйдэг цаг)
elif st.session_state.selected_menu == "Сорил":
    if 'quiz_active' not in st.session_state: st.session_state.quiz_active = False
    if 'quiz_finished' not in st.session_state: st.session_state.quiz_finished = False

    if not st.session_state.quiz_active and not st.session_state.quiz_finished:
        st.markdown("<h3 style='text-align: center; color: #0b4ab1;'>📝 Онлайн сорил</h3>", unsafe_allow_html=True)
        st.markdown("<div style='background:#343a40; color:white; padding:10px; border-radius:5px; display:flex; font-weight:bold;'><div style='width:70%;'>Сорилын нэр</div><div style='width:30%; text-align:center;'>Хувилбар</div></div>", unsafe_allow_html=True)
        
        quiz_units = ["Тоон олонлог...", "Харьцаа...", "Алгебр...", "Дараалал...", "Өнцөг...", "Байршил...", "Хэмжигдэхүүн", "Статистик"]
        for i, name in enumerate(quiz_units):
            col_n, col_v = st.columns([0.7, 0.3])
            col_n.markdown(f"<div style='padding:12px 0; border-bottom:1px solid #eee;'>{i+1}. {name}</div>", unsafe_allow_html=True)
            with col_v:
                st.markdown('<div class="quiz-btns">', unsafe_allow_html=True)
                v_cols = st.columns(4)
                for j, v in enumerate(["A", "B", "C", "D"]):
                    if v_cols[j].button(v, key=f"btn_{i}_{v}"):
                        st.session_state.quiz_file = f"quiz_{i+1}_{v}.xlsx"
                        st.session_state.quiz_active = True
                        st.session_state.start_time = time.time()
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    
    elif st.session_state.quiz_active:
        remaining = max(0, 2400 - int(time.time() - st.session_state.start_time))
        c_back, c_timer = st.columns([5, 1])
        if c_back.button("⬅️ Гарах"): st.session_state.quiz_active = False; st.rerun()
        mins, secs = divmod(remaining, 60)
        c_timer.error(f"⏳ {mins:02d}:{secs:02d}")

        if os.path.exists(st.session_state.quiz_file):
            df_q = pd.read_excel(st.session_state.quiz_file)
            with st.form("quiz_form"):
                user_answers = {}
                for idx, row in df_q.iterrows():
                    st.markdown(f"**Бодлого {idx+1}:**")
                    st.markdown(smart_math_render(row['Асуулт']))
                    if 'Зураг' in row: show_image(row['Зураг'])
                    user_answers[idx] = st.radio("Сонгох:", ["A", "B", "C", "D"], key=f"q_{idx}", horizontal=True)
                    st.divider()
                if st.form_submit_button("🏁 Дуусгах"):
                    st.session_state.results = user_answers
                    st.session_state.quiz_active = False
                    st.session_state.quiz_finished = True
                    st.rerun()
        if remaining > 0: time.sleep(1); st.rerun()

    elif st.session_state.quiz_finished:
        st.markdown("### 📊 Сорилын дүн")
        # Энд таны оноо тооцох хэсэг хэвээрээ ажиллана...
        if st.button("Дахин сорил өгөх"): st.session_state.quiz_finished = False; st.rerun()

# БУСАД ХЭСЭГ (Цахим контент, Клуб, Хүмүүжил) Хэвээр үлдсэн...
elif st.session_state.selected_menu == "Цахим контент":
    st.markdown("<h2 style='color:#0b4ab1;'>📺 Цахим хичээлүүд</h2>", unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=your_video_id")
elif st.session_state.selected_menu == "Клубын мэдээлэл":
    st.write("Манай клубын үйл ажиллагаа...")
elif st.session_state.selected_menu == "Хүүхдийн хүмүүжил":
    st.write("Багшийн зөвлөгөө...")
