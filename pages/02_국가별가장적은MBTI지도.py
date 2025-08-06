# https://chatgpt.com/share/6892ef5c-4d48-800d-9a04-6d77106946f5
import streamlit as st
import pandas as pd
import plotly.express as px
from pandas.api.types import CategoricalDtype

st.set_page_config(page_title="MBTI 최저 비율 지도", layout="wide")
st.title("🌍 국가별 MBTI 유형 중 가장 낮은 비율 지도 (Min1)")

# 1. CSV 파일 불러오기
file_path = "countriesMBTI_16types.csv"
df = pd.read_csv(file_path)

# 2. MBTI 16개 유형 정의
mbti_types = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# 3. 국가별 Min1 MBTI 추출
df["Min1"] = df[mbti_types].idxmin(axis=1)

# 4. Min1 유형별 국가 수 계산
min1_counts = df["Min1"].value_counts()
min1_counts_df = min1_counts.reset_index()
min1_counts_df.columns = ['MBTI', 'Countries_with_Min1']

# 5. "ISTP (89개국)" 형식의 범례 라벨 생성
min1_label_map = {
    row["MBTI"]: f"{row['MBTI']} ({row['Countries_with_Min1']}개국)"
    for _, row in min1_counts_df.iterrows()
}
df["Min1_label"] = df["Min1"].map(min1_label_map)

# 6. 범례 순서를 국가 수 많은 순으로 지정
ordered_min_labels = [min1_label_map[mbti] for mbti in min1_counts.index]
df["Min1_label"] = df["Min1_label"].astype(CategoricalDtype(categories=ordered_min_labels, ordered=True))

# 7. 색상 지정 (16개 MBTI)
mbti_colors = {
    "INTJ": "#1f77b4", "INTP": "#ff7f0e", "ENTJ": "#2ca02c", "ENTP": "#d62728",
    "INFJ": "#9467bd", "INFP": "#8c564b", "ENFJ": "#e377c2", "ENFP": "#7f7f7f",
    "ISTJ": "#bcbd22", "ISFJ": "#17becf", "ESTJ": "#aec7e8", "ESFJ": "#ffbb78",
    "ISTP": "#98df8a", "ISFP": "#ff9896", "ESTP": "#c5b0d5", "ESFP": "#c49c94"
}
min_color_map = {
    min1_label_map[mbti]: mbti_colors[mbti]
    for mbti in min1_counts.index
}

# 8. Hover 텍스트 생성 (소수점 2자리, 최소 Top3)
def make_hover_text_min(row):
    bottom3 = row[mbti_types].sort_values(ascending=True).head(3)
    lines = [f"{i+1}️⃣ {mbti}: {pct:.2f}%" for i, (mbti, pct) in enumerate(bottom3.items())]
    return f"<b>{row['Country']}</b><br>" + "<br>".join(lines)

df["hover_text_min"] = df.apply(make_hover_text_min, axis=1)

# 9. Plotly 지도 시각화
fig = px.choropleth(
    df,
    locations="Country",
    locationmode="country names",
    color="Min1_label",
    hover_name="Country",
    hover_data={"hover_text_min": True, "Country": False},
    color_discrete_map=min_color_map,
    title="🗺️ 국가별 가장 낮은 MBTI 유형 (Min1 기준)"
)

fig.update_traces(
    hovertemplate="%{customdata[0]}<extra>%{location}</extra>"
)

fig.update_layout(
    legend_title_text="Min1 MBTI 유형 (국가 수 기준)",
    geo=dict(showframe=False, showcoastlines=False),
    margin={"r":0,"t":50,"l":0,"b":0}
)

# 10. 지도 출력
st.plotly_chart(fig, use_container_width=True)
