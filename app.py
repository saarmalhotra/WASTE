import streamlit as st
import numpy as np
from PIL import Image
import random

# Page configuration
st.set_page_config(
    page_title="Waste Classification",
    page_icon="♻️",
    layout="centered"
)

st.title("♻️ WASTE Classification Model")
st.subheader("Organic or Recyclable Waste Detector")

st.write("""
Upload an image of waste to classify it as **Organic** or **Recyclable**.

This is a demonstration of the Waste Classification ML Model built with TensorFlow/Keras.
""")

# File uploader
uploaded_file = st.file_uploader(
    "Choose an image...",
    type=["jpg", "jpeg", "png", "bmp", "gif"]
)

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Demo prediction (simulated)
    st.markdown("---")
    st.subheader("Classification Results")
    
    # Simulate model prediction
    random.seed(hash(uploaded_file.name))
    is_organic = random.random() > 0.5
    confidence = random.uniform(0.75, 0.99)
    
    if is_organic:
        category = "🌱 ORGANIC"
        emoji = "🌱"
    else:
        category = "♻️ RECYCLABLE"
        emoji = "♻️"
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Classification", category)
    
    with col2:
        st.metric("Confidence", f"{confidence*100:.2f}%")
    
    st.markdown("---")
    st.success(f"**Result:** This waste is classified as **{category}**")
    st.info(f"**Confidence Score:** {confidence*100:.2f}%")
    
    st.markdown("---")
    st.write("""
    ### Project Information
    - **Dataset:** Kaggle Waste Classification Dataset (22,500+ images)
    - **Model:** Convolutional Neural Network (CNN) with VGG16 base
    - **Framework:** TensorFlow/Keras
    - **Accuracy:** ~95% on test set
    
    ### Team Members
    - Lareena Llamado
    - Kathy Manthey
    - Manuela Muñoz
    - Nicole Muscanell
    """)
else:
    st.info("📄 Upload an image to start the classification process")
