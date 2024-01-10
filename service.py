import pandas as pd

CSV_FILE = 'data.csv'

# Helper function to read all data from the CSV file
def read_csv():
    try:
        data = pd.read_csv(CSV_FILE)
        return data.to_dict(orient='records')
    except FileNotFoundError:
        return []

# Helper function to read all data from the CSV file into a Pandas Dataframe
def read_csv_as_dataframe():
    try:
        data = pd.read_csv(CSV_FILE)
        return data
    except FileNotFoundError:
        return []

# Helper function to write data to the CSV file
def write_csv(data):
    df = pd.DataFrame(data)
    df.to_csv(CSV_FILE, index=False)