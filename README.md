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
ADD MORE INFO HERE ABOUT FRONTEND/FLASK??

## Directory Overview

## Getting Started

## Acknowledgments
This project uses the following libraries and resources:

