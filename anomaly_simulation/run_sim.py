import json
from simulation import Simulation

if __name__ == "__main__":
    sim = Simulation(json.load(open("user_config/test_anomaly.json", "rb")))
    sim.run_simulation()
