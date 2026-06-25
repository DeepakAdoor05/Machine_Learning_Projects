import streamlit as st
import pickle
import pandas as pd

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Food Delivery Time Prediction",
    page_icon="🛵",
    layout="centered"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 40px;
    font-weight: 800;
    color: #ff4b4b;
    margin-top: 10px;
}
.sub-title {
    text-align: center;
    font-size: 18px;
    color: #555;
    margin-bottom: 30px;
}
.card {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.1);
    margin-bottom: 25px;
}
.predict-btn button {
    background-color: #ff4b4b;
    color: white;
    font-size: 18px;
    padding: 10px 24px;
    border-radius: 10px;
    border: none;
}

.predict-btn button:hover {
    background-color: #ff2e2e;
}
</style>
""", unsafe_allow_html=True)

# ---------- TOP IMAGE ----------
st.image(
    "https://media.licdn.com/dms/image/v2/D4D12AQG3kTNRfEEC4A/article-cover_image-shrink_600_2000/article-cover_image-shrink_600_2000/0/1696855112773?e=2147483647&v=beta&t=CsRDVN5hg8y7Z6_KIlRszFmg34Zq3KpWL-AKgZhXTe4",
    width="stretch"
)

# ---------- TITLE ----------
st.markdown('<div class="main-title">FOOD DELIVERY TIME PREDICTION SYSTEM</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Enter the details to predict delivery time:</div>', unsafe_allow_html=True)

# ---------- MAIN APP -----------
def main():
    model = pickle.load(open('model_rf.sav', 'rb'))
    label_encoders = pickle.load(open('label_encoders.sav', 'rb'))

    cat_cols = [
        'Weatherconditions',
        'Road_traffic_density',
        'Type_of_vehicle',
        'Festival',
        'City'
    ]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        weather = st.selectbox("Weather Conditions",label_encoders['Weatherconditions'].classes_,index=None,placeholder="Select option")
        # weather = st.selectbox("Weather Conditions", label_encoders['Weatherconditions'].classes_)
        traffic = st.selectbox("Road Traffic", label_encoders['Road_traffic_density'].classes_,index=None,placeholder="Select option")
        vehicle_type = st.selectbox("Vehicle Type", label_encoders['Type_of_vehicle'].classes_,index=None,placeholder="Select option")
        festival = st.selectbox("Festival", label_encoders['Festival'].classes_,index=None,placeholder="Select option")

    with col2:
        city = st.selectbox("City", label_encoders['City'].classes_,index=None,placeholder="Select option")
        age = st.number_input("Delivery Person Age", min_value=18, max_value=60, value=None, placeholder="Enter value")
        rating = st.number_input("Delivery Person Rating", min_value=1.0, max_value=5.0, value=None, placeholder="Enter value")
        distance = st.number_input("Distance (km)", value=None, placeholder="Enter value")

    col3, col4, col5 = st.columns(3)
    with col3:
        time = st.number_input("Order Hour (0–23)", min_value=0, max_value=23, value=None, placeholder="Enter value")
    with col4:
        no_deliveries = st.number_input("No. of Deliveries", min_value=0, value=None, placeholder="Enter value")
    with col5:
        vehicle_condition = st.number_input("Vehicle Condition (1–5)", min_value=1, max_value=5, value=None, placeholder="Enter value")

    pred = st.button("PREDICT")


    if pred:
        if None in [
            weather, traffic, vehicle_type, festival, city,
            age, rating, distance, time,
            no_deliveries, vehicle_condition
        ]:
            st.warning("Please fill all fields before prediction.")
            st.stop()
        df1 = pd.DataFrame({
            'Delivery_person_Age': [age],
            'Delivery_person_Ratings': [rating],
            'Distance_km': [distance],
            'Weatherconditions': [weather],
            'Road_traffic_density': [traffic],
            'Vehicle_condition': [vehicle_condition],
            'Type_of_vehicle': [vehicle_type],
            'multiple_deliveries': [no_deliveries],
            'Festival': [festival],
            'City': [city],
            'Order_hour': [time]
        })

        for col in cat_cols:
            df1[col] = label_encoders[col].transform(df1[col])

        prediction = model.predict(df1)[0]

        st.success(f"⏱ Your Order will be delivered in: {round(prediction)} minutes")

main()
