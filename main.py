from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Model import Model
from Node import Node
from Tour import Tour

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/nodes")
async def create_nodes(nodes: List[Node]):
    tour = Tour(nodes)
    distances = await tour.fetch_distances()
    model = Model(tour)
    routes = model.execute_model()
    output = {"distances": distances, "routes": routes}
    return output
