import streamlit as st
from core.data_loader import load_csv
from core.profiler import profile_dataset

def run_app():
    st.set_page_config(
        page_title="AI Data Scientist",
        page_icon="📊",
        layout="wide"
    )

    st.title("📊 AI Data Scientist")

    st.markdown("""
    Welcome to **AI Data Scientist**.

    Upload your dataset and let AI help you:

    - 📈 Analyze your data
    - 🧹 Clean your dataset
    - 📊 Generate visualizations
    - 🤖 Train machine learning models
    - 📝 Generate AI-powered reports
    """)

    uploaded_file = st.file_uploader(
        "Upload a CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:
        df,error = load_csv(uploaded_file)
        profile = profile_dataset(df)
        if error:
            st.error(error)
            return
        st.success(f"Successfuly uploaded: {uploaded_file.name}")
        st.subheader("📊 Dataset Overview")
        col1, col2, col3=st.columns(3)
        with col1:
            st.metric("Rows", profile["rows"])
        with col2:
            st.metric("Columns", profile["columns"])
        with col3:
            st.metric("Duplicate Rows", profile["duplicate_rows"])
        
        st.subheader("📋 Column Types")
        column_types={
            "Column": list(profile["data_types"].keys()),
            "Data Type": list(profile["data_types"].values())
        }
        st.table(column_types)

        st.subheader("❗Missing Values")
        missing_values={
            "Column": list(profile["missing_values"].keys()),
            "Missing Values": list(profile["missing_values"].values())
        }

        st.table(missing_values)

        st.subheader("👀Dataset Preview")
        st.dataframe(df.head(20), use_container_width=True)