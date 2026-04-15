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
    st.markdown('<p class="main-header" style="text-align: center;">⏳ Үнэлгээний нэгж 5: Сорил</p>', unsafe_allow_html=True)

    # Шалгалт эхлэх цагийг сешн дээр хадгалах
    if 'test_start_time' not in st.session_state:
        st.session_state.test_start_time = time.time()
    
    # Цаг харуулах талбар
    timer_placeholder = st.empty()
    
    # Нийт хугацаа 40 минут (2400 секунд)
    total_seconds = 40 * 60 
    elapsed = time.time() - st.session_state.test_start_time
    remaining = total_seconds - elapsed

    if remaining > 0:
        mins, secs = divmod(int(remaining), 60)
        # Цаг секунд бүрээр гүйж харагдах хэсэг
        timer_placeholder.markdown(f"""
            <div style="text-align: center; background-color: #f0f2f6; padding: 10px; border-radius: 10px; border: 2px solid #ffca28;">
                <h2 style="margin:0; color: #333;">🕒 Үлдсэн хугацаа: <span style="color: red;">{mins:02d}:{secs:02d}</span></h2>
            </div>
        """, unsafe_allow_html=True)

        with st.form("math_test_form"):
            st.write("### НЭГДҮГЭЭР ХЭСЭГ. СОНГОХ ДААЛГАВАР (12 даалгавар, 16 оноо)")
            
            q1 = st.radio("1. Тэгш өнцөгт △ABC-ийн ∠C=90° бол sinA харьцааг нэрлэнэ үү.", ["AC/AB", "BC/AB", "BC/AC", "AC/BC"], index=None)
            q2 = st.radio("2. Гурвалжны медианууд огтлолцлын цэгээрээ оройгоосоо тоолбол ямар харьцаагаар хуваагддаг вэ?", ["1:1", "1:2", "2:1", "3:1"], index=None)
            q3 = st.radio("3. Гурвалжны нэг оройгоос татсан биссектрис эсрэг талаа 4 см ба 6 см хэрчмүүдэд хуваажээ. Хэрэв биссектрис татсан оройд налсан нэг тал нь 8 см бол нөгөө талын уртыг ол.", ["12 см", "10 см", "14 см", "16 см"], index=None)
            q4 = st.radio("4. Тэгш өнцөгт гурвалжны катетууд 9 см ба 12 см бол гипотенузын уртыг ол.", ["13 см", "15 см", "17 см", "20 см"], index=None)
            q5 = st.radio("5. Тойргийн төвөөс хөвчид буусан перпендикуляр нь уг хөвчийг хэрхэн хуваадаг вэ?", ["2:1 харьцаагаар", "Гурав хуваана", "Хагаслан хуваана", "Хуваахгүй"], index=None)
            q6 = st.radio("6. Тойрогт багтсан өнцөг 40° бол түүнд тулсан нумын хэмжээг ол.", ["20°", "40°", "80°", "160°"], index=None)
            q7 = st.radio("7. Тэгш өнцөгт △ABC-ийн ∠C=90°, AC=12 см, tanA=3/4 бол катетын уртыг ол.", ["8 см", "9 см", "10 см", "16 см"], index=None)
            q8 = st.radio("8. Адил хажуут гурвалжны суурь 16 см, хажуу тал 10 см бол суурьт буусан өндрийг ол.", ["6 см", "8 см", "12 см", "5 см"], index=None)
            q9 = st.radio("9. Тойргийн радиус 13 см. Тойргийн төвөөс 5 см зайд орших хөвчийн уртыг ол.", ["12 см", "24 см", "26 см", "10 см"], index=None)
            q10 = st.radio("10. Тойргийн огтлолцсон хоёр хөвчийн нэг нь 4 см ба 9 см хэрчмүүдэд хуваагджээ. Нөгөө хөвчийн нэг хэсэг нь 6 см бол үлдсэн хэсгийг ол.", ["4 см", "5 см", "6 см", "8 см"], index=None)
            q11 = st.radio("11. Тойргийн гадна орших цэгээс тойрогт татсан шүргэгч 12 см, огтлогчийн гадна хэсэг 8 см бол огтлогчийн нийт уртыг ол.", ["15 см", "16 см", "18 см", "20 см"], index=None)
            q12 = st.radio("12. Тойргийн гадна оройтой өнцгийн хашиж буй их нум 110°, бага нум 30° бол уг өнцгийн хэмжээг ол.", ["80°", "140°", "40°", "70°"], index=None)

            st.write("---")
            st.write("### ХОЁРДУГААР ХЭСЭГ. НӨХӨХ ДААЛГАВАР (3 даалгавар, 11 оноо)")
            st.write("13. Монгол гэрийн тооно: Гэрийн тоононы гол хөндлөвч (хөвч) нь тойргийн төвөөс 9 см зайд оршино. Хэрэв тойргийн радиус 15 см бол:")
            st.latex(r"\sqrt{15^2 - 9^2}")
            q13 = st.text_input("(1) Хөвчийг хагаслан хуваах хэрчмийн урт нь:")
            
            st.write("14. Монгол гэрийн бүтэц: Гэрийн хананы өндөр 150 см, тоононы өндөр 230 см. Хэрэв унины хэвтээ тусгал 60 см бол:")
            q14 = st.text_input("(1) Унины уртыг олохын тулд катетууд нь 60 см ба хэд байх вэ? (Өндрийн зөрүү):")
            
            st.write("15. Чингис хааны морьт хөшөө: Хэрэв харагдах их нум 130°, бага нум 50° бол:")
            q15 = st.text_input("(1) Сурагчийн харах өнцөг хэдэн градус байх вэ?")

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
                st.success(f"Сорил амжилттай дууслаа! Таны авсан оноо: {score}")
    else:
        st.error("⌛ Шалгалтын хугацаа дууссан байна!")
        if st.button("Шалгалтыг дахин эхлүүлэх"):
            del st.session_state.test_start_time
            st.rerun()
