"""
==========================================================
ResIoT Simulator

Module 14 : main.py

Author : Kaneez Fizza

Description
-----------
Main entry point for the ResIoT simulator.

Workflow

1. Generate reproducible simulation scenario
2. Run all experiments
3. Export CSV files
4. Generate publication-quality figures
5. Print summary statistics

==========================================================
"""

import os
import time

from scenario import SimulationScenario
from experiments import ExperimentManager
from plotting import PlotManager


# ==========================================================
# Create Output Directories
# ==========================================================

def create_directories():

    directories = [

        "outputs",

        "outputs/csv",

        "outputs/figures"

    ]

    for directory in directories:

        os.makedirs(

            directory,

            exist_ok=True

        )


# ==========================================================
# Banner
# ==========================================================

def banner():

    print()

    print("=" * 70)

    print("        ResIoT Multi-Agent Resilience Simulator")

    print("=" * 70)

    print("Authors : Kaneez Fizza")

    print("Simulator Version : 1.0")

    print("=" * 70)

    print()


# ==========================================================
# Main
# ==========================================================

def main():

    banner()

    create_directories()

    start = time.time()

    # ------------------------------------------------------
    # Scenario
    # ------------------------------------------------------

    scenario = SimulationScenario(

        episodes=1000,

        seed=42

    )

    scenario.generate()

    print()

    print("Simulation Scenario Created")

    print("Episodes :", len(scenario))

    print()

    # ------------------------------------------------------
    # Experiments
    # ------------------------------------------------------

    manager = ExperimentManager(

        episodes=1000,

        seed=42

    )

    print()

    print("Running Experiments...")

    print()

    manager.run_all()

    print()

    print("Experiments Finished")

    # ------------------------------------------------------
    # Plotting
    # ------------------------------------------------------

    print()

    print("Generating Figures...")

    plotter = PlotManager(

        csv_dir="outputs/csv",

        fig_dir="outputs/figures"

    )

    plotter.plot_all()

    print()

    print("Figures Generated")

    # ------------------------------------------------------
    # Summary
    # ------------------------------------------------------

    manager.print_summary()

    end = time.time()

    print()

    print("=" * 70)

    print("Simulation Completed Successfully")

    print(f"Execution Time : {end-start:.2f} seconds")

    print()

    print("CSV Results")

    print("   outputs/csv/")

    print()

    print("Figures")

    print("   outputs/figures/")

    print("=" * 70)


# ==========================================================
# Entry
# ==========================================================

if __name__ == "__main__":

    main()