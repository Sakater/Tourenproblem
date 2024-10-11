from ortools.constraint_solver import pywrapcp, routing_enums_pb2
from Tour import Tour
import numpy


class Model:
    def __init__(self, tour: Tour):
        self.tour = tour

    def create_adjacency_matrix(self):

        """h = [[0, 1, 2, 3],
             [1, 0, 4, 5],
             [2, 4, 0, 6],
             [3, 5, 6, 0]]"""
        matrix = numpy.zeros((len(self.tour.nodes), len(self.tour.nodes)))
        for i, edges in enumerate(self.tour.edges):
            for j, edge in enumerate(edges):
                matrix[i][j] = edge.distance

        return matrix

    def create_data_model(self):
        """Stores the data for the problem."""
        data = {"distance_matrix": self.tour.edges, "num_vehicles": 1, "depot": 0}
        return data

    def print_solution(self, manager, routing, solution):
        """Prints solution on console."""
        print(f"Objective: {solution.ObjectiveValue()} miles")
        index = routing.Start(0)
        plan_output = "Route for vehicle 0:\n"
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += f" {manager.IndexToNode(index)} ->"
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
        plan_output += f" {manager.IndexToNode(index)}\n"
        print(plan_output)
        plan_output += f"Route distance: {route_distance}miles\n"

    def execute_model(self):
        data = self.create_data_model()
        manager = pywrapcp.RoutingIndexManager(
            len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
        )
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data["distance_matrix"][from_node][to_node]

        def get_routes(solution, routing, manager):
            """Get vehicle routes from a solution and store them in an array."""
            # Get vehicle routes and store them in a two dimensional array whose
            # i,j entry is the jth location visited by vehicle i along its route.
            routess = []
            for route_nbr in range(routing.vehicles()):
                index = routing.Start(route_nbr)
                route = [manager.IndexToNode(index)]
                while not routing.IsEnd(index):
                    index = solution.Value(routing.NextVar(index))
                    route.append(manager.IndexToNode(index))
                routess.append(route)
            return routess

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )

        solution = routing.SolveWithParameters(search_parameters)
        if solution:
            self.print_solution(manager, routing, solution)

        routes = get_routes(solution, routing, manager)
        # Display the routes.
        for i, route in enumerate(routes):
            print('Route', i, route)
