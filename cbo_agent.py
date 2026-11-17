from ai_client import ask_gemini

def generate_business_report(sales_report: str, inventory_report: str, review_report: str) -> str:
    prompt=f"You are the Chief Business Officer of DataPilot. Combine these reports into business health, top priorities, action plan and final advice. Do not invent data.\nSALES:\n{sales_report}\nINVENTORY:\n{inventory_report}\nCUSTOMER REVIEWS:\n{review_report}"
    return ask_gemini(prompt, "Executive report requires Gemini API. Review the sales, inventory and customer sections above for the current business picture.")
