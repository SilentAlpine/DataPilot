from config import GEMINI_API_KEY, GEMINI_MODEL


def get_client():
    """Return a Gemini client when an API key is configured; otherwise None."""
    if not GEMINI_API_KEY or GEMINI_API_KEY == "PASTE_YOUR_GEMINI_API_KEY_HERE":
        return None
    try:
        from google import genai
        return genai.Client(api_key=GEMINI_API_KEY)
    except Exception:
        return None


def ask_gemini(prompt: str, fallback: str = "AI response is unavailable.") -> str:
    client = get_client()
    if client is None:
        return ("Gemini API is not configured. Add your API key in the .env file to enable AI-generated insights.\n\n"
                + fallback)
    try:
        response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        return response.text or fallback
    except Exception as exc:
        return f"Gemini request failed: {exc}\n\n{fallback}"
