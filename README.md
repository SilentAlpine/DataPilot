# MerchantMind AI — Complete Data Science with AI Project

A Python-only Streamlit business intelligence application that preserves the MerchantMind AI business-agent concept and demonstrates the Internshala Data Science with AI course areas.

## Run on Windows
1. Install Python 3.10–3.12.
2. Extract this ZIP and open the `MerchantMind_AI_Complete` folder.
3. Open PowerShell in this folder.
4. Create a virtual environment (recommended): `py -m venv .venv`
5. Activate it: `.venv\Scripts\Activate.ps1`
6. Install dependencies: `python -m pip install -r requirements.txt`
7. Open `.env` and replace `PASTE_YOUR_GEMINI_API_KEY_HERE` with your Google Gemini API key.
8. Start the app: `python -m streamlit run app.py`

**Shortcut:** after Python is installed, double-click `RUN_MERCHANTMIND.bat`. It creates the virtual environment, installs the requirements and launches Streamlit automatically.

The included `.env` file already has the setting name. Only replace the placeholder value with your API key. Never share or upload your real API key.

## Demo mode
The app includes sample sales, inventory and customer review datasets. Data analysis, charts, cleaning, Excel export and the local Random Forest forecast work without an API key. Gemini-powered summaries and the multi-agent executive report require a valid key.

## Course mapping
- Introduction to Data Science with AI: end-to-end data workflow and AI-assisted business insights.
- Data Analysis with AI-Powered Excel: upload CSV/XLSX, descriptive statistics, correlation analysis, clean data and export to Excel.
- Data Visualization: interactive Python/Plotly dashboards demonstrating visualization concepts. This is not a native Power BI or Tableau file.
- Working with Data: column normalization, duplicate and missing-value checks, numeric conversion and cleaning.
- Predictive Analytics using Machine Learning: Random Forest regression forecast with MAE, RMSE and R² evaluation.
- Capstone Project: integrated MerchantMind AI business analytics workspace.
- Final Test: course assessment is not a software feature; retain the actual test score separately in the training report.

## Upload formats
- Sales: CSV/XLSX with `Date`, `Revenue`; optional `Orders`.
- Inventory: CSV/XLSX with `Product`, `Stock`; optional `Minimum_Stock`.
- Reviews: CSV/XLSX with `Review_Text`; optional `Rating`, `Product`, `Date`.

Column names are normalized for common variants. The app starts with built-in sample data and lets you upload your own files from the relevant pages.

## Main files
- `app.py`: Streamlit user interface and navigation
- `sales_agent.py`, `inventory_agent.py`, `review_agent.py`, `cbo_agent.py`: AI business agents
- `workflow.py`: multi-agent workflow orchestration
- `data_utils.py`: data loading, cleaning and preparation
- `ml_engine.py`: predictive analytics model
- `database.py`: SQLite persistence
- `data/`: sample datasets
- `RUN_MERCHANTMIND.bat`: Windows setup and launch helper
- `PROJECT_CHECK.py`: offline data/ML validation script

## Important academic note
Use this as a project implementation and learning aid. Run it, inspect the output, understand the workflow, and capture your own screenshots for the training report. Do not claim that the sample data represents real company transactions. The forecasting model is a demonstration and should not be presented as a guaranteed forecast.
