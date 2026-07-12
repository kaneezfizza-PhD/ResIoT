
"""
plotting.py
ResIoT Simulator - Module 13

Loads CSV outputs produced by experiments.py and generates
publication-ready figures.

Dependencies:
    pandas
    matplotlib
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


class PlotManager:

    def __init__(
        self,
        csv_dir="outputs/csv",
        fig_dir="outputs/figures"
    ):
        self.csv_dir = Path(csv_dir)
        self.fig_dir = Path(fig_dir)
        self.fig_dir.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------

    def _load(self, filename):
        path = self.csv_dir / filename
        if not path.exists():
            print(f"Missing: {path}")
            return None
        return pd.read_csv(path)

    # -------------------------------------------------

    def _save(self, name):
        outfile = self.fig_dir / name
        plt.tight_layout()
        plt.savefig(outfile, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"Saved {outfile}")

    # -------------------------------------------------

    def plot_learning_curve(self):
        df = self._load("learning_curve.csv")
        if df is None:
            return

        plt.figure(figsize=(8,4))
        plt.plot(df["Episode"], df["Confidence"], label="Confidence")
        plt.xlabel("Episode")
        plt.ylabel("Confidence")
        plt.title("Learning Curve")
        plt.grid(True)
        plt.legend()
        self._save("learning_curve.png")

    # -------------------------------------------------

    def plot_mttr(self):
        df = self._load("comparison.csv")
        if df is None:
            return

        plt.figure(figsize=(6,4))
        plt.bar(df["Approach"], df["Mean MTTR"])
        plt.ylabel("MTTR")
        plt.title("Mean Time To Recovery")
        self._save("mttr_comparison.png")

    # -------------------------------------------------

    def plot_mttd(self):

        df = self._load("comparison.csv")

        if df is None:
            return

        print("\nDEBUG: comparison.csv")
        print(df)
        print("\nColumns:", df.columns.tolist())
        print("\nMean MTTD values:")
        print(df["Mean MTTD"])

        plt.figure(figsize=(6, 4))

        plt.bar(
            df["Approach"],
            df["Mean MTTD"]
        )

        plt.ylabel("MTTD")
        plt.title("Mean Time To Detect")

        self._save("mttd_comparison.png")
    # -------------------------------------------------

    def plot_success_rate(self):
        df = self._load("comparison.csv")
        if df is None:
            return

        plt.figure(figsize=(6,4))
        plt.bar(df["Approach"], df["Success Rate"])
        plt.ylabel("Success Rate")
        plt.ylim(0,1)
        plt.title("Recovery Success Rate")
        self._save("success_rate.png")

    # -------------------------------------------------

    def plot_overhead(self):

        df = self._load("communication_overhead.csv")

        if df is None:
            return

        plt.figure(figsize=(7, 5))

        bars = plt.bar(
            df["Approach"],
            df["Average Messages"]
        )

        plt.xlabel("Approach")
        plt.ylabel("Average Messages per Fault")
        plt.title("Communication Overhead Comparison")
        plt.grid(axis="y", alpha=0.3)

        # Add numerical values above bars
        for bar in bars:
            height = bar.get_height()

            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{height:.2f}",
                ha="center",
                va="bottom"
            )

        self._save("communication_overhead.png")

    # -------------------------------------------------

    def plot_scalability(self):
        df = self._load("scalability.csv")
        if df is None:
            return

        plt.figure(figsize=(6,4))
        plt.plot(df["Devices"], df["Average MTTR"], marker="o")
        plt.xlabel("Number of Devices")
        plt.ylabel("Average MTTR")
        plt.title("Scalability Analysis")
        plt.grid(True)
        self._save("scalability.png")

    # -------------------------------------------------

    def plot_faultwise(self):
        df = self._load("faultwise.csv")
        if df is None:
            return

        summary = df.groupby("Fault")["Success"].mean().sort_values()

        plt.figure(figsize=(8,4))
        plt.bar(summary.index, summary.values)
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Success Rate")
        plt.ylim(0,1)
        plt.title("Fault-wise Recovery Success")
        self._save("faultwise_success.png")

    # -------------------------------------------------

    def plot_comparison(self):
        df = self._load("comparison.csv")
        if df is None:
            return

        fig, ax = plt.subplots(figsize=(8,4))
        width = 0.35
        x = range(len(df))

        ax.bar([i-width/2 for i in x], df["Mean MTTD"], width, label="MTTD")
        ax.bar([i+width/2 for i in x], df["Mean MTTR"], width, label="MTTR")

        ax.set_xticks(list(x))
        ax.set_xticklabels(df["Approach"])
        ax.set_ylabel("Time")
        ax.set_title("Overall Comparison")
        ax.legend()

        self._save("overall_comparison.png")

    # -------------------------------------------------

    def plot_all(self):
        self.plot_learning_curve()
        self.plot_mttd()
        self.plot_mttr()
        self.plot_success_rate()
        self.plot_overhead()
        self.plot_scalability()
        self.plot_faultwise()
        self.plot_comparison()


if __name__ == "__main__":

    plotter = PlotManager()
    plotter.plot_all()
