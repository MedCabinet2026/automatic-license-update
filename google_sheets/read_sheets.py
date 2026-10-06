import pandas as pd

GOOGLE_SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/1xyZRJS-K_Vrhf-_JmVbFJHu2C3LpBYET/export?format=csv&gid=2015338306"
)

def read_excel(): 
    return pd.read_csv(GOOGLE_SHEET_URL)

def get_customer_names(df):
    return df["Назва клініки"].tolist()