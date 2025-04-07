# Northeastern University RedEye Route Optimizer

## Overview
This project provides a Flask API to help visualize the efficiency of various local search algorithms for optimizing the route planning of Northeastern's RedEye safety escort service. The current RedEye app has a flaw – the path followed by a given van often takes the longest route first and drops those who live closest to the starting location, Snell Library, towards the backend of the route. The approach taken to solve this problem can be classified as a derivative of the Travelling Salesman Problem. Additonally, the problem is subdivied using k-means clustering. Each local search algorithm is applied within $k$ clusters where $k$ corresponds to the number of vans available. 

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

Using the Flask framework, a locally-hosted frontend is generated to conveniently allow users to enter input and view the results.
ADD MORE INFO HERE ABOUT FRONTEND/HOW FLASK WORKS??

## Directory Overview
- /.idea: ????
- /Controller: the main application file, controller.py, responsible for running each algorithm's backend
- /K_means: k-means clustering algorithm
- /Local_Search: implenmentations for all local search algorithms
- /Locations_dataset: datasets containing waypoint addresses, one of which includes each longitude and latitude
- /Parameters: ???
- /Random_data_generation: generates list of randomly picked waypoints based on number of locations
- /Route_maps: empty folder where each van's route is saved during runtime (visual map, saved as html file)
- /Route_maps_generation: ????
- /Route_order: empty folder where each van's route is saved during runtime ()
- /templates: ???
- app.py: front end of the application
- requirements.txt: project dependenices
- waypoints.json: ???

## Getting Started

## Acknowledgments
This project uses the following libraries and resources:

