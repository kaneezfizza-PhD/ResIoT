import random
import time
from typing import List, Dict, Tuple

# --- Configuration and Knowledge Base ---

# Define the types of failures and their complexity/detection latency
FAILURE_TYPES: Dict[str, Tuple[int, int, str]] = {
    "SENSOR_DRIFT": (45, 120, "Slow, subtle anomaly in S1. High diagnosis complexity."),
    "COMM_LOSS": (5, 30, "Fast, clear failure in S2. Medium diagnosis complexity."),
    "ACTUATOR_FAULT": (60, 180, "Immediate S5 failure, requires complex recalibration.")
}

# Knowledge Base (Simulated LLM/Agentic Reasoning)
# Mapping of Failure Type -> Optimal Fix Path, represented by required steps (complexity)
AGENTIC_KNOWLEDGE: Dict[str, Dict[str, int]] = {
    "SENSOR_DRIFT": {"A_S1": 10, "A_S3": 5, "A_S5": 20}, # Low steps needed due to accurate root cause analysis (A_S3)
    "COMM_LOSS": {"A_S2": 15, "A_S4": 5}, # Fast resolution via dynamic rerouting (A_S2)
    "ACTUATOR_FAULT": {"A_S3": 5, "A_S5": 10} # Fast plan generation and local recalibration (A_S5)
}

# Rules Base (Simulated Traditional RBS)
# Mapping of Failure Type -> Fixed, often redundant, steps needed (high total complexity)
RBS_RULES: Dict[str, Dict[str, int]] = {
    "SENSOR_DRIFT": {"Check_S1": 20, "Check_S2": 20, "Human_Triage": 40, "Act_S5": 50}, # Slow manual triage process
    "COMM_LOSS": {"Check_S2": 30, "Restart_Gateway": 40, "Failover": 10}, # Pre-defined, slow failover
    "ACTUATOR_FAULT": {"Reset_S5": 20, "Human_Override": 60, "Restart_System": 80} # Slow, general system restart required
}

# --- Core Simulation Functions ---

def simulate_detection(failure_type: str, system_type: str) -> int:
    """
    Simulates the time taken to detect a failure.
    Agentic AI uses proactive monitoring (lower latency).
    RBS uses reactive threshold alerting (higher latency).
    Returns detection time in seconds.
    """
    T_min, T_max, _ = FAILURE_TYPES[failure_type]

    if system_type == "AAS":
        # Agentic AI: Proactive A_S1 monitoring reduces detection time significantly
        return random.randint(T_min // 2, T_max // 2)
    else: # RBS
        # Rule-Based System: Depends on exceeding static thresholds (longer time)
        return random.randint(T_min, T_max)

def simulate_resolution(failure_type: str, system_type: str) -> int:
    """
    Simulates the time taken to resolve an incident (MTTR).
    Agentic AI uses autonomous, specialized planning (lower steps).
    RBS uses fixed, often redundant, procedures (higher steps).
    Returns resolution time in seconds (total steps * time per step).
    """
    steps_to_resolve: Dict[str, int]

    if system_type == "AAS":
        steps_to_resolve = AGENTIC_KNOWLEDGE[failure_type]
        # Agentic AI: Each step is faster due to specialization (simulated as 1 second per step)
        step_time = 1
    else: # RBS
        steps_to_resolve = RBS_RULES[failure_type]
        # RBS: Each step is slower due to manual checks/restarts (simulated as 2 seconds per step)
        step_time = 2

    # Total resolution time is the sum of all step complexities * step time
    total_steps = sum(steps_to_resolve.values())
    return total_steps * step_time

def run_simulation(num_runs: int = 100) -> Dict[str, Dict[str, List[int]]]:
    """
    Runs the full simulation for both AAS and RBS across various failure types.
    """
    results: Dict[str, Dict[str, List[int]]] = {
        "AAS": {"MTTD": [], "MTTR": []},
        "RBS": {"MTTD": [], "MTTR": []}
    }

    failure_list = list(FAILURE_TYPES.keys())

    for _ in range(num_runs):
        failure = random.choice(failure_list)

        # Agentic AI System (AAS)
        mttd_aas = simulate_detection(failure, "AAS")
        mttr_aas = simulate_resolution(failure, "AAS")
        results["AAS"]["MTTD"].append(mttd_aas)
        results["AAS"]["MTTR"].append(mttr_aas)

        # Rule-Based System (RBS)
        mttd_rbs = simulate_detection(failure, "RBS")
        mttr_rbs = simulate_resolution(failure, "RBS")
        results["RBS"]["MTTD"].append(mttd_rbs)
        results["RBS"]["MTTR"].append(mttr_rbs)

    return results

def calculate_average_metrics(results: Dict[str, Dict[str, List[int]]]) -> Dict[str, Dict[str, float]]:
    """
    Calculates the mean MTTD and MTTR for each system type.
    """
    averages: Dict[str, Dict[str, float]] = {}
    for system, metrics in results.items():
        averages[system] = {
            "MTTD": sum(metrics["MTTD"]) / len(metrics["MTTD"]),
            "MTTR": sum(metrics["MTTR"]) / len(metrics["MTTR"])
        }
    return averages



if __name__ == "__main__":
    print("--- Starting ResIoT vs. RBS Resilience Simulation ---")

    # Run a high number of simulations for statistical significance
    NUM_SIMS = 1000

    start_time = time.time()
    sim_results = run_simulation(NUM_SIMS)
    avg_metrics = calculate_average_metrics(sim_results)
    end_time = time.time()

    print(f"\nTotal Simulated Incidents: {NUM_SIMS}")
    print(f"Simulation Duration: {end_time - start_time:.2f} seconds\n")

    print("--- Comparative Mean Resilience Metrics (Time in Seconds) ---")

  
    print(f"{'System':<10} | {'Mean Time to Detect (MTTD)':<30} | {'Mean Time to Resolve (MTTR)':<30}")
    print("-" * 75)

    # Rule-Based System Results
    rbs_mttd = avg_metrics['RBS']['MTTD']
    rbs_mttr = avg_metrics['RBS']['MTTR']
    print(f"{'RBS':<10} | {rbs_mttd:<30.2f} | {rbs_mttr:<30.2f}")

    # ResIoT System Results
    aas_mttd = avg_metrics['AAS']['MTTD']
    aas_mttr = avg_metrics['AAS']['MTTR']
    print(f"{'ResIoT':<10} | {aas_mttd:<30.2f} | {aas_mttr:<30.2f}")


    mttd_improvement = (rbs_mttd - aas_mttd) / rbs_mttd * 100
    mttr_improvement = (rbs_mttr - aas_mttr) / rbs_mttr * 100

    print("-" * 75)
    print(f"MTTD Improvement (AAS over RBS): {mttd_improvement:.2f}%")
    print(f"MTTR Improvement (AAS over RBS): {mttr_improvement:.2f}%")
