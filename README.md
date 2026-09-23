# FastBox Mystery Delivery System

## Requirements
- Python

## Run
```bash
python main.py
```

The program:
1. Reads `data.json`.
2. Parses the JSON using Python's `json` module.
3. Calculates Euclidean distances.
4. Assigns each package to the nearest agent based on distance to its warehouse.
5. Simulates travel from the agent's current location -> warehouse -> destination.
6. Updates the agent's location after each delivery.
7. Calculates total distance and efficiency.
8. Saves `report.json`.
9. Exports the top performer to `top_performer.csv` (bonus).

## Efficiency
`efficiency = total_distance / packages_delivered`

A lower value means the agent travelled fewer distance units per delivered package.

## Test Cases
The supplied assignment contains 10 randomized test cases. The solution includes a
`test_runner.py` script that runs the same simulation against all of them.
