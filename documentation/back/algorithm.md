# TSP Path Finding Algorithm

This section details the data structures used to do the gestion of the algorithm and calculate distances before running the optimization algorithms.

## 1. Location Data Management

The Location class represents a city or a specific point on the map. 

* Attributes : each location has a unique ID, a name, a latitude, and a longitude
* Distance Calculation : the class uses the haversine library to compute the real distance between two coordinates in kilometers by calculating the great-circle distance between two points on a sphere

## 2. Tour and Graph Representation

The Tour class manages a collection of Location objects and creates the data structures needed by the pathfinding solvers.

* Adjacency Matrix : when locations are added, the class automatically generates a 2D list called distance_matrix. Each cell distance_matrix[i][j] stores the distance in kilometers between location i and location j. This matrix acts as a complete weighted graph.
* Score Evaluation : the tour_score method takes a list of indices representing a path and calculates the total distance of the trip.
* Itinerary Formatting: the format_itinerary method takes the raw sequence of indices and maps them back to the original Location objects with their visit order, starting at step 1.

## 3. Pathfinding Algorithms Architecture

The solving system uses object-oriented programming with an abstract base class to use different TSP strategies.

### Base Pathfinding Interface
The BasePathFindingAlgorithm class is an abstract base class (ABC). It defines a standard contract for all solving strategies.
* Abstract Method : every algorithm must implement the find_shortest_itinerary(distance_matrix) method
* Input/Output : it takes the 2D distance_matrix from a Tour object and must return an ordered list of integers representing the optimal route indices

### Exact Algorithm : Dynamic Held-Karp TSP
The DynamicHeldKarpTSP class inherits from BasePathFindingAlgorithm, it finds the absolute shortest itinerary using an exact mathematical approach.

* Methodology : it uses Programming Dynamique to break the TSP problem into smaller overlapping sub-problems 
* State Management : to save memory and track visited cities efficiently, the algorithm uses a binary integer mask, each bit in the integer represents a location (1 for visited, 0 for unvisited)
* Memoization : the class uses a dictionary (dict_distance) to keep the calculations, if the algorithm reaches a combination of a sub-tour (mask) and a current location (index_location) that was already computed, it retrieves the distance instantly
* Path Reconstruction : another dictionary (dict_decisions) tracks the best next node for each state, after the recursive analysis, a while loop reads these decisions to reconstruct the final path from the starting point back to index 0
* Complexity : this algorithm gives the optimal solution but has an exponential time complexity of O(n^2 \cdot 2^n)

### Heuristic Algorithm : Nearest Neighbours TSP
The NearestNeighboursTSP class also inherits from BasePathFindingAlgorithm, it implements a greedy heuristic method to find a fast solution for the TSP.

* Methodology : it uses a greedy approach, where the algorithm starts at the first location (index 0) and builds the route step-by-step. At each step, it looks at the current location and selects the closest unvisited location from the distance matrix.
* State Management : the class uses a standard Python set called visited to store the indices of the cities already included in the tour, this ensures that no city is visited twice.
* iterative Loop : a while loop runs until every single location is added to the path list, inside this loop, the loop checks on the unvisited nodes to find the minimum distance from the current_location.
* Tour Completion : once all locations are visited, the algorithm appends 0 to the end of the path list to close the loop and return to the starting point.
* Complexity : this algorithm has a polynomial time complexity of O(n^2). However, it doesn't guarantee the absolute shortest itinerary, but it runs instantly even with a very large number of locations.

## 4. Main Execution and Algorithm Selection

The main script orchestrates the minimal path search. It initializes the data, chooses the best routing strategy, and displays the final results.

### Workflow and Orchestration
1. Data Initialization : the script gets a raw list of dictionaries containing locations and geographic coordinates. It converts these dictionaries into Location objects and builds a global Tour instance, which computes the shared distance matrix.
2. Dynamic Routing Decision : the program uses a conditional statement to select the solving strategy based on the dataset size:
   * If there is 15 cities or less, it instantiates DynamicHeldKarpTSP() to get the exact optimal solution when the problem size allows it
   * If there is more than 15 cities, it switches to NearestNeighboursTSP(), that is less precise but doesn't take too long to run
3. Execution and Output : the chosen algorithm computes the path indices. The script then calculates the final distance, formats the tour data, and sends back the step-by-step itinerary along with the total distance in the terminal.