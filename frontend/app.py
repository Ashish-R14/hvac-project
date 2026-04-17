import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import hashlib

# ---------------- CONFIG ----------------
st.set_page_config(page_title="HVAC Smart System", layout="wide")

API_URL = "https://hvac-project.onrender.com/calculate"

# ---------------- UTILS ----------------

def generate_key(data):
    return hashlib.md5(str(data).encode()).hexdigest()

def quick_estimate(length, width, people):
    area = length * width
    return round(area * 20 + people * 500, 2)

def call_api(data):
    for _ in range(3):  # retry 3 times
        try:
            response = requests.post(API_URL, json=data, timeout=10)

            if response.status_code == 200:
                return response.json()

            if response.status_code == 429:
                time.sleep(4)

        except:
            time.sleep(4)

    return None

# ---------------- CACHE INIT ----------------
if "cache" not in st.session_state:
    st.session_state.cache = {}

if "last_click" not in st.session_state:
    st.session_state.last_click = 0

# ---------------- HEADER ----------------
st.title("🏢 TAN INNOVATIONS LLP.")
st.subheader("HVAC Smart Recommendation System")

st.info("💡 First request may take ~30 sec (server wake-up). Next runs will be instant ⚡")

st.markdown("---")

# ---------------- INPUT ----------------
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
        ["Top Wall", "Bottom Wall", "Left Wall", "Right Wall"]
    )

# ---------------- CALCULATE ----------------
if st.button("🚀 Calculate"):

    now = time.time()

    if now - st.session_state.last_click < 5:
        st.warning("⚠️ Please wait before trying again...")
        st.stop()

    st.session_state.last_click = now

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

    # ---------------- INSTANT PREVIEW ----------------
    st.markdown("### ⚡ Instant Estimate (Preview)")
    quick_btu = quick_estimate(length, width, people)
    st.metric("Estimated Cooling Load", f"{quick_btu} BTU")

    # ---------------- CACHE CHECK ----------------
    cache_key = generate_key(data)

    if cache_key in st.session_state.cache:
        result = st.session_state.cache[cache_key]
        st.success("⚡ Loaded instantly from cache")

    else:
        # ---------------- LOADING EXPERIENCE ----------------
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)

        # ---------------- API CALL ----------------
        result = call_api(data)

        if result is None:
            st.error("🚫 Server busy. Try again in few seconds.")
            st.stop()

        st.session_state.cache[cache_key] = result

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

    # ---------------- GRAPH ----------------
    st.markdown("---")
    st.subheader("📊 Placement Comparison Graph")

    names = [p1["name"], p2["name"]]
    scores = [p1["score"], p2["score"]]

    if scores[0] > scores[1]:
        colors = ["green", "red"]
        winner = p1["name"]
    elif scores[1] > scores[0]:
        colors = ["red", "green"]
        winner = p2["name"]
    else:
        colors = ["gray", "gray"]
        winner = "Both are equal"

    df = pd.DataFrame({"Placement": names, "Score": scores})

    fig, ax = plt.subplots()
    ax.barh(df["Placement"], df["Score"], color=colors)

    for i, v in enumerate(scores):
        ax.text(v + 0.05, i, str(v), va='center', fontweight='bold')

    ax.set_xlim(0, 3)
    ax.set_xlabel("Efficiency Score")
    ax.set_title("AC Placement Performance")

    st.pyplot(fig)

    # ---------------- INSIGHT ----------------
    st.markdown("### 🧠 Insight")

    if winner != "Both are equal":
        diff = abs(scores[0] - scores[1])
        st.success(f"✅ {winner} is better by {diff} point(s)")
    else:
        st.info("⚖️ Both placements are equal")

    st.metric("🏆 Best Placement", winner)

    # ---------------- BEST ----------------
    st.markdown("---")
    st.header("🔥 Best Placement Recommendation")

    st.success(f"Optimal Placement: {result['best_placement']}")
    st.write(f"Score: {result['score']}/3")

    for f in result["feedback"]:
        st.write(f"- {f}")