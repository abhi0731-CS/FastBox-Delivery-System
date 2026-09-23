"""
FastBox Mystery Delivery System
--------------------------------
Simulates one day of package deliveries.

Rules:
1. A package is assigned to the agent who is closest to its warehouse
   using Euclidean distance from the agent's CURRENT starting location.
2. The agent travels from its current location to the warehouse,
   then from the warehouse to the package destination.
3. After delivery, the agent's location becomes the destination.
4. Efficiency = total distance / number of packages delivered.
   Lower efficiency means fewer distance units per package.
"""

import json
import math
import csv
from pathlib import Path


def load_data(filename="data.json"):
    """Read and parse the JSON input file."""
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def euclidean_distance(point1, point2):
    """Return Euclidean distance between two [x, y] coordinates."""
    return math.sqrt(
        (point1[0] - point2[0]) ** 2 +
        (point1[1] - point2[1]) ** 2
    )


def normalize_data(data):
    """Accept both the assignment format and the base_case format."""
    warehouses = data["warehouses"]
    agents = data["agents"]
    packages = data["packages"]

    # Some supplied test files use dictionaries:
    # {"W1": [x, y], ...}
    if isinstance(warehouses, dict):
        normalized_warehouses = warehouses
    else:
        normalized_warehouses = {
            item["id"]: item["location"] for item in warehouses
        }

    if isinstance(agents, dict):
        normalized_agents = agents
    else:
        normalized_agents = {
            item["id"]: item["location"] for item in agents
        }

    normalized_packages = []
    for package in packages:
        normalized_packages.append({
            "id": package["id"],
            "warehouse": package.get("warehouse", package.get("warehouse_id")),
            "destination": package["destination"]
        })

    return normalized_warehouses, normalized_agents, normalized_packages


def assign_packages(warehouses, agents, packages):
    """Assign each package to the nearest agent by agent-to-warehouse distance."""
    assignments = {agent_id: [] for agent_id in agents}

    for package in packages:
        warehouse_location = warehouses[package["warehouse"]]

        nearest_agent = min(
            agents,
            key=lambda agent_id: euclidean_distance(
                agents[agent_id], warehouse_location
            )
        )
        assignments[nearest_agent].append(package)

    return assignments


def simulate(warehouses, agents, packages):
    """Assign and deliver all packages, returning the final report."""
    assignments = assign_packages(warehouses, agents, packages)

    # Copy starting positions so the input data is not modified.
    current_locations = {
        agent_id: list(location)
        for agent_id, location in agents.items()
    }

    report = {}
    delivered_packages = set()

    for agent_id, assigned_packages in assignments.items():
        total_distance = 0.0

        for package in assigned_packages:
            warehouse_location = warehouses[package["warehouse"]]
            destination = package["destination"]

            # Travel to the warehouse.
            total_distance += euclidean_distance(
                current_locations[agent_id], warehouse_location
            )

            # Travel from warehouse to destination.
            total_distance += euclidean_distance(
                warehouse_location, destination
            )

            # Agent ends this delivery at the destination.
            current_locations[agent_id] = list(destination)
            delivered_packages.add(package["id"])

        count = len(assigned_packages)
        efficiency = total_distance / count if count else 0.0

        report[agent_id] = {
            "packages_delivered": count,
            "total_distance": round(total_distance, 2),
            "efficiency": round(efficiency, 2)
        }

    if delivered_packages:
        best_agent = min(
            (agent_id for agent_id in report if report[agent_id]["packages_delivered"] > 0),
            key=lambda agent_id: report[agent_id]["efficiency"]
        )
    else:
        best_agent = None

    report["best_agent"] = best_agent

    # Safety check required by the assignment.
    assert len(delivered_packages) == len(packages), (
        "Not all packages were delivered."
    )

    return report


def save_report(report, filename="report.json"):
    """Save the report as formatted JSON."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)


def export_top_performer_csv(report, filename="top_performer.csv"):
    """Bonus: export the best agent's statistics to CSV."""
    best_agent = report["best_agent"]
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "agent", "packages_delivered", "total_distance", "efficiency"
        ])
        if best_agent:
            stats = report[best_agent]
            writer.writerow([
                best_agent,
                stats["packages_delivered"],
                stats["total_distance"],
                stats["efficiency"]
            ])


def print_report(report):
    """Display a readable report in the terminal."""
    print("\nFastBox Delivery Report")
    print("-" * 45)

    for agent_id, stats in report.items():
        if agent_id == "best_agent":
            continue
        print(
            f"{agent_id}: "
            f"{stats['packages_delivered']} package(s), "
            f"distance = {stats['total_distance']:.2f}, "
            f"efficiency = {stats['efficiency']:.2f}"
        )

    print(f"Most efficient agent: {report['best_agent']}")


def main():
    data = load_data()
    warehouses, agents, packages = normalize_data(data)

    report = simulate(warehouses, agents, packages)
    save_report(report)
    export_top_performer_csv(report)
    print_report(report)

    print("\nSaved: report.json")
    print("Saved: top_performer.csv")


if __name__ == "__main__":
    main()
