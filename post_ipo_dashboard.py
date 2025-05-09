import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 불러오기
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df = df.dropna(subset=["연도"])
    df["연도"] = df["연도"].astype(str)
    return df

# Streamlit 대시보드
def main():
    st.set_page_config(page_title="POST-IPO 재무 대시보드", layout="wide")
    st.title("📊 POST-IPO 실적 분석 대시보드")
    
    # 파일 선택
    st.sidebar.header("📁 파일 업로드")
    file = st.sidebar.file_uploader("에이치피오 재무요약 CSV 업로드", type=["csv"])
    
    if file:
        df = load_data(file)
        
        # 필터
        year_list = sorted(df["연도"].unique())
        report_list = df["보고서명"].unique().tolist()
        
        st.sidebar.subheader("📅 연도 선택")
        selected_years = st.sidebar.multiselect("연도", year_list, default=year_list)
        
        st.sidebar.subheader("📄 보고서 유형")
        selected_reports = st.sidebar.multiselect("보고서명", report_list, default=report_list)

        filtered_df = df[df["연도"].isin(selected_years) & df["보고서명"].isin(selected_reports)]
        
        if not filtered_df.empty:
            st.subheader("📑 재무제표 요약")
            st.dataframe(filtered_df)

            # 차트
            metrics = ["매출액", "영업이익", "당기순이익", "자산총계"]
            for metric in metrics:
                st.subheader(f"📈 {metric} 추이")
                plot_df = filtered_df[["연도", "보고서명", metric]].copy()
                plot_df[metric] = plot_df[metric].str.replace(",", "").astype(float)
                plot_df["label"] = plot_df["연도"] + " " + plot_df["보고서명"]

                fig, ax = plt.subplots()
                ax.plot(plot_df["label"], plot_df[metric], marker="o")
                ax.set_title(f"{metric} 변화 추이")
                ax.set_ylabel(metric)
                ax.set_xticks(plot_df["label"])
                ax.set_xticklabels(plot_df["label"], rotation=45)
                st.pyplot(fig)
        else:
            st.warning("선택된 조건에 해당하는 데이터가 없습니다.")
    else:
        st.info("왼쪽 사이드바에서 CSV 파일을 업로드하세요.")

if __name__ == "__main__":
    main()
