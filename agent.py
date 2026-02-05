# agent.py - Simple rule-based product improvement agent (no external APIs needed)
class ProductImprovementAgent:
    def __init__(self):
        # Common pain points → actionable recommendations
        self.rules = {
            "battery": "🔋 Extend battery life: Offer power-saving modes or higher-capacity battery options",
            "slow": "⚡ Performance boost: Optimize software or upgrade processor/RAM in next model",
            "expensive": "💰 Pricing strategy: Introduce EMI options or bundle with accessories for better value",
            "quality": "🛡️ Quality control: Strengthen QC checks on assembly line for durability issues",
            "delivery": "🚚 Logistics improvement: Partner with faster couriers or add real-time tracking",
            "screen": "📱 Display upgrade: Use Gorilla Glass protection or higher brightness panels",
            "camera": "📸 Camera enhancement: Improve low-light performance with larger sensors",
            "heating": "❄️ Thermal management: Redesign heat dissipation system with better vents",
            "sound": "🔊 Audio upgrade: Partner with audio brands for tuned speakers",
            "charging": "🔌 Charging solution: Include faster charger in-box or support wireless charging"
        }
    
    def run(self, review: str) -> str:
        review_lower = review.lower()
        # Find first matching pain point
        for keyword, recommendation in self.rules.items():
            if keyword in review_lower:
                return f"**Recommendation for '{keyword}' issue:**\n{recommendation}"
        
        # Fallback generic recommendation
        return "🔧 **General Improvement:**\nConduct customer interviews to identify root cause and prioritize fixes in next product iteration."