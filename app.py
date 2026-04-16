import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64
import pandas as pd
import re

# 1. Сайтын ерөнхий тохиргоо
st.set_page_config(page_title="Математикийн багшийн туслах", page_icon="📐", layout="wide")

# УХААЛАГ МАТЕМАТИК ТАНИГЧ (LaTeX засагч)
def smart_math_render(text):
    if not isinstance(text, str): return text
    # Сонголтуудыг (A. B. C. D.) доош нь цувуулах
    for label in ['A.', 'B.', 'C.', 'D.']:
        if label in text:
            text = text.replace(label, f'\n\n**{label}**')
    # LaTeX бичиглэлийг долларын тэмдэгт хавчуулж математик болгоно
    if ('\\' in text or '^' in text or '/' in text) and '$' not in text:
        clean_text = text.replace('\\displaystyle', '').strip()
        text = f"$\\displaystyle {clean_text}$"
    return text

# 2. ДИЗАЙН (CSS) - Илүү орчин үеийн болгосон
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    [data-testid="stSidebar"] { background-color: #004aad !important; }
    .sidebar-title { color: white; text-align: center; font-size: 32px; font-weight: bold; padding: 20px 0; border-bottom: 1px solid rgba(255,255,255,0.2); }
    
    /* Зорилгын хайрцаг */
    .goal-box {
        background: white; padding: 40px; border-radius: 20px;
        border-left: 10px solid #004aad; box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    }
    .main-header { color: #004aad; font-size: 45px; font-weight: 800; margin-bottom: 20px; }
    
    /* Шинэ картуудын загвар */
    .card-container {
        background: white; border-radius: 20px; padding: 40px 20px;
        text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        height: 100%; display: flex; flex-direction: column;
        justify-content: space-between; align-items: center;
    }
    .card-icon { font-size: 70px; margin-bottom: 20px; }
    .card-title { color: #004aad; font-size: 22px; font-weight: bold; margin-bottom: 20px; }
    .card-button {
        background-color: #f8f9fa; border: 1px solid #dee2e6;
        padding: 8px 25px; border-radius: 8px; color: #333; font-size: 14px;
    }
    .math-card {
        background: white; padding: 25px; border-radius: 15px;
        border: 1px solid #e0e0e0; margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR (Цэс)
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None, 
        options=["Нүүр хуудас", "Даалгаврын сан", "Сорил", "Клубын мэдээлэл", "Хүүхдийн хүмүүжил"],
        icons=['house', 'book', 'pencil-square', 'people', 'heart'],
        default_index=0,
        styles={
            "container": {"background-color": "#004aad"},
            "nav-link": {"color": "white", "font-weight": "bold"},
            "nav-link-selected": {"background-color": "rgba(255,255,255,0.2)"},
        }
    )

# 4. НҮҮР ХУУДАС
if selected == "Нүүр хуудас":
    # Дээд хэсэг: Зураг болон Зорилго
    col1, col2 = st.columns([1, 1.2], gap="large")
    with col1:
        if os.path.exists("logo.gif"):
            with open("logo.gif", "rb") as f:
                data_url = base64.b64encode(f.read()).decode("utf-8")
            st.markdown(f'<img src="data:image/gif;base64,{data_url}" width="100%">', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="goal-box">
                <div class="main-header">Бидний зорилго</div>
                <div style="font-size: 22px; line-height: 1.6; color: #444;">
                    Математикийн ертөнцөөр хамтдаа аялж, сонирхолтой цахим хичээл, 
                    бодлогын сангаар дамжуулан өөрийн мэдлэг чадвараа бие даан ахиулж, 
                    ирээдүйн амжилтынхаа эхлэлийг өнөөдөр тавьцгаая!
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Доод хэсэг: 3 Сонгох карт
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="medium")
    card_items = [
        {"icon": "📺", "title": "Цахим контент", "btn": "Үзэх"},
        {"icon": "📚", "title": "Даалгаврын сан", "btn": "Нээх"},
        {"icon": "📝", "title": "Сорил", "btn": "Эхлэх"}
    ]
    for i, col in enumerate([c1, c2, c3]):
        with col:
            st.markdown(f"""
                <div class="card-container">
                    <div>
                        <div class="card-icon">{card_items[i]['icon']}</div>
                        <div class="card-title">{card_items[i]['title']}</div>
                    </div>
                    <div class="card-button">{card_items[i]['btn']}</div>
                </div>
            """, unsafe_allow_html=True)
# 5. ДААЛГАВРЫН САН (Шинэчилсэн)
elif selected == "Даалгаврын сан":
    st.markdown("<h1 style='color: #004aad; text-align: center;'>📚 Бодлогын сан</h1>", unsafe_allow_html=True)
    
    if os.path.exists("data_bank.xlsx"):
        df = pd.read_excel("data_bank.xlsx")
        
        # Сонголт хийх хэсэг
        c1, c2 = st.columns(2)
        with c1:
            unit = st.selectbox("Сэдэв сонгох:", df['Нэгж'].unique())
        with c2:
            level = st.radio("Түвшин:", ["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"], horizontal=True)
            
        f_df = df[(df['Нэгж'] == unit) & (df['Түвшин'] == level)]
        
        if f_df.empty:
            st.info("Энэ хэсэгт бодлого хараахан ороогүй байна.")
        else:
            for i, row in f_df.iterrows():
                with st.container():
                    st.markdown('<div class="math-card">', unsafe_allow_html=True)
                    st.markdown(f"### 📝 Бодлого {i+1}")
                    st.markdown(smart_math_render(row['Асуулт']))
                    
                    # Хариулт шалгах хэсэг
                    ans = st.radio("Хариу сонгох:", ["A", "B", "C", "D"], key=f"ans_{i}", horizontal=True)
                    if st.button("Шалгах", key=f"btn_{i}"):
                        correct = str(row['Хариу']).strip().upper()
                        if ans == correct:
                            st.success("Зөв! ✅")
                            st.balloons()
                        else:
                            st.error(f"Буруу байна. Зөв хариу: {correct}")
                    st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("data_bank.xlsx файл олдсонгүй. Бодлого харуулахын тулд файлаа оруулна уу.")

# Бусад цэсүүд
else:
    st.markdown(f"<h1 style='color: #004aad; text-align: center; margin-top: 50px;'>{selected}</h1>", unsafe_allow_html=True)
    st.info("Энэ хэсэг удахгүй нэмэгдэнэ.")
