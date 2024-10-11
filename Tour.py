import json
from typing import List
import numpy
import httpx

from Edge import Edge
from Node import Node


class Tour:
    def __init__(self, nodes: List[Node]):
        self.nodes = nodes
        self.edges = None

    def set_nodes(self, nodes: List[Node]):
        self.nodes = nodes

    def get_nodes(self):
        return self.nodes

    async def fetch_distances(self):
        valEdges = {'sources': [], 'targets': []}
        for node in self.nodes:
            valEdges['sources'].append({'lat': node.lat, 'lon': node.lon})
            valEdges['targets'].append({'lat': node.lat, 'lon': node.lon})
        valEdges['costing'] = 'auto'

        # Konvertieren Sie das Dictionary in einen JSON-String
        valEdges_json = json.dumps(valEdges)

        async with httpx.AsyncClient() as client:
            # Fügen Sie den JSON-String direkt in die URL ein
            response = await client.get(f"https://valhalla1.openstreetmap.de/sources_to_targets?json={valEdges_json}")
            data = json.loads(response.content)
            distances = data['sources_to_targets']
            self.edges = [[] for _ in range(len(self.nodes))]
            for i, edges in enumerate(distances):
                for j, edge in enumerate(edges):
                    self.edges[i].append(Edge(originNode=self.nodes[i], targetNode=self.nodes[j],
                                              distance=edge['distance'], time=edge['time']))
            return self.edges
