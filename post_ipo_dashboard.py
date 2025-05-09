import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ✅ 데이터 불러오기 함수
@st.cache_data(show_spinner=True)
def load_data(file=None):
    if file is not None:
        df = pd.read_csv(file, encoding="utf-8-sig")
    else:
        # ✅ 정상적인 raw URL로 수정됨
        url = "https://raw.githubusercontent.com/Fairway220405/post-ipo-dashboard/main/sample.csv"
        df = pd.read_csv(url, encoding="utf-8-sig")

    df = df.dropna(subset=["연도"])
    df["연도"] = df["연도"].astype(str)

    if "label" not in df.columns:
        df["label"] = df["연도"].astype(str) + "_" + df["보고서명"].str.replace("보고서", "").str.replace("분기", "Q")

    return df

def main():
    st.set_page_config(page_title="POST-IPO 실적 대시보드", layout="wide")
    st.title("📊 POST-IPO 실적 분석 대시보드")

    st.sidebar.header("📁 CSV 업로드")
    file = st.sidebar.file_uploader("실적 CSV를 업로드하거나 샘플을 사용할 수 있습니다.", type=["csv"])
    df = load_data(file)

    st.subheader("✅ 데이터 미리보기 (한글 인코딩 확인)")
    st.dataframe(df.head())

    selected_years = st.sidebar.multiselect("📅 연도 선택", sorted(df["연도"].unique()), default=sorted(df["연도"].unique()))
    selected_reports = st.sidebar.multiselect("📄 보고서 선택", df["보고서명"].unique().tolist(), default=df["보고서명"].unique().tolist())
    filtered = df[df["연도"].isin(selected_years) & df["보고서명"].isin(selected_reports)]

    if filtered.empty:
        st.warning("❗ 조건에 맞는 데이터가 없습니다.")
        return

    st.subheader("📑 실적 요약")
    st.dataframe(filtered)

    for metric in ["매출액", "영업이익", "당기순이익", "자산총계"]:
        st.subheader(f"📈 {metric} 추이")
        plot_df = filtered[["label", metric]].copy()
        plot_df[metric] = plot_df[metric].astype(str).str.replace(",", "").astype(float)

        fig, ax = plt.subplots()
        ax.plot(plot_df["label"], plot_df[metric], marker="o")
        ax.set_title(metric)
        ax.set_ylabel(f"{metric} (억원)")
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x / 1e8)}억'))

        ax.set_xticks(plot_df["label"])
        ax.set_xticklabels(plot_df["label"], rotation=45)
        st.pyplot(fig)

if __name__ == "__main__":
    main()
