# app.py - Streamlit app with fallbacks for missing modules
import os
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import sys
sys.modules["tensorflow"] = None

import streamlit as st
import torch

# Fallback imports if agent/genai modules missing
try:
    from agent import ProductImprovementAgent
except ImportError:
    st.warning("⚠️ Using fallback agent (agent.py not found)")
    class ProductImprovementAgent:
        def run(self, review): 
            return "🔧 **Recommendation:** Improve product quality based on customer feedback"

try:
    from genai import genai_explain
except ImportError:
    st.warning("⚠️ Using fallback explainer (genai.py not found)")
    def genai_explain(review): 
        return "💡 **Explanation:** Negative sentiment detected in review text"

# Model loading with robust error handling
@st.cache_resource
def load_model():
    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        
        tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        model = AutoModelForSequenceClassification.from_pretrained(
            "distilbert-base-uncased",
            num_labels=2
        )
        
        # Try to load your trained model, fallback to pretrained if missing
        model_path = "fast_model.pt"
        if os.path.exists(model_path):
            try:
                model.load_state_dict(
                    torch.load(model_path, map_location=torch.device("cpu")),
                    strict=False
                )
                st.success("✅ Loaded custom trained model")
            except Exception as e:
                st.warning(f"⚠️ Custom model load failed ({e}), using pretrained weights")
        else:
            st.info("ℹ️ Using pretrained DistilBERT (no custom model found)")
        
        model.eval()
        return tokenizer, model
    except Exception as e:
        st.error(f"❌ Model loading failed: {str(e)}")
        st.stop()

tokenizer, model = load_model()
agent = ProductImprovementAgent()

# UI
st.set_page_config(page_title="Flipkart Review Analyzer", page_icon="🛒", layout="wide")
st.title("🛒 Flipkart Review Intelligence System")
st.markdown("### Get instant sentiment analysis + AI-powered improvement suggestions")

review = st.text_area(
    "📝 Enter Product Review", 
    height=120,
    placeholder="e.g., 'Battery dies in 2 hours and screen scratches easily'"
)

if st.button("🔍 Analyze Review", type="primary"):
    if not review.strip():
        st.warning("⚠️ Please enter a review first!")
        st.stop()
    
    with st.spinner("⚡ Analyzing sentiment..."):
        inputs = tokenizer(
            review,
            return_tensors="pt",
            truncation=True,
            max_length=64,
            padding="max_length"
        )
        
        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)
            sentiment = torch.argmax(probs, dim=1).item()
            confidence = probs[0][sentiment].item() * 100

    # Results display
    col1, col2 = st.columns([3, 1])
    with col1:
        if sentiment == 1:
            st.success(f"✅ **Positive Review** ({confidence:.1f}% confidence)")
            st.balloons()
        else:
            st.error(f"❌ **Negative Review** ({confidence:.1f}% confidence)")
    with col2:
        st.metric("Speed", "< 1s")

    # Show AI insights for negative reviews
    if sentiment == 0:
        st.markdown("---")
        
        with st.expander("🧠 GenAI Explanation", expanded=True):
            st.write(genai_explain(review))
        
        st.markdown("---")
        
        with st.expander("🤖 Product Improvement Recommendation", expanded=True):
            st.write(agent.run(review))

# Footer with setup instructions