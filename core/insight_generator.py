def dataset_insights(df):
    insights = []

    # Dataset overview
    insights.append(
        f"The dataset contains {df.shape[0]} rows and {df.shape[1]} columns."
    )

    numeric_columns = df.select_dtypes(include="number").columns
    categorical_columns = df.select_dtypes(include=["object", "category"]).columns

    insights.append(
        f"The dataset contains {len(numeric_columns)} numeric columns and {len(categorical_columns)} categorical columns."
    )

    return insights


def quality_insights(df, quality_report):
    insights=[]
    # Duplicate rows
    duplicates = df.duplicated().sum()

    if duplicates == 0:
        insights.append("No duplicate rows were found.")
    else:
        insights.append(f"The dataset contains {duplicates} duplicate rows.")

    # Missing values
    missing = sum(quality_report["missing_value_count"].values())

    if missing == 0:
        insights.append("No missing values were found.")
    else:
        insights.append(f"The dataset contains {missing} missing values.")
    return insights

def variability_insights(statistics):
    insights = []
    # Variability
    for column, values in statistics.items():

        mean = values["mean"]
        std = values["standard_deviation"]

        if mean != 0:

            cv = std / mean

            if cv < 0.2:
                insights.append(f"{column} has low variability.")

            elif cv < 0.5:
                insights.append(f"{column} has moderate variability.")

            else:
                insights.append(f"{column} has high variability.")

        else:
            insights.append(
                f"Variability for {column} could not be determined because the mean is zero."
            )
    return insights

def categorical_insights(df):
    insights =[]
    # Categorical columns
    categorical_columns = df.select_dtypes(include=["object", "category"]).columns
    for column in categorical_columns:

        unique_values = df[column].nunique()

        if unique_values <= 10:
            insights.append(
                f"{column} contains only {unique_values} unique categories."
            )
        else:
            insights.append(
                f"{column} contains {unique_values} unique values."
            )
    
    return insights

def correlation_insights(df):
    insights = []
    numeric_df = df.select_dtypes(include="number")
    if len(numeric_df.columns)<2:
        return insights
    correlation_matrix=numeric_df.corr()
    columns=correlation_matrix.columns

    for i in range(len(columns)):
        for j in range(i+1, len(columns)):
            correlation = correlation_matrix.iloc[i,j]
            if abs(correlation)>=0.7:
                direction = "positive" if correlation > 0 else "negative"
                insights.append(f"{columns[i]} and {columns[j]} have a strong {direction} correlation ({correlation:.2f}).")
    return insights

def outlier_insights(df):
    insights = []
    numeric_columns=df.select_dtypes(include="number").columns
    for column in numeric_columns:
        q1=df[column].quantile(0.25)
        q3=df[column].quantile(0.75)

        iqr=q3-q1
        lower = q1 - 1.5*iqr
        upper = q3 + 1.5*iqr

        outliers=df[(df[column]<lower) | (df[column]>upper)]

        count=len(outliers)
        if count==0:
            insights.append(f"{column} contains no significant outliers.")
        else:
            insights.append(f"{column} contains {count} potential outliers.")
    return insights
        
    

def generate_insights(df, statistics, quality_report):
    insights = []
    insights.extend(dataset_insights(df))
    insights.extend(quality_insights(df, quality_report))
    insights.extend(variability_insights(statistics))
    insights.extend(categorical_insights(df))
    insights.extend(correlation_insights(df))
    insights.extend(outlier_insights(df))
    
    return insights