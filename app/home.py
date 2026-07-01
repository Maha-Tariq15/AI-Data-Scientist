import streamlit as st
import pandas as pd
from core.data_loader import load_csv
from core.profiler import profile_dataset
from core.quality_checker import analyze_data_quality
from core.visualizer import (plot_histogram, plot_boxplot, plot_correlation_heatmap, plot_bar_chart)
from core.cleaner import clean_dataset
from core.statistics import generate_statistics
from core.insight_generator import generate_insights

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
        if numeric_columns:
            selected_column=st.selectbox("Select a numeric column", numeric_columns)
            figure=plot_histogram(df, selected_column)
            st.plotly_chart(figure, use_container_width=True)
        
            st.subheader("Box Plot")
            box_fig=plot_boxplot(df, selected_column)
            st.plotly_chart(box_fig, use_container_width=True)

            st.subheader("Correlation Heatmap")
            heatmap = plot_correlation_heatmap(df)
            if heatmap:
                st.plotly_chart(heatmap, use_container_width=True)
        else:
            st.info("No numeric columns available for a correlation heatmap.")
        
        st.subheader("Categorical Distribution")
        categorical_columns=df.select_dtypes(include=["object", "category"]).columns.tolist()
        if categorical_columns:
            selected_cat=st.selectbox("Select categorical column", categorical_columns)

            bar_fig=plot_bar_chart(df,selected_cat)
            st.plotly_chart(bar_fig, use_container_width=True)
        else:
            st.info("No categorical columns found.")
        
        statistics=generate_statistics(df)
        st.subheader("📈 Descriptive statistics")
        for column, values in statistics.items():
            st.write(f"### {column}")
            stats_df = pd.DataFrame(values.items(), columns=["Statistic", "Value"])
            st.table(stats_df)

        insights=generate_insights(df, statistics, quality_report)
        st.subheader("AI Inshights")
        for insight in insights:
            st.write(f". {insight}")
            

        st.subheader("👀Dataset Preview")
        st.dataframe(df.head(20), use_container_width=True)


        st.subheader("🧹 Data Cleaning")
        strategy = st.selectbox("Missing Value Strategy", ["mean", "median", "mode"])
        threshold = st.slider("Missing Value Threshold (%)", min_value=0, max_value=100, value=50)

        if st.button("Clean Dataset"):
            cleaned_df, cleaning_report=clean_dataset(df, strategy, threshold)
            st.success("Dataset cleaned successfully!")
            st.write(f"Duplicate rows removed: {cleaning_report['duplicate_rows_removed']}")
            st.write("### Removed high missing columns")

            if cleaning_report["high_missing_columns_removed"]:
                st.write(cleaning_report["high_missing_columns_removed"])
            else:
                st.info("No columns removed")

            st.write("### Removed constant columns")
            if cleaning_report["constant_columns_removed"]:
                st.write(cleaning_report["constant_columns_removed"])
            else:
                st.info("No constant columns removed")

            st.subheader("🧹Cleaned Dataset Preview")
            st.dataframe(cleaned_df.head(20), use_container_width=True)
            csv=cleaned_df.to_csv(index=False)
            st.download_button(label="Download Cleaned Dataset", data=csv, file_name="cleaned_dataset.csv", mime="text/csv")
            
    

