import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache_data
def load_data(file=None):
    if file is not None:
        df = pd.read_csv(file)
    else:
        # ✅ GitHub에서 자동으로 샘플 CSV 불러오기
        url = "https://raw.githubusercontent.com/YOUR_GITHUB_ID/YOUR_REPO_NAME/main/sample.csv"
        df = pd.read_csv(url)
    df = df.dropna(subset=["연도"])
    df["연도"] = df["연도"].astype(str)
    return df

def main():
    st.set_page_config(page_title="POST-IPO 재무 대시보드", layout="wide")
    st.title("📊 POST-IPO 실적 분석 대시보드")

    st.sidebar.header("📁 CSV 파일 업로드")
    file = st.sidebar.file_uploader("실적 CSV 업로드", type=["csv"])

    df = load_data(file)

    # 필터 설정
    years = sorted(df["연도"].unique())
    report_types = df["보고서명"].unique().tolist()

    selected_years = st.sidebar.multiselect("📅 연도", years, default=years)
    selected_reports = st.sidebar.multiselect("📄 보고서 유형", report_types, default=report_types)

    filtered = df[df["연도"].isin(selected_years) & df["보고서명"].isin(selected_reports)]

    if filtered.empty:
        st.warning("⚠ 조건에 맞는 데이터가 없습니다.")
        return

    st.subheader("📑 실적 요약")
    st.dataframe(filtered)

    for metric in ["매출액", "영업이익", "당기순이익", "자산총계"]:
        st.subheader(f"📈 {metric} 추이")
        plot_df = filtered[["연도", "보고서명", metric]].copy()
        plot_df[metric] = plot_df[metric].astype(str).str.replace(",", "").astype(float)
        plot_df["label"] = plot_df["연도"] + " " + plot_df["보고서명"]

        fig, ax = plt.subplots()
        ax.plot(plot_df["label"], plot_df[metric], marker="o")
        ax.set_title(metric)
        ax.set_ylabel(metric)
        ax.set_xticks(plot_df["label"])
        ax.set_xticklabels(plot_df["label"], rotation=45)
        st.pyplot(fig)

if __name__ == "__main__":
    main()
