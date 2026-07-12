"""
==========================================================
ResIoT Simulator

Module 11 : scenario.py

Author : Kaneez Fizza

Description
-----------
Generates reproducible simulation scenarios that are used
by all resilience approaches (ResIoT, Rule-Based and
ML-Based).

Every approach is evaluated using the EXACT same sequence
of faults.

==========================================================
"""

import random
from dataclasses import dataclass
from typing import List

from failures import FaultGenerator


# ==========================================================
# Simulation Event
# ==========================================================

@dataclass
class SimulationEvent:

    episode: int

    fault: object

    injection_time: float


# ==========================================================
# Simulation Scenario
# ==========================================================

class SimulationScenario:

    def __init__(

            self,

            episodes=1000,

            seed=42

    ):

        self.episodes = episodes

        self.seed = seed

        self.events = []

        self.generator = FaultGenerator()

    # ------------------------------------------------------

    def generate(self):

        random.seed(self.seed)

        self.events.clear()

        current_time = 0

        for episode in range(self.episodes):

            fault = self.generator.generate_fault()

            current_time += random.randint(5,20)

            self.events.append(

                SimulationEvent(

                    episode,

                    fault,

                    current_time

                )

            )

        return self.events

    # ------------------------------------------------------

    def reset(self):

        self.events.clear()

    # ------------------------------------------------------

    def __iter__(self):

        return iter(self.events)

    # ------------------------------------------------------

    def __len__(self):

        return len(self.events)

    # ------------------------------------------------------

    def statistics(self):

        counter = {}

        for event in self.events:

            name = event.fault.name

            counter[name] = counter.get(name,0)+1

        return counter


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    scenario = SimulationScenario(

        episodes=20,

        seed=10

    )

    events = scenario.generate()

    for event in events:

        print(

            event.episode,

            event.fault.name,

            event.fault.stage

        )

    print()

    print(scenario.statistics())