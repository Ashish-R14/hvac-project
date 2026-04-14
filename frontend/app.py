import requests
import streamlit as st
from hvac_engine import evaluate_placement
from hvac_engine import calculate_btu, recommend_ac, suggest_placement, estimate_cooling_time
from hvac_engine import find_best_placement
from visualization import draw_room

st.title("TAN INNOVATIONS LLP. PRESENTS ")
st.title("HVAC Smart Recommendation System Chatbot for residential houses.")
st.header("Enter Room Details-")

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
    
    url = "http://127.0.0.1:8000/calculate"
    data = {
    "length": length,
    "width": width,
    "height": height,
    "people": people,
    "windows": windows,
    "sunlight": sunlight,
    "room_type": room_type
    }
    response = requests.post(url, json=data)

    result = response.json()
    
    st.subheader("Results")
    st.write(f"Estimated Cooling Load: {result['btu']} BTU")
    st.write(f"Recommended AC: {result['recommended_ac']}")
    st.write(f"Estimated Cooling Time: {result['cooling_time']} minutes")
    st.subheader("🌡️ Cooling Visualization")
    col1, col2 = st.columns(2)
    with col1:
      st.write(f"### {placement_option}")
    fig1 = draw_room(length, width, placement_option)
    st.pyplot(fig1)
    
    with col2:
      st.write(f"### {placement_option_2}")
    fig2 = draw_room(length, width, placement_option_2)
    st.pyplot(fig2)
    
    score1, verdict1, feedback1 = evaluate_placement(length, width, placement_option)
    score2, verdict2, feedback2 = evaluate_placement(length, width, placement_option_2)

    st.markdown("## 🔍 Your Selected Comparison")

    if score1 > score2:
      st.success(f"{placement_option} is better ✅")
    elif score2 > score1:
      st.success(f"{placement_option_2} is better ✅")
    else:
      st.warning("Both placements perform similarly")

    st.markdown("## 🧠 System Recommended Best Option")
    st.caption("Based on evaluation of all possible placements system found ")
    best_placement, best_score, best_feedback = find_best_placement(length, width)
    st.success(f"Overall best: {best_placement} ✅")
   
    if result['best_placement'] not in [placement_option, placement_option_2]:
     st.warning(
        f"Better option available: {result['best_placement']} was not in your selected comparison"
    )
    
       
    st.write(f"Score: {best_score}/3")

    st.write("Why this works:")
    for f in best_feedback:
     st.write(f"- {f}")
     
   
    


   