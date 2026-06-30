import pandas as pd

def load_csv(uploaded_file):
    """
    Loads a CSV file and return a pandas Dataframe
    """
    try: 
        df=pd.read_csv(uploaded_file)
        return df, None
    except Exception as e:
        return None, str(e)
    
