import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from PIL import Image
import io

# Page configuration
st.set_page_config(
    page_title="Waste Classification",
    page_icon="♻️",
    layout="centered"
)

st.title("♻️ WASTE Classification Model")
st.subheader("Organic or Recyclable Waste Detector")

# Load model
@st.cache_resource
def load_model():
    try:
        model = tf.keras.models.load_model('final_model_weights.hdf5')
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()

if model is not None:
    st.write("Upload an image of waste to classify it as **Organic** or **Recyclable**.")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=["jpg", "jpeg", "png", "bmp", "gif"]
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Process image for prediction
        img = image.resize((180, 180))
        img_array = img_to_array(img)
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Make prediction
        prediction = model.predict(img_array, verbose=0)
        confidence = max(prediction[0])
        
        # Interpret results
        if prediction[0][0] > prediction[0][1]:
            category = "🌱 ORGANIC"
            confidence_score = prediction[0][0]
        else:
            category = "♻️ RECYCLABLE"
            confidence_score = prediction[0][1]
        
        # Display results
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Classification", category)
        
        with col2:
            st.metric("Confidence", f"{confidence_score*100:.2f}%")
        
        st.markdown("---")
        st.write(f"**Result:** This waste is classified as **{category}**")
        st.write(f"**Confidence Score:** {confidence_score*100:.2f}%")
else:
    st.error("Failed to load the model. Please check if the model file exists.")
