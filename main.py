import json

from fastapi import FastAPI
from typing import List
from Model import Model
from Node import Node
from Tour import Tour

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/nodes")
async def create_nodes(nodes: List[Node]):
    tour = Tour(nodes)
    distances = await tour.fetch_distances()
    model = Model(tour)
    routes = model.execute_model()
    output = {"distances:": distances, "routes:": routes}
    # routesWrapper(routes, distances)
    return json.dumps(output)
