"""
==========================================================
ResIoT Simulator

Module 12 : experiments.py

Author : Kaneez Fizza

Description
-----------
Runs all experiments for evaluating:

1. ResIoT
2. Rule-Based Baseline
3. ML-Based Baseline

Generates CSV-ready results that are later visualized
using plotting.py

==========================================================
"""

from pathlib import Path
import csv
from collections import defaultdict
import pandas as pd
from failures import FaultGenerator

from scenario import SimulationScenario
from environment import Environment
from baselines import RuleBasedBaseline, MLBasedBaseline


class ExperimentManager:

    def __init__(
        self,
        episodes=1000,
        seed=42,
        output_dir="outputs/csv"
    ):

        self.episodes = episodes
        self.seed = seed

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.scenario = SimulationScenario(
            episodes=episodes,
            seed=seed
        )

        self.results = defaultdict(list)

    # -------------------------------------------------

    def _save_csv(self, filename, rows):

        filepath = self.output_dir / filename

        if len(rows) == 0:
            return

        with open(filepath, "w", newline="") as f:

            writer = csv.DictWriter(
                f,
                fieldnames=list(rows[0].keys())
            )

            writer.writeheader()

            writer.writerows(rows)

        print(f"Saved {filepath}")

    def run_resiot(self):

        print("=" * 60)
        print("Running ResIoT")
        print("=" * 60)

        env = Environment()

        self.scenario.generate()

        rows = []

        for event in self.scenario:
            result = env.step(event.fault)

            rows.append({

                "Episode": event.episode,

                "Fault": event.fault.name,

                "Stage": event.fault.stage,

                "Success": result["success"],

                "MTTD": result["mttd"],

                "MTTR": result["mttr"],

                "Messages": result["messages"],

                "Confidence": result["confidence"]

            })

        self.results["ResIoT"] = rows

        self._save_csv(
            "resiot_results.csv",
            rows
        )

        return env.statistics()

    def run_rule_baseline(self):

        print("=" * 60)
        print("Running Rule-Based Baseline")
        print("=" * 60)

        baseline = RuleBasedBaseline()

        self.scenario.generate()

        rows = []

        for event in self.scenario:
            # Detect fault and obtain MTTD
            mttd = baseline.detect(event.fault)

            # Diagnose fault
            baseline.diagnose(event.fault)

            # Recover from fault
            result = baseline.recover(event.fault)

            rows.append({

                "Episode": event.episode,

                "Fault": event.fault.name,

                "Success": result["success"],

                "MTTD": mttd,

                "MTTR": result["mttr"],

                "Messages": result["messages"]

            })

        self.results["Rule"] = rows

        self._save_csv(
            "rule_results.csv",
            rows
        )

        return baseline.statistics()

    def run_ml_baseline(self):

        print("=" * 60)
        print("Running ML Baseline")
        print("=" * 60)

        baseline = MLBasedBaseline()

        self.scenario.generate()

        rows = []

        for event in self.scenario:
            # Detect fault and obtain MTTD
            mttd = baseline.detect(event.fault)

            # Diagnose fault
            baseline.diagnose(event.fault)

            # Recover from fault
            result = baseline.recover(event.fault)

            rows.append({

                "Episode": event.episode,

                "Fault": event.fault.name,

                "Success": result["success"],

                "MTTD": mttd,

                "MTTR": result["mttr"],

                "Messages": result["messages"]

            })

        self.results["ML"] = rows

        self._save_csv(
            "ml_results.csv",
            rows
        )

        return baseline.statistics()
    # ==========================================================
    # Learning Curve Experiment
    # ==========================================================

    def experiment_learning_curve(self):

        """
        Evaluates how the ResIoT agents improve over time.
        """

        print("=" * 60)
        print("Learning Curve Experiment")
        print("=" * 60)

        env = Environment()

        self.scenario.generate()

        rows = []

        episode = 0

        for event in self.scenario:

            result = env.step(event.fault)

            episode += 1

            confidence = result.get("confidence", 0)

            reward = max(0, 100 - result["mttr"])

            rows.append({

                "Episode": episode,

                "Confidence": confidence,

                "Reward": reward,

                "Success": int(result["success"])

            })

        self.results["LearningCurve"] = rows

        self._save_csv(

            "learning_curve.csv",

            rows

        )

        return rows
    # ==========================================================
    # Fault-wise Evaluation
    # ==========================================================

    def experiment_faultwise(self):

        """
        Evaluates recovery performance for each fault type.
        """

        print("=" * 60)
        print("Fault-wise Experiment")
        print("=" * 60)

        env = Environment()

        self.scenario.generate()

        rows = []

        for event in self.scenario:

            result = env.step(event.fault)

            rows.append({

                "Fault": event.fault.name,

                "Stage": event.fault.stage,

                "MTTR": result["mttr"],

                "Success": int(result["success"])

            })

        self.results["Faultwise"] = rows

        self._save_csv(

            "faultwise.csv",

            rows

        )

        return rows

    # ==========================================================
    # Communication Overhead Experiment
    # ==========================================================

    def experiment_communication_overhead(self):

        print("=" * 60)
        print("Communication Overhead Experiment")
        print("=" * 60)

        # --------------------------------------------------
        # Load experiment results
        # --------------------------------------------------

        resiot = pd.read_csv(
            self.output_dir / "resiot_results.csv"
        )

        rule = pd.read_csv(
            self.output_dir / "rule_results.csv"
        )

        ml = pd.read_csv(
            self.output_dir / "ml_results.csv"
        )

        # --------------------------------------------------
        # Calculate communication metrics
        # --------------------------------------------------

        rows = [

            {
                "Approach": "ResIoT",
                "Total Messages": resiot["Messages"].sum(),
                "Average Messages": resiot["Messages"].mean()
            },

            {
                "Approach": "Rule-Based",
                "Total Messages": rule["Messages"].sum(),
                "Average Messages": rule["Messages"].mean()
            },

            {
                "Approach": "ML-Based",
                "Total Messages": ml["Messages"].sum(),
                "Average Messages": ml["Messages"].mean()
            }

        ]

        # --------------------------------------------------
        # Save results
        # --------------------------------------------------

        self.results["Communication Overhead"] = rows

        self._save_csv(
            "communication_overhead.csv",
            rows
        )

        return rows
    # ==========================================================
    # Scalability
    # ==========================================================

    def experiment_scalability(self):

        print("=" * 60)
        print("Scalability Experiment")
        print("=" * 60)

        device_counts = [
            100,
            500,
            1000,
            2500,
            5000
        ]

        rows = []

        # Number of fault events evaluated at each scale
        episodes_per_scale = 1000

        for num_devices in device_counts:

            # ------------------------------------------
            # Create a fresh environment for each scale
            # ------------------------------------------

            env = Environment()

            # ------------------------------------------
            # Load factor
            #
            # 100 devices  -> 1.00
            # 500 devices  -> 1.08
            # 1000 devices -> 1.18
            # 2500 devices -> 1.48
            # 5000 devices -> 1.98
            # ------------------------------------------

            load_factor = 1.0 + (
                    (num_devices - 100) / 5000.0
            )

            mttr_values = []
            mttd_values = []
            message_values = []
            success_values = []

            # ------------------------------------------
            # Generate faults for this deployment scale
            # ------------------------------------------

            fault_generator = FaultGenerator()

            for episode in range(
                    episodes_per_scale
            ):
                fault = (
                    fault_generator.generate_fault()
                )

                result = env.step(
                    fault
                )

                # --------------------------------------
                # Apply scale-dependent system load
                # --------------------------------------

                scaled_mttr = (
                        result["mttr"]
                        * load_factor
                )

                scaled_mttd = (
                        result["mttd"]
                        * (
                                1.0
                                + 0.30
                                * (load_factor - 1.0)
                        )
                )

                scaled_messages = int(
                    result["messages"]
                    * load_factor
                )

                # --------------------------------------
                # Store episode results
                # --------------------------------------

                mttr_values.append(
                    scaled_mttr
                )

                mttd_values.append(
                    scaled_mttd
                )

                message_values.append(
                    scaled_messages
                )

                success_values.append(
                    result["success"]
                )

            # ------------------------------------------
            # Aggregate results for this scale
            # ------------------------------------------

            rows.append({

                "Devices":
                    num_devices,

                "Average MTTR":
                    sum(mttr_values)
                    / len(mttr_values),

                "Average MTTD":
                    sum(mttd_values)
                    / len(mttd_values),

                "Average Messages":
                    sum(message_values)
                    / len(message_values),

                "Success Rate":
                    sum(success_values)
                    / len(success_values)

            })

            print(
                f"Devices: {num_devices} | "
                f"MTTR: {rows[-1]['Average MTTR']:.3f} | "
                f"MTTD: {rows[-1]['Average MTTD']:.3f} | "
                f"Messages: {rows[-1]['Average Messages']:.3f} | "
                f"Success: {rows[-1]['Success Rate']:.3f}"
            )

        # ----------------------------------------------
        # Save results
        # ----------------------------------------------

        self._save_csv(
            "scalability.csv",
            rows
        )

        return rows
    # ======================================================
    # Compare All Approaches
    # ======================================================

        # ======================================================
        # Compare All Approaches
        # ======================================================

    def compare_all(self):

            print("=" * 70)
            print("Comparative Evaluation")
            print("=" * 70)

            # Ensure fresh results exist
            #self.run_resiot()
            #self.run_rule_baseline()
            #self.run_ml_baseline()

            # Load experiment results
            resiot = pd.read_csv(
                self.output_dir / "resiot_results.csv"
            )

            rule = pd.read_csv(
                self.output_dir / "rule_results.csv"
            )

            ml = pd.read_csv(
                self.output_dir / "ml_results.csv"
            )

            # --------------------------------------------------
            # Validate required columns
            # --------------------------------------------------

            for name, df in [
                ("ResIoT", resiot),
                ("Rule-Based", rule),
                ("ML-Based", ml)
            ]:

                required_columns = [
                    "MTTD",
                    "MTTR",
                    "Success",
                    "Messages"
                ]

                missing = [
                    column
                    for column in required_columns
                    if column not in df.columns
                ]

                if missing:
                    raise ValueError(
                        f"{name} results are missing columns: {missing}"
                    )

            # --------------------------------------------------
            # Comparative Metrics
            # --------------------------------------------------

            comparison = [

                {
                    "Approach": "ResIoT",
                    "Mean MTTD": resiot["MTTD"].mean(),
                    "Mean MTTR": resiot["MTTR"].mean(),
                    "Success Rate": resiot["Success"].mean(),
                    "Messages": resiot["Messages"].mean()
                },

                {
                    "Approach": "Rule-Based",
                    "Mean MTTD": rule["MTTD"].mean(),
                    "Mean MTTR": rule["MTTR"].mean(),
                    "Success Rate": rule["Success"].mean(),
                    "Messages": rule["Messages"].mean()
                },

                {
                    "Approach": "ML-Based",
                    "Mean MTTD": ml["MTTD"].mean(),
                    "Mean MTTR": ml["MTTR"].mean(),
                    "Success Rate": ml["Success"].mean(),
                    "Messages": ml["Messages"].mean()
                }

            ]

            # --------------------------------------------------
            # Store Results
            # --------------------------------------------------

            self.results["Comparison"] = comparison

            self._save_csv(
                "comparison.csv",
                comparison
            )

            # --------------------------------------------------
            # Print Comparison
            # --------------------------------------------------

            print("\nComparison Results")

            for row in comparison:
                print(
                    f"{row['Approach']:12} | "
                    f"MTTD={row['Mean MTTD']:.3f} | "
                    f"MTTR={row['Mean MTTR']:.3f} | "
                    f"Success={row['Success Rate']:.3f} | "
                    f"Messages={row['Messages']:.3f}"
                )

            return comparison

        # ======================================================
        # Learning Summary
        # ======================================================

    def learning_summary(self):

            rows = self.results.get(
                "LearningCurve",
                []
            )

            if len(rows) == 0:
                return {}

            confidence = [
                r["Confidence"]
                for r in rows
            ]

            reward = [
                r["Reward"]
                for r in rows
            ]

            success = [
                r["Success"]
                for r in rows
            ]

            return {
                "Average Confidence":
                    sum(confidence) / len(confidence),

                "Average Reward":
                    sum(reward) / len(reward),

                "Success Rate":
                    sum(success) / len(success)
            }

        # ======================================================
        # Print Summary
        # ======================================================

    def print_summary(self):

            print()

            print("=" * 70)

            print("Experiment Summary")

            print("=" * 70)

            for experiment, rows in self.results.items():
                print(
                    f"{experiment:<30}"
                    f"{len(rows):>8} records"
                )

        # ======================================================
        # Export Summary
        # ======================================================

    def export_summary(self):

            rows = []

            for name, data in self.results.items():
                rows.append({
                    "Experiment": name,
                    "Records": len(data)
                })

            self._save_csv(
                "summary.csv",
                rows
            )

        # ======================================================
        # Run All Experiments
        # ======================================================

    def run_all(self):

            print("\nRunning ResIoT...")
            self.run_resiot()

            print("\nRunning Rule-Based Baseline...")
            self.run_rule_baseline()

            print("\nRunning ML Baseline...")
            self.run_ml_baseline()

            print("\nRunning Learning Curve...")
            self.experiment_learning_curve()

            print("\nRunning Fault-wise Evaluation...")
            self.experiment_faultwise()

            print("\nRunning Communication Overhead...")
            self.experiment_communication_overhead()

            print("\nRunning Scalability...")
            self.experiment_scalability()

            print("\nGenerating Comparison...")
            self.compare_all()

            print("\nExporting Summary...")
            self.export_summary()

            print("\nFinished.")

    # ==========================================================
    # Main
    # ==========================================================

    if __name__ == "__main__":
        manager = ExperimentManager(
            episodes=1000,
            seed=42
        )
        manager.run_all()