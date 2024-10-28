import json
from typing import List

import httpx

from Edge import Edge


def get_routes(result: List[List[int]], edges):
    ordered_routes = []
    for outerIndex, distances in enumerate(edges):
        for innerIndex, distance in enumerate(distances):
            if outerIndex + 1 < len(result[0]):
                routes = result[0][outerIndex]
                target = result[0][outerIndex + 1]
                if distance == edges[routes][target]:
                    ordered_routes.append({'lat': distance['originNode']['lat'], 'lon': distance['originNode']['lon']})
                    if outerIndex + 1 == len(edges):
                        ordered_routes.append(
                            {'lat': distance['targetNode']['lat'], 'lon': distance['targetNode']['lon']})
                    """print(
                        f"start: {distance.originNode.display_name}\n"
                        f"lat: {distance.originNode.lat}, lon: {distance.originNode.lon}\n"
                        f"target: {distance.targetNode.display_name}\n"
                        f"lat: {distance.targetNode.lat}, lon: {distance.targetNode.lon}\n")"""

    return ordered_routes


async def fetch_routes(ordered_routes):
    async with httpx.AsyncClient() as client:
        # Fügen Sie den JSON-String direkt in die URL ein
        body = {'locations': ordered_routes, 'costing': 'auto', "directions_options": {"units": "kilometers"}}
        print(body)
        body = json.dumps(body)
        response = await client.get(f"https://valhalla1.openstreetmap.de/route?json={body}")
        print(response.content)
        # data = json.loads(response.content)
        return response
