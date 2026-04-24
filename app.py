import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import pandas as pd
import time

st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# ── SESSION STATE ЭХЛҮҮЛЭХ ──────────────────────────────────────────────────
def init_state():
    defaults = {
        "selected_menu": "Нүүр хуудас",
        "quiz_active": False,
        "quiz_finished": False,
        "quiz_file": None,
        "quiz_results": {},
        "std_info": {},
        "start_time": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── КЭШТЭЙ EXCEL УНШИГЧ — удаашралын гол засвар ─────────────────────────────
@st.cache_data(show_spinner=False)
def load_excel(path: str) -> pd.DataFrame | None:
    """Файлыг нэг удаа уншиж кэшэлнэ. Дахин ачааллах үед дискнээс унших хэрэггүй."""
    if os.path.exists(path):
        return pd.read_excel(path)
    return None

# ── МАТЕМАТИК БИЧИГЛЭЛ ТАНИГЧ ────────────────────────────────────────────────
def smart_math_render(text):
    if not isinstance(text, str):
        return str(text)
    for label in ["A.", "B.", "C.", "D."]:
        text = text.replace(label, f"\n\n**{label}**")
    if any(kw in text for kw in ["\\", "^", "_", "{", "}"]) and "$" not in text:
        return f"$\\displaystyle {text.replace('\\displaystyle','').strip()}$"
    return text

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.stApp { background-color: white; }
[data-testid="stSidebar"] { background-color: #0b4ab1 !important; min-width: 260px !important; }
.sidebar-title { color: white; text-align: center; font-size: 45px; font-weight: bold; padding: 20px 0; }
.goal-box {
    background: white; padding: 25px; border-radius: 20px;
    border: 1px solid #f0f2f6; border-left: 10px solid #0b4ab1;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}
.main-header { color: #0b4ab1; font-size: 45px; font-weight: 800; line-height: 1.1; }
.nav-btn {
    display: block; width: 100%; padding: 40px 10px;
    border-radius: 20px; border: 1px solid #e8eaf0;
    background: #fdfdfd; text-align: center;
    font-size: 20px; font-weight: bold; color: #0b4ab1;
    cursor: pointer; box-shadow: 0 6px 20px rgba(0,0,0,0.05);
    transition: transform 0.1s;
}
.nav-btn:hover { transform: translateY(-2px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
MENU_OPTIONS = ["Нүүр хуудас", "Цахим контент", "Даалгаврын сан",
                "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил"]
MENU_ICONS  = ["house", "play-btn", "book", "pencil-square", "people", "heart"]

with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None,
        options=MENU_OPTIONS,
        icons=MENU_ICONS,
        default_index=MENU_OPTIONS.index(st.session_state.selected_menu)
            if st.session_state.selected_menu in MENU_OPTIONS else 0,
        styles={
            "container": {"background-color": "#0b4ab1"},
            "nav-link": {"color": "white"},
            "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)"},
        },
    )
    if selected != st.session_state.selected_menu:
        st.session_state.selected_menu = selected
        st.rerun()

# ── НҮҮР ХУУДАС ──────────────────────────────────────────────────────────────
if st.session_state.selected_menu == "Нүүр хуудас":
    col1, col2 = st.columns([1, 1.2], gap="large")

    with col1:
        if os.path.exists("logo.gif"):
            with open("logo.gif", "rb") as f:
                data_url = base64.b64encode(f.read()).decode()
            st.markdown(
                f'<img src="data:image/gif;base64,{data_url}" style="width:100%;border-radius:20px;">',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div style="height:250px;background:#e8f0fe;border-radius:20px;'
                'display:flex;align-items:center;justify-content:center;'
                'font-size:60px;">📐</div>',
                unsafe_allow_html=True,
            )

    with col2:
        st.markdown(
            '<div class="goal-box">'
            '<div class="main-header">Математикийн ертөнцөд тавтай морил!</div>'
            '<div style="font-size:19px;color:#444;text-align:justify;margin-top:12px;">'
            "Сонирхолтой цахим хичээл, баялаг бодлогын сангаар дамжуулан "
            "математик сэтгэлгээгээ бие даан хөгжүүлж, ирээдүйн амжилтынхаа "
            "суурийг өнөөдөр тавихад тань бид туслах болно.</div></div>",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # HTML товчлуур — st.button-ийн 190px хязгааргүй, хуудас дахин ачааллахгүй
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📺  Цахим контент", use_container_width=True):
            st.session_state.selected_menu = "Цахим контент"; st.rerun()
    with c2:
        if st.button("📚  Даалгаврын сан", use_container_width=True):
            st.session_state.selected_menu = "Даалгаврын сан"; st.rerun()
    with c3:
        if st.button("📝  Сорил", use_container_width=True):
            st.session_state.selected_menu = "Сорил"; st.rerun()

# ── ЦАХИМ КОНТЕНТ ─────────────────────────────────────────────────────────────
elif st.session_state.selected_menu == "Цахим контент":
    st.markdown("<h1 style='color:#0b4ab1;'>📺 Цахим хичээлүүд</h1>", unsafe_allow_html=True)
    st.write("Доорх жагсаалтаас үзэх хичээлээ сонгоно уу.")

    # ── ЭНД ЖИНХЭНЭ ЛИНКҮҮДЭЭ ОРУУЛНА ──
    lessons = {
        "Хичээл 1: Тоон олонлог": "https://www.youtube.com/watch?v=ЖИНХЭНЭ_ID_ЭНДИ",
        "Хичээл 2: Пропорц":      "https://www.youtube.com/watch?v=ЖИНХЭНЭ_ID_ЭНДИ",
        "Хичээл 3: Алгебр":       "https://www.youtube.com/watch?v=ЖИНХЭНЭ_ID_ЭНДИ",
    }

    valid_lessons = {k: v for k, v in lessons.items() if "ЖИНХЭНЭ_ID" not in v}

    if not valid_lessons:
        st.warning("⚠️ Хичээлийн линкүүдийг app.py файлд тохируулна уу.")
    else:
        sel = st.selectbox("Хичээл сонгох:", list(valid_lessons.keys()))
        st.video(valid_lessons[sel])
        st.info(f"Одоо үзэж буй: {sel}")

# ── ДААЛГАВРЫН САН ────────────────────────────────────────────────────────────
elif st.session_state.selected_menu == "Даалгаврын сан":
    st.markdown("<h3 style='text-align:center;color:#0b4ab1;'>📚 Бодлогын сан</h3>",
                unsafe_allow_html=True)

    units = [
        "Тоон олонлог, зэрэг, язгуур, тоог жиших, тоймлох",
        "Харьцаа, пропорц, процент",
        "Алгебрын илэрхийлэл, тэгшитгэл, тэнцэтгэл биш",
        "Дараалал, функц",
        "Өнцөг, дүрс, байгуулалт",
        "Байршил, хөдөлгөөн, хувиргалт",
        "Хэмжигдэхүүн",
        "Магадлал, статистик",
    ]
    LEVELS = {"Мэдлэг ойлголт": 1, "Чадвар": 2, "Хэрэглээ": 3}

    col_u, col_l = st.columns([0.6, 0.4])
    u_choice = col_u.selectbox("Сэдэв сонгох:", units)
    l_choice = col_l.radio("Түвшин:", list(LEVELS.keys()), horizontal=True)

    f_path = f"task_{units.index(u_choice)+1}_{LEVELS[l_choice]}.xlsx"
    df_tasks = load_excel(f_path)   # кэштэй — удаашралгүй

    if df_tasks is None:
        st.info(f"📂 '{f_path}' файл олдсонгүй. Файлыг програмтай нэг хавтсанд байрлуулна уу.")
    elif "Асуулт" not in df_tasks.columns or "Хариу" not in df_tasks.columns:
        st.error("❌ Excel файлд 'Асуулт' болон 'Хариу' баганууд байх ёстой.")
    else:
        for idx, row in df_tasks.iterrows():
            st.markdown(f"#### 📝 Бодлого {idx+1}")
            st.markdown(smart_math_render(row["Асуулт"]))
            user_ans = st.radio(
                f"Хариу {idx+1}:", ["A", "B", "C", "D"],
                key=f"t_{units.index(u_choice)}_{idx}",
                horizontal=True, label_visibility="collapsed",
            )
            if st.button(f"Шалгах {idx+1}", key=f"check_{idx}"):
                c_ans = str(row["Хариу"]).strip().upper()
                if user_ans == c_ans:
                    st.success("✅ Зөв!")
                else:
                    st.error(f"❌ Буруу. Зөв хариу: **{c_ans}**")
                    if "Бодолт" in row and pd.notna(row["Бодолт"]):
                        with st.expander("Бодолт харах"):
                            st.markdown(smart_math_render(row["Бодолт"]))
            st.write("---")

# ── СОРИЛ ────────────────────────────────────────────────────────────────────
elif st.session_state.selected_menu == "Сорил":

    # ── БҮРТГЭЛИЙН ХУУДАС ──
    if not st.session_state.quiz_active and not st.session_state.quiz_finished:
        st.markdown("<h3 style='text-align:center;color:#0b4ab1;'>📝 Онлайн сорилын бүртгэл</h3>",
                    unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        s_school = c1.text_input("Сургууль:")
        s_name   = c2.text_input("Овог нэр:")
        s_class  = c3.text_input("Анги:")
        st.divider()

        quiz_units = [
            "Тоон олонлог, зэрэг, язгуур, тоог жиших, тоймлох",
            "Харьцаа, пропорц, процент",
            "Алгебрын илэрхийлэл, тэгшитгэл, тэнцэтгэл биш",
            "Дараалал, функц",
            "Өнцөг, дүрс, байгуулалт",
            "Байршил, хөдөлгөөн, хувиргалт",
            "Хэмжигдэхүүн",
            "Магадлал, статистик",
        ]

        for i, name in enumerate(quiz_units):
            col_n, col_v = st.columns([0.7, 0.3])
            col_n.markdown(
                f"<div style='padding:10px 0;border-bottom:1px solid #eee;'>"
                f"{i+1}. {name}</div>",
                unsafe_allow_html=True,
            )
            with col_v:
                v_cols = st.columns(4)
                for j, v in enumerate(["A", "B", "C", "D"]):
                    if v_cols[j].button(v, key=f"q_btn_{i}_{v}"):
                        if s_school and s_name and s_class:
                            st.session_state.std_info = {
                                "school": s_school, "name": s_name, "class": s_class
                            }
                            st.session_state.quiz_file = f"quiz_{i+1}_{v}.xlsx"
                            st.session_state.quiz_active = True
                            st.session_state.start_time = time.time()
                            st.session_state.quiz_results = {}
                            st.rerun()
                        else:
                            st.warning("⚠️ Мэдээллээ бүрэн бөглөнө үү!")

    # ── СОРИЛЫН ХУУДАС — @st.fragment: зөвхөн таймер дахин ачаална ──
    elif st.session_state.quiz_active:

        # Таймерийг тусдаа fragment болгох — гол хуудас дахин ачааллахгүй
        @st.fragment(run_every=1)
        def timer_widget():
            elapsed  = int(time.time() - st.session_state.start_time)
            remaining = max(0, 2400 - elapsed)
            mins, secs = divmod(remaining, 60)
            color = "#dc3545" if remaining < 300 else "#0b4ab1"
            st.markdown(
                f"<div style='text-align:center;font-size:28px;font-weight:bold;"
                f"color:{color};padding:8px;border-radius:10px;border:2px solid {color};'>"
                f"⏳ {mins:02d}:{secs:02d}</div>",
                unsafe_allow_html=True,
            )
            if remaining <= 0:
                st.session_state.quiz_active = False
                st.session_state.quiz_finished = True
                st.rerun()

        timer_widget()

        df_q = load_excel(st.session_state.quiz_file)  # кэштэй

        if df_q is None:
            st.error(f"❌ '{st.session_state.quiz_file}' файл олдсонгүй.")
            if st.button("← Буцах"):
                st.session_state.quiz_active = False; st.rerun()
        elif "Асуулт" not in df_q.columns:
            st.error("❌ Excel файлд 'Асуулт' багана байхгүй байна.")
        else:
            with st.form("quiz_form"):
                user_answers = {}
                for idx, row in df_q.iterrows():
                    st.markdown(f"**Бодлого {idx+1}:**")
                    st.markdown(smart_math_render(row["Асуулт"]))
                    user_answers[idx] = st.radio(
                        f"Хариу {idx}", ["A", "B", "C", "D"],
                        key=f"aq_{idx}", horizontal=True, label_visibility="collapsed",
                    )
                    st.write("---")

                if st.form_submit_button("🏁 Дуусгах"):
                    st.session_state.quiz_results  = user_answers
                    st.session_state.quiz_active   = False
                    st.session_state.quiz_finished = True
                    st.rerun()

    # ── ҮР ДҮН ──
    elif st.session_state.quiz_finished:
        df_q = load_excel(st.session_state.quiz_file)

        # Аюулгүй шалгалт
        if df_q is None:
            st.error("Үр дүнг тооцоолох файл олдсонгүй.")
        elif "Хариу" not in df_q.columns:
            st.error("Excel файлд 'Хариу' багана байхгүй байна.")
        else:
            total_score, max_score, log = 0.0, 0.0, []
            for idx, row in df_q.iterrows():
                u_ans = st.session_state.quiz_results.get(idx, "—")  # .get — KeyError алга
                c_ans = str(row["Хариу"]).strip().upper()
                pts   = float(row["Оноо"]) if "Оноо" in df_q.columns and pd.notna(row.get("Оноо")) else 1.0
                max_score += pts
                if u_ans == c_ans:
                    total_score += pts
                log.append(f"Б{idx+1}:{u_ans}")

            std = st.session_state.std_info
            pct = round(total_score / max_score * 100) if max_score else 0

            st.balloons()
            st.markdown(
                f"<div style='text-align:center;padding:30px;border:2px solid #0b4ab1;border-radius:20px;'>"
                f"<h2 style='color:#0b4ab1;'>{std.get('name','')} — "
                f"{std.get('school','')} / {std.get('class','')} анги</h2>"
                f"<h1 style='font-size:72px;color:#0b4ab1;'>{total_score:g} / {max_score:g}</h1>"
                f"<p style='font-size:22px;color:#555;'>Оноо: {pct}%</p></div>",
                unsafe_allow_html=True,
            )

            g_url = ("https://docs.google.com/forms/d/e/"
                     "1FAIpQLSeM9y7SN_kMvo0KfZZgt1A1_UM01mbm18s2cAizZQzGZtKfhw/formResponse")
            params = (
                f"?entry.1163331065={std.get('name','')} ({std.get('school','')})"
                f"&entry.589452758={std.get('class','')}"
                f"&entry.599767365={total_score}/{max_score}"
                f"&entry.1997083807={', '.join(log)}"
                f"&submit=Submit"
            )
            st.markdown(
                f'<a href="{g_url+params}" target="_blank" style="text-decoration:none;">'
                '<div style="background:#28a745;color:white;padding:18px;border-radius:12px;'
                'text-align:center;font-weight:bold;margin-top:20px;font-size:18px;">'
                "🚀 БАГШ РУУ ДҮНГ ИЛГЭЭХ</div></a>",
                unsafe_allow_html=True,
            )

            if st.button("🏠 Нүүр хуудас"):
                st.session_state.quiz_finished = False
                st.session_state.selected_menu = "Нүүр хуудас"
                st.rerun()

# ── КЛУБЫН МЭДЭЭЛЭЛ ──────────────────────────────────────────────────────────
elif st.session_state.selected_menu == "Клубын мэдээлэл":
    st.markdown("<h1 style='color:#0b4ab1;text-align:center;'>👥 Математикийн клуб</h1>",
                unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#f0f5ff;padding:20px;border-radius:15px;
                border-left:5px solid #0b4ab1;margin-bottom:20px;'>
        <h3>Манай клубын танилцуулга:</h3>
        <p style='font-size:18px;'>
            "NextGen Robotics" клуб нь ирээдүйн технологийн салбарын түүчээ болох хүсэл
            эрмэлзэлтэй, инженерчлэл болон програмчлалын хорхойтнуудын нэгдэл юм.
            Бид зөвхөн робот угсраад зогсохгүй, орчин үеийн хиймэл оюун ухаан (AI) болон
            технологийн хөгжлийг эх хэл дээрээ судалж, бүтээлчээр сэтгэхийг эрхэмлэдэг.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📸 Клубын зураг")
        if os.path.exists("club_photo.jpg"):
            st.image("club_photo.jpg", caption="Клубын үйл ажиллагаа", use_container_width=True)
        else:
            st.info("club_photo.jpg файлыг программтай нэг хавтсанд байрлуулна уу.")
    with col2:
        st.subheader("🎥 Клубын үйл ажиллагаа")
        if os.path.exists("club_video.mp4"):
            st.video("club_video.mp4")
        else:
            st.info("club_video.mp4 файлыг програмтай нэг хавтсанд байрлуулна уу.")

    st.divider()
    st.markdown("#### ✨ Клубын амжилтаас")
    st.write("- 2025 оны Эрдэнэ сумын математикийн олимпиадад: Б.Тэмүүлэн дэд байр, "
             "О.Хонгорзул дэд байр, Р.Энхчимэг гуравдугаар байр.")
    st.write("- Логик паззлын уралдаанд С.Цэнгүүнжаргал тусгай байрт орсон.")

# ── ХҮҮХДИЙН ХҮМҮҮЖИЛ ────────────────────────────────────────────────────────
elif st.session_state.selected_menu == "Хүүхдийн хүмүүжил":
    st.markdown("<h1 style='color:#0b4ab1;'>❤️ Зөвлөгөө</h1>", unsafe_allow_html=True)
    st.info("Энэ хэсгийн контентыг энд нэмнэ үү.")
