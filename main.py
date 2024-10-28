import json
from typing import List
from fastapi import Request
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Model import Model
from Node import Node
from Tour import Tour
import Routing as routing

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
    print(routing.get_routes(output['routes'], output['distances']))
    # routesWrapper(routes, distances)
    return output


@app.post("/routes")
async def get_routes(request: Request):
    try:
        results = await request.json()
        routes = routing.get_routes(results['routes'], results['distances'])
        response = await routing.fetch_routes(routes)
        response_data = response.json()  # Convert the response to a dictionary
        return response_data
    except Exception as e:
        return {"error": str(e)}
