"""Quick offline validation for DataPilot data and ML modules."""
from data_utils import load_sample, prepare_sales, prepare_inventory, prepare_reviews
from ml_engine import forecast_sales

sales = prepare_sales(load_sample("sales"))
inventory = prepare_inventory(load_sample("inventory"))
reviews = prepare_reviews(load_sample("reviews"))
forecast, metrics = forecast_sales(sales, 7)

assert len(sales) >= 20
assert "Stock_Status" in inventory.columns
assert "Review_Text" in reviews.columns
assert len(forecast) == 7
assert {"MAE", "RMSE", "R2"}.issubset(metrics)
print("DataPilot validation passed.")
print(f"Sales rows: {len(sales)} | Inventory products: {len(inventory)} | Reviews: {len(reviews)}")
print(f"Forecast rows: {len(forecast)} | Metrics: {metrics}")
