import pandas as pd

def remove_duplicates(df):
    """
    Removes duplicate rows from a dataset.

    Args:
        df:Pandas DataFrame.
    
    Returns:
        cleaned_df: Dataframe after removing duplicates.
        removed_df: Number of duplicate rows removed.
    """

    duplicate_count = df.duplicated().sum()
    cleaned_df=df.drop_duplicates()
    return cleaned_df, duplicate_count

def fill_missing_values(df, strategy):
    """
    Fills missing values in dataset.

    Args:
        df:Pandas DataFrame
        strategy: mean, median or mode.

    returns:
        Cleaned DataFrame
    """

    cleaned_df = df.copy()
    numeric_columns = cleaned_df.select_dtypes(include="number").columns
    categorical_columns = cleaned_df.select_dtypes(include=["object", "category"]).columns

    if strategy=="mean":
        for column in numeric_columns:
            cleaned_df[column]=cleaned_df[column].fillna(cleaned_df[column].mean())
    
    elif strategy=="median":
        for column in numeric_columns:
            cleaned_df[column]=cleaned_df[column].fillna(cleaned_df[column].median())

    elif strategy=="mode":
        for column in numeric_columns:
            cleaned_df[column]=cleaned_df[column].fillna(cleaned_df[column].mode()[0])

    for column in categorical_columns:
        cleaned_df[column]=cleaned_df[column].fillna(cleaned_df[column].mode()[0])

    
    return cleaned_df


def drop_high_missing_columns(df, threshold=50):
    """
    Drop columns with missing values above the given threshold.

    Args:
        df: Pandas DataFrame.
        threshold: Maximum allowed percentage of missing values.

    Returns:
        cleaned_df: DataFrame after dropping columns.
        removed_columns: List of removed column names.
    """

    cleaned_df=df.copy()
    missing_percentage=cleaned_df.isnull().mean()*100
    removed_columns=missing_percentage[missing_percentage>threshold].index.tolist()

    cleaned_df=cleaned_df.drop(columns=removed_columns)
    return cleaned_df, removed_columns

def remove_constant_columns(df):
    """
    Remove columns that contain only one unique value.

    Args:
        df: Pandas DataFrame.

    Returns:
        cleaned_df: DataFrame after removing constant columns.
        removed_columns: List of removed column names.
    """

    cleaned_df=df.copy()
    removed_columns=[]
    for column in cleaned_df.columns:
        if cleaned_df[column].nunique(dropna=False)==1:
            removed_columns.append(column)
    cleaned_df=cleaned_df.drop(columns=removed_columns)
    
    return cleaned_df, removed_columns

def clean_dataset(df, strategy="median", threshold=50):
    """
     Clean a dataset using a complete cleaning pipeline.

    Args:
        df: Pandas DataFrame.
        strategy: Strategy for filling missing values.
        threshold: Maximum allowed percentage of missing values.

    Returns:
        cleaned_df: Cleaned DataFrame.
        cleaning_report: Summary of cleaning operations.
    """

    cleaned_df=df.copy()
    
    # Removes duplicate rows
    cleaned_df, duplicate_count=remove_duplicates(cleaned_df)

    # Drop columns with too many missing values
    cleaned_df, removed_missing_columns = drop_high_missing_columns(cleaned_df, threshold)

    # Fill remaining missing values
    cleaned_df = fill_missing_values(cleaned_df, strategy)

    # Removes constant columns
    cleaned_df, removed_constant_columns=remove_constant_columns(cleaned_df)

    cleaning_report={
        "duplicate_rows_removed":duplicate_count,
        "high_missing_columns_removed": removed_missing_columns,
        "constant_columns_removed": removed_constant_columns,
        "missing_value_strategy": strategy,
        "threshold": threshold
    }

    return cleaned_df, cleaning_report