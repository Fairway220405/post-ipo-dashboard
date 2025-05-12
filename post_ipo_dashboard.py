import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import platform

# ✅ 한글 폰트 설정
if platform.system() == 'Windows':
    matplotlib.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':
    matplotlib.rc('font', family='AppleGothic')
else:
    matplotlib.rc('font', family='DejaVu Sans')
matplotlib.rcParams['axes.unicode_minus'] = False

# ✅ sample.csv 불러오기 (같은 GitHub 폴더에 있어야 함)
try:
    df = pd.read_csv("sample.csv")
except FileNotFoundError:
    st.error("⚠️ sample.csv 파일을 찾을 수 없습니다. GitHub 저장소 루트에 sample.csv가 있는지 확인하세요.")
    st.stop()

# ✅ 수치형 컬럼 변환
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

# ✅ 실적 그래프
st.subheader("📊 실적 구성 그래프")
fig, ax = plt.subplots(figsize=(6, 4))
bars = ['매출액', '영업이익', '당기순이익']
values = [df_target[col].iloc[0] for col in bars]
ax.bar(bars, values)
ax.set_title(f"{selected_company} 주요 재무지표 (억원)")
st.pyplot(fig)
