"""
==========================================================
ResIoT Simulator

Failure Models

Author : Kaneez Fizza

Description:
Defines all IoT fault models used during simulation.
==========================================================
"""

from dataclasses import dataclass
import random
from typing import Dict

from config import (
    DETECTION_TIME,
    FAULT_PROBABILITIES,
    FAULT_SEVERITY
)


# ==========================================================
# Fault Class
# ==========================================================

@dataclass
class Fault:
    """
    Represents one IoT fault.
    """

    name: str
    severity: int
    stage: str

    detection_min: int
    detection_max: int

    resolved: bool = False

    def detection_time(self):

        return random.randint(
            self.detection_min,
            self.detection_max
        )


# ==========================================================
# Fault Database
# ==========================================================

FAULT_DATABASE: Dict[str, Fault] = {

    "SensorDrift":

        Fault(
            name="SensorDrift",
            severity=FAULT_SEVERITY["MEDIUM"],
            stage="AS1",
            detection_min=40,
            detection_max=120
        ),

    "SensorNoise":

        Fault(
            name="SensorNoise",
            severity=FAULT_SEVERITY["LOW"],
            stage="AS1",
            detection_min=15,
            detection_max=60
        ),

    "MissingData":

        Fault(
            name="MissingData",
            severity=FAULT_SEVERITY["LOW"],
            stage="AS1",
            detection_min=10,
            detection_max=40
        ),

    "CommunicationLoss":

        Fault(
            name="CommunicationLoss",
            severity=FAULT_SEVERITY["HIGH"],
            stage="AS2",
            detection_min=5,
            detection_max=30
        ),

    "PacketDelay":

        Fault(
            name="PacketDelay",
            severity=FAULT_SEVERITY["MEDIUM"],
            stage="AS2",
            detection_min=10,
            detection_max=40
        ),

    "GatewayFailure":

        Fault(
            name="GatewayFailure",
            severity=FAULT_SEVERITY["HIGH"],
            stage="AS2",
            detection_min=20,
            detection_max=80
        ),

    "AnalyticsFailure":

        Fault(
            name="AnalyticsFailure",
            severity=FAULT_SEVERITY["HIGH"],
            stage="AS3",
            detection_min=30,
            detection_max=100
        ),

    "ModelDrift":

        Fault(
            name="ModelDrift",
            severity=FAULT_SEVERITY["HIGH"],
            stage="AS3",
            detection_min=60,
            detection_max=180
        ),

    "InformationDelay":

        Fault(
            name="InformationDelay",
            severity=FAULT_SEVERITY["MEDIUM"],
            stage="AS4",
            detection_min=15,
            detection_max=50
        ),

    "ActuatorFailure":

        Fault(
            name="ActuatorFailure",
            severity=FAULT_SEVERITY["HIGH"],
            stage="AS5",
            detection_min=60,
            detection_max=180
        )

}


# ==========================================================
# Fault Generator
# ==========================================================

class FaultGenerator:
    """
    Generates random faults according to
    predefined probabilities.
    """

    def __init__(self):

        self.fault_names = list(
            FAULT_PROBABILITIES.keys()
        )

        self.weights = list(
            FAULT_PROBABILITIES.values()
        )

    def generate_fault(self):

        fault_name = random.choices(

            self.fault_names,

            weights=self.weights,

            k=1

        )[0]

        return FAULT_DATABASE[fault_name]


# ==========================================================
# Utility Functions
# ==========================================================

def get_fault(name):

    return FAULT_DATABASE[name]


def list_faults():

    return list(FAULT_DATABASE.keys())


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    fg = FaultGenerator()

    print("=" * 60)
    print("Generated Faults")
    print("=" * 60)

    for _ in range(10):

        f = fg.generate_fault()

        print(
            f.name,
            f.stage,
            f.severity,
            f.detection_time()
        )