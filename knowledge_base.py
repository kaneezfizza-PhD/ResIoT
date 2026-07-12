"""
==========================================================
ResIoT Simulator

Module 3 : knowledge_base.py

Author : Kaneez Fizza

Description:
Shared Knowledge Base for all Functional Agents.

The KB stores previous recovery experiences but does NOT
make decisions. Each Functional Agent retrieves policies
from the KB, updates them after execution, and learns from
experience.

==========================================================
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import time
import json
import copy

from config import (
    INITIAL_CONFIDENCE,
    MAX_CONFIDENCE,
    MIN_CONFIDENCE
)


# ==========================================================
# Recovery Policy
# ==========================================================

@dataclass
class RecoveryPolicy:
    """
    One recovery policy stored in the Knowledge Base.
    """

    fault_type: str
    strategy: str

    confidence: float = INITIAL_CONFIDENCE

    attempts: int = 0
    successes: int = 0
    failures: int = 0

    average_mttr: float = 0.0
    average_reward: float = 0.0

    created_by: str = ""
    last_updated: float = field(default_factory=time.time)

    # ------------------------------------------------------

    @property
    def success_rate(self):

        if self.attempts == 0:
            return 0.0

        return self.successes / self.attempts

    # ------------------------------------------------------

    @property
    def score(self):
        """
        Overall policy score.

        Combines

        confidence
        success rate
        recovery speed

        Higher score = better policy
        """

        if self.average_mttr == 0:

            mttr_score = 1

        else:

            mttr_score = 1 / self.average_mttr

        return (

            0.5 * self.confidence +

            0.3 * self.success_rate +

            0.2 * mttr_score

        )

    # ------------------------------------------------------

    def to_dict(self):

        return {

            "fault_type": self.fault_type,

            "strategy": self.strategy,

            "confidence": self.confidence,

            "attempts": self.attempts,

            "successes": self.successes,

            "failures": self.failures,

            "average_mttr": self.average_mttr,

            "average_reward": self.average_reward,

            "created_by": self.created_by,

            "last_updated": self.last_updated

        }


# ==========================================================
# Shared Knowledge Base
# ==========================================================

class KnowledgeBase:

    def __init__(self):

        # fault -> strategy -> policy

        self.memory: Dict[str, Dict[str, RecoveryPolicy]] = {}

    # =======================================================
    # Register
    # =======================================================

    def register_fault(

            self,

            fault_type: str,

            strategies: List[str],

            creator="System"

    ):

        if fault_type not in self.memory:

            self.memory[fault_type] = {}

        for strategy in strategies:

            if strategy not in self.memory[fault_type]:

                self.memory[fault_type][strategy] = RecoveryPolicy(

                    fault_type=fault_type,

                    strategy=strategy,

                    created_by=creator

                )

    # =======================================================
    # Retrieve
    # =======================================================

    def get_policy(

            self,

            fault_type,

            strategy

    ) -> RecoveryPolicy:

        return self.memory[fault_type][strategy]

    # =======================================================
    # Retrieve all
    # =======================================================

    def get_all_policies(

            self,

            fault_type

    ) -> List[RecoveryPolicy]:

        return list(

            self.memory[fault_type].values()

        )

    # =======================================================
    # Best policy
    # =======================================================

    def best_policy(

            self,

            fault_type

    ) -> RecoveryPolicy:

        return max(

            self.memory[fault_type].values(),

            key=lambda x: x.score

        )

    # =======================================================
    # Update
    # =======================================================

    def update_policy(

            self,

            fault_type,

            strategy,

            success,

            reward,

            mttr

    ):

        policy = self.get_policy(

            fault_type,

            strategy

        )

        policy.attempts += 1

        if success:

            policy.successes += 1

        else:

            policy.failures += 1

        # -------------------------
        # Average Reward
        # -------------------------

        if policy.attempts == 1:

            policy.average_reward = reward

        else:

            policy.average_reward = (

                (

                    policy.average_reward *

                    (policy.attempts - 1)

                )

                + reward

            ) / policy.attempts

        # -------------------------
        # Average MTTR
        # -------------------------

        if policy.attempts == 1:

            policy.average_mttr = mttr

        else:

            policy.average_mttr = (

                (

                    policy.average_mttr *

                    (policy.attempts - 1)

                )

                + mttr

            ) / policy.attempts

        # -------------------------
        # Confidence
        # -------------------------

        target = policy.success_rate

        policy.confidence = (

            0.8 * policy.confidence +

            0.2 * target

        )

        policy.confidence = max(

            MIN_CONFIDENCE,

            min(

                MAX_CONFIDENCE,

                policy.confidence

            )

        )

        policy.last_updated = time.time()

    # =======================================================
    # Ranking
    # =======================================================

    def rank_policies(

            self,

            fault_type

    ) -> List[RecoveryPolicy]:

        return sorted(

            self.memory[fault_type].values(),

            key=lambda x: x.score,

            reverse=True

        )

    # =======================================================
    # Statistics
    # =======================================================

    def statistics(self):

        faults = len(self.memory)

        strategies = 0

        attempts = 0

        successes = 0

        failures = 0

        for fault in self.memory.values():

            strategies += len(fault)

            for policy in fault.values():

                attempts += policy.attempts

                successes += policy.successes

                failures += policy.failures

        return {

            "Fault Types": faults,

            "Policies": strategies,

            "Attempts": attempts,

            "Successes": successes,

            "Failures": failures

        }

    # =======================================================
    # Save
    # =======================================================

    def save(

            self,

            filename

    ):

        data = {}

        for fault in self.memory:

            data[fault] = {}

            for strategy in self.memory[fault]:

                data[fault][strategy] = (

                    self.memory[fault][strategy].to_dict()

                )

        with open(filename, "w") as f:

            json.dump(

                data,

                f,

                indent=4

            )

    # =======================================================
    # Summary
    # =======================================================

    def print_summary(self):

        print("=" * 100)

        print("Knowledge Base")

        print("=" * 100)

        for fault in self.memory:

            print(f"\n{fault}")

            print("-" * 100)

            for policy in self.rank_policies(fault):

                print(

                    f"{policy.strategy:20}"

                    f" Score={policy.score:.3f}"

                    f" Conf={policy.confidence:.3f}"

                    f" Success={policy.success_rate:.2f}"

                    f" Attempts={policy.attempts:4}"

                    f" AvgMTTR={policy.average_mttr:.2f}"

                )


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    kb = KnowledgeBase()

    kb.register_fault(

        "SensorDrift",

        [

            "FastCalibration",

            "ReplaceSensor",

            "RedundantSensor"

        ]

    )

    kb.update_policy(

        "SensorDrift",

        "FastCalibration",

        success=True,

        reward=10,

        mttr=12

    )

    kb.update_policy(

        "SensorDrift",

        "FastCalibration",

        success=True,

        reward=10,

        mttr=10

    )

    kb.update_policy(

        "SensorDrift",

        "ReplaceSensor",

        success=False,

        reward=-5,

        mttr=35

    )

    kb.print_summary()

    print()

    print(kb.statistics())