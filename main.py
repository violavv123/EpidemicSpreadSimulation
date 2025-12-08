import matplotlib.pyplot as plt
from sir.model import SIR

def get_int_input(prompt: str, default: int) -> int:
    s = input(f"{prompt} [{default}]: ").strip()
    if s == "":
        return default
    try:
        return int(s)
    except ValueError:
        print("Invalid input, using default.")
        return default


def get_float_input(prompt: str, default: float) -> float:
    s = input(f"{prompt} [{default}]: ").strip()
    if s == "":
        return default
    try:
        return float(s)
    except ValueError:
        print("Invalid input (float), using default.")
        return default


def print_summary(model: SIR) -> None:
    print("\n************** EPIDEMIC SUMMARY **************")
    print(f"Basic reproduction number R0: {model.R0:.3f}")

    peak = model.peak_infections()
    print("Peak infections:")
    print(f"  - time  = {peak['time']:.2f}")
    print(f"  - I_max = {peak['I_max']:.2f}")

    final_size = model.final_size()
    print(f"Final epidemic size: {final_size:.3f} (fraction of population)")

    Rt_time = model.time_Rt_below_one()
    if Rt_time is None:
        print("R(t) never dropped below 1 during the simulation.")
    else:
        print(f"Time when R(t) first drops below 1: t = {Rt_time:.2f}")

    duration = model.epidemic_duration()
    if duration is None:
        print("Epidemic did not end (I(t) never fell below threshold).")
    else:
        print(f"Epidemic duration (I(t) < 1): {duration:.2f}")

    print("*************************************************")



def main() -> None:
    print("********* SIR Epidemic Simulation **********")

    N = get_int_input("Total population N", 1000)
    I0 = get_int_input("Initial infected I0", 10)
    R0 = get_int_input("Initial recovered R0", 0)

    beta = get_float_input("Transmission rate beta", 0.3)
    gamma = get_float_input("Recovery rate gamma", 0.1)

    T = get_float_input("Total simulation time T", 300.0)
    dt = get_float_input("Time step dt", 1.0)

    method = input("Numerical method ('euler' or 'rk4') [euler]: ").strip().lower()
    if method == "":
        method = "euler"
    if method not in ("euler", "rk4"):
        print("Unknown method, defaulting to euler'.")
        method = "euler"

    model = SIR(N = N, I0 = I0, R0 = R0, beta = beta, gamma = gamma, T = T, dt = dt)
    results = model.run( method = method)

    print_summary(model)

    fig, ax = plt.subplots()
    ax.plot(results["time"], results["S"], label = "Susceptible")
    ax.plot(results["time"], results["I"], label = "Infected")
    ax.plot(results["time"], results["R"], label = "Recovered")

    ax.set_xlabel("Time")
    ax.set_ylabel("Population")
    ax.set_title("SIR Model Dynamics")
    ax.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
            main()