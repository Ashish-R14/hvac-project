import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="HVAC Smart System",
    layout="wide"
)

API_URL = "https://hvac-project.onrender.com/calculate"

# ---------------- HEADER ----------------
st.title("🏢 TAN INNOVATIONS LLP.")
st.subheader("HVAC Smart Recommendation System")

st.markdown("---")

# ---------------- INPUT SECTION ----------------
st.header("📥 Enter Room Details")

col1, col2, col3 = st.columns(3)

with col1:
    length = st.number_input("Room Length (ft)", min_value=1.0)
    width = st.number_input("Room Width (ft)", min_value=1.0)

with col2:
    height = st.number_input("Room Height (ft)", min_value=1.0)
    people = st.number_input("Number of People", min_value=0)

with col3:
    windows = st.number_input("Number of Windows", min_value=0)
    sunlight = st.selectbox("Sunlight Exposure", ["Low", "Medium", "High"])

room_type = st.selectbox("Room Type", ["Bedroom", "Living Room", "Office"])

st.markdown("---")

# ---------------- PLACEMENT ----------------
st.header("📍 Placement Selection")

col4, col5 = st.columns(2)

with col4:
    placement_option = st.selectbox(
        "Primary Placement",
        ["Top Wall", "Bottom Wall", "Left Wall", "Right Wall"]
    )

with col5:
    placement_option_2 = st.selectbox(
        "Compare With",
        ["Top Wall", "Bottom Wall", "Left Wall", "Right Wall"],
        key="placement2"
    )

# ---------------- CALCULATE ----------------
if st.button("🚀 Calculate"):

    data = {
        "length": length,
        "width": width,
        "height": height,
        "people": people,
        "windows": windows,
        "sunlight": sunlight,
        "room_type": room_type,
        "placement_1": placement_option,
        "placement_2": placement_option_2
    }

    try:
        response = requests.post(API_URL, json=data, timeout=60)

        if response.status_code != 200:
            st.error(f"❌ Backend Error: {response.text}")
            st.stop()

        result = response.json()

        # ---------------- RESULTS ----------------
        st.markdown("---")
        st.header("📊 Results")

        colA, colB, colC = st.columns(3)

        with colA:
            st.metric("Cooling Load", f"{round(result['btu'],2)} BTU")

        with colB:
            st.metric("Recommended AC", result["recommended_ac"])

        with colC:
            st.metric("Cooling Time", f"{result['cooling_time']} min")

        # ---------------- COMPARISON ----------------
        st.markdown("---")
        st.header("🔍 Placement Comparison")

        p1 = result["comparison"]["placement_1"]
        p2 = result["comparison"]["placement_2"]

        col6, col7 = st.columns(2)

        with col6:
            st.subheader(f"📌 {p1['name']}")
            st.write(f"Score: {p1['score']}")
            st.write(p1["verdict"])
            for f in p1["feedback"]:
                st.write(f"- {f}")

        with col7:
            st.subheader(f"📌 {p2['name']}")
            st.write(f"Score: {p2['score']}")
            st.write(p2["verdict"])
            for f in p2["feedback"]:
                st.write(f"- {f}")
        
        st.markdown("---")
        st.subheader("📊 Placement Comparison Graph")
       
        try:
           p1 = result["comparison"]["placement_1"]
           p2 = result["comparison"]["placement_2"]

            # Data for graph
           names = [p1["name"], p2["name"]]
           scores = [p1["score"], p2["score"]]

           df = pd.DataFrame({
           "Placement": names,
           "Score": scores
           })

    # Plot
           fig, ax = plt.subplots()
           ax.bar(df["Placement"], df["Score"])
           ax.set_xlabel("Placement")
           ax.set_ylabel("Score")
           ax.set_title("AC Placement Comparison")

           st.pyplot(fig)

        except Exception as e:
          st.warning("Graph could not be generated")       

        # ---------------- BEST PLACEMENT ----------------
        st.markdown("---")
        st.header("🔥 Best Placement Recommendation")

        st.success(f"Optimal Placement: {result['best_placement']}")

        st.write(f"Score: {result['score']}/3")

        st.write("Why this works:")
        for f in result["feedback"]:
            st.write(f"- {f}")

    except requests.exceptions.Timeout:
        st.error("⏱️ Server timeout. Try again.")

    except Exception as e:
        st.error(f"⚠️ Error connecting to API: {e}")