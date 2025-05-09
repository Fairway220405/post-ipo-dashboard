import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib
import platform

# ✅ 한글 폰트 설정
if platform.system() == 'Windows':
    matplotlib.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':
    matplotlib.rc('font', family='AppleGothic')
else:
    matplotlib.rc('font', family='NanumGothic')

matplotlib.rcParams['axes.unicode_minus'] = False

# ✅ 데이터 불러오기
@st.cache_data(show_spinner=True)
def load_data(file=None):
    if file is not None:
        df = pd.read_csv(file, encoding="utf-8-sig")
    else:
        url = "https://raw.githubusercontent.com/Fairway220405/post-ipo-dashboard/main/sample.csv"
        df = pd.read_csv(url, encoding="utf-8-sig")

    df = df.dropna(subset=["연도"])
    df["연도"] = df["연도"].astype(str)

    if "label" not in df.columns:
        df["label"] = df["연도"].astype(str) + "_" + df["보고서명"].str.replace("보고서", "").str.replace("분기", "Q")

    return df

# ✅ 메인
def main():
    st.set_page_config(page_title="POST-IPO 실적 대시보드", layout="wide")
    st.title("📊 POST-IPO 실적 분석 대시보드")

    file = st.sidebar.file_uploader("CSV 파일 업로드 (없으면 샘플 사용)", type=["csv"])
    df = load_data(file)

    selected_years = st.sidebar.multiselect("📅 연도 선택", sorted(df["연도"].unique()), default=sorted(df["연도"].unique()))
    selected_reports = st.sidebar.multiselect("📄 보고서 선택", df["보고서명"].unique().tolist(), default=df["보고서명"].unique().tolist())
    filtered = df[df["연도"].isin(selected_years) & df["보고서명"].isin(selected_reports)]

    if filtered.empty:
        st.warning("❗ 조건에 맞는 데이터가 없습니다.")
        return

    # ✅ 실적 요약 테이블: 통화 포맷 적용
    numeric_cols = ["매출액", "영업이익", "당기순이익", "자산총계"]
    for col in numeric_cols:
        filtered[col] = filtered[col].astype(float).map(lambda x: f"₩{x:,.0f}")

    st.subheader("📑 실적 요약")
    st.dataframe(filtered)

    # ✅ 그래프 (값 위에 '억' 표기)
    for metric in numeric_cols:
        st.subheader(f"📈 {metric} 추이")
        plot_df = df[df["연도"].isin(selected_years) & df["보고서명"].isin(selected_reports)][["label", metric]].copy()
        plot_df[metric] = plot_df[metric].astype(str).str.replace(",", "").str.replace("₩", "").astype(float)

        fig, ax = plt.subplots()
        ax.plot(plot_df["label"], plot_df[metric], marker="o")
        ax.set_title(metric)
        ax.set_ylabel(f"{metric} (억원)")
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x / 1e8)}억'))
        ax.set_xticks(plot_df["label"])
        ax.set_xticklabels(plot_df["label"], rotation=45)

        # ✅ 각 점에 “123억” 형식으로 표시
        for i, row in plot_df.iterrows():
            ax.annotate(f"{int(row[metric] / 1e8)}억", (row["label"], row[metric]),
                        textcoords="offset points", xytext=(0, -15), ha='center', fontsize=8)

        st.pyplot(fig)

# ✅ 실행
if __name__ == "__main__":
    main()
