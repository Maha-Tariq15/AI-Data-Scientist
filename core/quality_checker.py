def analyze_data_quality(df, missing_threshold=50):
    """
    Analyze quality of dataset.

    Args:
        df: Pandas DataFrame.
        missing_theshold: Percentage above ehich a coulmn is considered to have a higer number of missing values.

    Returns:
        dict: Data quality info.
    """
    missing_counts=df.isnull().sum()
    missing_percentages=(missing_counts / len(df)*100).round(2)

    quality_report={
        "duplicate_rows": int(df.duplicated().sum()),
        "columns_with_missing": missing_counts[missing_counts>0].index.tolist(),
        "missing_value_count": missing_counts[missing_counts>0].to_dict(),
        "missing_percentage": missing_percentages[missing_percentages>0].to_dict(),
        "constant_columns": [col for col in df.columns if df[col].nunique(dropna=False)==1],
        "high_missing_columns": missing_percentages[missing_percentages >= missing_threshold].index.tolist()
    }

    return quality_report