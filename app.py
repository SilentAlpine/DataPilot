import io
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from config import GEMINI_API_KEY
from data_utils import load_sample, prepare_sales, prepare_inventory, prepare_reviews, clean_dataframe
from database import init_db, save_data, load_data
from sales_agent import analyze_sales
from inventory_agent import analyze_inventory
from review_agent import analyze_review
from cbo_agent import generate_business_report
from ml_engine import forecast_sales

st.set_page_config(page_title="DataPilot", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")
init_db()

st.markdown("""
<style>
.block-container{padding-top:1.5rem;padding-bottom:2rem;max-width:1500px}
[data-testid="stMetric"]{background:linear-gradient(135deg,rgba(59,130,246,.10),rgba(16,185,129,.08));padding:16px;border:1px solid rgba(128,128,128,.18);border-radius:14px}
[data-testid="stSidebar"]{border-right:1px solid rgba(128,128,128,.18)}
.hero{padding:24px 26px;border-radius:18px;background:linear-gradient(120deg,#101827,#183b56);color:white;margin-bottom:18px}
.hero p{color:#d7e5f2;margin-bottom:0}
.small-note{color:gray;font-size:.88rem}
</style>
""", unsafe_allow_html=True)

if "sales_data" not in st.session_state: st.session_state.sales_data=load_sample("sales")
if "inventory_data" not in st.session_state: st.session_state.inventory_data=load_sample("inventory")
if "reviews_data" not in st.session_state: st.session_state.reviews_data=load_sample("reviews")

sales=prepare_sales(st.session_state.sales_data)
inventory=prepare_inventory(st.session_state.inventory_data)
reviews=prepare_reviews(st.session_state.reviews_data)

with st.sidebar:
    st.markdown("# 🧠 DataPilot")
    st.caption("AI-powered business intelligence")
    page=st.radio("NAVIGATION",["Overview","Sales Analytics","Excel & Data Analysis","Inventory Management","Customer Reviews","Predictive Analytics","AI Business Assistant","Data Quality & Reports"],label_visibility="collapsed")
    st.divider()
    st.caption("DATA SOURCE")
    st.write(f"Sales records: **{len(sales)}**")
    st.write(f"Inventory products: **{len(inventory)}**")
    st.write(f"Customer reviews: **{len(reviews)}**")
    if GEMINI_API_KEY and GEMINI_API_KEY != "PASTE_YOUR_GEMINI_API_KEY_HERE": st.success("Gemini API configured")
    else: st.warning("Demo mode · Add Gemini API key in .env for AI insights")
    if st.button("Restore sample datasets", use_container_width=True):
        st.session_state.sales_data=load_sample("sales"); st.session_state.inventory_data=load_sample("inventory"); st.session_state.reviews_data=load_sample("reviews"); st.rerun()

st.markdown('<div class="hero"><h1>DataPilot</h1><p>Your Python-powered business analytics and AI decision support workspace.</p></div>',unsafe_allow_html=True)

def metric_row():
    revenue=float(sales.Revenue.sum()) if len(sales) else 0
    orders=float(sales.Orders.sum()) if len(sales) else 0
    a,b,c,d=st.columns(4)
    a.metric("Total Revenue",f"₹{revenue:,.0f}")
    b.metric("Total Orders",f"{orders:,.0f}")
    c.metric("Average Order Value",f"₹{(revenue/orders if orders else 0):,.0f}")
    d.metric("Low-stock Products",f"{int((inventory.Stock_Status=='Reorder').sum())}")

@st.cache_data
def _excel_bytes(df):
    buffer=io.BytesIO()
    with pd.ExcelWriter(buffer,engine="openpyxl") as writer: df.to_excel(writer,index=False,sheet_name="Cleaned Data")
    return buffer.getvalue()

def chart_download(df, filename, label="Download CSV"):
    st.download_button(label,df.to_csv(index=False).encode("utf-8"),file_name=filename,mime="text/csv")

if page=="Overview":
    metric_row(); st.subheader("Business performance")
    l,r=st.columns([1.6,1])
    with l:
        daily=sales.groupby("Date",as_index=False).agg(Revenue=("Revenue","sum"),Orders=("Orders","sum"))
        st.plotly_chart(px.line(daily,x="Date",y="Revenue",title="Revenue trend",markers=True,template="plotly_white"),use_container_width=True)
    with r:
        st.plotly_chart(px.pie(inventory,names="Stock_Status",title="Inventory health",hole=.55),use_container_width=True)
    st.subheader("Recent sales records"); st.dataframe(sales.tail(10),use_container_width=True,hide_index=True)
    st.subheader("Products requiring attention")
    low=inventory[inventory.Stock_Status=="Reorder"]
    if low.empty: st.success("All products are at or above their minimum stock level.")
    else: st.dataframe(low,use_container_width=True,hide_index=True)

elif page=="Sales Analytics":
    st.subheader("Sales Analytics")
    sales_upload=st.file_uploader("Upload sales CSV / Excel",type=["csv","xlsx"],key="sales_upload")
    if sales_upload:
        try:
            raw_sales=pd.read_csv(sales_upload) if sales_upload.name.lower().endswith(".csv") else pd.read_excel(sales_upload)
            # Validate before replacing the active sales dataset.
            prepare_sales(raw_sales)
            st.session_state.sales_data=raw_sales
            st.success("Sales dataset loaded successfully. Refreshing analytics...")
            st.rerun()
        except Exception as e:
            st.error(f"Sales upload error: {e}")
    metric_row()
    freq=st.selectbox("Group sales by",["Daily","Weekly","Monthly"])
    temp=sales.set_index("Date")
    rule={"Daily":"D","Weekly":"W","Monthly":"MS"}[freq]
    grouped=temp.resample(rule).agg(Revenue=("Revenue","sum"),Orders=("Orders","sum")).reset_index()
    a,b=st.columns(2)
    a.plotly_chart(px.line(grouped,x="Date",y="Revenue",markers=True,title=f"{freq} revenue",template="plotly_white"),use_container_width=True)
    b.plotly_chart(px.bar(grouped,x="Date",y="Orders",title=f"{freq} orders",template="plotly_white"),use_container_width=True)
    st.subheader("Sales data"); st.dataframe(sales,use_container_width=True,hide_index=True); chart_download(sales,"merchantmind_sales_clean.csv")
    if st.button("Generate AI sales analysis",type="primary"):
        with st.spinner("Analysing sales..."): st.markdown(analyze_sales(sales))

elif page=="Excel & Data Analysis":
    st.subheader("Excel & Data Analysis")
    st.write("Upload a CSV or Excel workbook. The first worksheet is read by default.")
    uploaded=st.file_uploader("Upload sales / business data",type=["csv","xlsx"])
    if uploaded:
        try:
            raw=pd.read_csv(uploaded) if uploaded.name.lower().endswith(".csv") else pd.read_excel(uploaded)
            st.session_state.uploaded_analysis=raw
        except Exception as e: st.error(f"Could not read file: {e}")
    raw=st.session_state.get("uploaded_analysis",sales)
    cleaned=clean_dataframe(raw)
    st.caption(f"Rows: {len(cleaned)} · Columns: {len(cleaned.columns)}")
    st.dataframe(cleaned.head(100),use_container_width=True)
    a,b,c=st.columns(3); a.metric("Duplicate rows",int(raw.duplicated().sum())); b.metric("Missing cells",int(raw.isna().sum().sum())); c.metric("Numeric columns",len(cleaned.select_dtypes(include="number").columns))
    st.subheader("Descriptive statistics"); st.dataframe(cleaned.describe(include="all").T,use_container_width=True)
    numeric=cleaned.select_dtypes(include="number")
    if len(numeric.columns)>=2:
        st.subheader("Correlation analysis"); st.plotly_chart(px.imshow(numeric.corr(numeric_only=True),text_auto=True,aspect="auto",title="Numeric feature correlation"),use_container_width=True)
    st.download_button("Download cleaned Excel file",data=_excel_bytes(cleaned),file_name="merchantmind_cleaned_data.xlsx",mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    chart_download(cleaned,"merchantmind_cleaned_data.csv")

elif page=="Inventory Management":
    st.subheader("Inventory Management")
    uploaded=st.file_uploader("Upload inventory CSV / Excel",type=["csv","xlsx"],key="inv_upload")
    if uploaded:
        try:
            raw=pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
            st.session_state.inventory_data=raw; st.rerun()
        except Exception as e: st.error(str(e))
    low=inventory[inventory.Stock_Status=="Reorder"]
    a,b,c=st.columns(3); a.metric("Total SKUs",len(inventory)); b.metric("Need reorder",len(low)); c.metric("Units to reorder",int(low.Reorder_Quantity.sum()))
    st.plotly_chart(px.bar(inventory.sort_values("Stock"),x="Product",y="Stock",color="Stock_Status",title="Current stock by product",template="plotly_white"),use_container_width=True)
    st.dataframe(inventory,use_container_width=True,hide_index=True); chart_download(inventory,"merchantmind_inventory_status.csv")
    if st.button("Generate AI inventory recommendations",type="primary"):
        with st.spinner("Reviewing inventory..."): st.markdown(analyze_inventory(inventory))

elif page=="Customer Reviews":
    st.subheader("Customer Review Analysis")
    uploaded=st.file_uploader("Upload reviews CSV / Excel",type=["csv","xlsx"],key="review_upload")
    if uploaded:
        try:
            raw=pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
            st.session_state.reviews_data=raw; st.rerun()
        except Exception as e: st.error(str(e))
    if "Rating" in reviews.columns:
        a,b=st.columns(2); a.metric("Average rating",f"{reviews.Rating.mean():.2f} / 5"); b.metric("Total reviews",len(reviews))
        st.plotly_chart(px.histogram(reviews,x="Rating",nbins=5,title="Customer rating distribution"),use_container_width=True)
    st.dataframe(reviews,use_container_width=True,hide_index=True)
    review_text=st.text_area("Analyse an individual customer review",height=120,placeholder="Paste a customer review here...")
    if st.button("Analyse review with Gemini",type="primary",disabled=not bool(review_text.strip())):
        with st.spinner("Analysing review..."): st.markdown(analyze_review(review_text))
    if st.button("Summarise uploaded reviews"):
        summary=reviews[[c for c in ["Rating","Review_Text","Product"] if c in reviews.columns]].head(100).to_string(index=False)
        from ai_client import ask_gemini
        st.markdown(ask_gemini("Summarise review themes, sentiment patterns and improvement opportunities. Do not invent statistics.\n"+summary,"Review records loaded. Add Gemini API to generate AI review themes."))

elif page=="Predictive Analytics":
    st.subheader("Predictive Analytics using Machine Learning")
    st.info("A Random Forest regression model uses historical date patterns to estimate upcoming revenue. This is a learning/demo forecast, not a guaranteed business prediction.")
    horizon=st.slider("Forecast horizon (days)",7,30,14)
    if st.button("Train model and generate forecast",type="primary"):
        try:
            with st.spinner("Training Random Forest model..."): future,metrics=forecast_sales(sales,horizon)
            st.session_state.forecast=future; st.session_state.forecast_metrics=metrics
        except Exception as e: st.error(str(e))
    if "forecast" in st.session_state:
        future=st.session_state.forecast; metrics=st.session_state.forecast_metrics
        a,b,c=st.columns(3); a.metric("MAE",f"₹{metrics['MAE']:,.2f}"); b.metric("RMSE",f"₹{metrics['RMSE']:,.2f}"); c.metric("R²",f"{metrics['R2']:.3f}")
        fig=go.Figure(); fig.add_trace(go.Scatter(x=sales.Date,y=sales.Revenue,name="Historical revenue")); fig.add_trace(go.Scatter(x=future.Date,y=future.Predicted_Revenue,name="Predicted revenue",line=dict(dash="dash"))); fig.update_layout(title="Historical and forecast revenue",template="plotly_white",xaxis_title="Date",yaxis_title="Revenue")
        st.plotly_chart(fig,use_container_width=True); st.dataframe(future,use_container_width=True,hide_index=True); chart_download(future,"merchantmind_sales_forecast.csv")

elif page=="AI Business Assistant":
    st.subheader("AI Business Assistant · Multi-agent business report")
    st.write("Combines Sales, Inventory and Customer Review agents into one executive report.")
    review_sample="\n".join(reviews.Review_Text.astype(str).head(12).tolist()) if "Review_Text" in reviews.columns else "No review text available"
    if st.button("Generate complete business report",type="primary"):
        with st.spinner("Running Sales, Inventory, Review and CBO agents..."):
            sr=analyze_sales(sales); ir=analyze_inventory(inventory); rr=analyze_review(review_sample); er=generate_business_report(sr,ir,rr)
        st.session_state.business_reports={"Sales Agent":sr,"Inventory Agent":ir,"Review Agent":rr,"Chief Business Officer":er}
    if "business_reports" in st.session_state:
        for title,body in st.session_state.business_reports.items():
            with st.expander(title,expanded=(title=="Chief Business Officer")): st.markdown(body)

elif page=="Data Quality & Reports":
    st.subheader("Working with Data · Data quality")
    for title,df in [("Sales",st.session_state.sales_data),("Inventory",st.session_state.inventory_data),("Reviews",st.session_state.reviews_data)]:
        with st.expander(f"{title} dataset",expanded=(title=="Sales")):
            clean=clean_dataframe(df)
            a,b,c=st.columns(3); a.metric("Rows",len(df)); b.metric("Duplicate rows",int(df.duplicated().sum())); c.metric("Missing cells",int(df.isna().sum().sum()))
            st.dataframe(clean.head(200),use_container_width=True)
            st.download_button(f"Download {title} cleaned CSV",clean.to_csv(index=False).encode(),file_name=f"{title.lower()}_cleaned.csv",mime="text/csv",key=f"dl_{title}")
    st.divider(); st.subheader("Save current data to local SQLite database")
    if st.button("Save all datasets to database"):
        save_data(sales,"sales"); save_data(inventory,"inventory"); save_data(reviews,"reviews"); st.success("All datasets saved to merchantmind.db")
    st.caption("The database is stored locally alongside the app. Streamlit Community Cloud storage may reset after app restarts; use external persistent storage for production deployments.")

