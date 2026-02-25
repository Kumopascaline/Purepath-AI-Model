import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# Set page configuration
st.set_page_config(page_title="EcoSort: Waste Classifier", layout="centered")

# --- Waste Information Dictionary ---
# This dictionary maps the class index to the specific recycling advice
WASTE_DETAILS = {
    0: {
        "label": "Battery",
        "category": "Hazardous Waste",
        "methods": ["Do NOT throw in regular trash.", "Take to a dedicated e-waste collection point or battery recycling bin.", "Check local retail stores (like Best Buy or Home Depot) for drop-off kiosks."],
        "impact": "Batteries contain heavy metals like lead and mercury that leak into soil."
    },
    1: {
        "label": "Biological",
        "category": "Organic/Compostable",
        "methods": ["Home composting for food scraps.", "Municipal green bin collection.", "Vermicomposting (worm bins)."],
        "impact": "Organic waste in landfills produces methane, a potent greenhouse gas."
    },
    2: {"label": "Brown-glass", "category": "Recyclable (Glass)", "methods": ["Rinse and remove caps.", "Place in glass recycling bin.", "Can be recycled infinitely."], "impact": "Reduces energy needed to create new glass by 40%."},
    3: {"label": "Cardboard", "category": "Recyclable (Paper)", "methods": ["Flatten boxes to save space.", "Ensure it is dry and free of grease (no pizza boxes with oil).", "Curbside recycling."], "impact": "Recycling 1 ton of cardboard saves 17 trees."},
    4: {"label": "Clothes", "category": "Textiles", "methods": ["Donate if in good condition.", "Textile recycling banks for torn items.", "Upcycle into cleaning rags."], "impact": "The fashion industry is responsible for 10% of global carbon emissions."},
    5: {"label": "Green-glass", "category": "Recyclable (Glass)", "methods": ["Rinse and place in glass-specific bins.", "Check for local bottle deposit schemes."], "impact": "Glass never loses quality when recycled."},
    6: {"label": "Metal", "category": "Recyclable (Metal)", "methods": ["Rinse aluminum cans and tin food containers.", "Crush cans to save space.", "Scrap metal yards for larger items."], "impact": "Recycling aluminum saves 95% of the energy needed to make new metal."},
    7: {"label": "Paper", "category": "Recyclable (Paper)", "methods": ["Recycle newspapers, magazines, and office paper.", "Avoid recycling shredded paper unless in a bag (check local rules).", "Keep paper dry."], "impact": "Saves landfill space and reduces deforestation."},
    8: {"label": "Plastic", "category": "Recyclable (Plastic)", "methods": ["Check the resin code (1-7).", "Rinse out food residue.", "Remove plastic films/wraps (often recycled separately at grocery stores)."], "impact": "Plastic can take up to 500 years to decompose in oceans."},
    9: {"label": "Shoes", "category": "Textiles/Specialty", "methods": ["Donate wearable pairs.", "Specific brands (like Nike) have shoe recycling programs for soles.", "Remove laces before recycling."], "impact": "Prevents complex synthetic materials from entering landfills."},
    10: {"label": "Trash", "category": "General Waste (Non-Recyclable)", "methods": ["Landfill bin.", "Try to minimize use of these items.", "Check if item is 'Wish-cycling' (items you hope are recyclable but aren't)."], "impact": "This waste is buried and contributes to long-term pollution."},
    11: {"label": "White-glass", "category": "Recyclable (Glass)", "methods": ["Rinse and sort into clear glass containers.", "Remove metal lids (recycle lids with metal)."], "impact": "Clear glass is the most valuable for manufacturers."}
}

# --- Load Model ---
@st.cache_resource
def load_garbage_model():
    # Ensure the file name matches your uploaded file
    model = tf.keras.models.load_model('garbage_classification_model_inception.h5')
    return model

model = load_garbage_model()

# --- UI Header ---
st.title("♻️ EcoSort: Garbage Classification")
st.write("Upload an image of waste to determine its category and get recycling tips.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png","mp4"])

if uploaded_file is not None:
    # Display the image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # Preprocessing
    # Note: InceptionV3 usually requires 299x299. If you used 224x224, change it here.
    img = image.resize((224, 224)) 
    img_array = np.array(img) / 255.0  # Normalize if your model expects [0,1]
    img_array = np.expand_dims(img_array, axis=0)

    # Prediction
    with st.spinner('Analyzing...'):
        predictions = model.predict(img_array)
        class_idx = np.argmax(predictions)
        confidence = np.max(predictions)

    # Display Results
    details = WASTE_DETAILS[class_idx]
    
    st.success(f"**Prediction: {details['label']}** (Confidence: {confidence:.2%})")
    
    st.markdown(f"### 📋 Waste Category: {details['category']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("How to Recycle:")
        for method in details['methods']:
            st.write(f"- {method}")
            
    with col2:
        st.subheader("Environmental Impact:")
        st.info(details['impact'])

    st.warning("**Note:** Local recycling rules vary by city. Always check your local municipality's guidelines.")
    