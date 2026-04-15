import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64

# 1. Сайтын ерөнхий тохиргоо
st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# 2. ДИЗАЙН (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    [data-testid="stSidebar"] { background-color: #004aad !important; min-width: 300px !important; }
    .sidebar-title { color: #ffffff !important; text-align: center; font-size: 40px !important; font-weight: bold; padding: 20px 0; border-bottom: 2px solid rgba(255,255,255,0.3); margin-bottom: 20px; }
    .main-header { color: #004aad !important; font-size: 55px !important; font-weight: 900; margin: 0px 0px 15px 0px !important; line-height: 1.1 !important; }
    .goal-text { font-size: 24px !important; color: #333; line-height: 1.6; background: white; padding: 35px; border-left: 15px solid #004aad; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); text-align: justify; }
    .logo-container { display: flex; justify-content: center; align-items: center; }
    .custom-card { background: white; border-radius: 25px; padding: 35px 20px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.05); transition: all 0.3s ease; border: 1px solid #eee; height: 280px; }
    .custom-card:hover { transform: translateY(-10px); box-shadow: 0 15px 35px rgba(0,74,173,0.15); }
    .card-icon { font-size: 60px; margin-bottom: 15px; }
    .card-title { color: #004aad; font-size: 24px; font-weight: bold; }
    .quiz-card { background: white; padding: 30px; border-radius: 20px; border-top: 10px solid #004aad; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-top: 20px; }
    [data-testid="stHeaderActionElements"], .stAppDeployButton { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Цэс)
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None, 
        options=["Нүүр хуудас", "Цахим контент", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил төлөвшил МХБ"],
        icons=['house', 'play-btn', 'book', 'pencil-square', 'people', 'heart'],
        default_index=0,
        styles={
            "container": {"background-color": "#004aad", "padding": "0"},
            "icon": {"color": "white", "font-size": "20px"}, 
            "nav-link": {"font-size": "17px", "color": "white", "font-family": "Arial", "font-weight": "bold", "margin": "5px"},
            "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)"},
        }
    )

# 4. АГУУЛГА
if selected == "Нүүр хуудас":
    col1, col2 = st.columns([1, 1.4], gap="large")
    with col1:
        logo_path = "logo.gif" 
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                data = f.read()
                data_url = base64.b64encode(data).decode("utf-8")
            st.markdown(f'<div class="logo-container"><img src="data:image/gif;base64,{data_url}" width="100%"></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<p class="main-header">Бидний зорилго</p>', unsafe_allow_html=True)
        st.markdown('<div class="goal-text">Математикийн ертөнцөөр хамтдаа аялж, сонирхолтой цахим хичээл, бодлогын сангаар дамжуулан өөрийн мэдлэг чадвараа бие даан ахиулж, ирээдүйн амжилтынхаа эхлэлийг өнөөдөр тавьцгаая!</div>', unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="medium")
    cards = [
        {"icon": "📺", "title": "Цахим контент", "desc": "Видео хичээл болон интерактив материалууд"},
        {"icon": "📚", "title": "Даалгаврын сан", "desc": "Өөрийгөө сорих бодлого, дасгалууд"},
        {"icon": "📝", "title": "Сорил", "desc": "Мэдлэгээ шалгах онлайн шалгалтууд"}
    ]
    for i, col in enumerate([c1, c2, c3]):
        with col:
            st.markdown(f'<div class="custom-card"><div class="card-icon">{cards[i]["icon"]}</div><div class="card-title">{cards[i]["title"]}</div><p style="color:#777; font-size:15px; margin-top:10px;">{cards[i]["desc"]}</p></div>', unsafe_allow_html=True)

elif selected == "Сорил":
    import time
    from datetime import datetime, timedelta

    st.markdown('<p class="main-header" style="text-align: center;">⏳ Үнэлгээний нэгж 5: Сорил</p>', unsafe_allow_html=True)

    # 1. Шалгалт эхлэх цагийг хадгалах
    if 'test_start_time' not in st.session_state:
        st.session_state.test_start_time = time.time()
    
    # 2. Хугацаа тоологч (40 минут = 2400 секунд)
    total_seconds = 40 * 60 
    elapsed_time = time.time() - st.session_state.test_start_time
    remaining_seconds = total_seconds - elapsed_time

    if remaining_seconds > 0:
        # Цагийг дэлгэц дээр гүйлгэж харуулах
        mins, secs = divmod(int(remaining_seconds), 60)
        timer_text = f"🕒 Үлдсэн хугацаа: {mins:02d}:{secs:02d}"
        
        # Цаг дуусахад ойртоход улаан өнгөтэй болгох
        if remaining_seconds < 300: # Сүүлийн 5 минут
            st.error(timer_text)
        else:
            st.warning(timer_text)

        with st.form("math_test_form"):
            st.info("Санамж: 1-12 хүртэлх асуултаас зөв хариултыг сонгоно. 13-15 хүртэлх асуултад зөвхөн тоон хариултыг бичнэ үү.")
            
            st.write("### I ХЭСЭГ. СОНГОХ ДААЛГАВАР")
            q1 = st.radio("1. Тэгш өнцөгт △ABC-ийн ∠C=90° бол sinA харьцааг нэрлэнэ үү?", ["AC/AB", "BC/AB", "BC/AC", "AC/BC"], index=None)
            q2 = st.radio("2. Гурвалжны медианууд огтлолцлын цэгээрээ оройгоосоо тоолбол ямар харьцаагаар хуваагддаг вэ?", ["1:1", "1:2", "2:1", "3:1"], index=None)
            q3 = st.radio("3. Биссектрис эсрэг талаа 4 см ба 6 см-ээр хуваасан, налсан тал нь 8 см бол нөгөө талыг ол.", ["12 см", "10 см", "14 см", "16 см"], index=None)
            q4 = st.radio("4. Катетууд 9 см ба 12 см бол гипотенузыг ол.", ["13 см", "15 см", "17 см", "20 см"], index=None)
            q5 = st.radio("5. Хөвчид буусан перпендикуляр хөвчийг хэрхэн хуваадаг вэ?", ["2:1 харьцаагаар", "Хагаслан хуваана", "Гурав хуваана", "Хуваахгүй"], index=None)
            q6 = st.radio("6. Багтсан өнцөг 40° бол тулсан нумын хэмжээг ол.", ["20°", "40°", "80°", "160°"], index=None)
            q7 = st.radio("7. △ABC-ийн ∠C=90°, AC=12 см, tanA=3/4 бол BC катетыг ол.", ["8 см", "9 см", "10 см", "16 см"], index=None)
            q8 = st.radio("8. Суурь 16 см, хажуу тал 10 см бол суурьт буусан өндрийг ол.", ["6 см", "8 см", "12 см", "5 см"], index=None)
            q9 = st.radio("9. Радиус 13 см, төвөөс хөвч хүртэл 5 см бол хөвчийн уртыг ол.", ["12 см", "24 см", "26 см", "10 см"], index=None)
            q10 = st.radio("10. Хөвч 4 см ба 9 см-ээр хуваагдсан. Нөгөө хөвчийн нэг хэсэг 6 см бол нөгөөг ол.", ["4 см", "5 см", "6 см", "8 см"], index=None)
            q11 = st.radio("11. Шүргэгч 12 см, огтлогчийн гадна хэсэг 8 см бол нийт уртыг ол.", ["15 см", "16 см", "18 см", "20 см"], index=None)
            q12 = st.radio("12. Их нум 110°, бага нум 30° бол гадна оройтой өнцгийг ол.", ["80°", "140°", "40°", "70°"], index=None)

            st.write("---")
            st.write("### II ХЭСЭГ. НӨХӨХ ДААЛГАВАР")
            st.latex(r"\text{13. } \sqrt{15^2 - 9^2}")
            q13 = st.text_input("13. Хөвчийг хагаслан хуваах хэрчмийн урт:")
            st.latex(r"\text{14. } h = 230 - 150")
            q14 = st.text_input("14. Унины өндрийн зөрүү (катет):")
            st.latex(r"\text{15. } \alpha = (130^\circ - 50^\circ) / 2")
            q15 = st.text_input("15. Сурагчийн харах өнцөг:")

            submitted = st.form_submit_button("Шалгалтыг дуусгах")

            if submitted:
                score = 0
                if q1 == "BC/AB": score += 1
                if q2 == "2:1": score += 1
                if q3 == "12 см": score += 1
                if q4 == "15 см": score += 1
                if q5 == "Хагаслан хуваана": score += 1
                if q6 == "80°": score += 1
                if q7 == "9 см": score += 1
                if q8 == "6 см": score += 1
                if q9 == "24 см": score += 1
                if q10 == "6 см": score += 1
                if q11 == "18 см": score += 1
                if q12 == "40°": score += 1
                if q13 == "12": score += 2
                if q14 == "80": score += 2
                if q15 == "40": score += 2
                
                st.balloons()
                st.success(f"Сорил дууслаа! Таны авсан оноо: {score}")
                # Дахин шалгалт өгөх боломжтой болгохын тулд цагийг устгаж болно
                # del st.session_state.test_start_time
    else:
        st.error("⌛ Шалгалтын хугацаа дууссан байна!")
        if st.button("Шалгалтыг дахин эхлүүлэх"):
            del st.session_state.test_start_time
            st.rerun()
