# Northeastern University RedEye Route Optimizer

## Overview
This project provides a Flask API to help visualize the efficiency of various local search algorithms for optimizing the route planning of Northeastern's RedEye safety escort service. The current RedEye app has a flaw – the path followed by a given van often takes the longest route first and drops those who live closest to the starting location, Snell Library, towards the backend of the route. The approach taken to solve this problem can be classified as a derivative of the Traveling Salesman Problem. Additionally, the problem is subdivided using k-means clustering. Each local search algorithm is applied within $k$ clusters where $k$ corresponds to the number of vans available. 

## Features
**Local Search**

There are 5 search algorithms implemented to address the RedEye problem:
- Hill climbing
- Local beam serach
- Simulated annealing
- Genetic algorithm
- A* 

Whenever the code is executed, all 5 algorithms are run so their corresponding efficiencies can be viewed and compared amongst each other.

**K-Means Clustering**

Given the number of vans, $k$, the waypoints are clustered into $k$ clusters using k-means clustering. The idea is to enable the search algorithms to utilize all available resources at the current time (e.g. number of vans) to make the route's as optimal as possible. 

**Flask Frontend**

Using the Flask framework, a locally-hosted frontend is generated to conveniently allow users to enter input and view the results. Here it takes care of the entire functionality of the web app. It takes input from the html file and passes it on to the controller and then recieves the output from the controller and pasees it on to the front end.

## Directory Overview
- /.idea: Flask generated file.
- /Controller: the main application file, `controller.py`, responsible for running each algorithm's backend
- /K_means: k-means clustering algorithm
- /Local_Search: implementations for all local search algorithms
- /Locations_dataset: datasets containing waypoint addresses, one of which includes each longitude and latitude
- /Parameters: Has functions to calculte time and generate waypoints.
- /Random_data_generation: generates list of randomly picked waypoints based on number of locations
- /Route_maps: empty folder where each van's route is saved during runtime (visual map, saved as html file)
- /Route_maps_generation: The helper functions used to build this project.
- /Route_order: empty folder where each van's route is saved during runtime (list of addresses in order traversed)
- /templates: folder to store all html files for the front end.
- app.py: front end of the application
- requirements.txt: project dependencies
  

## Getting Started

**Prerequisites**

Ensure you have the following installed to run the front and backend application, details regarding version can be found in `requirements.txt`:
- Flask
- folium
- openrouteservice
- numpy
- scikit-learn
- pandas
- requests

**Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/aditya1225/NEU_RedEye_Path_Optimization.git
   
2. Navigate to the project directory:
   ```bash
   cd NEU_RedEye_Path_Optimization
   
3. Install the required packages:
   ```bash
   pip install -r requirements.txt

4. Run the Flask API:
   ```bash
   python3 app.py

## Acknowledgments
This project uses the following libraries and resources:
- [OpenRouteService API](https://openrouteservice.org/) for route timing calculation
