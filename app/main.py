import json
import pathlib
from typing import List

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel

app = FastAPI(title="Restaurant API")

RESTAURANTS = {}


@app.on_event("startup")
def startup_event():
    restaurants_file_path = pathlib.Path(__file__).parent / "restaurants.json"
    with open(restaurants_file_path) as restaurants_file:
        restaurant_data = json.load(restaurants_file)
    for restaurant_data in restaurant_data["restaurants"]:
        lon, lat = restaurant_data["location"]
        restaurant_id = restaurant_data["id"]
        restaurant = FullRestaurant(
            name=restaurant_data["name"],
            description=restaurant_data["description"],
            id=restaurant_data["id"],
            location=Location(
                city=restaurant_data["city"],
                coordinates=Coordinates(lat=lat, lon=lon),
            ),
            tags=restaurant_data["tags"],
        )
        RESTAURANTS[restaurant_id] = restaurant


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


class LightLocation(BaseModel):
    city: str


class Coordinates(BaseModel):
    lat: float
    lon: float


class Location(BaseModel):
    city: str
    coordinates: Coordinates


class LightRestaurant(BaseModel):
    name: str
    description: str
    id: str
    location: LightLocation


class FullRestaurant(BaseModel):
    name: str
    description: str
    id: str
    location: Location
    tags: List[str]


@app.get("/restaurants", response_model=List[LightRestaurant])
def get_restaurants():
    return list(RESTAURANTS.values())


@app.get("/restaurants/{restaurant_id}", response_model=FullRestaurant)
def get_restaurant(restaurant_id: str):
    if restaurant_id in RESTAURANTS:
        return RESTAURANTS[restaurant_id]
    else:
        raise HTTPException(
            status_code=404, detail="Sorry, this restaurant does not exist"
        )
