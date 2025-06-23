# viewer/app.py

import streamlit as st
from parser import flatten_metrics_data

st.set_page_config(page_title="OTEL JSON Viewer", layout="wide")
st.title("📊 대용량 OTEL JSON Viewer")

uploaded_file = st.file_uploader("JSON 파일 업로드 (.json)", type=["json"])

if uploaded_file:
    try:
        st.info("📥 JSON 파일을 처리 중입니다...")
        df = flatten_metrics_data(uploaded_file)
        st.success(f"✅ {len(df)}개의 메트릭 데이터를 로드했습니다.")
        st.dataframe(df, use_container_width=True)

        # 필터 및 검색 (선택 사항)
        with st.expander("🔍 필터 기능", expanded=False):
            metric_filter = st.selectbox("메트릭 이름 선택", options=["전체"] + sorted(df["metric_name"].unique().tolist()))
            if metric_filter != "전체":
                filtered_df = df[df["metric_name"] == metric_filter]
                st.dataframe(filtered_df, use_container_width=True)

    except Exception as e:
        st.error(f"❌ 에러 발생: {str(e)}")
