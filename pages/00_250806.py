import streamlit as st
import pandas as pd
import altair as alt

st.title("🌍 국가별 MBTI 유형 분석 대시보드")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    mbti_types = [
        "INTJ", "INTP", "ENTJ", "ENTP",
        "INFJ", "INFP", "ENFJ", "ENFP",
        "ISTJ", "ISFJ", "ESTJ", "ESFJ",
        "ISTP", "ISFP", "ESTP", "ESFP"
    ]

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

    st.markdown("## 📈 2. 특정 MBTI 유형이 높은 국가 TOP 10")
    selected_type = st.selectbox("MBTI 유형을 선택하세요", mbti_types)

    top_countries = df[['Country', selected_type]].sort_values(by=selected_type, ascending=False).head(10)

    chart2 = alt.Chart(top_countries).mark_bar().encode(
        x=alt.X(selected_type, title="비율(%)"),
        y=alt.Y('Country', sort='-x', title="국가"),
        color=alt.value("#0072B5")
    ).properties(
        width=600,
        height=400,
        title=f"{selected_type} 유형이 많은 국가 TOP 10"
    )

    st.altair_chart(chart2, use_container_width=True)

else:
    st.warning("먼저 CSV 파일을 업로드해주세요. 예: `countriesMBTI_16types.csv`")
