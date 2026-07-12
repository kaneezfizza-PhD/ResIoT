"""
==========================================================
ResIoT Simulator

Module 8 : communication.py

Author : Kaneez Fizza

Description
-----------
Implements communication among Functional Agents.

This module provides:

• Message
• MessageBus
• AgentRegistry
• CommunicationManager

==========================================================
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import time


# ==========================================================
# Message
# ==========================================================

@dataclass
class Message:
    """
    Generic message exchanged between agents.
    """

    sender: str
    receiver: str

    performative: str

    fault_type: str = ""

    content: Dict[str, Any] = field(default_factory=dict)

    timestamp: float = field(default_factory=time.time)

    priority: int = 1


# ==========================================================
# Agent Registry
# ==========================================================

class AgentRegistry:
    """
    Stores references to all agents.
    """

    def __init__(self):

        self.agents = {}

    # ------------------------------------------------------

    def register(self, agent):

        self.agents[agent.name] = agent

    # ------------------------------------------------------

    def unregister(self, name):

        if name in self.agents:

            del self.agents[name]

    # ------------------------------------------------------

    def get(self, name):

        return self.agents.get(name)

    # ------------------------------------------------------

    def all_agents(self):

        return list(self.agents.values())


# ==========================================================
# Message Bus
# ==========================================================

class MessageBus:
    """
    Central communication channel.

    Responsible for routing messages between agents.
    """

    def __init__(self):

        self.queue: List[Message] = []

        self.total_messages = 0

    # ------------------------------------------------------

    def send(self, message: Message):

        self.queue.append(message)

        self.total_messages += 1

    # ------------------------------------------------------

    def broadcast(

        self,

        sender,

        receivers,

        performative,

        fault_type="",

        content=None

    ):

        if content is None:

            content = {}

        for receiver in receivers:

            self.send(

                Message(

                    sender=sender,

                    receiver=receiver,

                    performative=performative,

                    fault_type=fault_type,

                    content=content

                )

            )

    # ------------------------------------------------------

    def pending(self):

        return len(self.queue)

    # ------------------------------------------------------

    def statistics(self):

        return {

            "Messages": self.total_messages,

            "Pending": len(self.queue)

        }


# ==========================================================
# Communication Manager
# ==========================================================

class CommunicationManager:
    """
    Delivers queued messages.
    """

    def __init__(

        self,

        registry: AgentRegistry,

        bus: MessageBus

    ):

        self.registry = registry

        self.bus = bus

        self.delivered = 0

        self.failed = 0

    # ------------------------------------------------------

    def deliver(self):

        while self.bus.queue:

            msg = self.bus.queue.pop(0)

            receiver = self.registry.get(

                msg.receiver

            )

            if receiver is None:

                self.failed += 1

                continue

            receiver.receive(msg)

            self.delivered += 1

    # ------------------------------------------------------

    def statistics(self):

        return {

            "Delivered": self.delivered,

            "Failed": self.failed

        }


# ==========================================================
# Message Types
# ==========================================================

REQUEST = "REQUEST"

INFORM = "INFORM"

PROPOSE = "PROPOSE"

APPROVE = "APPROVE"

REJECT = "REJECT"

FAILURE = "FAILURE"

SUCCESS = "SUCCESS"


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    class DummyAgent:

        def __init__(self, name):

            self.name = name

        def receive(self, msg):

            print(

                f"{self.name} received",

                msg.performative,

                "from",

                msg.sender

            )

    registry = AgentRegistry()

    bus = MessageBus()

    manager = CommunicationManager(

        registry,

        bus

    )

    a1 = DummyAgent("AS1")

    a2 = DummyAgent("AS2")

    oa = DummyAgent("OA")

    registry.register(a1)

    registry.register(a2)

    registry.register(oa)

    bus.send(

        Message(

            sender="AS1",

            receiver="OA",

            performative=PROPOSE,

            fault_type="SensorDrift",

            content={

                "strategy":"Calibration"

            }

        )

    )

    bus.broadcast(

        sender="OA",

        receivers=["AS1","AS2"],

        performative=APPROVE,

        fault_type="SensorDrift",

        content={

            "strategy":"Calibration"

        }

    )

    manager.deliver()

    print()

    print(bus.statistics())

    print(manager.statistics())