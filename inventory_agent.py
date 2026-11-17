from ai_client import ask_gemini

def analyze_inventory(df):
    if df.empty: return "No inventory records are available."
    low=df[df.Stock_Status=="Reorder"]
    fallback=f"Products analysed: {len(df)}\nProducts needing reorder: {len(low)}\nTotal units to reorder: {int(low.Reorder_Quantity.sum())}\n\nReorder list:\n{low[['Product','Stock','Minimum_Stock','Reorder_Quantity']].to_string(index=False)}"
    prompt=f"Act as an inventory analyst. Explain inventory risks and practical reorder priorities. Do not invent figures.\n{fallback}"
    return ask_gemini(prompt, fallback)
