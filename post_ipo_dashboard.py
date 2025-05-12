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
    matplotlib.rc('font', family='DejaVu Sans')  # 리눅스 기본

matplotlib.rcParams['axes.unicode_minus'] = False

# ✅ 데이터 로드 + 수익률 숫자 변환
df = pd.read_csv("ipo_merged_with_yield.csv")
df['수익률'] = pd.to_numeric(df['수익률'], errors='coerce')

st.title("📈 IPO 대시보드")

st.subheader("📋 데이터 미리보기")
st.dataframe(df)

st.subheader("📊 공모주 수익률 차트")

if '회사명' in df.columns and '수익률' in df.columns:
    df_clean = df.dropna(subset=['수익률'])  # NaN 제거
    df_sorted = df_clean.sort_values(by='수익률', ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(df_sorted['회사명'], df_sorted['수익률'])
    ax.set_title("공모주 수익률 비교", fontsize=14)
    ax.set_xlabel("회사명")
    ax.set_ylabel("수익률 (%)")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)
else:
    st.warning("데이터에 '회사명'과 '수익률' 컬럼이 필요합니다.")
