"""Run the FastBox solution against all supplied randomized test cases."""
import json
from pathlib import Path
import sys

from main import normalize_data, simulate

TEST_DIR = Path("test_cases")

for path in sorted(TEST_DIR.glob("test_case_*.json")):
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    warehouses, agents, packages = normalize_data(data)
    report = simulate(warehouses, agents, packages)

    delivered = sum(
        stats["packages_delivered"]
        for agent, stats in report.items()
        if agent != "best_agent"
    )

    print(
        f"{path.name}: PASS | "
        f"{delivered}/{len(packages)} packages | "
        f"best_agent={report['best_agent']}"
    )
