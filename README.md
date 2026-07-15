# ResIoT: Multi-Agent Simulator for Self-Healing IoT Systems

ResIoT is a modular, event-driven simulator for evaluating **Agentic AI-based resilience and self-healing in Internet of Things (IoT) systems**. It implements the proposed **ResIoT multi-agent framework**, in which specialized autonomous agents operate across the end-to-end IoT data-to-actuation lifecycle to detect faults, support diagnosis, select recovery actions, coordinate responses, and learn from recovery outcomes.

The simulator provides a controlled environment for evaluating ResIoT against **Rule-Based** and **Machine-Learning-Based** baseline approaches under consistent heterogeneous IoT fault scenarios.

---

## Overview

Modern IoT systems consist of interconnected sensing, communication, analytics, information transmission, and actuation components. A fault at one stage can propagate across the system and affect downstream decisions or physical actions.

ResIoT addresses this challenge using specialized autonomous agents distributed across five stages of the IoT lifecycle:

1. **AS1 – Data Sensing Agent**
2. **AS2 – Data Transmission Agent**
3. **AS3 – Data Analytics Agent**
4. **AS4 – Information Transmission Agent**
5. **AS5 – Actuation / Decision-Making Agent**

An **Orchestrator Agent** supports cross-agent coordination, conflict resolution, and system-wide resilience management.

The simulator evaluates how this multi-agent architecture performs under heterogeneous IoT faults.

---

## Simulator Architecture

The simulator consists of the following major components:

### 1. Inputs

The simulator receives configurable inputs through:

- **Fault Library**
  - Defines heterogeneous IoT fault types
  - Covers faults across the complete IoT lifecycle
  - Specifies fault properties and severity

- **Scenario Generator**
  - Generates fault events for simulation episodes
  - Supports configurable episode counts
  - Supports random or seeded fault generation

- **Configuration**
  - Agent capabilities and policies
  - Detection and recovery parameters
  - Thresholds
  - Baseline configurations
  - Simulation settings

### 2. ResIoT Multi-Agent Environment

The core simulation environment implements the proposed ResIoT framework.

The five lifecycle agents are:

#### AS1 – Data Sensing Agent

Monitors sensing behaviour and handles faults related to sensor operation and data quality.

Example faults:

- Sensor drift
- Sensor noise
- Missing data

#### AS2 – Data Transmission Agent

Monitors communication and network conditions.

Example faults:

- Communication loss
- Packet delay
- Gateway failure

#### AS3 – Data Analytics Agent

Supports analytics-related fault handling and diagnosis.

Example faults:

- Analytics failure
- Model drift

#### AS4 – Information Transmission Agent

Monitors the delivery of information and recovery commands.

Example faults:

- Information delay

#### AS5 – Actuation / Decision-Making Agent

Handles faults affecting physical action and recovery execution.

Example faults:

- Actuator failure

### Orchestrator Agent

The Orchestrator Agent supports:

- Cross-agent coordination
- Recovery-plan selection
- Conflict resolution
- Resource coordination
- System-wide resilience management

### Shared Knowledge and Communication Layer

The ResIoT environment maintains shared information including:

- Fault history
- Recovery policies
- Recovery outcomes
- Confidence scores
- Agent communication
- Context information

Successful recovery experiences reinforce the corresponding recovery policies, while unsuccessful outcomes influence subsequent recovery decisions.

---

## Fault Types

The current simulator evaluates the following ten representative IoT fault types:

| Lifecycle Stage | Fault Types |
|---|---|
| Data Sensing | Sensor Drift, Sensor Noise, Missing Data |
| Data Transmission | Communication Loss, Packet Delay, Gateway Failure |
| Data Analytics | Analytics Failure, Model Drift |
| Information Transmission | Information Delay |
| Actuation | Actuator Failure |

These fault types represent heterogeneous failures that may occur across the IoT data-to-actuation lifecycle.

---

## Simulation Episode

A simulation **episode** represents one complete fault-handling trial.

For each episode:

1. A fault is generated from the predefined fault library.
2. The evaluated approach detects the fault.
3. The fault is diagnosed or mapped to a recovery strategy.
4. A recovery action is selected and executed.
5. The recovery outcome is evaluated.
6. Performance metrics are recorded.
7. For ResIoT, recovery experience is used to update confidence and learning information.
8. 
**Project Structure**
ResIoT/
│
├── main.py
├── agents.py
├── environment.py
├── orchestrator.py
├── knowledge_base.py
├── agent_learning.py
├── faults.py
├── baselines.py
├── metrics.py
├── experiments.py
├── plotting.py
│
├── outputs/
│   ├── csv/
│   │   ├── resiot_results.csv
│   │   ├── rule_results.csv
│   │   ├── ml_results.csv
│   │   ├── learning_curve.csv
│   │   ├── faultwise.csv
│   │   ├── communication_overhead.csv
│   │   └── scalability.csv
│   │
│   └── figures/
│
├── requirements.txt
└── README.md
