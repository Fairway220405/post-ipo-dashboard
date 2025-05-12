import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib
import platform

# ✅ 한글 폰트 설정 (설치 없이 시스템 내 기본값으로만 적용)
if platform.system() == 'Windows':
    matplotlib.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':
    matplotlib.rc('font', family='AppleGothic')
else:  # Linux 등
    matplotlib.rc('font', family='DejaVu Sans')

# 마이너스 깨짐 방지
matplotlib.rcParams['axes.unicode_minus'] = False

# 변경된 CSV 파일명 사용
df = pd.read_csv("ipo_merged_with_yield.csv")

# Streamlit 앱 시작
st.title("📈 IPO 대시보드")

st.subheader("데이터 미리보기")
st.dataframe(df)

st.subheader("종목별 수익률 시각화 예시")

if '회사명' in df.columns and '수익률' in df.columns:
    fig, ax = plt.subplots()
    df_sorted = df.sort_values(by='수익률', ascending=False)
    ax.bar(df_sorted['회사명'], df_sorted['수익률'])
    ax.set_xlabel("회사명")
    ax.set_ylabel("수익률 (%)")
    ax.set_title("공모주 수익률 비교")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)
else:
    st.warning("'회사명'과 '수익률' 컬럼이 필요합니다. CSV 파일을 확인하세요.")
