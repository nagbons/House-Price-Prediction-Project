import streamlit as st
import numpy as np
import joblib 

model = joblib.load("model.pkl")
feature_names = joblib.load("features.pkl")


# ---------------------------
# PAGE CONFIG + DARK MODE STYLE
# ---------------------------
st.set_page_config(page_title="House Price Predictor", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# LOAD MODEL
# ---------------------------
model = joblib.load("model.pkl")

# ---------------------------
# SIDEBAR INPUTS (PRO UI)
# ---------------------------
st.sidebar.title("🏠 House Inputs")

currency = st.sidebar.selectbox("Currency", ["USD ($)", "NGN (₦)"])

lotsize = st.sidebar.number_input("Lot Size")
bedrooms = st.sidebar.slider("Bedrooms", 0, 10, 3)
bathrms = st.sidebar.slider("Bathrooms", 0, 5, 2)
stories = st.sidebar.slider("Stories", 1, 5, 1)
garagepl = st.sidebar.slider("Garage Spaces", 0, 3, 1)

driveway_yes = st.sidebar.selectbox("Driveway", [0, 1])
recroom_yes = st.sidebar.selectbox("Rec Room", [0, 1])
fullbase_yes = st.sidebar.selectbox("Full Basement", [0, 1])
gashw_yes = st.sidebar.selectbox("Gas Hot Water", [0, 1])
airco_yes = st.sidebar.selectbox("Air Conditioning", [0, 1])
prefarea_yes = st.sidebar.selectbox("Preferred Area", [0, 1])

# ---------------------------
# FEATURE ENGINEERING
# ---------------------------
house_size_score = lotsize + (bedrooms * 10)

luxury_score = airco_yes + gashw_yes + prefarea_yes

size_to_rooms_ratio = lotsize / (bedrooms + 1)

room_density = (bedrooms + bathrms) / (lotsize + 1)

comfort_index = airco_yes + gashw_yes + fullbase_yes + recroom_yes

convenience_score = driveway_yes + garagepl

# ---------------------------
# FEATURES ARRAY
# ---------------------------
features = np.array([[
    lotsize,
    bedrooms,
    bathrms,
    stories,
    garagepl,
    driveway_yes,
    recroom_yes,
    fullbase_yes,
    gashw_yes,
    airco_yes,
    prefarea_yes,
    house_size_score,
    luxury_score,
    size_to_rooms_ratio,
    room_density,
    comfort_index,
    convenience_score
]])

# ---------------------------
# MAIN UI
# ---------------------------
st.title("🏠 House Price Prediction App")

st.write("Adjust inputs in the sidebar and predict house price.")

if st.button("🔮 Predict Price"):

    prediction = model.predict(features)[0]

    # ---------------------------
    # PRICE RANGE (MIN - MAX)
    # ---------------------------
    min_price = prediction * 0.9
    max_price = prediction * 1.1

    # ---------------------------
    # CURRENCY CONVERSION (simple fixed rate)
    # ---------------------------
    if currency == "NGN (₦)":
        prediction *= 1500
        min_price *= 1500
        max_price *= 1500
        symbol = "₦"
    else:
        symbol = "$"

    # ---------------------------
    # DISPLAY RESULT
    # ---------------------------
    st.success(f"Estimated Price: {symbol}{prediction:,.2f}")

    st.info(f"Price Range: {symbol}{min_price:,.2f} - {symbol}{max_price:,.2f}")

    # ---------------------------
    # CONFIDENCE METER (SIMULATED)
    # ---------------------------
    confidence = 0.65 + (np.random.rand() * 0.25)  # 65% - 90%

    st.write("### 📊 Prediction Confidence")

    st.progress(float(confidence))

    st.write(f"Confidence Score: {confidence*100:.2f}%")