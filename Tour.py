import json
from typing import List

import httpx

from Edge import Edge
from Node import Node


class Tour:
    def __init__(self, nodes: List[Node]):
        self.nodes = nodes
        self.edges: List[Edge] = []

    def set_nodes(self, nodes: List[Node]):
        self.nodes = nodes

    def get_nodes(self):
        return self.nodes

    """ def find_edges(self):
            edges = []
            for i in range(len(self.nodes)):
                for j in range(i + 1, len(self.nodes)):  # Vermeide doppelte Kanten (i, j) und (j, i)
                    edges.append(({'name': self.nodes[i].display_name + '_' + self.nodes[j].display_name,
                                   'lon_origin': self.nodes[i].lon, 'lat_origin': self.nodes[i].lat,
                                   'lon_dest': self.nodes[j].lon, 'lat_dest': self.nodes[j].lat, 'distance': 0.0}))
            self.edges = edges"""

    async def fetch_distances(self):
        # self.find_edges()
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
            for i in range(len(distances)):
                if distances[i][0]['distance'] == 0.0:
                    self.edges.append(
                        Edge(origin=self.nodes[i].display_name, target=self.nodes[i].display_name, lat_origin=self.nodes[i].lat,
                             lon_origin=self.nodes[i].lon, lat_target=self.nodes[i].lat, lon_target=self.nodes[i].lon,
                             distance=0.0))
                self.edges[i]['distance'] = distances[i][i]['distance']

            return self.edges
