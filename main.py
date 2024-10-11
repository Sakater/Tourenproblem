from fastapi import FastAPI
from typing import List
from Model import Model
from Node import Node
from Tour import Tour

app = FastAPI()





@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/nodes")
async def create_nodes(nodes: List[Node]):
    tour = Tour(nodes)
    distances = await tour.fetch_distances()
    model = Model(tour)
    model.execute_model()
    return distances