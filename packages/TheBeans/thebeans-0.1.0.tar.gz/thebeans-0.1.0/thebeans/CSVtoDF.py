"""This module imports a csv as a pandas dataframe."""

def csv_to_df(csv_file):
    """Converts a csv file to a pandas dataframe.

    Args:
        csv (str): The path to the csv file.

    Returns:
        pd.DataFrame: The pandas dataframe.
    """
    import pandas as pd

    return pd.read_csv(csv_file)