import streamlit as st
import numpy as np
from PIL import Image
import sqlite3
from datetime import datetime
import random

# Page config
st.set_page_config(
    page_title="🗑️ Smart Waste Classifier", 
    page_icon="🗑️",
    layout="wide"
)

# Simulate model (demo mode)
class_names = ['Organic 🌿', 'Plastic ♻️', 'Recyclable 📈']

# Database setup
@st.cache_resource
def init_db():
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS predictions 
                 (id INTEGER PRIMARY KEY, class TEXT, confidence REAL, 
                  timestamp TEXT)''')
    conn.commit()
    return conn

conn = init_db()

def save_prediction(class_name, confidence):
    c = conn.cursor()
    c.execute("INSERT INTO predictions (class, confidence, timestamp) VALUES (?, ?, ?)",
             (class_name, confidence, datetime.now().isoformat()))
    conn.commit()

def get_history():
    c = conn.cursor()
    c.execute("SELECT class, confidence, timestamp FROM predictions ORDER BY timestamp DESC LIMIT 10")
    data = [{'class': row[0], 'confidence': row[1], 'time': row[2]} for row in c.fetchall()]
    return data

# Header
st.title("🗑️ Smart Waste Classifier")
st.markdown("**Upload photo → Instant classification + disposal advice**")

# Sidebar
st.sidebar.header("📊 Stats")
st.sidebar.success("✅ Model loaded!")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📁 Upload Image")
    uploaded_file = st.file_uploader("Choose waste photo...", type=['jpg', 'jpeg', 'png'])
    
    st.header("📇 Live Camera")
    camera_image = st.camera_input("Take photo")

with col2:
    st.header("Recent History")
    history = get_history()
    if history:
        for item in history:
            st.metric(
                item['class'], 
                f"{float(item['confidence']):.1%}",
                delta=f"{datetime.fromisoformat(item['time']).strftime('%H:%M')}"
            )
    else:
        st.info("No predictions yet")

# Process image
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
elif camera_image:
    image = Image.open(camera_image)

if image:
    # Display image
    st.image(image, caption="Uploaded Waste", use_column_width=True)
    
    # Demo prediction
    with st.spinner("🔍 Analyzing waste..."):
        # Simulate model prediction
        random.seed(hash(image.tobytes()))
        prediction = np.array([random.random() for _ in range(3)])
        prediction = prediction / prediction.sum()
        
        confidence = float(np.max(prediction))
        predicted_class = np.argmax(prediction)
        class_name = class_names[predicted_class]
        
        # Save to DB
        save_prediction(class_name, confidence)
    
    # Results
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"### 🎉 **{class_name}**")
        st.markdown(f"**Confidence: {confidence:.1%}**")
    
    with col2:
        st.progress(confidence)
    
    with col3:
        st.metric("Score", f"{confidence:.1%}")
    
    # Advice
    advice = {
        0: "🍌 **Organic Waste** - Compost in green bin!",
        1: "📯️ **Plastic Waste** - Clean & recycle if symbol present!",
        2: "📋 **Recyclable** - Paper/metal/glass → Blue bin!"
    }
    st.success(advice[predicted_class])
    
    # Confidence breakdown
    st.subheader("📊 Confidence Breakdown")
    st.write("Class Probabilities:")
    for i, (cls, prob) in enumerate(zip(class_names, prediction)):
        st.write(f"{cls}: {prob:.1%}")
    
    # Simple bar display
    st.bar_chart(dict(zip(class_names, prediction)))

# Instructions
with st.expander("💵 Setup Instructions"):
    st.markdown("""
    **This is a demo version - no model training required!**
    
    **Features:**
    - 📇 Image upload from device
    - 📈 Live camera capture
    - 📋 Waste classification (3 categories)
    - 📊 Confidence breakdown
    - 📜 History tracking
    - 💯 Smart disposal advice
    
    **Perfect for E-Cell demos!**
    """)

# Footer
st.markdown("---")
st.markdown("*Built with Streamlit | Smart Waste Classification*")
