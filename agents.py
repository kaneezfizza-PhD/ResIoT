"""agents.py
Core agent implementations for ResIoT.
"""

import random
from abc import ABC

from communication import Message
from agent_learning import AgentLearning

class FunctionalAgent(ABC):
    def __init__(self, name, knowledge_base):
        self.name = name
        self.kb = knowledge_base
        self.learning = AgentLearning(self.name)
        self.received_messages = []
        self.success = 0
        self.failures = 0

    def perceive(self, fault):
        return fault

    def reason(self, fault):

        return self.learning.choose_policy(

            self.kb,

            fault.name

        )

    def plan(self, strategy):
        return {
            "strategy": getattr(strategy, "name", str(strategy)),
            "confidence": getattr(strategy, "confidence", 0.8)
        }

    def execute(self, fault, plan):
        success = random.random() < plan["confidence"]
        mttr = random.randint(8,20) if success else random.randint(20,40)
        if success:
            self.success += 1
        else:
            self.failures += 1
        return success, mttr

    def learn(self, fault, policy, success, mttr):
        """
        Update the shared Knowledge Base through the
        AgentLearning module.
        """

        self.learning.learn(

            kb=self.kb,

            fault_type=fault.name,

            policy=policy,

            success=success,

            mttr=mttr

        )

    def receive(self, message: Message):
        self.received_messages.append(message)

    def statistics(self):
        total = self.success + self.failures
        return {
            "agent": self.name,
            "success": self.success,
            "failures": self.failures,
            "success_rate": self.success/total if total else 0,
            "messages_received": len(self.received_messages)
        }

class AS1SensingAgent(FunctionalAgent):
    def __init__(self, kb):
        super().__init__("AS1", kb)

class AS2TransmissionAgent(FunctionalAgent):
    def __init__(self, kb):
        super().__init__("AS2", kb)

class AS3AnalyticsAgent(FunctionalAgent):
    def __init__(self, kb):
        super().__init__("AS3", kb)

class AS4InformationAgent(FunctionalAgent):
    def __init__(self, kb):
        super().__init__("AS4", kb)

class AS5ActuationAgent(FunctionalAgent):
    def __init__(self, kb):
        super().__init__("AS5", kb)
