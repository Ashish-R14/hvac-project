import requests
import streamlit as st

st.title("TAN INNOVATIONS LLP. PRESENTS")
st.title("HVAC Smart Recommendation System Chatbot for residential houses.")
st.header("Enter Room Details-")

# Inputs
length = st.number_input("Room Length (ft)", min_value=1.0)
width = st.number_input("Room Width (ft)", min_value=1.0)
height = st.number_input("Room Height (ft)", min_value=1.0)

people = st.number_input("Number of People", min_value=0)

windows = st.number_input("Number of Windows", min_value=0)

sunlight = st.selectbox("Sunlight Exposure", ["Low", "Medium", "High"])

room_type = st.selectbox("Room Type", ["Bedroom", "Living Room", "Office"])

placement_option = st.selectbox(
    "Choose AC Placement Wall",
    ["Top Wall", "Bottom Wall", "Left Wall", "Right Wall"]
)

placement_option_2 = st.selectbox(
    "Compare with another placement",
    ["Top Wall", "Bottom Wall", "Left Wall", "Right Wall"],
    key="placement2"
)

if st.button("Calculate"):

    url = "https://hvac-project.onrender.com/calculate"

    data = {
        "length": length,
        "width": width,
        "height": height,
        "people": people,
        "windows": windows,
        "sunlight": sunlight,
        "room_type": room_type
    }

    try:
        response = requests.post(url, json=data)

        if response.status_code != 200:
            st.error("Backend error. Check API.")
        else:
            result = response.json()

            st.subheader("Results")
            st.write(f"Estimated Cooling Load: {result['btu']} BTU")
            st.write(f"Recommended AC: {result['recommended_ac']}")
            st.write(f"Estimated Cooling Time: {result['cooling_time']} minutes")

            st.markdown("## 🔍 Comparison Result")
            st.success(result["comparison_result"])

            st.markdown("## 🔥 Best Placement Recommendation")
            st.success(f"Optimal Placement: {result['best_placement']}")

            st.write(f"Score: {result['score']}/3")

            st.write("Why this works:")
            for f in result["feedback"]:
                st.write(f"- {f}")

    except Exception as e:
        st.error(f"Error connecting to API: {e}")
   
    


   