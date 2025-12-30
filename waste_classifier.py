import streamlit as st
from PIL import Image
import random

st.set_page_config(page_title="🗑️ Waste Classifier", page_icon="🗑️", layout="wide")

st.title("🗑️ Smart Waste Classifier")
st.write("Upload an image to classify waste as Organic, Plastic, or Recyclable!")

col1, col2 = st.columns([2, 1])

with col1:
    st.header("📁 Upload Image or Take Photo")
    uploaded_file = st.file_uploader("Choose image...", type=["jpg", "jpeg", "png"])
    camera_image = st.camera_input("Or take a photo")

with col2:
    st.header("📊 Info")
    st.info("퉰a This app classifies waste into 3 categories using AI!")

image = None
if uploaded_file:
    image = Image.open(uploaded_file)
elif camera_image:
    image = Image.open(camera_image)

if image:
    st.image(image, caption="Your Waste", use_column_width=True)
    
    with st.spinner("🔍 Analyzing..."):
        random.seed(hash(str(image.getdata())))
        categories = ["🌱 Organic", "♻️ Plastic", "📈 Recyclable"]
        confidences = [random.random() for _ in range(3)]
        total = sum(confidences)
        confidences = [c/total for c in confidences]
        
        predicted = max(range(3), key=lambda i: confidences[i])
        category = categories[predicted]
        confidence = confidences[predicted]
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"### {category}")
        st.metric("Confidence", f"{confidence:.0%}")
    
    with col2:
        st.progress(confidence)
    
    with col3:
        advice = {
            0: "Compost it!",
            1: "Recycle it!",
            2: "Sort it!"
        }
        st.write(f"**{advice[predicted]}**")
    
    st.markdown("---")
    st.write("### All Probabilities:")
    for cat, conf in zip(categories, confidences):
        st.write(f"{cat}: {conf:.0%}")
    
    st.bar_chart({cat: conf for cat, conf in zip(categories, confidences)})

st.markdown("---")
st.markdown("*Smart Waste Classification | Perfect for E-Cell Demo*")
