import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import cv2
import tempfile

# 1. Page Configuration
st.set_page_config(page_title="PurePath AI - Africa Edition", layout="wide")

# Custom CSS for the "Eco-Green" African theme
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
    }
    .waste-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border-left: 10px solid #388e3c;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        color: #1b5e20;
    }
    .card-title { font-size: 22px; font-weight: 800; color: #2e7d32; }
    .section-header { font-weight: 700; color: #388e3c; margin-top: 10px; display: block; }
    </style>
    """, unsafe_allow_html=True)

# 2. Africa-Specific Waste Data
WASTE_DETAILS = {
    0: {
        "label": "Battery",
        "category": "Hazardous",
        "methods": ["Take to e-waste center.", "Do not dispose in regular trash."],
        "impact": "Prevents heavy metal soil pollution.",
        "companies": {
            "Nigeria": ["Hinckley Recycling", "E-terra Technologies"],
            "Uganda": ["WEEE Centre Uganda", "NEMA"],
            "Cameroon": ["Solidarité Technologique", "WorldLoop"],
            "South_Africa": ["Desco Electronic Recyclers", "Reclite SA"],
            "Kenya": ["WEEE Centre", "Alpha Recycling"],
            "Rwanda": ["Enviroserve Rwanda"],
            "Global": ["Call2Recycle"]
        },
        "contacts": {
            "Kenya": ["Kofi (+254 712 483 591)", "Amani (+254 768 952 410)", "Zuri (+254 701 935 842)"], 
            "Rwanda": ["Gabo (+250 781 693 820)", "Inaya (+250 784 129 576)", "Claude (+250 783 905 174)"],
            "South_Africa": ["Jaco (+27 83 291 7465)", "Lindiwe (+27 76 318 5409)", "Sipho (+27 71 482 6935)"],
            "Cameroon": ["Moussa (+237 671 482 903)", "Evelyne (+237 655 903 174)", "Bello (+237 699 284 561)"],
            "Uganda": ["Paddy (+256 704 839 215)", "Scovia (+256 772 516 904)", "Juma (+256 781 290 673)"],
            "Nigeria": ["Tunde (+234 803 482 7193)", "Blessing (+234 816 905 2741)", "Abubakar (+234 907 384 5628)"]
        }
    },
    1: {
        "label": "Biological",
        "category": "Organic",
        "methods": ["Home composting.", "Use for biogas generation."],
        "impact": "Methane reduction and soil enrichment.",
        "companies": {
            "Nigeria": ["LAWMA Composting", "Wecyclers Organic"],
            "Uganda": ["Marula Proteen", "KCCA"],
            "Cameroon": ["Bocom Recycling", "Municipal Centers"],
            "South_Africa": ["Reliance Compost", "Zube’s Composting"],
            "Kenya": ["TakaTaka Solutions", "Sanergy"],
            "Rwanda": ["GreenCare Rwanda", "Copedu Ltd"],
            "Global": ["Waste Management (WM)"]
        },
        "contacts": {
            "Kenya": ["Jabari (+254 712 111 222)", "Malaika (+254 768 333 444)", "Kwame (+254 701 555 666)"],
            "Rwanda": ["Ange (+250 781 000 111)", "Pacifique (+250 784 222 333)", "Divine (+250 783 444 555)"],
            "South_Africa": ["Andile (+27 83 666 7777)", "Lebo (+27 76 888 9999)", "Kobus (+27 71 000 1111)"],
            "Cameroon": ["Oumar (+237 671 222 333)", "Sali (+237 655 444 555)", "Fany (+237 699 666 777)"],
            "Uganda": ["Okello (+256 704 888 999)", "Nantongo (+256 772 000 111)", "Kizza (+256 781 222 333)"],
            "Nigeria": ["Femi (+234 803 444 5555)", "Nkechi (+234 816 666 7777)", "Umar (+234 907 888 9999)"]
        }
    },
    2: {
        "label": "Brown-glass",
        "category": "Glass",
        "methods": ["Rinse and remove caps.", "Color-sort for recycling."],
        "impact": "40% energy savings in glass production.",
        "companies": {
            "Nigeria": ["GZ Industries", "Frigoglass"],
            "Uganda": ["Madhavani Group", "Uganda Breweries"],
            "Cameroon": ["SABC Recycling", "Namé Recycling"],
            "South_Africa": ["Consol Glass", "Glass Recycling Co"],
            "Kenya": ["Central Glass Industries", "Kapa Oil"],
            "Rwanda": ["Skol Rwanda", "Nyarugenge Hub"],
            "Global": ["Strategic Materials"]
        },
        "contacts": {
            "Kenya": ["Baraka (+254 712 222 333)", "Zahra (+254 768 444 555)", "Kibet (+254 701 666 777)"],
            "Rwanda": ["Thierry (+250 781 123 456)", "Solange (+250 784 654 321)", "Blaise (+250 783 987 654)"],
            "South_Africa": ["Johan (+27 83 111 2222)", "Thandi (+27 76 333 4444)", "Riaan (+27 71 555 6666)"],
            "Cameroon": ["Abel (+237 671 111 222)", "Celine (+237 655 333 444)", "Henri (+237 699 555 666)"],
            "Uganda": ["Ssemwanga (+256 704 111 222)", "Atwine (+256 772 333 444)", "Lule (+256 781 555 666)"],
            "Nigeria": ["Segun (+234 803 111 2222)", "Ada (+234 816 333 4444)", "Danjuma (+234 907 555 6666)"]
        }
    },
    3: {
        "label": "Cardboard",
        "category": "Paper",
        "methods": ["Flatten boxes.", "Keep dry & oil-free."],
        "impact": "Saves 17 trees per ton.",
        "companies": {
            "Nigeria": ["Chanja Datti", "Wecyclers"],
            "Uganda": ["Riley Packaging", "Global Paper"],
            "Cameroon": ["Focus Packaging", "Namé Recycling"],
            "South_Africa": ["Mpact Recycling", "Sappi Re-Cycle"],
            "Kenya": ["Kamongo Waste Paper", "Chandaria Industries"],
            "Rwanda": ["Eco-Plastic Rwanda", "Ecogroup Rwanda"],
            "Global": ["WestRock"]
        },
        "contacts": {
            "Kenya": ["Maina (+254 712 777 888)", "Wanjala (+254 768 999 000)", "Moraa (+254 701 111 222)"],
            "Rwanda": ["Samson (+250 781 222 333)", "Liliane (+250 784 444 555)", "Yvan (+250 783 666 777)"],
            "South_Africa": ["Gert (+27 83 777 8888)", "Nandi (+27 76 999 0000)", "Bongani (+27 71 111 2222)"],
            "Cameroon": ["Elias (+237 671 777 888)", "Grace (+237 655 999 000)", "Guy (+237 699 111 222)"],
            "Uganda": ["Mukiibi (+256 704 777 888)", "Kyomu (+256 772 999 000)", "Otai (+256 781 111 222)"],
            "Nigeria": ["Ife (+234 803 777 8888)", "Kelechi (+234 816 999 0000)", "Sani (+234 907 111 2222)"]
        }
    },
    4: {
        "label": "Clothes",
        "category": "Textiles",
        "methods": ["Donate wearable items.", "Upcycle into cleaning rags."],
        "impact": "Reduces landfill mass and water waste.",
        "companies": {
            "Nigeria": ["Lagos Fashion Relief", "African Clean Up"],
            "Uganda": ["TexFad", "Secondary Hubs"],
            "Cameroon": ["Local Charity Networks", "Red Cross"],
            "South_Africa": ["The Clothing Bank", "H&M Take-back"],
            "Kenya": ["Africa Collect Textiles", "Gikomba Sorting"],
            "Rwanda": ["Sustainable Fashion", "Rwanda Red Cross"],
            "Global": ["I:CO", "ThredUp"]
        },
        "contacts": {
            "Kenya": ["Nuru (+254 712 456 789)", "Kamali (+254 768 123 456)", "Tito (+254 701 789 123)"],
            "Rwanda": ["Daphine (+250 781 555 123)", "Placide (+250 784 555 456)", "Gisele (+250 783 555 789)"],
            "South_Africa": ["Siphiwe (+27 83 456 7890)", "Melanie (+27 76 123 4567)", "Tumi (+27 71 789 0123)"],
            "Cameroon": ["Blaise (+237 671 456 789)", "Marthe (+237 655 123 456)", "Simon (+237 699 789 123)"],
            "Uganda": ["Waiswa (+256 704 456 789)", "Naka (+256 772 123 456)", "Bagonza (+256 781 789 123)"],
            "Nigeria": ["Bunmi (+234 803 456 7890)", "Emeka (+234 816 123 4567)", "Aisha (+234 907 789 0123)"]
        }
    },
    5: {
        "label": "Green-glass",
        "category": "Glass",
        "methods": ["Rinse and recycle.", "Keep separate from white glass."],
        "impact": "Infinite recyclability without quality loss.",
        "companies": {
            "Nigeria": ["Frigoglass", "LAWMA"],
            "Uganda": ["Uganda Breweries", "Nile Breweries"],
            "Cameroon": ["Namé Recycling", "SABC"],
            "South_Africa": ["Glass Recycling Co", "Consol Glass"],
            "Kenya": ["Central Glass Industries", "Friends of Environment"],
            "Rwanda": ["Bralirwa Recycling", "Skol Rwanda"],
            "Global": ["Suez"]
        },
        "contacts": {
            "Kenya": ["Chebet (+254 712 101 101)", "Odhiambo (+254 768 202 202)", "Makena (+254 701 303 303)"],
            "Rwanda": ["Kelia (+250 781 111 222)", "Arsene (+250 784 222 333)", "Janvi (+250 783 333 444)"],
            "South_Africa": ["Karel (+27 83 101 1011)", "Zanele (+27 76 202 2022)", "Willie (+27 71 303 3033)"],
            "Cameroon": ["Desire (+237 671 101 101)", "Pascaline (+237 655 202 202)", "Fabien (+237 699 303 303)"],
            "Uganda": ["Kibirige (+256 704 101 101)", "Babirye (+256 772 202 202)", "Mukasa (+256 781 303 303)"],
            "Nigeria": ["Tope (+234 803 101 1011)", "Uche (+234 816 202 2022)", "Musa (+234 907 303 3033)"]
        }
    },
    6: {
        "label": "Metal",
        "category": "Metal",
        "methods": ["Rinse aluminum cans.", "Collect scrap metal."],
        "impact": "Saves 95% energy compared to raw mining.",
        "companies": {
            "Nigeria": ["Nigeria Foundries", "Shree Metals"],
            "Uganda": ["Steel Rolling Mills", "Roofings Group"],
            "Cameroon": ["Les Aciéries", "Alucam"],
            "South_Africa": ["Collect-a-Can", "Reclam Group"],
            "Kenya": ["Devki Steel", "Mabati Rolling Mills"],
            "Rwanda": ["SteelRwa", "Master Steel Rwanda"],
            "Global": ["Schnitzer Steel"]
        },
        "contacts": {
            "Kenya": ["Mutiso (+254 712 555 999)", "Kemboi (+254 768 444 888)", "Adhiambo (+254 701 333 777)"],
            "Rwanda": ["Enoch (+250 781 999 000)", "Nadine (+250 784 888 111)", "Patrick (+250 783 777 222)"],
            "South_Africa": ["Hendrik (+27 83 555 9999)", "Zodwa (+27 76 444 8888)", "Barend (+27 71 333 7777)"],
            "Cameroon": ["Lucas (+237 671 555 999)", "Clarisse (+237 655 444 888)", "Raoul (+237 699 333 777)"],
            "Uganda": ["Nsubuga (+256 704 555 999)", "Nandutu (+256 772 444 888)", "Kato (+256 781 333 777)"],
            "Nigeria": ["Jimi (+234 803 555 9999)", "Nneka (+234 816 444 8888)", "Bala (+234 907 333 7777)"]
        }
    },
    7: {
        "label": "Paper",
        "category": "Paper",
        "methods": ["Recycle newspapers.", "Keep dry and separate."],
        "impact": "Prevents deforestation and water pollution.",
        "companies": {
            "Nigeria": ["Bel Papyrus", "Chanja Datti"],
            "Uganda": ["Global Paper", "Riley Packaging"],
            "Cameroon": ["SITRACEL", "Namé Recycling"],
            "South_Africa": ["Mpact Recycling", "Sappi"],
            "Kenya": ["Chandaria Industries", "Kamongo Waste Paper"],
            "Rwanda": ["Eco-Group Rwanda", "Nyarugenge Hub"],
            "Global": ["DS Smith"]
        },
        "contacts": {
            "Kenya": ["Omondi (+254 712 121 212)", "Wairimu (+254 768 232 323)", "Korir (+254 701 343 434)"],
            "Rwanda": ["Jean (+250 781 121 212)", "Yvette (+250 784 232 323)", "Leon (+250 783 343 434)"],
            "South_Africa": ["Stephan (+27 83 121 2121)", "Phumzile (+27 76 232 3232)", "Danie (+27 71 343 4343)"],
            "Cameroon": ["Moise (+237 671 121 212)", "Sandrine (+237 655 232 323)", "Julien (+237 699 343 434)"],
            "Uganda": ["Kimbugwe (+256 704 121 212)", "Akiiki (+256 772 232 323)", "Owori (+256 781 343 434)"],
            "Nigeria": ["Kayode (+234 803 121 2121)", "Amarachi (+234 816 232 3232)", "Garba (+234 907 343 4343)"]
        }
    },
    8: {
        "label": "Plastic",
        "category": "Plastic",
        "methods": ["Check resin codes.", "Rinse food residue."],
        "impact": "Prevents microplastics in the ecosystem.",
        "companies": {
            "Nigeria": ["Wecyclers", "Chanja Datti", "RecyclePoints"],
            "Uganda": ["Takataka Plastics", "Ecoplastile"],
            "Cameroon": ["Namé Recycling", "Red-Plast"],
            "South_Africa": ["Extrupet", "Petco", "Mpact"],
            "Kenya": ["Mr. Green Africa", "TakaTaka Solutions"],
            "Rwanda": ["EcoPlastic Rwanda", "Copedu"],
            "Global": ["Veolia"]
        },
        "contacts": {
            "Kenya": ["Kamau (+254 712 999 111)", "Chepkorir (+254 768 999 222)", "Mwakio (+254 701 999 333)"],
            "Rwanda": ["Alphonse (+250 781 888 111)", "Beata (+250 784 888 222)", "Donat (+250 783 888 333)"],
            "South_Africa": ["Lucky (+27 83 888 1111)", "Busi (+27 76 888 2222)", "Wayne (+27 71 888 3333)"],
            "Cameroon": ["Basile (+237 671 888 111)", "Solange (+237 655 888 222)", "Eric (+237 699 888 333)"],
            "Uganda": ["Ochan (+256 704 888 111)", "Namubiru (+256 772 888 222)", "Kintu (+256 781 888 333)"],
            "Nigeria": ["Obinna (+234 803 888 1111)", "Tayo (+234 816 888 2222)", "Zaid (+234 907 888 3333)"]
        }
    },
    9: {
        "label": "Shoes",
        "category": "Textiles",
        "methods": ["Donate to local charities.", "Professional repair."],
        "impact": "Complex material recovery for circularity.",
        "companies": {
            "Nigeria": ["Shoe Shop Repair", "Lagos Hubs"],
            "Uganda": ["TexFad", "Local Cobblers"],
            "Cameroon": ["Marche Central Hub", "NGO Initiatives"],
            "South_Africa": ["Sneaker Lab", "Clothing Bank"],
            "Kenya": ["Africa Collect Textiles", "Umoja Rubber"],
            "Rwanda": ["Rwanda Clothing", "Charity Hubs"],
            "Global": ["Nike Grind"]
        },
        "contacts": {
            "Kenya": ["Babu (+254 712 141 141)", "Zola (+254 768 252 252)", "Kimani (+254 701 363 363)"],
            "Rwanda": ["Hassan (+250 781 141 141)", "Zita (+250 784 252 252)", "Yussuf (+250 783 363 363)"],
            "South_Africa": ["Theuns (+27 83 141 1411)", "Lerato (+27 76 252 2522)", "Muzi (+27 71 363 3633)"],
            "Cameroon": ["Clement (+237 671 141 141)", "Lydie (+237 655 252 252)", "Valerie (+237 699 363 363)"],
            "Uganda": ["Wavamunno (+256 704 141 141)", "Nampijja (+256 772 252 252)", "Aisha (+256 781 363 363)"],
            "Nigeria": ["Chima (+234 803 141 1411)", "Ronke (+234 816 252 2522)", "Suleiman (+234 907 363 3633)"]
        }
    },
    10: {
        "label": "Trash",
        "category": "General",
        "methods": ["Proper landfill disposal.", "Identify recyclables first."],
        "impact": "Managed pollution growth.",
        "companies": {
            "Nigeria": ["LAWMA", "Visionscape"],
            "Uganda": ["KCCA", "Nabugabo Updeal"],
            "Cameroon": ["HYSACAM"],
            "South_Africa": ["Pikitup", "Waste Group"],
            "Kenya": ["Nairobi County Services", "TakaTaka Solutions"],
            "Rwanda": ["Copedu", "Agruni Ltd"],
            "Global": ["Republic Services"]
        },
        "contacts": {
            "Kenya": ["Juma (+254 712 000 001)", "Akiini (+254 768 000 002)", "Sewe (+254 701 000 003)"],
            "Rwanda": ["Fabien (+250 781 000 001)", "Umu (+250 784 000 002)", "Didier (+250 783 000 003)"],
            "South_Africa": ["Sias (+27 83 000 0001)", "Nomsa (+27 76 000 0002)", "Pieter (+27 71 000 0003)"],
            "Cameroon": ["Titus (+237 671 000 001)", "Bernadette (+237 655 000 002)", "Achille (+237 699 000 003)"],
            "Uganda": ["Matovu (+256 704 000 001)", "Namara (+256 772 000 002)", "Okot (+256 781 000 003)"],
            "Nigeria": ["Emeka (+234 803 000 0001)", "Bisi (+234 816 000 0002)", "Abba (+234 907 000 0003)"]
        }
    },
    11: {
        "label": "White-glass",
        "category": "Glass",
        "methods": ["Rinse thoroughly.", "Remove all caps."],
        "impact": "High-value raw material for manufacturing.",
        "companies": {
            "Nigeria": ["Frigoglass", "Beta Glass"],
            "Uganda": ["Uganda Breweries", "Coca-Cola Africa"],
            "Cameroon": ["Namé Recycling", "SABC"],
            "South_Africa": ["Glass Recycling Co", "Consol Glass"],
            "Kenya": ["Central Glass Industries", "Kapa Oil"],
            "Rwanda": ["Bralirwa", "Skol Rwanda"],
            "Global": ["Ardagh Group"]
        },
        "contacts": {
            "Kenya": ["Gitonga (+254 712 808 808)", "Nyambura (+254 768 707 707)", "Wekesa (+254 701 606 606)"],
            "Rwanda": ["Gisele (+250 781 808 808)", "Bosco (+250 784 707 707)", "Yvonne (+250 783 606 606)"],
            "South_Africa": ["Fanie (+27 83 808 8088)", "Dudu (+27 76 707 7077)", "Kobus (+27 71 606 6066)"],
            "Cameroon": ["Gaston (+237 671 808 808)", "Brigitte (+237 655 707 707)", "Charles (+237 699 606 606)"],
            "Uganda": ["Kaggwa (+256 704 808 808)", "Nakato (+256 772 707 707)", "Mwesigwa (+256 781 606 606)"],
            "Nigeria": ["Kunle (+234 803 808 8088)", "Obi (+234 816 707 7077)", "Usman (+234 907 606 6066)"]
        }
    }
}

# 3. Model Loading and Logic
@st.cache_resource
def load_garbage_model():
    try:
        # Ensure your file is named exactly this and in the same folder
        return tf.keras.models.load_model('garbage_classification_model_inception.h5', compile=False)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_garbage_model()

def predict_multi(img_array, threshold=0.15):
    if model is None: return [], []
    predictions = model.predict(img_array, verbose=0)[0]
    return np.where(predictions > threshold)[0], predictions

def get_partners(waste_idx, country):
    data = WASTE_DETAILS.get(waste_idx, WASTE_DETAILS[10])
    country_map = data.get("companies", {})
    return country_map.get(country, country_map.get("Global", ["Local Recycling Center"]))

# --- APP LAYOUT ---
st.sidebar.title("🌍 Location Settings")
selected_country = st.sidebar.selectbox(
    "Choose Country", 
    ["Nigeria", "Uganda", "Cameroon", "South_Africa", "Kenya", "Rwanda"],
    index=0
)
country_display = selected_country.replace("_", " ")

st.markdown(f"<h1 style='text-align: center;color: #1b5e20;'>♻️ PurePath AI: {country_display}</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #2e7d32;'>Advanced Multi-Waste Detection & Corporate Partners</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Scan Waste (Image/Video)", type=["jpg", "png", "jpeg", "mp4"])

if uploaded_file:
    file_type = uploaded_file.type.split('/')[0]
    
    if file_type == 'image':
        col_view, col_info = st.columns([1.2, 1])
        image = Image.open(uploaded_file)
        
        with col_view:
            st.image(image, use_container_width=True, caption="Analyzing waste stream...")

        # Process Image for Model
        img_res = image.resize((224, 224))
        img_arr = np.array(img_res).astype('float32') / 255.0
        img_arr = np.expand_dims(img_arr, axis=0)
        indices, preds = predict_multi(img_arr)

        with col_info:
            if len(indices) > 0:
                st.markdown(f"<h3 style='color: #1b5e20;'>📍Recycling Methods and Partners in {country_display}</h3>", unsafe_allow_html=True)
                for idx in indices:
                    details = WASTE_DETAILS.get(idx, WASTE_DETAILS[10])
                    partners = get_partners(idx, selected_country)
                    # Fetching the specific manager names and numbers
                    contacts = details.get("contacts", {}).get(selected_country, ["Local Collector (+000 000 000)"])
                    
                    
                    st.markdown(f"""
                    <div class="waste-card">
                        <div class="card-title">{details['label']} <span style='font-size:14px; color:#666;'>({preds[idx]:.1%})</span></div>
                        <span class="section-header">♻️ Recycling Pathway:</span>
                        <p>{' • '.join(details['methods'])}</p>
                        <span class="section-header">🏢 Recommended Partners:</span>
                        <p><b>{', '.join(partners)}</b></p>
                        
                        
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                        <div class="waste-card">
                            <b>📞 Local Buyer's Contact Details:</b>
                                <div style='margin-bottom:10px;'></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Adding the specific contact names and click-to-copy numbers
                    for contact in contacts:
                        name_part = contact.split(" (")[0]
                        phone_part = contact.split("(")[-1].replace(")", "")
                        st.markdown(f"<span style='color: #1b5e20; font-weight: bold;'>👤 {name_part}</span>", unsafe_allow_html=True)
                        st.code(phone_part, language="text")


                    st.markdown(f"""
                        <div class="waste-card">
                            <b>Local Impact:</b> {details['impact']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No specific waste types detected above threshold.")

    elif file_type == 'video':
        tfile = tempfile.NamedTemporaryFile(delete=False) 
        tfile.write(uploaded_file.read())
        st.video(uploaded_file)
        
        if st.button("🚀 Run Africa-Wide Analysis"):
            cap = cv2.VideoCapture(tfile.name)
            fps = cap.get(cv2.CAP_PROP_FPS)
            all_found = set()
            
            with st.status(f"AI scanning frames for {country_display} infrastructure...", expanded=True):
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret: break
                    # Sample 1 frame per second to speed up analysis
                    if int(cap.get(cv2.CAP_PROP_POS_FRAMES)) % int(fps or 1) == 0:
                        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        img = Image.fromarray(img).resize((224, 224))
                        img_arr = np.array(img).astype('float32') / 255.0
                        img_arr = np.expand_dims(img_arr, axis=0)
                        idx_list, _ = predict_multi(img_arr)
                        for i in idx_list: all_found.add(i)
            
            # st.markdown(f"### 📋 Final Waste Audit: {country_display}")
            # if all_found:
            #     cols = st.columns(3)
            #     for i, idx in enumerate(all_found):
            #         with cols[i % 3]:
            #             d = WASTE_DETAILS.get(idx, WASTE_DETAILS[10])
            #             partners = get_partners(idx, selected_country)
            #             st.markdown(f"""
            #             <div class="waste-card" style='padding:15px;'>
            #                 <div style='font-size:20px; font-weight:700;'>{d['label']}</div>
            #                 <p style='font-size:13px;'><b>🏢Top Partner:</b><br>{partners[0]}</p>
            #             </div>
            #             """, unsafe_allow_html=True)
            # else:
            #     st.warning("No recyclable materials identified in video.")

            st.markdown(f"<h3 style='color: #1b5e20;'>📋 Final Waste Audit: {country_display}</h3>", unsafe_allow_html=True)
            if all_found:
                # We use columns to organize the cards neatly
                cols = st.columns(min(len(all_found), 2)) # Adjusted to 2 for better readability of detailed cards
                for i, idx in enumerate(all_found):
                    with cols[i % len(cols)]:
                        d = WASTE_DETAILS.get(idx, WASTE_DETAILS[10])
                        partners = get_partners(idx, selected_country)
                        # Fetching the specific manager names and numbers
                        contacts = d.get("contacts", {}).get(selected_country, ["Local Collector (+000 000 000)"])
                    
                        
                        # Full detail card for video results
                        st.markdown(f"""
                        <div class="waste-card">
                            <div class="card-title">{d['label']}</div>
                            <div style="font-size: 12px; color: #666; margin-top: -10px; margin-bottom: 10px;">
                                Category: {d.get('category', 'General')}
                            </div>
                            <div>
                            <p style='font-size:13px;'><b>♻️ Recycling Pathway:</b><br>{' • '.join(d['methods'])}</p>
                            <div>
                            <p style='font-size:13px;'><b>🏢 Recommended Partners ({country_display}):</b><br>{partners[0]}</p>
                            </div></div>
                            <div style='background:#f1f8e9; padding:12px; border-radius:10px; font-size:13px; margin-top:10px;'>
                                <b>🌍 Environmental Impact:</b><br>{d['impact']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown(f"""
                        <div class="waste-card">
                            <b>📞 Local Buyer's Contact Details:</b>
                                <div style='margin-bottom:10px;'></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Adding the specific contact names and click-to-copy numbers
                        for contact in contacts:
                            name_part = contact.split(" (")[0]
                            phone_part = contact.split("(")[-1].replace(")", "")
                            # Change the manager's name color to match the app heading
                            st.markdown(f"<span style='color: #1b5e20; font-weight: bold;'>👤 {name_part}</span>", unsafe_allow_html=True)
                            st.code(phone_part, language="text")


            else:
                st.warning("No recyclable materials identified in video.")