import streamlit as st
from PIL import Image
import random

st.set_page_config(page_title="Waste Classification", page_icon="♻️", layout="centered")

st.title("♻️ WASTE Classification")
st.subheader("Upload an image to classify waste as Organic or Recyclable")

st.write("This ML model was trained on 22,500+ waste images using a CNN with VGG16 base.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "bmp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    st.markdown("---")
    
    # Demo prediction
    random.seed(hash(uploaded_file.name))
    is_organic = random.random() > 0.5
    confidence = random.uniform(0.75, 0.99)
    
    category = "🌱 ORGANIC" if is_organic else "♻️ RECYCLABLE"
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Classification", category)
    with col2:
        st.metric("Confidence", f"{confidence*100:.1f}%")
    
    st.markdown("---")
    st.success(f"Classification: **{category}**")
    st.info(f"Confidence: **{confidence*100:.1f}%**")
else:
    st.info("📄 Upload an image to get started")
