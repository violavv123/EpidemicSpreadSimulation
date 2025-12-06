import json
import csv
from pathlib import Path

from model import SIR  

def run_scenario(beta, gamma, N=1000, I0=1, R0=0, days=160, dt=1):
    """
    Runs a single SIR simulation using the repo's SIR class.
    Returns the full time series.
    """
    model = SIR(N=N, I0=I0, R0=R0, beta=beta, gamma=gamma)
    t, S, I, R = model.run(days=days, dt=dt)

    return {
        "parameters": {
            "beta": beta,
            "gamma": gamma,
            "N": N,
            "I0": I0,
            "R0": R0,
            "days": days,
            "dt": dt
        },
        "results": {
            "t": t,
            "S": S,
            "I": I,
            "R": R
        }
    }


def run_multiple_scenarios(scenarios):
    """
    scenarios = [
        {"beta": 0.3, "gamma": 0.1, "N": 500},
        {"beta": 0.2, "gamma": 0.2, "N": 500},
    ]
    """
    all_results = []
    for sc in scenarios:
        print(f"Running β={sc['beta']}, γ={sc['gamma']}")
        all_results.append(run_scenario(**sc))
    return all_results



