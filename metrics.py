"""
==========================================================
ResIoT Simulator

Module 9 : metrics.py

Author : Kaneez Fizza

Description
-----------
Stores and computes all evaluation metrics used
throughout the simulator.

The same Metrics class is shared by

• ResIoT
• Rule-Based Baseline
• ML Baseline

==========================================================
"""

from collections import defaultdict
import statistics


class Metrics:

    def __init__(self):

        # --------------------------------------------------
        # Detection / Recovery
        # --------------------------------------------------

        self.mttd = []

        self.mttr = []

        self.total_recovery = []

        # --------------------------------------------------
        # Learning
        # --------------------------------------------------

        self.learning_curve = []

        self.policy_confidence = []

        self.rewards = []

        # --------------------------------------------------
        # Success
        # --------------------------------------------------

        self.success = 0

        self.failure = 0

        # --------------------------------------------------
        # Communication
        # --------------------------------------------------

        self.messages = []

        self.communication_delay = []

        # --------------------------------------------------
        # Resource Usage
        # --------------------------------------------------

        self.cpu_usage = []

        self.memory_usage = []

        # --------------------------------------------------
        # Fault Statistics
        # --------------------------------------------------

        self.fault_counter = defaultdict(int)

        self.fault_success = defaultdict(int)

        # --------------------------------------------------
        # Scalability
        # --------------------------------------------------

        self.scalability = {}

    # ======================================================
    # Detection
    # ======================================================

    def record_detection(self, time):

        self.mttd.append(time)

    # ======================================================
    # Recovery
    # ======================================================

    def record_recovery(self, time):

        self.mttr.append(time)

        self.total_recovery.append(time)

    # ======================================================
    # Learning
    # ======================================================

    def record_learning(

        self,

        confidence,

        reward

    ):

        self.policy_confidence.append(confidence)

        self.rewards.append(reward)

    # ======================================================
    # Success
    # ======================================================

    def record_success(

        self,

        fault_type

    ):

        self.success += 1

        self.fault_counter[fault_type] += 1

        self.fault_success[fault_type] += 1

    # ======================================================

    def record_failure(

        self,

        fault_type

    ):

        self.failure += 1

        self.fault_counter[fault_type] += 1

    # ======================================================
    # Communication
    # ======================================================

    def record_message(

        self,

        count=1

    ):

        self.messages.append(count)

    # ======================================================

    def record_delay(

        self,

        delay

    ):

        self.communication_delay.append(delay)

    # ======================================================
    # Resources
    # ======================================================

    def record_cpu(

        self,

        cpu

    ):

        self.cpu_usage.append(cpu)

    # ======================================================

    def record_memory(

        self,

        memory

    ):

        self.memory_usage.append(memory)

    # ======================================================
    # Scalability
    # ======================================================

    def record_scalability(

        self,

        devices,

        recovery_time

    ):

        self.scalability[devices] = recovery_time

    # ======================================================
    # Mean
    # ======================================================

    @staticmethod
    def mean(values):

        if len(values) == 0:

            return 0

        return statistics.mean(values)

    # ======================================================
    # Success Rate
    # ======================================================

    @property
    def success_rate(self):

        total = self.success + self.failure

        if total == 0:

            return 0

        return self.success / total

    # ======================================================
    # Fault Success
    # ======================================================

    def fault_success_rate(

        self,

        fault

    ):

        if self.fault_counter[fault] == 0:

            return 0

        return (

            self.fault_success[fault]

            /

            self.fault_counter[fault]

        )

    # ======================================================
    # Summary
    # ======================================================

    def summary(self):

        return {

            "Mean MTTD":

                self.mean(self.mttd),

            "Mean MTTR":

                self.mean(self.mttr),

            "Recovery Time":

                self.mean(self.total_recovery),

            "Success Rate":

                self.success_rate,

            "Average Reward":

                self.mean(self.rewards),

            "Average Confidence":

                self.mean(self.policy_confidence),

            "Messages":

                sum(self.messages),

            "Communication Delay":

                self.mean(

                    self.communication_delay

                ),

            "CPU":

                self.mean(self.cpu_usage),

            "Memory":

                self.mean(self.memory_usage)

        }

    # ======================================================
    # Pretty Print
    # ======================================================

    def print_summary(self):

        print()

        print("=" * 70)

        print("Simulation Metrics")

        print("=" * 70)

        summary = self.summary()

        for key, value in summary.items():

            if isinstance(value, float):

                print(

                    f"{key:30}"

                    f"{value:.2f}"

                )

            else:

                print(

                    f"{key:30}"

                    f"{value}"

                )

    # ======================================================
    # Reset
    # ======================================================

    def reset(self):

        self.__init__()


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    metrics = Metrics()

    metrics.record_detection(12)

    metrics.record_detection(10)

    metrics.record_detection(16)

    metrics.record_recovery(18)

    metrics.record_recovery(12)

    metrics.record_recovery(15)

    metrics.record_success("SensorDrift")

    metrics.record_success("SensorDrift")

    metrics.record_failure("SensorDrift")

    metrics.record_learning(

        confidence=0.82,

        reward=74

    )

    metrics.record_learning(

        confidence=0.91,

        reward=81

    )

    metrics.record_message(5)

    metrics.record_message(8)

    metrics.record_cpu(14)

    metrics.record_cpu(16)

    metrics.record_memory(128)

    metrics.record_memory(132)

    metrics.record_delay(5)

    metrics.record_delay(7)

    metrics.record_scalability(

        100,

        22

    )

    metrics.record_scalability(

        500,

        26

    )

    metrics.print_summary()