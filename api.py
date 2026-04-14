from fastapi import FastAPI
from pydantic import BaseModel

from backend.hvac_engine import (
    calculate_btu,
    recommend_ac,
    estimate_cooling_time,
    find_best_placement
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

    best_placement, score, feedback = find_best_placement(data.length, data.width)

    return {
        "btu": round(btu, 2),
        "recommended_ac": ac,
        "cooling_time": time,
        "best_placement": best_placement,
        "score": score,
        "why": feedback
    }