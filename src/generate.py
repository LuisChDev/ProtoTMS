"""
This module contains the main sequence of operations for the calculation
of routes.
"""
from typing import Dict, Union, List
from ortools.constraint_solver import (
    pywrapcp,
    routing_enums_pb2
)

from src.matrix import matrix


def create_data_model(
        matx: List[List[float]] = matrix) -> Dict[
            str, Union[int, List[List[float]]]
        ]:
    """Stores the data for the problem."""

    return {
        "distance_matrix": matx if matx is not None else matrix,
        "num_vehicles": 4,
        "depot": 0
    }


def print_solution(data: Dict, manager, routing, solution):
    """
    Prints the calculated routing schedule.
    """
    max_route_distance = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} -> '.format(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index. index, vehicle_id
            )
        plan_output += '{}\n'.format(manager.IndexToNode(index))
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    print('Maximum of the route distances: {}m'.format(max_route_distance))


def gen_route(distances=None):
    """
    creates the data model, the routing model and runs the optimization.
    """
    data = create_data_model(matx=distances)
    print("created data model")

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']),
        data['num_vehicles'],
        data['depot']
    )
    print("created routing index manager")

    # Create routing model.
    routing = pywrapcp.RoutingModel(manager)
    print("created routing model")

    # Create and register a distance callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between two nodes."""
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    print("created and registered a distance callback")

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,     # no slack
        3000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name
    )

    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    print("setting first heuristic")

    # solve the problem.
    solution = routing.SolveWithParameters(search_parameters)
    print("actually solve the problem")

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)
        print(data, manager, routing, solution)
    else:
        print("solution was None, here's the rest:",
              data, manager, routing, solution)
