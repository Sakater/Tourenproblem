from pydantic import BaseModel


class Edge(BaseModel):
    origin: str
    target: str
    lat_origin: float
    lon_origin: float
    lat_target: float
    lon_target: float
    distance: float