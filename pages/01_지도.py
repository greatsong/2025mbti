import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="MBTI 세계지도", layout="wide")
st.title("🌍 국가별 MBTI 유형 분포 지도")

# 1. CSV 파일 로드
file_path = "countriesMBTI_16types.csv"
df = pd.read_csv(file_path)

# 2. MBTI 유형 리스트
mbti_types = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# 3. Top 3 유형 및 hover text 생성
def extract_top_info(row):
    sorted_mbti = row[mbti_types].sort_values(ascending=False)
    top1, top2, top3 = sorted_mbti.index[:3]
    v1, v2, v3 = sorted_mbti.iloc[:3]
    hover_text = (
        f"<b>{row['Country']}</b><br>"
        f"1️⃣ {top1}: {v1}%<br>"
        f"2️⃣ {top2}: {v2}%<br>"
        f"3️⃣ {top3}: {v3}%"
    )
    return pd.Series({
        "Top1": top1,
        "hover_text": hover_text
    })

df = df.join(df.apply(extract_top_info, axis=1))

# 4. MBTI 색상 정의 (16가지)
mbti_colors = {
    "INTJ": "#1f77b4", "INTP": "#ff7f0e", "ENTJ": "#2ca02c", "ENTP": "#d62728",
    "INFJ": "#9467bd", "INFP": "#8c564b", "ENFJ": "#e377c2", "ENFP": "#7f7f7f",
    "ISTJ": "#bcbd22", "ISFJ": "#17becf", "ESTJ": "#aec7e8", "ESFJ": "#ffbb78",
    "ISTP": "#98df8a", "ISFP": "#ff9896", "ESTP": "#c5b0d5", "ESFP": "#c49c94"
}

# 5. 범례를 항상 16개 고정하기 위해 Categorical로 변환
df["Top1"] = pd.Categorical(df["Top1"], categories=list(mbti_colors.keys()))

# 6. 지도 시각화
fig = px.choropleth(
    df,
    locations="Country",
    locationmode="country names",
    color="Top1",
    hover_name="Country",
    hover_data={"hover_text": True, "Country": False},
    color_discrete_map=mbti_colors,
    title="🗺️ 국가별 최다 MBTI 유형"
)

# 마우스 오버 시 국가명 + Top3 MBTI 표시
fig.update_traces(
    hovertemplate="%{customdata[0]}<extra>%{location}</extra>"
)

# 지도 설정
fig.update_layout(
    legend_title_text="Top1 MBTI 유형",
    geo=dict(showframe=False, showcoastlines=False),
    margin={"r":0,"t":50,"l":0,"b":0}
)

# Streamlit 출력
st.plotly_chart(fig, use_container_width=True)
