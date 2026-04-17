def calculate_btu(length, width, height, people, windows, sunlight, room_type):
    area = length * width

    base_btu = area * 20

    people_btu = people * 600
    window_btu = windows * 1000

    sunlight_factor = {
        "Low": 0.9,
        "Medium": 1.0,
        "High": 1.2
    }.get(sunlight, 1.0)

    room_factor = {
        "Bedroom": 0.9,
        "Living Room": 1.1,
        "Office": 1.2
    }.get(room_type, 1.0)

    total_btu = (base_btu + people_btu + window_btu) * sunlight_factor * room_factor

    return round(total_btu, 2)


# ================= AC RECOMMENDATION =================
def recommend_ac(btu):
    tonnage = btu / 12000

    if tonnage <= 1:
        return "1 Ton AC (Small Room)"
    elif tonnage <= 1.5:
        return "1.5 Ton AC (Medium Room)"
    elif tonnage <= 2:
        return "2 Ton AC (Large Room)"
    else:
        return "Multiple Units or Central AC"


# ================= COOLING TIME =================
def estimate_cooling_time(btu, area):
    cooling_capacity = btu / 60  # BTU per minute
    time = (area * 25) / cooling_capacity
    return round(time, 2)


# ================= PLACEMENT EVALUATION =================
def evaluate_placement(
    length,
    width,
    placement,
    door_position=None,
    furniture_density="Low"
):
    score = 0
    feedback = []

    longer_wall = "horizontal" if length >= width else "vertical"

    # Rule 1: Match airflow direction
    if longer_wall == "horizontal" and placement in ["Top Wall", "Bottom Wall"]:
        score += 2
        feedback.append("Good: Airflow spreads across longer dimension")
    elif longer_wall == "vertical" and placement in ["Left Wall", "Right Wall"]:
        score += 2
        feedback.append("Good: Matches room width for airflow")
    else:
        feedback.append("Warning: Airflow may not cover entire room")

    # Rule 2: Central distribution advantage
    if placement in ["Top Wall", "Bottom Wall"]:
        score += 1
        feedback.append("Better: Central air distribution")

    # Rule 3: Side placement note
    if placement in ["Left Wall", "Right Wall"]:
        feedback.append("Note: Side placement can create uneven cooling")

    # ---------------- REAL-WORLD FACTORS ----------------

    # Door penalty (air leakage)
    if door_position and placement == door_position:
        score -= 1
        feedback.append("Air loss due to door proximity")

    # Furniture impact
    if furniture_density == "High":
        score -= 0.5
        feedback.append("Obstruction reduces airflow efficiency")
    elif furniture_density == "Medium":
        score -= 0.2
        feedback.append("Moderate obstruction present")

    # Clamp score between 0–3
    score = max(0, min(score, 3))

    # ---------------- VERDICT ----------------
    if score >= 2.5:
        verdict = "✅ Optimal Placement"
    elif score >= 2:
        verdict = "👍 Good Placement"
    elif score >= 1:
        verdict = "⚠️ Moderate Placement"
    else:
        verdict = "❌ Poor Placement"

    return round(score, 2), verdict, feedback

# ================= BEST PLACEMENT =================
def find_best_placement(length, width):
    placements = ["Top Wall", "Bottom Wall", "Left Wall", "Right Wall"]

    best_score = -1
    best_placement = None
    best_feedback = []
    best_verdict = ""

    for p in placements:
        score, verdict, feedback = evaluate_placement(length, width, p)

        if score > best_score:
            best_score = score
            best_placement = p
            best_feedback = feedback
            best_verdict = verdict

    return best_placement, best_score, best_feedback