import pandas as pd
import numpy as np

ALIASES = {
    "date": "Date", "day": "Date", "revenue": "Revenue", "sales": "Revenue",
    "orders": "Orders", "order_count": "Orders", "product": "Product",
    "stock": "Stock", "minimum stock": "Minimum_Stock", "minimum_stock": "Minimum_Stock",
    "rating": "Rating", "review": "Review_Text", "review_text": "Review_Text",
}

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    out=df.copy()
    out.columns=[ALIASES.get(str(c).strip().lower(), str(c).strip().replace(" ", "_")) for c in out.columns]
    return out

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    out=normalize_columns(df)
    out=out.drop_duplicates().copy()
    for col in out.columns:
        if out[col].dtype == "object":
            out[col]=out[col].replace(r"^\s*$", np.nan, regex=True)
    return out

def load_sample(name: str) -> pd.DataFrame:
    from config import DATA_DIR
    safe={"sales":"sample_sales.csv", "inventory":"sample_inventory.csv", "reviews":"sample_reviews.csv"}
    if name not in safe: raise ValueError("Unknown sample dataset")
    return pd.read_csv(DATA_DIR/safe[name])

def prepare_sales(df: pd.DataFrame) -> pd.DataFrame:
    out=clean_dataframe(df)
    if "Revenue" not in out.columns: raise ValueError("Sales data must contain a Revenue column.")
    if "Date" not in out.columns: out["Date"]=pd.date_range(end=pd.Timestamp.today(), periods=len(out), freq="D")
    out["Date"]=pd.to_datetime(out["Date"], errors="coerce")
    out["Revenue"]=pd.to_numeric(out["Revenue"], errors="coerce")
    if "Orders" not in out.columns: out["Orders"]=1
    out["Orders"]=pd.to_numeric(out["Orders"], errors="coerce")
    out=out.dropna(subset=["Date","Revenue","Orders"])
    return out.sort_values("Date").reset_index(drop=True)

def prepare_inventory(df: pd.DataFrame) -> pd.DataFrame:
    out=clean_dataframe(df)
    required=["Product","Stock"]
    missing=[c for c in required if c not in out.columns]
    if missing: raise ValueError("Inventory data missing columns: "+", ".join(missing))
    if "Minimum_Stock" not in out.columns: out["Minimum_Stock"]=10
    out["Stock"]=pd.to_numeric(out["Stock"],errors="coerce")
    out["Minimum_Stock"]=pd.to_numeric(out["Minimum_Stock"],errors="coerce")
    out=out.dropna(subset=["Product","Stock","Minimum_Stock"])
    out["Stock_Status"]=np.where(out["Stock"]<out["Minimum_Stock"],"Reorder","Healthy")
    out["Reorder_Quantity"]=(out["Minimum_Stock"]-out["Stock"]).clip(lower=0)
    return out

def prepare_reviews(df: pd.DataFrame) -> pd.DataFrame:
    out=clean_dataframe(df)
    if "Review_Text" not in out.columns: raise ValueError("Reviews data must contain Review_Text.")
    if "Rating" in out.columns: out["Rating"]=pd.to_numeric(out["Rating"],errors="coerce")
    return out.dropna(subset=["Review_Text"])
