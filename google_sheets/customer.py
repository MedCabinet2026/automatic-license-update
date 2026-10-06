from dataclasses import dataclass
import pandas as pd

@dataclass
class Customer:
    name: str
    database: str
    port: str
    license_guid: str
    server: str

def get_customer(df: pd.DataFrame, customer_name: str) -> Customer:
    row = df.loc[df["Назва клініки"] == customer_name].iloc[0]
    return Customer(
        name=row["Назва клініки"],
        database=row["Clinic DB"],
        port=row["Port"],
        license_guid=row["SecurityProfileGUID"],
        server=row["ServerName"],
    )
