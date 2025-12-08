from sir.model import SIR
from sir.config import DEFAULT_CONFIG


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

def save_to_json(data, filepath):
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)


def load_json(filepath):
    with open(filepath) as f:
        return json.load(f)


def save_to_csv(simulation_results, filepath):
    """
    Accepts a list of simulation dictionaries (from run_multiple_scenarios)
    """
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["beta", "gamma", "t", "S", "I", "R"])

        for entry in simulation_results:
            beta = entry["parameters"]["beta"]
            gamma = entry["parameters"]["gamma"]
            t = entry["results"]["t"]
            S = entry["results"]["S"]
            I = entry["results"]["I"]
            R = entry["results"]["R"]

            for ti, si, ii, ri in zip(t, S, I, R):
                writer.writerow([beta, gamma, ti, si, ii, ri])



def standard_scenarios():
    return {
        "fast_spread":  {"beta": 0.5, "gamma": 0.1, "N": 1000, "I0": 10},
        "slow_spread":  {"beta": 0.15, "gamma": 0.1, "N": 1000, "I0": 10},
        "high_recovery": {"beta": 0.25, "gamma": 0.35, "N": 1000, "I0": 10},
    }




