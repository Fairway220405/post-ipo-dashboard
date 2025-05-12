import streamlit as st
import pandas as pd
import plotly.express as px

# ✅ sample.csv 불러오기
df = pd.read_csv("sample.csv")

# 수치형 변환
for col in ['매출액', '영업이익', '당기순이익']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# ✅ 회사 선택
company_list = df['회사명'].unique().tolist()
selected_company = st.selectbox("📌 분석할 상장사 선택", company_list)

df_target = df[df['회사명'] == selected_company]

st.title(f"📊 {selected_company} - Post IPO 실적 대시보드")
st.markdown(f"📆 연도: **{df_target['연도'].iloc[0]}** &nbsp;&nbsp; | &nbsp;&nbsp; 💵 단위: 억원")

# ✅ 요약 지표
st.subheader("📌 핵심 지표")
col1, col2, col3 = st.columns(3)
col1.metric("매출액", f"{df_target['매출액'].iloc[0]:,.1f} 억원")
col2.metric("영업이익", f"{df_target['영업이익'].iloc[0]:,.1f} 억원")
col3.metric("당기순이익", f"{df_target['당기순이익'].iloc[0]:,.1f} 억원")

# ✅ 실적 그래프 (한글 폰트 설정)
st.subheader("📊 실적 구성 그래프")
plot_df = pd.DataFrame({
    "지표": ["매출액", "영업이익", "당기순이익"],
    "금액": [df_target['매출액'].iloc[0], df_target['영업이익'].iloc[0], df_target['당기순이익'].iloc[0]]
})

fig = px.bar(plot_df, x="지표", y="금액", text="금액",
             title=f"{selected_company} 주요 재무지표 (억원)", height=400)

fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
fig.update_layout(
    font=dict(
        family="Arial, NanumGothic, Malgun Gothic, AppleGothic, sans-serif"  # 한글 폰트 후보들
    ),
    uniformtext_minsize=8,
    uniformtext_mode='hide'
)

st.plotly_chart(fig)
