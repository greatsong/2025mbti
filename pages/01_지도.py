import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="MBTI 세계지도", layout="wide")
st.title("🌍 국가별 MBTI 유형 분포 지도")

# 1. CSV 파일 로드
file_path = "countriesMBTI_16types.csv"
df = pd.read_csv(file_path)

# 2. MBTI 유형 컬럼 리스트
mbti_types = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# 3. Top1~Top3 유형 추출 + hover 텍스트 생성
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
        "Top2": top2,
        "Top3": top3,
        "hover_text": hover_text
    })

top_info = df.apply(extract_top_info, axis=1)
df = pd.concat([df, top_info], axis=1)

# 4. 16가지 MBTI 유형에 대해 구별 가능한 색상 지정
mbti_colors = {
    "INTJ": "#1f77b4", "INTP": "#ff7f0e", "ENTJ": "#2ca02c", "ENTP": "#d62728",
    "INFJ": "#9467bd", "INFP": "#8c564b", "ENFJ": "#e377c2", "ENFP": "#7f7f7f",
    "ISTJ": "#bcbd22", "ISFJ": "#17becf", "ESTJ": "#aec7e8", "ESFJ": "#ffbb78",
    "ISTP": "#98df8a", "ISFP": "#ff9896", "ESTP": "#c5b0d5", "ESFP": "#c49c94"
}

# 5. Plotly 지도 시각화
fig = px.choropleth(
    df,
    locations="Country",
    locationmode="country names",
    color="Top1",
    hover_name="Country",
    hover_data={"Top1": False, "Top2": False, "Top3": False, "hover_text": True},
    color_discrete_map=mbti_colors,
    title="🗺️ 국가별 최다 MBTI 유형"
)

# 6. 마우스 오버 텍스트 커스터마이징
fig.update_traces(
    hovertemplate="%{customdata[0]}<extra></extra>"
)

fig.update_layout(
    legend_title_text="Top1 MBTI 유형",
    geo=dict(showframe=False, showcoastlines=False),
    margin={"r":0,"t":50,"l":0,"b":0}
)

# 7. Streamlit 출력
st.plotly_chart(fig, use_container_width=True)
