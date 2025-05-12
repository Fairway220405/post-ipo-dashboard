import os
import platform
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# ✅ 한글 폰트 설정
if platform.system() == 'Windows':
    matplotlib.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':
    matplotlib.rc('font', family='AppleGothic')
else:
    matplotlib.rc('font', family='DejaVu Sans')
matplotlib.rcParams['axes.unicode_minus'] = False

# ✅ 바탕화면 경로로 CSV 로드
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
csv_path = os.path.join(desktop, "sample.csv")  # 여기에 파일이 있어야 함
df = pd.read_csv(csv_path)

# 수치형 컬럼 변환
for col in ['매출액', '영업이익', '당기순이익']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# ✅ 회사 선택
company_options = df['회사명'].unique().tolist()
selected_company = st.selectbox("📌 분석할 상장사 선택", company_options)

df_target = df[df['회사명'] == selected_company]

st.title(f"📊 {selected_company} - Post IPO 실적 대시보드")
st.write(f"단위: 억원 | 연도: {df_target['연도'].iloc[0]}")

# ✅ 매출액
st.subheader("💰 매출액")
st.metric(label="매출액", value=f"{df_target['매출액'].iloc[0]:,.1f} 억원")

# ✅ 영업이익
st.subheader("📈 영업이익")
st.metric(label="영업이익", value=f"{df_target['영업이익'].iloc[0]:,.1f} 억원")

# ✅ 당기순이익
st.subheader("📉 당기순이익")
st.metric(label="당기순이익", value=f"{df_target['당기순이익'].iloc[0]:,.1f} 억원")

# ✅ 그래프 출력
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(['매출액', '영업이익', '당기순이익'], 
       [df_target['매출액'].iloc[0], df_target['영업이익'].iloc[0], df_target['당기순이익'].iloc[0]])
ax.set_title(f"{selected_company} 주요 실적 (억원)")
st.pyplot(fig)
