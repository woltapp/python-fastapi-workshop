import json
import pathlib
from typing import List

from fastapi import FastAPI, Query, Path
from pydantic import BaseModel

app = FastAPI(title="Restaurant API")

@app.get("/")
def hello_world():
    return {"Hello": "World"}


@app.get(
    "/showcase-features/{my_parameter}",
    summary="My custom summary",
    description="My custom description",
)
def showcase_features(
    my_parameter: int = Path(description="My description for my parameter"),
    debug: bool = Query(default=False, description="This is for debugging"),
):
    if debug:
        print("Now we are debugging something")
    return {"Hello": "Jerry", "Got my_parameter": my_parameter}



class Location(BaseModel):
    city: str


class Restaurant(BaseModel):
    name: str
    description: str
    id: str
    location: Location


@app.get("/restaurants", response_model=List[Restaurant])
def get_restaurants():
    restaurants_file_path = pathlib.Path(__file__).parent / "restaurants.json"
    with open(restaurants_file_path) as restaurants_file:
        restaurant_data = json.load(restaurants_file)
    restaurants = []
    for restaurant_data in restaurant_data["restaurants"]:
        restaurant = Restaurant(
            name=restaurant_data["name"],
            description=restaurant_data["description"],
            id=restaurant_data["id"],
            location=Location(city=restaurant_data["city"]),
        )
        restaurants.append(restaurant)
    return restaurants
