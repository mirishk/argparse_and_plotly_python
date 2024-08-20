import pandas as pd

def load_data(file_path: str, date_column: str) -> pd.DataFrame | None:

    # Load data from a CSV file and convert the specified column to datetime.
    
    try:
        df = pd.read_csv(file_path)

        if date_column not in df.columns:
            print(f"Column '{date_column}' not found in the file: {file_path}")
            return None
        
        df[date_column] = pd.to_datetime(df[date_column])
        return df
    
    except FileNotFoundError:
        print(f"File not found at path: {file_path}")
        return None
    except pd.errors.ParserError:
        print(f"Error parsing CSV file: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred while loading data: {e}")
        return None
