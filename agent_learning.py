"""
==========================================================
ResIoT Simulator

Module 4 : agent_learning.py

Author : Kaneez Fizza

Description
-----------
Learning module owned by each Functional Agent.

Implements experience-based continual learning using
epsilon-greedy exploration.

Each Functional Agent owns one AgentLearning object.

==========================================================
"""

import random

from knowledge_base import KnowledgeBase, RecoveryPolicy

from config import (
    LEARNING_RATE,
    EPSILON,
    EPSILON_DECAY,
    MIN_EPSILON
)


class AgentLearning:
    """
    Learning engine owned by ONE Functional Agent.

    Responsibilities

    • choose recovery strategy
    • evaluate outcome
    • update KB
    • gradually reduce exploration
    """

    def __init__(self, agent_name: str):

        self.agent_name = agent_name

        self.epsilon = EPSILON

        self.total_decisions = 0

        self.total_successes = 0

        self.total_failures = 0

        self.learning_history = []

    # ======================================================
    # Choose Recovery Policy
    # ======================================================

    def choose_policy(

        self,

        kb: KnowledgeBase,

        fault_type: str

    ) -> RecoveryPolicy:

        policies = kb.rank_policies(fault_type)

        # --------------------------------------------
        # Exploration
        # --------------------------------------------

        if random.random() < self.epsilon:

            policy = random.choice(policies)

        # --------------------------------------------
        # Exploitation
        # --------------------------------------------

        else:

            policy = policies[0]

        self.total_decisions += 1

        return policy

    # ======================================================
    # Learn
    # ======================================================

    def learn(

        self,

        kb: KnowledgeBase,

        fault_type: str,

        policy: RecoveryPolicy,

        success: bool,

        mttr: float

    ):

        if success:

            reward = self.compute_reward(

                success=True,

                mttr=mttr

            )

            self.total_successes += 1

        else:

            reward = self.compute_reward(

                success=False,

                mttr=mttr

            )

            self.total_failures += 1

        kb.update_policy(

            fault_type=fault_type,

            strategy=policy.strategy,

            success=success,

            reward=reward,

            mttr=mttr

        )

        self.learning_history.append({

            "fault": fault_type,

            "strategy": policy.strategy,

            "success": success,

            "reward": reward,

            "mttr": mttr,

            "epsilon": self.epsilon

        })

        self.decay()

    # ======================================================
    # Reward Function
    # ======================================================

    def compute_reward(

        self,

        success,

        mttr

    ):

        """
        Faster recovery receives higher reward.
        """

        if success:

            reward = 100 - mttr

        else:

            reward = -50 - mttr

        return reward

    # ======================================================
    # Decay Exploration
    # ======================================================

    def decay(self):

        self.epsilon *= EPSILON_DECAY

        if self.epsilon < MIN_EPSILON:

            self.epsilon = MIN_EPSILON

    # ======================================================
    # Statistics
    # ======================================================

    @property
    def success_rate(self):

        if self.total_decisions == 0:

            return 0

        return self.total_successes / self.total_decisions

    # ======================================================

    @property
    def failure_rate(self):

        if self.total_decisions == 0:

            return 0

        return self.total_failures / self.total_decisions

    # ======================================================

    def statistics(self):

        return {

            "Agent": self.agent_name,

            "Decisions": self.total_decisions,

            "Successes": self.total_successes,

            "Failures": self.total_failures,

            "Success Rate": self.success_rate,

            "Current Epsilon": self.epsilon

        }

    # ======================================================

    def print_statistics(self):

        stats = self.statistics()

        print("=" * 60)

        print(self.agent_name)

        print("=" * 60)

        for k, v in stats.items():

            print(f"{k:20}: {v}")

    # ======================================================

    def reset(self):

        self.total_decisions = 0

        self.total_successes = 0

        self.total_failures = 0

        self.learning_history.clear()

        self.epsilon = EPSILON