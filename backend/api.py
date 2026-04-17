from fastapi import FastAPI
from pydantic import BaseModel 

from hvac_engine import (
    calculate_btu,
    recommend_ac,
    estimate_cooling_time,
    find_best_placement,
    evaluate_placement
)

app = FastAPI()


# ---------------- INPUT MODEL ----------------
class RoomInput(BaseModel):
    length: float
    width: float
    height: float
    people: int
    windows: int
    sunlight: str
    room_type: str
    placement_1: str
    placement_2: str
    door_position: str
    furniture_density: str


# ---------------- HEALTH CHECK ----------------
@app.get("/")
def home():
    return {"message": "HVAC API is running"}


# ---------------- MAIN API ----------------
@app.post("/calculate")
def calculate(data: RoomInput):

    # 🔹 Core Calculations
    btu = calculate_btu(
        data.length,
        data.width,
        data.height,
        data.people,
        data.windows,
        data.sunlight,
        data.room_type
    )

    ac = recommend_ac(btu)
    area = data.length * data.width
    cooling_time = estimate_cooling_time(btu, area)

    # 🔹 Comparison Logic
    score1, verdict1, feedback1 = evaluate_placement(
    data.length,
    data.width,
    data.placement_1,
    data.door_position,
    data.furniture_density
    )

    score2, verdict2, feedback2 = evaluate_placement(
    data.length,
    data.width,
    data.placement_2,
    data.door_position,
    data.furniture_density
    )

    # 🔹 Best Placement
    best_placement, best_score, best_feedback = find_best_placement(
        data.length, data.width
    )

    # 🔹 Final Response
    return {
        "btu": round(btu, 2),
        "recommended_ac": ac,
        "cooling_time": cooling_time,

            "comparison": {
            "placement_1": {
                "name": data.placement_1,
                "score": score1,
                "verdict": verdict1,
                "feedback": feedback1
            },
            "placement_2": {
                "name": data.placement_2,
                "score": score2,
                "verdict": verdict2,
                "feedback": feedback2
            }
        },

        "best_placement": best_placement,
        "score": best_score,
        "feedback": best_feedback
    }