
# ♻️ PurePath AI: Africa Edition

### *Bridging the Gap Between Waste Detection and Regional Infrastructure*

**PurePath AI** is an advanced Waste Classification system designed specifically for the African continent. It uses Computer Vision to identify waste types and immediately connects users with local recycling partners and buyers in **Nigeria, Kenya, South Africa, Uganda, Cameroon, and Rwanda**.

---

## 🌟 Key Features

* **Multi-Stream Detection**: Analyze both static images and live video streams using a MobileNetV2-based Deep Learning model.
* **Regional Localization**: Automatically suggests recycling companies and local buyer contacts based on the user's selected country.
* **Actionable Insights**: Provides "Recycling Pathways" and explains the specific environmental impact for each material detected.
* **Seamless UX**: Features a specialized "Click-to-Copy" contact system for local collectors and an eco-friendly African-themed interface.

---

## 🧠 Technical Architecture

### **Deep Learning Model**

The "brain" of PurePath AI is built on **MobileNetV2** (via Transfer Learning), optimized for deployment in web and mobile environments.

* **Accuracy**: ~90% validation accuracy on 12 distinct waste categories.
* **Frameworks**: TensorFlow, Keras, and OpenCV for real-time frame analysis.
* **Preprocessing**: Normalization and 224x224 resizing for high-speed inference.

### **The Stack**

* **Frontend**: Streamlit (Python-based Web Framework)
* **Computer Vision**: OpenCV (Video frame sampling & RGB conversion)
* **Inference Engine**: TensorFlow 2.x
* **Deployment**: Support for `.h5` model integration and `tempfile` video stream handling.

---

## 📁 Project Structure

```text
├── app.py              # Main Streamlit Application
├── requirements.txt    # Dependencies (TensorFlow, Streamlit, OpenCV, etc.)
├── garbage_model.h5    # Pre-trained MobileNetV2 Weights
└── README.md           # Project Documentation

```

---

## 🚀 Getting Started

### **1. Prerequisites**

Ensure you have Python 3.9+ installed. You will also need the pre-trained model file (`garbage_classification_model_inception.h5`) in the root directory.

### **2. Installation**

```bash
git clone https://github.com/your-username/purepath-ai.git
cd purepath-ai
pip install -r requirements.txt

```

### **3. Running the App**

```bash
streamlit run app.py

```

---

## 🌍 Environmental Impact & Vision

Waste management in many African urban centers remains a manual challenge. **PurePath AI** aims to digitize this process. By identifying high-value recyclables (like **White Glass**, **PET Plastic**, and **Scrap Metal**) and providing the direct phone numbers of local buyers, we empower users to turn waste into a resource while protecting the local ecosystem.

---

## 🧾 Keywords

**Computer Vision • Deep Learning • Environmental AI • MobileNetV2 • Circular Economy • Waste Management Africa • TensorFlow**
