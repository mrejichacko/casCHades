import os
import pandas as pd


def export(data: dict,
           filename: str,
           directory: str = 'results') -> None:
    """
    Export the given dictionary data as a CSV file.

    Parameters:
    - data: Dictionary to be exported.
    - filename: Name of the CSV file (without path).
    - directory: Directory where the CSV should be saved (default is 'results').

    Returns:
    - None
    """

    # Create a DataFrame
    df = pd.DataFrame.from_dict(data, orient='index').transpose()
    # Pivot the DataFrame to have rows for each metric value
    # df = df.melt(var_name='Metric', value_name='Value')

    full_directory = os.path.join(os.getcwd(), directory)
    os.makedirs(full_directory, exist_ok=True)

    # Ensure filename ends with .csv
    if not filename.endswith('.csv'):
        filename += '.csv'

    results_path = os.path.join(full_directory, filename)

    df.to_csv(results_path, index=False)
