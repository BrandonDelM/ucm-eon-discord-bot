import pandas as pd

def is_csv_accessible(file):
    try:
        df = pd.read_csv(file)
    except FileNotFoundError:
        print(f"{file} can't be found")
        return None
    except Exception as e:
        print(f"Error reading {file}: {e}")
        return None
    return df

def get_csv_column(df, name):
    try:
        return df[name]
    except:
        return None

def get_csv_columns(df):
    urls = get_csv_column(df, 'URL')
    channels = get_csv_column(df, 'CHANNEL')
    mentions = get_csv_column(df, 'MENTION')
    files = get_csv_column(df, 'FILE')

    return urls, channels, mentions, files