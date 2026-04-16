import streamlit as st
from streamlit_option_menu import option_menu
import os
import pandas as pd
import re

st.set_page_config(page_title="Математик Багш", page_icon="📐", layout="wide")

# 1. УХААЛАГ МАТЕМАТИК ТАНИГЧ (Энэ хэсэг таны бичиглэлийг засна)
def smart_math_render(text):
    if not isinstance(text, str): return text
    
    # Сонголтуудыг (A. B. C. D.) доош нь цувуулах
    for label in ['A.', 'B.', 'C.', 'D.']:
        if label in text:
            text = text.replace(label, f'\n\n**{label}**')

    # Хэрэв текст дотор \ , ^ эсвэл / байвал LaTeX гэж үзээд $ $ тэмдэгт хавчуулна
    if ('\\' in text or '^' in text or '/' in text) and '$' not in text:
        # \displaystyle-г заавал нэмж том харагдуулна
        clean_text = text.replace('\\displaystyle', '').strip()
        text = f"$\\displaystyle {clean_text}$"
    
    return text

# 2. ДИЗАЙН
st.markdown("""
    <style>
    .stApp { background-color: #eef2f6 !important; }
    .math-card { background: white; padding: 30px; border-radius: 8px; border: 1px solid #dee2e6; margin-bottom: 25px; box-shadow: 0 2px 8px rgba(0,0,0,0.02); }
    .sidebar-title { color: white; text-align: center; font-size: 26px; font-weight: bold; padding: 20px 0; }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR
with st.sidebar:
    st.markdown('<p class="sidebar-title">ЦЭС</p>', unsafe_allow_html=True)
    selected = option_menu(None, ["Нүүр хуудас", "Даалгаврын сан"], 
                           icons=['house', 'book'], default_index=0)

# 4. НҮҮР ХУУДАС
if selected == "Нүүр хуудас":
    st.title("Бидний зорилго")
    st.write("Математикийн ертөнцөөр хамтдаа аялцгаая!")

# 5. ДААЛГАВРЫН САН
elif selected == "Даалгаврын сан":
    st.markdown('<h1 style="color:#1a3a5f; text-align:center;">📚 Даалгаврын сан</h1>', unsafe_allow_html=True)
    if os.path.exists("data_bank.xlsx"):
        df = pd.read_excel("data_bank.xlsx")
        unit = st.selectbox("Сэдэв сонгох:", df['Нэгж'].unique())
        tabs = st.tabs(["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"])
        
        for idx, lvl in enumerate(["Мэдлэг ойлголт", "Чадвар", "Хэрэглээ"]):
            with tabs[idx]:
                f_df = df[(df['Нэгж'] == unit) & (df['Түвшин'] == lvl)]
                for i, row in f_df.iterrows():
                    st.markdown('<div class="math-card">', unsafe_allow_html=True)
                    
                    # БОДЛОГЫН ДУГААРЫГ ТОД БОЛГОХ
                    st.markdown(f"### 📝 Бодлого {i+1}")
                    
                    # АСУУЛТЫГ МАТЕМАТИК ХЭЛБЭРТ ОРУУЛАХ
                    st.markdown(smart_math_render(row['Асуулт']))
                    
                    ans = st.radio("Хариу сонгох:", ["A", "B", "C", "D"], key=f"ans_{lvl}_{idx}_{i}", horizontal=True)
                    
                    if st.button("Шалгах", key=f"chk_{lvl}_{idx}_{i}"):
                        correct_ans = str(row['Хариу']).strip().upper()
                        if str(ans).strip().upper() == correct_ans:
                            st.success("Зөв! ✅"); st.balloons()
                        else: 
                            st.error(f"Буруу. Зөв хариу: {correct_ans}")
                    st.markdown('</div>', unsafe_allow_html=True)
