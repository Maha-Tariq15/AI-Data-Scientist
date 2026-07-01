import plotly.express as px
import pandas as pd

def plot_histogram(df, column):
    """
    Create a histogram  for a numeric column.

    Args:
        df: Pandas DataFrame.
        column: Name of the numeric colummn.
    
    Returns:
        Plotly Figure.
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist.")
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"Column '{column}' must be numeric")
    fig=px.histogram(df, x=column,title=f"DIstribution of {column}",nbins=30)
    fig.update_layout(xaxis_title=column, yaxis_title="Count")

    return fig


def plot_boxplot(df, column):
    """
    Creates a box plot for a numeric column
    """

    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist.")
    if not pd.api.types.is_numeric_dtype(df[column]):
        raise ValueError(f"Column '{column}' must be numeric")
    
    fig = px.box(df, y=column, title=f"Box plot of {column}")

    fig.update_layout(yaxis_title=column)

    return fig

def plot_correlation_heatmap(df):
    """
    Creates a correlation heatmap for all numerical columns.

    Args:
        df: Pandas DataFrame
    
    Returns:
        plotly figure.
    """

    numeric_df=df.select_dtypes(include="number")
    correlation_matrix=numeric_df.corr()
    fig=px.imshow(correlation_matrix, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r", title="Correkation Heatmap")

    return fig

def plot_bar_chart(df, column):
    """
    Creates a bar chart for a categorica column.

    Args:
        df: Pandas DataFrame.
        column: Categorical column

    Returns: 
        plotly figure
    """

    if column not in df.columns:
        raise ValueError(f"{column} not found.")
    
    counts=(df[column].value_counts().reset_index())
    counts.columns=[column,"Count"]
    fig=px.bar(counts, x=column, y="Count", title=f"{column} Distribution")

    return fig