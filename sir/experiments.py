import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sir.model import SIR

OUTPUT_DIR = Path("experiments_output")
OUTPUT_DIR.mkdir(exist_ok=True)


def convergence_study():

    betas = 0.3
    gamma = 0.1
    N = 1000
    I0 = 10
    R0 = 0
    T = 160

    dt_values = [1.0, 0.5, 0.2, 0.1, 0.05]
    dt_ref = 0.001

    ref = SIR(N, I0, R0, betas, gamma, T=T, dt=dt_ref)
    ref.run("rk4")
    ref_peak = ref.peak_infections()
    ref_final = ref.final_size()

    rows = []

    for method in ("euler", "rk4"):
        for dt in dt_values:
            model = SIR(N, I0, R0, betas, gamma, T=T, dt=dt)
            model.run(method)

            peak = model.peak_infections()
            final = model.final_size()

            rows.append({
                "method": method,
                "dt": dt,
                "error_peak_I": abs(peak["I_max"] - ref_peak["I_max"]),
                "error_final_size": abs(final - ref_final),
            })

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_DIR / "convergence.csv", index=False)

    plt.figure()
    for method in ("euler", "rk4"):
        sub = df[df["method"] == method]
        plt.plot(sub["dt"], sub["error_peak_I"], marker="o", label=method)
    plt.xlabel("dt")
    plt.ylabel("Error in peak infections")
    plt.title("Convergence Study: Error vs dt")
    plt.legend()
    plt.savefig(OUTPUT_DIR / "convergence_error_peak.png")
    plt.close()

    return df

def time_complexity_experiment():

    T_values = [500, 1000, 2000, 4000, 8000]
    dt = 0.1

    results = []
    for T in T_values:
        model = SIR(N=1000, I0=10, R0=0, beta=0.3, gamma=0.1, T=T, dt=dt)
        start = time.perf_counter()
        model.run("euler")
        end = time.perf_counter()
        results.append({
            "T": T,
            "steps": model.steps,
            "runtime": end - start
        })

    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_DIR / "time_complexity.csv", index=False)

    plt.figure()
    plt.plot(df["steps"], df["runtime"], marker="o")
    plt.xlabel("Number of steps")
    plt.ylabel("Runtime (s)")
    plt.title("Time Complexity: Runtime vs Steps")
    plt.savefig(OUTPUT_DIR / "time_complexity.png")
    plt.close()

    return df

def parameter_sweep():

    betas = np.linspace(0.1, 0.6, 6)
    gammas = np.linspace(0.05, 0.3, 6)

    rows = []
    for b in betas:
        for g in gammas:
            model = SIR(1000, 10, 0, b, g, T=160, dt=0.1)
            model.run()
            peak = model.peak_infections()
            rows.append({"beta": b, "gamma": g, "I_max": peak["I_max"]})

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_DIR / "sweep.csv", index=False)

    Z = df.pivot(index="gamma", columns="beta", values="I_max")

    plt.figure()
    plt.imshow(Z, origin="lower", aspect="auto",
               extent=[min(betas), max(betas), min(gammas), max(gammas)])
    plt.colorbar(label="Peak infections")
    plt.xlabel("beta")
    plt.ylabel("gamma")
    plt.title("Peak Infections Heatmap")
    plt.savefig(OUTPUT_DIR / "sweep_heatmap.png")
    plt.close()

    return df
