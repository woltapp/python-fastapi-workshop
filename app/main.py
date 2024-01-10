import json
import pathlib

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel

app = FastAPI(title="Restaurant API")


@app.get("/")
def hello_world():
    return {"Hello": "World"}


@app.get(
    "/showcase-features/{some_path_parameter}",
    summary="Example endpoint",
    description="My description",
)
def showcase_features(
    some_path_parameter: int = Path(title="my title"),
    debug: bool = Query(default=False, description="description"),
):
    if debug:
        print("Now we are debugging")
    return {"Hello": "Jerry", "Got param": some_path_parameter}


"""
[
  {
    "name": "Example restaurant",
    "description": "Example description",
    "id": "unique-id-for-the-restaurant",
    "location": {
      "city": "Example city",
      "coordinates": {
        "lat": 60.169938852212965,
        "lon": 24.941325187683105
      }
    }
  }
]
"""


class Coordinates(BaseModel):
    lat: float
    lon: float


class Location(BaseModel):
    city: str
    coordinates: Coordinates


class Restaurant(BaseModel):
    name: str
    id: str
    description: str
    location: Location


@app.get("/restaurants")
def get_restaurants() -> list[Restaurant]:
    data_file_path = pathlib.Path(__file__).parent / "restaurants.json"
    with open(data_file_path) as my_file:
        restaurants_data = json.load(my_file)

    restaurants = []
    for restaurant in restaurants_data["restaurants"]:
        name = restaurant["name"]
        id = restaurant["id"]
        description = restaurant["description"]
        lon, lat = restaurant["location"]
        city = restaurant["city"]

        restaurants.append(
            Restaurant(
                name=name,
                id=id,
                description=description,
                location=Location(city=city, coordinates=Coordinates(lat=lat, lon=lon)),
            )
        )

    return restaurants
