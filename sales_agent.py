import pandas as pd
from ai_client import ask_gemini

def analyze_sales(df: pd.DataFrame) -> str:
    if df.empty: return "No sales records are available."
    total=float(df.Revenue.sum()); orders=float(df.Orders.sum())
    avg=total/orders if orders else 0
    best=df.loc[df.Revenue.idxmax()]; worst=df.loc[df.Revenue.idxmin()]
    fallback=(f"Total revenue: {total:,.2f}\nTotal orders: {orders:,.0f}\nAverage order value: {avg:,.2f}\n"
              f"Highest revenue date: {best.Date.date()} ({best.Revenue:,.2f})\nLowest revenue date: {worst.Date.date()} ({worst.Revenue:,.2f})")
    prompt=f"Act as DataPilot Sales Analyst. Explain this real dataset in simple business language. Do not invent numbers. Include trends, risks and 3 actionable recommendations.\n{fallback}\nRecent data:\n{df.tail(30).to_string(index=False)}"
    return ask_gemini(prompt, fallback)
