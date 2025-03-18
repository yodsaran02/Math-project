
from flask import Flask, render_template, request, redirect
import time
import json
import math
import cv2

app = Flask(__name__)
time.sleep(5)


def dijkstra(graph, start, end):
    distances = {vertex: float("infinity") for vertex in graph}
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




def remove_key_value(graph, key_to_remove):
    # Create a new graph to hold the modified structure
    new_graph = {}
    
    for node, neighbors in graph.items():
        if node == key_to_remove:
            # Skip this node entirely if its key matches key_to_remove
            continue
        
        # Filter out any edges where the neighbor is key_to_remove
        new_neighbors = {neighbor: weight for neighbor, weight in neighbors.items() if neighbor != key_to_remove}
        
        if new_neighbors:
            new_graph[node] = new_neighbors
    
    return new_graph




graph = {
    1: {2: 12, 20: 7, 16: 33},
    2: {1: 12, 3: 8},
    3: {2: 8, 12: 24, 4: 12},
    4: {3: 12, 14: 15, 5: 5},
    5: {4: 5, 10: 27, 6: 15},
    6: {5: 15, 13: 15, 9: 24, 7: 11},
    7: {6: 11, 8: 24},
    8: {7: 24, 9: 10},
    9: {8: 10, 10: 13, 6: 24, 19: 17},
    10: {11: 12, 9: 13, 18: 17, 5: 27},
    11: {10: 12, 17: 14, 12: 8},
    12: {11: 8, 16: 11, 3: 24},
    13: {6: 15, 14: 20},
    14: {13: 20, 4: 15, 20: 27},
    15: {16: 17},
    16: {15: 17, 1: 33, 12: 10},
    17: {11: 14},
    18: {10: 17},
    19: {9: 17},
    20: {1: 7, 16: 43, 14: 27},
}

vertical = [
    [14, 20],
    [13, 14],
    [1, 2],
    [3, 4],
    [4, 5],
    [5, 6],
    [6, 7],
    [8, 9],
    [9, 10],
    [10, 11],
    [11, 12],
    [12, 16],
]

horizontal = [
    [1, 20],
    [1, 16],
    [15, 16],
    [3, 12],
    [2, 3],
    [4, 14],
    [5, 10],
    [6, 9],
    [7, 8],
    [6, 13],
    [11, 17],
    [10, 18],
    [9, 19],
]

number = [
    [1118, 1428],
    [1106, 1132],
    [942, 1141],
    [942, 899],
    [934, 793],
    [928, 477],
    [922, 267],
    [416, 206],
    [419, 448],
    [422, 747],
    [436, 1009],
    [436, 1184],
    [1213, 505],
    [1233, 891],
    [97, 1540],
    [445, 1494],
    [101, 1018],
    [98, 721],
    [88, 481],
    [1237, 1427],
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    # Get the JSON string from the hidden input fields
    active_buttons_json = request.form.get('active_buttons')
    yellow_buttons_json = request.form.get('yellow_buttons')
    
    # Parse the JSON strings into Python lists
    active_buttons = []
    yellow_buttons = []
    if active_buttons_json:
        active_buttons = active_buttons_json
    
    if yellow_buttons_json:
        yellow_buttons = yellow_buttons_json

    # Process the active and yellow-stage buttons separately
    print("Active Buttons:", active_buttons)
    print("Yellow-Stage Buttons:", yellow_buttons)

    img = cv2.imread("./maps.png")
    selected = active_buttons
    src = int(selected[0])
    dst = int(selected[1])
    graph2 = {}
    for number in yellow_buttons:
        graph2 = remove_key_value(graph,number)
    shortest_path, shortest_distance = dijkstra(graph2, src, dst)
    print(f"Shortest path from {src} to {dst}: {shortest_path}")
    msg = ""
    for node in shortest_path:
        msg = msg + "," + str(node)
    counter = 1
    vertical_length = 0
    horizontal_length = 0
    while counter < len(shortest_path):
        if shortest_path[counter] > shortest_path[counter - 1]:
            start = shortest_path[counter - 1]
            end = shortest_path[counter]
        else:
            start = shortest_path[counter]
            end = shortest_path[counter - 1]
        cv2.line(
            img,
            (number[start - 1][0], number[start - 1][1]),
            (number[end - 1][0], number[end - 1][1]),
            (0, 0, 255),
            5,
        )
        for side in vertical:
            if side[0] == start and side[1] == end:
                vertical_length += graph[start][end]
        for side in horizontal:
            if side[0] == start and side[1] == end:
                horizontal_length += graph[start][end]
        counter += 1
    direct_distance = math.sqrt(vertical_length**2 + horizontal_length**2)
    print(f"Direct distance = {int(direct_distance)}")
    print(f"Distance = {shortest_distance}")
    cv2.line(
        img,
        (number[src - 1][0], number[src - 1][1]),
        (number[dst - 1][0], number[dst - 1][1]),
        (0, 255, 0),
        5,
    )
    for number in yellow_buttons:
        center_coordinates = (number[number-1][0],number[number-1][1])
        radius = 10
        thickness = 10
        color = (0, 0, 255) 
        img = cv2.circle(img, center_coordinates, radius, color, thickness)
    cv2.imwrite("./maps_annotated.png", img)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0")

