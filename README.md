# CPU Scheduling Simulator (Python)

## Overview

This project is a CPU Scheduling Simulator developed using Python and Tkinter. It demonstrates how different CPU scheduling algorithms work in an operating system. The simulator also analyzes the input process data and recommends the most suitable scheduling algorithm based on specific characteristics.

The project is designed for educational purposes, helping students understand scheduling algorithms, their execution order, and their impact on performance metrics.


## Features

- Simulation of four major CPU scheduling algorithms:
  - FCFS (First Come First Serve)
  - SJF (Shortest Job First)
  - Priority Scheduling
  - Round Robin
- Calculation and display of:
  - Completion Time
  - Turnaround Time
  - Waiting Time
  - Average Waiting Time
  - Average Turnaround Time
- Gantt chart visualization
- Algorithm recommendation based on process characteristics
- Graphical User Interface (GUI) using Tkinter


## How It Works

1. Enter the number of processes.
2. Input the arrival time, burst time, and priority for each process.
3. Use the "Suggest Best Algorithm" option to view the recommended scheduling method.
4. Choose an algorithm and run the simulation.
5. View the results including the scheduling table, average metrics, and Gantt chart.


## Example Output

| PID | Arrival | Burst | Completion | Turnaround | Waiting |
|-----|---------|-------|------------|------------|----------|
| P1  | 0       | 5     | 5          | 5          | 0        |
| P2  | 1       | 3     | 8          | 7          | 4        |
| P3  | 2       | 8     | 16         | 14         | 6        |

- Average Waiting Time: 3.33  
- Average Turnaround Time: 8.67  

A Gantt chart is also generated to visually represent CPU time allocation.


## Algorithm Suggestion Criteria

The simulator recommends a scheduling algorithm based on the characteristics of the input data:

- Priority Scheduling: Recommended if priority differences are significant.
- SJF: Recommended if burst times vary significantly.
- FCFS: Recommended if arrival times are far apart.
- Round Robin: Recommended if processes are similar and require fair time sharing.


## Technologies Used

- Programming Language: Python 3.x
- GUI Library: Tkinter
- Data Visualization: Matplotlib

```bash
git clone https://github.com/Abhay-Cybersec/cpu-scheduling-simulator.git
