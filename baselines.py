"""
==========================================================
ResIoT Simulator

Module : baselines.py

Author : Kaneez Fizza

Description
-----------
Defines baseline approaches used for comparison with ResIoT:

1. Rule-Based Baseline
2. ML-Based Baseline

All approaches use the same underlying fault profiles
defined in fault_model.py for fair comparison.

==========================================================
"""

from abc import ABC, abstractmethod
from collections import defaultdict
import random

from metrics import Metrics

from fault_model import (
    get_fault_profile,
    simulate_detection,
    simulate_recovery,
    success_probability,
    communication_cost
)


# ==========================================================
# Abstract Baseline
# ==========================================================

class Baseline(ABC):

    def __init__(self, name):

        self.name = name

        self.metrics = Metrics()

    @abstractmethod
    def detect(self, fault):
        pass

    @abstractmethod
    def diagnose(self, fault):
        pass

    @abstractmethod
    def recover(self, fault):
        pass

    def statistics(self):

        return self.metrics.summary()


# ==========================================================
# Rule-Based Baseline
# ==========================================================

class RuleBasedBaseline(Baseline):

    RULES = {

        "SensorDrift":
            "FastCalibration",

        "SensorNoise":
            "NoiseFilter",

        "MissingData":
            "Interpolation",

        "CommunicationLoss":
            "RestartGateway",

        "PacketDelay":
            "QoSAdjust",

        "GatewayFailure":
            "Failover",

        "AnalyticsFailure":
            "RestartModel",

        "ModelDrift":
            "RetrainModel",

        "InformationDelay":
            "Resend",

        "ActuatorFailure":
            "ResetActuator"

    }

    def __init__(self):

        super().__init__("RuleBased")

    # ------------------------------------------------------
    # Detection
    # ------------------------------------------------------

    def detect(self, fault):

        profile = get_fault_profile(
            fault.name
        )

        mttd = simulate_detection(
            profile,
            "Rule"
        )

        self.metrics.record_detection(
            mttd
        )

        return mttd

    # ------------------------------------------------------
    # Diagnosis
    # ------------------------------------------------------

    def diagnose(self, fault):

        return self.RULES[
            fault.name
        ]

    # ------------------------------------------------------
    # Recovery
    # ------------------------------------------------------

    def recover(self, fault):

        profile = get_fault_profile(
            fault.name
        )

        strategy = self.RULES[
            fault.name
        ]

        mttr = simulate_recovery(
            profile,
            "Rule"
        )

        probability = success_probability(
            profile,
            "Rule"
        )

        messages = communication_cost(
            profile,
            "Rule"
        )

        success = (
            random.random()
            < probability
        )

        self.metrics.record_recovery(
            mttr
        )

        for _ in range(messages):

            self.metrics.record_message(
                1
            )

        if success:

            self.metrics.record_success(
                fault.name
            )

        else:

            self.metrics.record_failure(
                fault.name
            )

        return {

            "strategy":
                strategy,

            "success":
                success,

            "mttr":
                mttr,

            "messages":
                messages

        }


# ==========================================================
# ML-Based Baseline
# ==========================================================

class MLBasedBaseline(Baseline):

    def __init__(self):

        super().__init__(
            "MLBaseline"
        )

        self.history = defaultdict(
            list
        )

    # ------------------------------------------------------
    # Detection
    # ------------------------------------------------------

    def detect(self, fault):

        profile = get_fault_profile(
            fault.name
        )

        mttd = simulate_detection(
            profile,
            "ML"
        )

        self.metrics.record_detection(
            mttd
        )

        return mttd

    # ------------------------------------------------------
    # Diagnosis
    # ------------------------------------------------------

    def diagnose(self, fault):

        return "MLRecovery"

    # ------------------------------------------------------
    # Recovery
    # ------------------------------------------------------

    def recover(self, fault):

        profile = get_fault_profile(
            fault.name
        )

        mttr = simulate_recovery(
            profile,
            "ML"
        )

        probability = success_probability(
            profile,
            "ML"
        )

        messages = communication_cost(
            profile,
            "ML"
        )

        success = (
            random.random()
            < probability
        )

        self.history[
            fault.name
        ].append(
            mttr
        )

        self.metrics.record_recovery(
            mttr
        )

        for _ in range(messages):

            self.metrics.record_message(
                1
            )

        if success:

            self.metrics.record_success(
                fault.name
            )

        else:

            self.metrics.record_failure(
                fault.name
            )

        return {

            "strategy":
                "MLRecovery",

            "success":
                success,

            "mttr":
                mttr,

            "messages":
                messages

        }