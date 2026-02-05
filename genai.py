# genai.py - Lightweight explanation generator (no API keys needed)
def genai_explain(review: str) -> str:
    review_lower = review.lower()
    
    # Simple pattern matching for explanations
    explanations = {
        "not worth": "Customer feels the product's value doesn't justify its price point",
        "waste of money": "Strong dissatisfaction with cost-to-benefit ratio",
        "disappointed": "Product failed to meet expectations set by marketing/description",
        "cheap": "Perceived low quality materials or construction",
        "broken": "Product arrived defective or failed prematurely",
        "slow": "Performance issues affecting user experience",
        "overheating": "Thermal management problems causing discomfort/safety concerns",
        "battery": "Power management issues leading to short usage time",
        "scratched": "Poor packaging or fragile materials causing cosmetic damage",
        "fake": "Customer suspects counterfeit product was delivered"
    }
    
    # Find best matching explanation
    for phrase, explanation in explanations.items():
        if phrase in review_lower:
            return f"💡 **Why this is negative:** {explanation}"
    
    # Fallback generic explanation
    negative_words = ["bad", "worst", "terrible", "horrible", "useless", "awful", "poor"]
    if any(word in review_lower for word in negative_words):
        return "💡 **Why this is negative:** Contains strong negative sentiment indicating product failure to meet basic expectations"
    
    return "💡 **Why this is negative:** Review expresses dissatisfaction with product performance or quality"