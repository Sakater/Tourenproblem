from pydantic import BaseModel
from Node import Node


class Edge(BaseModel):
    originNode: Node
    targetNode: Node
    distance: float
    time: int
