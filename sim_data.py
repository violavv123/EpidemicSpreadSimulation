import json
import csv
from pathlib import Path
from model import SIR  
from config import DEFAULT_CONFIG


def run_scenario(beta, gamma, N=None, I0=None, R0=None, days=None, dt=None):
    """
    Runs a single SIR simulation using default config parameters unless overridden.
    """
    N = N if N is not None else DEFAULT_CONFIG["N"]
    I0 = I0 if I0 is not None else DEFAULT_CONFIG["I0"]
    R0 = R0 if R0 is not None else DEFAULT_CONFIG["R0"]
    days = days if days is not None else DEFAULT_CONFIG["days"]
    dt = dt if dt is not None else DEFAULT_CONFIG["dt"]

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



