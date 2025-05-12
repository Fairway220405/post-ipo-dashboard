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
    matplotlib.rc('font', family='DejaVu Sans')  # 리눅스 기본 폰트

matplotlib.rcParams['axes.unicode_minus'] = False

# ✅ CSV 파일 (동일 디렉토리에 업로드되어 있어야 함)
df = pd.read_csv("ipo_merged_with_yield.csv")

# ✅ 수치형 컬럼 정리
for col in ['수익률', '매출액', '영업이익', '당기순이익']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# ✅ 연도 선택 UI
available_years = df['연도'].dropna().unique()
available_years.sort()
selected_year = st.selectbox("📅 연도를 선택하세요", available_years[::-1])

df_year = df[df['연도'] == selected_year]

# ✅ 대시보드 시작
st.title("📈 IPO 통합 대시보드")
st.markdown(f"선택된 연도: **{selected_year}**")

st.subheader("📋 데이터 미리보기")
st.dataframe(df_year)

# ✅ 수익률 그래프
st.subheader("📊 공모주 수익률 (%)")
df_yield = df_year.dropna(subset=['수익률']).sort_values(by='수익률', ascending=False)
if not df_yield.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df_yield['회사명'], df_yield['수익률'])
    ax.set_xlabel("회사명")
    ax.set_ylabel("수익률 (%)")
    ax.set_title("공모주 수익률 비교")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)
else:
    st.info("수익률 데이터가 없습니다.")

# ✅ 매출액 그래프
st.subheader("📊 매출액")
df_rev = df_year.dropna(subset=['매출액']).sort_values(by='매출액', ascending=False)
if not df_rev.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df_rev['회사명'], df_rev['매출액'])
    ax.set_title("매출액")
    ax.set_xlabel("회사명")
    ax.set_ylabel("금액")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

# ✅ 영업이익 그래프
st.subheader("📊 영업이익")
df_op = df_year.dropna(subset=['영업이익']).sort_values(by='영업이익', ascending=False)
if not df_op.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df_op['회사명'], df_op['영업이익'])
    ax.set_title("영업이익")
    ax.set_xlabel("회사명")
    ax.set_ylabel("금액")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

# ✅ 당기순이익 그래프
st.subheader("📊 당기순이익")
df_net = df_year.dropna(subset=['당기순이익']).sort_values(by='당기순이익', ascending=False)
if not df_net.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df_net['회사명'], df_net['당기순이익'])
    ax.set_title("당기순이익")
    ax.set_xlabel("회사명")
    ax.set_ylabel("금액")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)
