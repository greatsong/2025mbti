import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="MBTI 세계지도", layout="wide")
st.title("🌐 국가별 MBTI 유형 분포 지도")

# CSV 파일 로드 (같은 폴더에 있다고 가정)
file_path = "countriesMBTI_16types.csv"
df = pd.read_csv(file_path)

mbti_types = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# 각 국가별 Top 3 MBTI 유형 추출
def get_top_3(row):
    top3 = row[mbti_types].sort_values(ascending=False).head(3)
    return {
        "top1_type": top3.index[0],
        "top1_val": top3.iloc[0],
        "top2_type": top3.index[1],
        "top2_val": top3.iloc[1],
        "top3_type": top3.index[2],
        "top3_val": top3.iloc[2],
        "hover_text": f"1️⃣ {top3.index[0]}: {top3.iloc[0]}%<br>"
                      f"2️⃣ {top3.index[1]}: {top3.iloc[1]}%<br>"
                      f"3️⃣ {top3.index[2]}: {top3.iloc[2]}%"
    }

top3_data = df.apply(get_top_3, axis=1, result_type='expand')
df = pd.concat([df, top3_data], axis=1)

# 색상 매핑 (16가지 MBTI → 구별되는 색)
mbti_colors = {
    "INTJ": "#1f77b4", "INTP": "#ff7f0e", "ENTJ": "#2ca02c", "ENTP": "#d62728",
    "INFJ": "#9467bd", "INFP": "#8c564b", "ENFJ": "#e377c2", "ENFP": "#7f7f7f",
    "ISTJ": "#bcbd22", "ISFJ": "#17becf", "ESTJ": "#aec7e8", "ESFJ": "#ffbb78",
    "ISTP": "#98df8a", "ISFP": "#ff9896", "ESTP": "#c5b0d5", "ESFP": "#c49c94"
}

df['color'] = df['top1_type'].map(mbti_colors)

# 지도 시각화
fig = px.choropleth(
    df,
    locations="Country",
    locationmode="country names",
    color="top1_type",
    hover_name="Country",
    hover_data={"hover_text": True, "Country": False, "top1_type": False, "color": False},
    color_discrete_map=mbti_colors,
    title="🌍 국가별 최다 MBTI 유형"
)

fig.update_traces(
    hovertemplate="%{hovertext}<extra>%{location}</extra>"
)

fig.update_layout(
    legend_title_text='Top MBTI 유형',
    geo=dict(showframe=False, showcoastlines=False),
    margin={"r":0,"t":50,"l":0,"b":0}
)

st.plotly_chart(fig, use_container_width=True)
