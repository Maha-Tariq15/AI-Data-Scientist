def generate_statistics(df):
    """
    Generate descriptive statistics for numeric columns.

    Args:
        df: Pandas DataFrame.

    Returns:
        Dictionary containing statistics.
    """

    statistics={}
    numeric_columns=df.select_dtypes(include="number").columns

    for column in numeric_columns:
        statistics[column]={
            "mean": round(df[column].mean(),2),
            "median":round(df[column].median(),2),
            "minimum": round(df[column].min(),2),
            "maximum": round(df[column].max(),2),
            "standard_deviation": round(df[column].std(),2),
            "variance": round(df[column].var(),2)
        }
    return statistics