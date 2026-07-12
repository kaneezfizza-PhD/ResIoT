"""
==========================================================
ResIoT Simulator

Module : fault_model.py

Author : Kaneez Fizza

Description
-----------
Defines realistic fault profiles used by the simulator.

Instead of randomly generating recovery times,
each fault has intrinsic characteristics that influence

• Detection Time (MTTD)
• Recovery Time (MTTR)
• Communication Cost
• Recovery Difficulty

==========================================================
"""

from dataclasses import dataclass
import random


# ==========================================================
# Fault Profile
# ==========================================================

@dataclass
class FaultProfile:

    name: str

    difficulty: float

    base_mttd: float

    base_mttr: float

    communication_cost: int

    recovery_complexity: int

    learning_gain: float


# ==========================================================
# Fault Library
# ==========================================================

FAULT_LIBRARY = {

    "SensorNoise":

        FaultProfile(
            "SensorNoise",
            difficulty=0.15,
            base_mttd=1.2,
            base_mttr=6,
            communication_cost=2,
            recovery_complexity=1,
            learning_gain=0.015
        ),

    "SensorDrift":

        FaultProfile(
            "SensorDrift",
            difficulty=0.25,
            base_mttd=2,
            base_mttr=8,
            communication_cost=3,
            recovery_complexity=2,
            learning_gain=0.020
        ),

    "MissingData":

        FaultProfile(
            "MissingData",
            difficulty=0.30,
            base_mttd=2.5,
            base_mttr=9,
            communication_cost=2,
            recovery_complexity=2,
            learning_gain=0.018
        ),

    "PacketDelay":

        FaultProfile(
            "PacketDelay",
            difficulty=0.45,
            base_mttd=3.5,
            base_mttr=12,
            communication_cost=4,
            recovery_complexity=3,
            learning_gain=0.022
        ),

    "CommunicationLoss":
        FaultProfile(
        "CommunicationLoss",
        difficulty=0.60,
        base_mttd=4.5,
        base_mttr=15,
        communication_cost=5,
        recovery_complexity=4,
        learning_gain=0.025
    ),

    "GatewayFailure":

        FaultProfile(
            "GatewayFailure",
            difficulty=0.70,
            base_mttd=5.5,
            base_mttr=18,
            communication_cost=6,
            recovery_complexity=5,
            learning_gain=0.030
        ),

    "ActuatorFailure":
        FaultProfile(
            "ActuatorFailure",
            difficulty=0.80,
            base_mttd=6,
            base_mttr=20,
            communication_cost=6,
            recovery_complexity=5,
            learning_gain=0.035
        ),

    "AnalyticsFailure":

        FaultProfile(
            "AnalyticsFailure",
            difficulty=0.85,
            base_mttd=7,
            base_mttr=22,
            communication_cost=7,
            recovery_complexity=6,
            learning_gain=0.040
        ),
    "ModelDrift":

        FaultProfile(
            "ModelDrift",
            difficulty=0.90,
            base_mttd=8.0,
            base_mttr=24,
            communication_cost=8,
            recovery_complexity=7,
            learning_gain=0.045
        ),

    "InformationDelay":

        FaultProfile(
            "InformationDelay",
            difficulty=0.40,
            base_mttd=3.0,
            base_mttr=11,
            communication_cost=3,
            recovery_complexity=2,
            learning_gain=0.020
        )

}



# ==========================================================
# Retrieve Profile
# ==========================================================

def get_fault_profile(fault_name):

    return FAULT_LIBRARY[fault_name]


# ==========================================================
# Generate Detection Time
# ==========================================================

def simulate_detection(profile, approach):

    multiplier = {

        "ResIoT": 0.60,
        "ML": 0.85,
        "Rule": 1.20

    }[approach]

    noise = random.uniform(0.90, 1.10)

    return profile.base_mttd * multiplier * noise


# ==========================================================
# Generate Recovery Time
# ==========================================================

def simulate_recovery(profile, approach):

    multiplier = {

        "ResIoT": 0.55,
        "ML": 0.85,
        "Rule": 1.20

    }[approach]

    noise = random.uniform(0.90, 1.10)

    return profile.base_mttr * multiplier * noise


# ==========================================================
# Success Probability
# ==========================================================

def success_probability(profile, approach):

    base = {

        "ResIoT": 0.97,
        "ML": 0.90,
        "Rule": 0.82

    }[approach]

    return max(

        0.30,

        base - profile.difficulty * 0.12

    )


# ==========================================================
# Communication Cost
# ==========================================================

def communication_cost(profile, approach):

    overhead = {

        "ResIoT": 3,
        "ML": 1,
        "Rule": 0

    }[approach]

    return profile.communication_cost + overhead