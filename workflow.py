from sales_agent import analyze_sales
from inventory_agent import analyze_inventory
from review_agent import analyze_review
from cbo_agent import generate_business_report

def run_business_workflow(sales_data, inventory_data, review_text):
    sales=analyze_sales(sales_data)
    inventory=analyze_inventory(inventory_data)
    review=analyze_review(review_text)
    executive=generate_business_report(sales,inventory,review)
    return {"sales_report":sales,"inventory_report":inventory,"review_report":review,"executive_report":executive}
