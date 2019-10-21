from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

import itertools

#   CONSTANTS

N = 6
ARBITRARY_START_END = True
USE_GUIDED_LOCAL_SEARCH = True
SEARCH_TIME_LIMIT = 60 * 5

verboseMode = False

#   FUNCTIONS


def write_file(n, superpermutation):

    def readFile(dict):
        file = open("superpermutations.txt", "r")

        keyFlag = False
        for val in file.read().split():

            if keyFlag:
                if key in dict:
                    dict[key].append(int(val))

                else:
                    dict[key] = [int(val)]
                keyFlag = False

            if int(val) < 121:
                keyFlag = True
                key = int(val)

        file.close()
        return dict

    dict = {}
    dict = readFile(dict)

    file = open("superpermutations.txt", "a")

    if n in dict:
        if int(superpermutation) in dict[n]:
            print('SuperPermutation already exists in file')
        else:
            string = '\n' + str(n) + ' ' + str(superpermutation)
            file.write(string)
            print('Written to file')
    else:
        string = '\n' + str(n) + ' ' + str(superpermutation)
        file.write(string)
        print('Written to file')

    file.close()
    return


def convertTuple(tup):
    str1 =  ''.join(str(e) for e in tup)
    return str1


def generate_matrix(permutations):

    if ARBITRARY_START_END:
        zeros = []
        for i in range(len(permutations) + 1):
            zeros.append(0)

        Matrix = [zeros]
    else:
        Matrix = []

    # start node
    for i in permutations:

        if ARBITRARY_START_END: rowList = [0]
        else: rowList = []

        # end node
        for j in permutations:

            weight = get_weight(i, j)

            rowList.append(weight)
        Matrix.append(rowList)

    return Matrix

def get_weight(p1, p2):
    p1 = convertTuple(p1)
    p2 = convertTuple(p2)
    n = len(p1)

    weight = 0
    # string starting positions
    for i in range(n):

        matches = 0
        # character positions
        for j in range(n - i):

            if verboseMode: print('comparing ', p1[j + i], ' to ', p2[j])
            if p1[j + i] == p2[j]:
                if verboseMode: print('match')
                matches += 1
            else:
                if verboseMode: print('no match')
                if matches > 0:
                    matches = 0
                weight += 1
                break
        if matches + weight == n:
            break

    return weight

def generate_permutations(n):
    nList = []

    for i in range(n):
        nList.append(i+1)

    # calculate all permutations
    permutations = list(itertools.permutations(nList))

    return permutations


def create_data_model(Matrix, startNode):
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = Matrix  # yapf: disable
    data['num_vehicles'] = 1
    data['depot'] = startNode
    return data

def my_print_only_nodes(manager, routing, assignment):
    """Prints only node route on console."""
    plan_output = ''
    index = routing.Start(0)
    List = []
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        List.append(manager.IndexToNode(index))
        previous_index = index
        index = assignment.Value(routing.NextVar(index))
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    return List


def main():
    """Entry point of the program."""
    Permutations = generate_permutations(N)

    Matrix = generate_matrix(Permutations)

    data = create_data_model(Matrix, 0)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']), data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Use Guided Local Search?
    if USE_GUIDED_LOCAL_SEARCH:
        search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
        search_parameters.time_limit.seconds = SEARCH_TIME_LIMIT

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if assignment:
        List = my_print_only_nodes(manager, routing, assignment)

        listIndex = 0
        listAdjuster = 0
        if ARBITRARY_START_END: listIndex = 1; listAdjuster = -1

        fullPerm = convertTuple(Permutations[List[listIndex] + listAdjuster])

        totalLen = N

        for i in range(0, len(List)):

            if i != len(List)-1:

                nextWeight = distance_callback(List[i], List[i + 1])
                totalLen += nextWeight

                while nextWeight > 0:
                    fullPerm += convertTuple(Permutations[List[i + 1] + listAdjuster])[N - nextWeight]
                    nextWeight += -1


        print("N =", N)
        print("The Total Length is: ", totalLen)
        print(fullPerm)
        write_file(N, fullPerm)



if __name__ == '__main__':
    main()