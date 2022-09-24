# Python FastAPI workshop
Let's build Restaurant API using modern Python and [FastAPI](https://fastapi.tiangolo.com/) as the web framework.

## Restaurant API - specification
This is what we are going to implement today!

A simple backend service which stores information about restaurants and has two endpoints for accessing that information:
1. GET _/restaurants_ which returns data for all the restaurants.The response payload format should be:
```json
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
```

2. GET _/restaurants/(restaurant-id)_ which returns data for a single restaurant. The response payload format should be:
```json
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
```


## Restaurant data
The restaurant data is stored in the [restaurants.json](app/restaurants.json) file which contains information about 20 imaginary restaurants which are located in Helsinki area.

Example data for a single restaurant:
```json
{
  "blurhash": "UUKJMXv|x]oz0gtRM{V@AHRQwvxZXSs9s;o0",
  "city": "Helsinki",
  "description": "Burgers with attitude!",
  "id": "456162c4-8dab-4959-8cdd-3777c7ede20d",
  "image": "https://prod-wolt-venue-images-cdn.wolt.com/5b348b31fe8992000bbec771/2be8c7738b220df2f9a0974da5c90d90",
  "location": [
    24.941325187683105,
    60.169938852212965
  ],
  "name": "Burger plaza",
  "tags": [
    "hamburger",
    "fries"
  ]
}
```

Fields:

* blurhash: A compact representation of a placeholder for an image (type: string), see https://blurha.sh/.
* city: A city where the restaurant is located (type: string)
* description: More information about what kind of restaurant it is (type: string)
* id: Unique identifier for the restaurant (type: string)
* image: A link to restaurant's image (type: string)
* location: Restaurant's location in latitude & longitude coordinates. First element in the list is the longitude (type: a list containing two numbers)
* name: The name of the restaurant (type: string)
* tags: A list of tags describing what kind of food the restaurant sells, e.g. pizza / burger (type: a list of strings, max. 3 elements)

## Development

### Without Docker
**Prerequisites**
* Python 3.9 or later: [https://www.python.org/downloads/](https://www.python.org/downloads/)
* Poetry: [https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation)

Install the dependencies:
```
poetry install
```

Activate the poetry environment:
```
poetry shell
```
Run the server (`--reload` automatically restarts the server when there are changes in the code):
```
uvicorn app.main:app --reload
```

The API documentation is available in http://127.0.0.1:8000/docs.

### With Docker
Run the app:
```
docker-compose up
```

The API documentation is available in http://127.0.0.1:8000/docs.

## Additional features

__You can code these on your own after the workshop 😉__
1. Implement an endpoint which lists all the restaurants for a given tag. For example: GET /restaurants/tags/hamburger
2. Implement a search endpoint which takes a search string as a query parameter and returns the restaurants which have a full or a partial match for the search string in their name, description or tags fields. For example: GET /restaurants/search?q=sushi
3. Implement an endpoint which takes the customer location as a query parameter and returns the restaurants which are within 500 meters radius from the customer's location. For example: GET /restaurants/nearby?lat=60.17106&lon=24.934434
4. Instead of storing the restaurants in a static json file, store them in a database instead (hint: have a look at [SQLModel](https://sqlmodel.tiangolo.com/)). Additionally add endpoints for creating, updating, and deleting restaurants.
5. Implement automated tests for all the functionality you've built. Familiarise yourself with [pytest](https://docs.pytest.org/en/latest/) and read [how to test FastAPI applications](https://fastapi.tiangolo.com/tutorial/testing/).