from fastapi import FastAPI

app = FastAPI(title="Restaurant API")


@app.get("/")
def hello_world():
    return {"Hello": "World"}
