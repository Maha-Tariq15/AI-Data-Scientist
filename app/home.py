import streamlit as st
import pandas as pd
from core.data_loader import load_csv
from core.profiler import profile_dataset
from core.quality_checker import analyze_data_quality
from core.visualizer import plot_histogram
from core.visualizer import plot_histogram, plot_boxplot

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
        if error:
            st.error(error)
            return
        
        profile = profile_dataset(df)
        quality_report = analyze_data_quality(df)
        st.success(f"Successfully uploaded: {uploaded_file.name}")
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
            "Column": list(quality_report["missing_value_count"].keys()),
            "Missing Values": list(quality_report["missing_value_count"].values())
        }

        st.table(missing_values)


        st.subheader("🔍 Data Quality Report")
        col1, col2=st.columns(2)
        with col1:
            st.write('### Columns with missing Values')
            if quality_report["columns_with_missing"]:
                missing_columns_df = pd.DataFrame({
                    "Column": quality_report["columns_with_missing"]
                })
                st.table(missing_columns_df)
            else:
                st.success("No missing values found")
        with col2:
            st.write('### High Missing Columns')
            if quality_report["high_missing_columns"]:
                high_missing_df=pd.DataFrame({
                    "Column": quality_report["high_missing_columns"]
                })
                st.table(high_missing_df)
            else:
                st.success("No high missing columns")
        
        st.write('### Constant Columns')
        if quality_report["constant_columns"]:
            constant_df = pd.DataFrame({
                "Column": quality_report["constant_columns"]
            })
            st.table(constant_df)
        else:
            st.success("No constant columns")

        st.subheader("📊 Data Visualization")
        numeric_columns=df.select_dtypes(include=["number"]).columns.tolist()
        selected_column=st.selectbox("Select a numeric column", numeric_columns)
        figure=plot_histogram(df, selected_column)
        st.plotly_chart(figure, use_container_width=True)
        
        st.subheader("Box Plot")
        box_fig=plot_boxplot(df, selected_column)
        st.plotly_chart(box_fig, use_container_width=True)

        
        st.subheader("👀Dataset Preview")
        st.dataframe(df.head(20), use_container_width=True)