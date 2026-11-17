from ai_client import ask_gemini

def analyze_review(review_text: str) -> str:
    if not str(review_text).strip(): return "Please enter a customer review."
    prompt=f"Analyze this customer review. Return sentiment (positive/negative/neutral), main concern, what customer likes, priority and suggested business action. Do not infer facts not present.\nReview: {review_text}"
    return ask_gemini(prompt, "Review received. Add a Gemini API key to enable AI sentiment interpretation.")
