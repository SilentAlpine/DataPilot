import sqlite3
import pandas as pd
from config import DB_PATH

ALLOWED_TABLES = {"sales", "inventory", "reviews"}

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS sales (Date TEXT, Revenue REAL, Orders INTEGER)")
        conn.execute("CREATE TABLE IF NOT EXISTS inventory (Product TEXT, Stock REAL, Minimum_Stock REAL)")
        conn.execute("CREATE TABLE IF NOT EXISTS reviews (Review_ID INTEGER, Date TEXT, Product TEXT, Rating REAL, Review_Text TEXT)")

def save_data(df: pd.DataFrame, table_name: str):
    if table_name not in ALLOWED_TABLES: raise ValueError("Invalid table name")
    with sqlite3.connect(DB_PATH) as conn: df.to_sql(table_name, conn, if_exists="replace", index=False)

def load_data(table_name: str) -> pd.DataFrame:
    if table_name not in ALLOWED_TABLES: raise ValueError("Invalid table name")
    with sqlite3.connect(DB_PATH) as conn: return pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
