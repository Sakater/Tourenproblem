from pydantic import BaseModel


class Node(BaseModel):
    display_name: str
    lat: float
    lon: float
