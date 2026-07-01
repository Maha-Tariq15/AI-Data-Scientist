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

    fig=px.histogram(df, x=column,title=f"DIstribution of {column}",nbins=30)
    fig.update_layout(xaxis_title=column, yaxix_title="Count")

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