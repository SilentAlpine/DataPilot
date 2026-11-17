import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

def forecast_sales(df: pd.DataFrame, horizon: int = 14):
    data=df[["Date","Revenue"]].dropna().copy().sort_values("Date")
    if len(data)<20: raise ValueError("At least 20 valid dated sales records are required for a forecast.")
    data["day_index"]=(data.Date-data.Date.min()).dt.days
    data["weekday"]=data.Date.dt.weekday
    data["month"]=data.Date.dt.month
    data["day_of_month"]=data.Date.dt.day
    X=data[["day_index","weekday","month","day_of_month"]]; y=data.Revenue.astype(float)
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,shuffle=False)
    model=RandomForestRegressor(n_estimators=160,random_state=42,min_samples_leaf=2)
    model.fit(X_train,y_train)
    pred_test=model.predict(X_test)
    metrics={"MAE":float(mean_absolute_error(y_test,pred_test)),"RMSE":float(np.sqrt(mean_squared_error(y_test,pred_test))),"R2":float(r2_score(y_test,pred_test)) if len(y_test)>1 else 0.0}
    # Refit on all available records before future prediction
    model.fit(X,y)
    future_dates=pd.date_range(data.Date.max()+pd.Timedelta(days=1), periods=int(horizon), freq="D")
    future=pd.DataFrame({"Date":future_dates})
    future["day_index"]=(future.Date-data.Date.min()).dt.days
    future["weekday"]=future.Date.dt.weekday; future["month"]=future.Date.dt.month; future["day_of_month"]=future.Date.dt.day
    future["Predicted_Revenue"]=model.predict(future[["day_index","weekday","month","day_of_month"]]).clip(min=0)
    return future,metrics
