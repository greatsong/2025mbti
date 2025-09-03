import streamlit as st
import pandas as pd
import altair as alt
import os

st.title("🌍 국가별 MBTI 유형 분석 대시보드")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

# MBTI 16유형 정의
mbti_types = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# 데이터 불러오기
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
elif os.path.exists("countriesMBTI_16types.csv"):
    df = pd.read_csv("countriesMBTI_16types.csv")
    st.info("업로드된 파일이 없어 레파지토리의 `countriesMBTI_16types.csv` 파일을 불러왔습니다.")
else:
    st.error("CSV 파일을 업로드하거나 레파지토리에 `countriesMBTI_16types.csv`가 존재해야 합니다.")
    st.stop()

# --- 1. 특정 국가 MBTI 분포 ---
st.markdown("## 🔍 1. 특정 국가의 MBTI 분포 보기")
selected_Country = st.selectbox("국가를 선택하세요", df['Country'].unique())

Country_data = df[df['Country'] == selected_Country][mbti_types].T.reset_index()
Country_data.columns = ['MBTI', '비율']

chart1 = alt.Chart(Country_data).mark_bar().encode(
    x=alt.X('MBTI', sort=mbti_types),
    y='비율',
    color='MBTI'
).properties(
    width=600,
    height=400,
    title=f"{selected_Country}의 MBTI 유형 분포"
)

st.altair_chart(chart1, use_container_width=True)

st.markdown("---")

# --- 2. 특정 MBTI 유형 높은 국가 TOP 10 ---
st.markdown("## 📈 2. 특정 MBTI 유형이 높은 국가 TOP 10")
selected_type = st.selectbox("MBTI 유형을 선택하세요", mbti_types)

top_countries = df[['Country', selected_type]].sort_values(
    by=selected_type, ascending=False
).head(10)

# 1위 국가명
top_country_name = top_countries.iloc[0]['Country']

# Altair 차트 생성
chart2 = alt.Chart(top_countries).mark_bar().encode(
    x=alt.X(selected_type, title="비율(%)"),
    y=alt.Y('Country', sort='-x', title="국가"),
    # 조건부 색상: 1위 국가만 빨강, 나머지는 viridis 컬러맵
    color=alt.condition(
        alt.datum.Country == top_country_name,
        alt.value("red"),
        alt.Color(selected_type, scale=alt.Scale(scheme="viridis"), legend=None)
    ),
    tooltip=['Country', selected_type]
).properties(
    width=600,
    height=400,
    title=f"{selected_type} 유형이 많은 국가 TOP 10"
)

st.altair_chart(chart2, use_container_width=True)
