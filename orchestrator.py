"""
==========================================================
ResIoT Simulator

Module 6 : orchestrator.py

Author : Kaneez Fizza

Description
-----------
Implements the Orchestrator Agent (OA).

The Orchestrator is responsible for

• Coordinating Functional Agents
• Receiving recovery plans
• Resolving conflicting plans
• Selecting the highest priority plan
• Broadcasting approved plans
• Collecting system-wide statistics

Unlike Functional Agents,
the Orchestrator DOES NOT LEARN.

==========================================================
"""

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from communication import Message


# ==========================================================
# Recovery Plan
# ==========================================================

@dataclass
class RecoveryPlan:

    sender: str

    fault_type: str

    strategy: str

    confidence: float

    priority: int = 1

    timestamp: float = field(default_factory=time.time)

    metadata: Dict = field(default_factory=dict)


# ==========================================================
# Orchestrator
# ==========================================================

class Orchestrator:

    """
    Global coordinator.

    Responsibilities

    • Receive plans from agents

    • Resolve conflicts

    • Select best recovery plan

    • Broadcast decision

    • Maintain statistics
    """

    def __init__(self):

        self.plan_queue: List[RecoveryPlan] = []

        self.broadcast_queue: List[Message] = []

        self.total_plans = 0

        self.total_conflicts = 0

        self.total_approved = 0

    # ======================================================
    # Receive Plan
    # ======================================================

    def receive_plan(

        self,

        plan: RecoveryPlan

    ):

        self.plan_queue.append(plan)

        self.total_plans += 1

    # ======================================================
    # Resolve Conflict
    # ======================================================

    def resolve_conflicts(

        self

    ) -> Optional[RecoveryPlan]:

        """
        Conflict resolution strategy

        1. Highest confidence

        2. Highest priority

        3. Earliest submission
        """

        if len(self.plan_queue) == 0:

            return None

        if len(self.plan_queue) > 1:

            self.total_conflicts += 1

        best = sorted(

            self.plan_queue,

            key=lambda p: (

                p.confidence,

                p.priority,

                -p.timestamp

            ),

            reverse=True

        )[0]

        self.plan_queue.clear()

        self.total_approved += 1

        return best

    # ======================================================
    # Broadcast Approved Plan
    # ======================================================

    def broadcast(

        self,

        receivers: List[str],

        approved_plan: RecoveryPlan

    ):

        self.broadcast_queue.clear()

        for receiver in receivers:

            msg = Message(

                sender="OA",

                receiver=receiver,

                fault_type=approved_plan.fault_type,

                payload={

                    "strategy": approved_plan.strategy,

                    "confidence": approved_plan.confidence,

                    "priority": approved_plan.priority

                }

            )

            self.broadcast_queue.append(msg)

    # ======================================================
    # Retrieve Messages
    # ======================================================

    def get_messages(self):

        messages = self.broadcast_queue.copy()

        self.broadcast_queue.clear()

        return messages

    # ======================================================
    # Statistics
    # ======================================================

    def statistics(self):

        return {

            "Plans Received": self.total_plans,

            "Conflicts": self.total_conflicts,

            "Approved": self.total_approved

        }

    # ======================================================
    # Reset
    # ======================================================

    def reset(self):

        self.plan_queue.clear()

        self.broadcast_queue.clear()

        self.total_plans = 0

        self.total_conflicts = 0

        self.total_approved = 0


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    oa = Orchestrator()

    p1 = RecoveryPlan(

        sender="AS1",

        fault_type="SensorDrift",

        strategy="Calibration",

        confidence=0.83,

        priority=2

    )

    p2 = RecoveryPlan(

        sender="AS3",

        fault_type="SensorDrift",

        strategy="ReplaceSensor",

        confidence=0.91,

        priority=1

    )

    p3 = RecoveryPlan(

        sender="AS5",

        fault_type="SensorDrift",

        strategy="RedundantSensor",

        confidence=0.75,

        priority=3

    )

    oa.receive_plan(p1)

    oa.receive_plan(p2)

    oa.receive_plan(p3)

    best = oa.resolve_conflicts()

    print()

    print("Approved Plan")

    print("----------------")

    print(best)

    oa.broadcast(

        ["AS1", "AS2", "AS3", "AS4", "AS5"],

        best

    )

    print()

    print("Broadcast Messages")

    print("------------------")

    for msg in oa.get_messages():

        print(msg)

    print()

    print("Statistics")

    print("----------------")

    print(oa.statistics())