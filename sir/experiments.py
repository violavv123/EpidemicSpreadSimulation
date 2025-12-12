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
