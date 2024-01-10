import json
import pathlib

from fastapi import FastAPI, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="Restaurant API")

restaurants_by_id = {}


@app.on_event("startup")
def startup_event():
    data_file_path = pathlib.Path(__file__).parent / "restaurants.json"
    with open(data_file_path) as my_file:
        restaurants_data = json.load(my_file)

    for restaurant in restaurants_data["restaurants"]:
        name = restaurant["name"]
        id = restaurant["id"]
        description = restaurant["description"]
        lon, lat = restaurant["location"]
        city = restaurant["city"]

        restaurants_by_id[id] = Restaurant(
            name=name,
            id=id,
            description=description,
            location=Location(city=city, coordinates=Coordinates(lat=lat, lon=lon)),
        )


@app.get("/")
def hello_world():
    return {"Hello": "World"}


@app.get(
    "/showcase-features/{some_path_parameter}",
    summary="Example endpoint",
    description="My description",
)
def showcase_features(
    some_path_parameter: int = Path(
        title="path param title", description="path param description"
    ),
    debug: bool = Query(
        default=False, title="debug title", description="my query param description"
    ),
):
    if debug:
        print("Now we are debugging")
    return {"Hello": "Jerry", "Got param": some_path_parameter}


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
    return restaurants_by_id.values()


@app.get("/restaurant/{restaurant_id}")
def get_restaurant(restaurant_id: str) -> Restaurant:
    if restaurant_id in restaurants_by_id:
        return restaurants_by_id[restaurant_id]
    else:
        return JSONResponse(status_code=404, content={"detail": "Restaurant unknown"})
