"""
==========================================================
ResIoT Simulator
Configuration File

Author : Kaneez Fizza
Description:
Global configuration parameters used throughout the
ResIoT Multi-Agent Learning Simulator.
==========================================================
"""

from dataclasses import dataclass


# ==========================================================
# General Simulation Settings
# ==========================================================

RANDOM_SEED = 42

TOTAL_EPISODES = 1000

TIME_STEP = 1                 # seconds

OUTPUT_DIRECTORY = "outputs/"

SAVE_RESULTS = True

VERBOSE = False



# ==========================================================
# IoT Environment
# ==========================================================

NUM_SENSORS = 100

NUM_GATEWAYS = 10

NUM_ANALYTICS_NODES = 5

NUM_ACTUATORS = 100

EDGE_NODES = 5

CLOUD_NODES = 1



# ==========================================================
# Agent Configuration
# ==========================================================

NUM_AGENTS = 5

AGENT_NAMES = [

    "AS1_Sensing",

    "AS2_Transmission",

    "AS3_Analytics",

    "AS4_Information",

    "AS5_Actuation"

]



ORCHESTRATOR_NAME = "OA"



# ==========================================================
# Learning Parameters
# ==========================================================

LEARNING_RATE = 0.20

DISCOUNT_FACTOR = 0.95

INITIAL_CONFIDENCE = 0.50

MAX_CONFIDENCE = 0.99

MIN_CONFIDENCE = 0.05



# ε-greedy exploration

EPSILON = 0.25

EPSILON_DECAY = 0.995

MIN_EPSILON = 0.02



# ==========================================================
# Knowledge Base
# ==========================================================

MAX_KB_SIZE = 10000

ENABLE_KNOWLEDGE_PRUNING = False

KB_UPDATE_AFTER_EVERY_EPISODE = True



# ==========================================================
# Failure Generation
# ==========================================================

FAULT_PROBABILITIES = {

    "SensorDrift": 0.20,

    "SensorNoise": 0.10,

    "MissingData": 0.10,

    "CommunicationLoss": 0.20,

    "PacketDelay": 0.10,

    "GatewayFailure": 0.05,

    "AnalyticsFailure": 0.10,

    "ModelDrift": 0.05,

    "InformationDelay": 0.05,

    "ActuatorFailure": 0.05

}



# ==========================================================
# Fault Severity
# ==========================================================

FAULT_SEVERITY = {

    "LOW": 1,

    "MEDIUM": 2,

    "HIGH": 3

}



# ==========================================================
# Detection Time (seconds)
# ==========================================================

DETECTION_TIME = {

    "SensorDrift": (40,120),

    "SensorNoise": (15,60),

    "MissingData": (10,40),

    "CommunicationLoss": (5,30),

    "PacketDelay": (10,40),

    "GatewayFailure": (20,80),

    "AnalyticsFailure": (30,100),

    "ModelDrift": (60,180),

    "InformationDelay": (15,50),

    "ActuatorFailure": (60,180)

}



# ==========================================================
# Recovery Strategies
# ==========================================================

RECOVERY_STRATEGIES = {

    "SensorDrift":[

        "FastCalibration",

        "RedundantSensor",

        "SensorReplacement"

    ],

    "SensorNoise":[

        "NoiseFiltering",

        "SensorReset"

    ],

    "MissingData":[

        "Interpolation",

        "NeighbourEstimate"

    ],

    "CommunicationLoss":[

        "DynamicRouting",

        "GatewayRestart",

        "BackupLink"

    ],

    "PacketDelay":[

        "QoSAdjustment",

        "PriorityRouting"

    ],

    "GatewayFailure":[

        "GatewayFailover",

        "EdgeMigration"

    ],

    "AnalyticsFailure":[

        "ModelRestart",

        "ModelReload"

    ],

    "ModelDrift":[

        "ModelRetraining",

        "Rollback"

    ],

    "InformationDelay":[

        "MessageResend",

        "AlternativeChannel"

    ],

    "ActuatorFailure":[

        "LocalRecalibration",

        "Retry",

        "SafeMode"

    ]

}



# ==========================================================
# Communication Cost
# ==========================================================

MESSAGE_SIZE = 2          # KB

NETWORK_LATENCY = 5       # ms

EDGE_LATENCY = 2          # ms

CLOUD_LATENCY = 25        # ms



# ==========================================================
# Resource Usage
# ==========================================================

CPU_COST_PER_AGENT = 1.5

MEMORY_COST_PER_AGENT = 8

KB_COST_PER_ENTRY = 0.002



# ==========================================================
# Evaluation Metrics
# ==========================================================

WINDOW_SIZE = 50

SAVE_LEARNING_CURVE = True

SAVE_SCALABILITY_RESULTS = True

SAVE_OVERHEAD_RESULTS = True



# ==========================================================
# Plot Settings
# ==========================================================

FIGURE_DPI = 300

FIGURE_FORMAT = "png"

FIGURE_WIDTH = 8

FIGURE_HEIGHT = 5



# ==========================================================
# Dataclass
# ==========================================================

@dataclass
class SimulationState:

    episode: int = 0

    epsilon: float = EPSILON

    total_messages: int = 0

    total_cpu: float = 0

    total_memory: float = 0

    kb_entries: int = 0

    detected_faults: int = 0

    recovered_faults: int = 0