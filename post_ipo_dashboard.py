import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import platform

# ✅ 폰트 설정
if platform.system() == 'Windows':
    matplotlib.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':
    matplotlib.rc('font', family='AppleGothic')
else:
    matplotlib.rc('font', family='DejaVu Sans')

matplotlib.rcParams['axes.unicode_minus'] = False

# ✅ 데이터 로드 및 정리
df = pd.read_csv("ipo_merged_with_yield.csv")
df['수익률'] = pd.to_numeric(df['수익률'], errors='coerce')
df['매출액'] = pd.to_numeric(df['매출액'], errors='coerce')
df['영업이익'] = pd.to_numeric(df['영업이익'], errors='coerce')
df['당기순이익'] = pd.to_numeric(df['당기순이익'], errors='coerce')

st.title("📈 IPO 통합 대시보드")

st.subheader("📋 데이터 미리보기")
st.dataframe(df)

# ✅ 수익률 그래프
st.subheader("📊 수익률 비교")
if '회사명' in df.columns and '수익률' in df.columns:
    df_yield = df.dropna(subset=['수익률'])
    df_yield_sorted = df_yield.sort_values(by='수익률', ascending=False)

    fig1, ax1 = plt.subplots()
    ax1.bar(df_yield_sorted['회사명'], df_yield_sorted['수익률'])
    ax1.set_title("공모주 수익률 (%)")
    ax1.set_xlabel("회사명")
    ax1.set_ylabel("수익률")
    ax1.tick_params(axis='x', rotation=45)
    st.pyplot(fig1)

# ✅ 재무지표 시각화
st.subheader("📊 주요 재무 지표 시각화")

selected_year = st.selectbox("연도를 선택하세요", sorted(df['연도'].unique(), reverse=True))

df_year = df[df['연도'] == selected_year]

fig2, ax2 = plt.subplots()
ax2.bar(df_year['회사명'], df_year['매출액'])
ax2.set_title(f"{selected_year}년 매출액")
ax2.set_xlabel("회사명")
ax2.set_ylabel("매출액")
ax2.tick_params(axis='x', rotation=45)
st.pyplot(fig2)

fig3, ax3 = plt.subplots()
ax3.bar(df_year['회사명'], df_year['영업이익'])
ax3.set_title(f"{selected_year}년 영업이익")
ax3.set_xlabel("회사명")
ax3.set_ylabel("영업이익")
ax3.tick_params(axis='x', rotation=45)
st.pyplot(fig3)

fig4, ax4 = plt.subplots()
ax4.bar(df_year['회사명'], df_year['당기순이익'])
ax4.set_title(f"{selected_year}년 당기순이익")
ax4.set_xlabel("회사명")
ax4.set_ylabel("당기순이익")
ax4.tick_params(axis='x', rotation=45)
st.pyplot(fig4)
