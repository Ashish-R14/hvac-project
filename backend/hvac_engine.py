def calculate_btu(length, width, height, people, windows, sunlight, room_type):
    area = length * width

    base_btu = area * 20

    people_btu = people * 600
    window_btu = windows * 1000

    # Sunlight factor
    sunlight_factor = {
        "Low": 0.9,
        "Medium": 1.0,
        "High": 1.2
    }[sunlight]

    # Room type factor
    room_factor = {
        "Bedroom": 0.9,
        "Living Room": 1.1,
        "Office": 1.2
    }[room_type]

    total_btu = (base_btu + people_btu + window_btu) * sunlight_factor * room_factor

    return total_btu

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


def suggest_placement(length, width):
    if length > width:
        wall = "longer wall (length side)"
        position = "center of the longer wall"
    else:
        wall = "shorter wall (width side)"
        position = "center of the shorter wall"

    return f"Install AC on the {wall}, preferably at the {position}, facing open area"

def estimate_cooling_time(btu, area):
    # simplified model
    cooling_capacity = btu / 60  # BTU per minute

    time = (area * 25) / cooling_capacity

    return round(time, 2)

def evaluate_placement(length, width, placement):
    score = 0
    feedback = []

    # Rule 1: Match with longer wall
    if length > width and placement in ["Top Wall", "Bottom Wall"]:
        score += 3
        feedback.append("Best: Covers wider area effectively")
    elif width > length and placement in ["Left Wall", "Right Wall"]:
        score += 2
        feedback.append("Good: Matches room width for airflow")

    else:
        feedback.append("Warning: May not distribute air evenly")

    # Rule 2: Corner effect (simplified)
    if placement in ["Left Wall", "Right Wall"]:
        feedback.append("Note: Side placement may create uneven cooling")

    # Rule 3: General efficiency
    if score >= 2:
        verdict = "✅ Good Placement"
    elif score == 1:
        verdict = "⚠️ Moderate Placement"
    else:
        verdict = "❌ Poor Placement"

    return score, verdict, feedback

def find_best_placement(length, width):
    placements = ["Top Wall", "Bottom Wall", "Left Wall", "Right Wall"]

    best_score = -1
    best_placement = None
    best_feedback = []

    for p in placements:
        score, verdict, feedback = evaluate_placement(length, width, p)

        if score > best_score:
            best_score = score
            best_placement = p
            best_feedback = feedback

    return best_placement, best_score, best_feedback