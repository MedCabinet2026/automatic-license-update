from dotenv import load_dotenv
from os import getenv

load_dotenv()

def create_connection_strign(database_name) -> str:
    return  (
    f"DRIVER={getenv('DRIVER_DB')};"
    f"SERVER={getenv('SERVER')};"
    f"DATABASE={database_name};"
    f"UID={getenv('UID')};"
    f"PWD={getenv('PASSWORD')};"
    f"TrustServerCertificate={getenv('TrustServerCertificate')};"
    f"Encrypt={getenv('Encrypt')}"
)