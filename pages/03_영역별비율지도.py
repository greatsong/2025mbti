import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="MBTI 차원별 세계지도", layout="wide")
st.title("🌍 국가별 MBTI 차원 비율 시각화")

# CSV 파일 경로 (같은 폴더에 있다고 가정)
file_path = "countriesMBTI_16types.csv"
df = pd.read_csv(file_path)

# MBTI 16개 유형 정의
mbti_types = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# 4가지 차원별 비율 계산
df["E"] = df[["ENTJ", "ENTP", "ENFJ", "ENFP", "ESTJ", "ESFJ", "ESTP", "ESFP"]].sum(axis=1)
df["I"] = df[["INTJ", "INTP", "INFJ", "INFP", "ISTJ", "ISFJ", "ISTP", "ISFP"]].sum(axis=1)

df["S"] = df[["ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]].sum(axis=1)
df["N"] = df[["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP"]].sum(axis=1)

df["T"] = df[["INTJ", "INTP", "ENTJ", "ENTP", "ISTJ", "ISTP", "ESTJ", "ESTP"]].sum(axis=1)
df["F"] = df[["INFJ", "INFP", "ENFJ", "ENFP", "ISFJ", "ISFP", "ESFJ", "ESFP"]].sum(axis=1)

df["J"] = df[["INTJ", "INFJ", "ENTJ", "ENFJ", "ISTJ", "ISFJ", "ESTJ", "ESFJ"]].sum(axis=1)
df["P"] = df[["INTP", "INFP", "ENTP", "ENFP", "ISTP", "ISFP", "ESTP", "ESFP"]].sum(axis=1)

# Hover 텍스트 생성
def make_hover_text_dim(row):
    return (
        f"<b>{row['Country']}</b><br>"
        f"E: {row['E']:.2f}% / I: {row['I']:.2f}%<br>"
        f"N: {row['N']:.2f}% / S: {row['S']:.2f}%<br>"
        f"T: {row['T']:.2f}% / F: {row['F']:.2f}%<br>"
        f"J: {row['J']:.2f}% / P: {row['P']:.2f}%"
    )

df["hover_text_dim"] = df.apply(make_hover_text_dim, axis=1)

# 사용자 선택
dimension_option = st.selectbox(
    "분석할 차원을 선택하세요:",
    ["E/I", "S/N", "T/F", "J/P"]
)

# 시각화에 사용할 컬럼 지정
if dimension_option == "E/I":
    value_col = "E"
    title_suffix = "외향형 비율 (E)"
elif dimension_option == "S/N":
    value_col = "N"
    title_suffix = "직관형 비율 (N)"
elif dimension_option == "T/F":
    value_col = "T"
    title_suffix = "사고형 비율 (T)"
else:
    value_col = "J"
    title_suffix = "판단형 비율 (J)"

# Plotly 시각화
fig = px.choropleth(
    df,
    locations="Country",
    locationmode="country names",
    color=value_col,
    hover_name="Country",
    hover_data={"hover_text_dim": True, "Country": False},
    color_continuous_scale="Viridis",
    title=f"🧭 {title_suffix} 기준 MBTI 세계 지도"
)

fig.update_traces(
    hovertemplate="%{customdata[0]}<extra>%{location}</extra>"
)

fig.update_layout(
    coloraxis_colorbar=dict(title="비율 (%)"),
    geo=dict(showframe=False, showcoastlines=False),
    margin={"r":0,"t":50,"l":0,"b":0}
)

st.plotly_chart(fig, use_container_width=True)
