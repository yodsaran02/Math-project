import serial
import time


ser = serial.Serial(port='COM3',baudrate=9600,)
time.sleep(5)
def dijkstra(graph, start, end):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    predecessors = {vertex: None for vertex in graph}

    # List to store vertices with their distances
    vertices = list(graph.keys())
    while vertices:
        # Find the vertex with the smallest distance
        current_vertex = min(vertices, key=lambda vertex: distances[vertex])

        # Remove the current vertex from the list
        vertices.remove(current_vertex)

        for neighbor, weight in graph[current_vertex].items():
            distance = distances[current_vertex] + weight

            # Update distance and predecessor if a shorter path is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_vertex

    # Build the path from source to destination
    path = []
    current_vertex = end
    while current_vertex is not None:
        path.insert(0, current_vertex)
        current_vertex = predecessors[current_vertex]

    return path, distances[end]

graph = {
	1:{2:12,20:7,16:33},
    2:{1:12,3:8},
    3:{2:8,12:24,4:12},
    4:{3:12,14:15,5:5},
    5:{4:5,10:27,6:15},
    6:{5:15,13:15,9:24,7:11},
    7:{6:11,8:24},
    8:{7:24,9:10},
    9:{8:10,10:13,6:24,17:17},
    10:{11:12,9:13,18:14,5:27},
    11:{10:12,17:14,12:8},
    12:{11:8,16:11,3:24},
    13:{6:15,14:20},
    14:{13:20,4:15,20:27},
    15:{16:17},
    16:{15:17,1:33,12:10},
    17:{11:14},
    18:{10:14},
    19:{9:17},
    20:{1:7,16:43,14:27}
}


shortest_path, shortest_distance = dijkstra(graph, source, destination)

print(f"Shortest path from {source} to {destination}: {shortest_path}")
print(f"Shortest distance: {shortest_distance}")

msg=""
for node in shortest_path:
	msg = msg+","+str(node)

ser.write(msg.encode())







