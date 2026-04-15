from fastapi import FastAPI
from pydantic import BaseModel

from hvac_engine import (
    calculate_btu,
    recommend_ac,
    estimate_cooling_time,
    find_best_placement,
    evaluate_placement   # 👈 ADD THIS
)

app = FastAPI()

# Input model
class RoomInput(BaseModel):
    length: float
    width: float
    height: float
    people: int
    windows: int
    sunlight: str
    room_type: str


@app.get("/")
def home():
    return {"message": "HVAC API is running"}


@app.post("/calculate")
def calculate(data: RoomInput):

    # Core calculations
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
    time = estimate_cooling_time(btu, area)

    # Best placement
    best_placement, best_score, best_feedback = find_best_placement(
        data.length, data.width
    )

    # 🔥 Comparison logic (default comparison for API)
    score1, _, _ = evaluate_placement(data.length, data.width, "Top Wall")
    score2, _, _ = evaluate_placement(data.length, data.width, "Right Wall")

    if score1 > score2:
        comparison = "Top Wall is better"
    elif score2 > score1:
        comparison = "Right Wall is better"
    else:
        comparison = "Both placements perform similarly"

    # Final response
    return {
        "btu": round(btu, 2),
        "recommended_ac": ac,
        "cooling_time": round(time, 2),
        "best_placement": best_placement,
        "score": best_score,
        "feedback": best_feedback,   # ✅ FIXED KEY NAME
        "comparison_result": comparison  # ✅ ADDED
    }