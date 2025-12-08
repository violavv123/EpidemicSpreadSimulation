import matplotlib.pyplot as plt
from sir.model import SIR
from sir.sim_data import (
    run_multiple_scenarios,
    save_to_csv,
    standard_scenarios
)
import os,json

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

def plot_results(df, title="SIR Model Dynamics"):
    plt.plot(df["time"], df["S"], label="Susceptible")
    plt.plot(df["time"], df["I"], label="Infected")
    plt.plot(df["time"], df["R"], label="Recovered")

    plt.xlabel("Time")
    plt.ylabel("Population")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.show()



def menu():
    print("\n******** MAIN MENU ********")
    print("1. Manual simulation")
    print("2. Run predefined scenario")
    print("3. Run multiple scenarios")
    print("4. Exit")
    return input("Choose (1–4): ").strip()


def manual_simulation():
    print("********* SIR Epidemic Simulation **********")

    N = get_int_input("Total population N", 1000)
    I0 = get_int_input("Initial infected I0", 10)
    R0 = get_int_input("Initial recovered R0", 0)

    beta = get_float_input("Transmission rate beta", 0.3)
    gamma = get_float_input("Recovery rate gamma", 0.1)

    T = get_float_input("Total simulation time T", 300.0)
    dt = get_float_input("Time step dt", 1.0)

    method = input("Numerical method ('euler' or 'rk4') [euler]: ").strip().lower()
    if method not in ("euler", "rk4"):
        method = "euler"

    model = SIR(N=N, I0=I0, R0=R0, beta=beta, gamma=gamma, T=T, dt=dt)
    df = model.run(method=method)
    print_summary(model)
    plot_results(df)


def predefined_simulation():
    scenarios = standard_scenarios()
    print("\nAvailable scenarios:")
    for name in scenarios:
        print(" -", name)

    choice = input("Choose scenario (spread simulation): ").strip()
    if choice not in scenarios:
        print("Invalid choice")
        return

    params = scenarios[choice]

    model = SIR(
        N=params.get("N", 1000),
        I0=params.get("I0", 10),
        R0=params.get("R0", 0),
        beta=params.get("beta", 0.3),
        gamma=params.get("gamma", 0.1),
        T=params.get("T", 300.0),
        dt=params.get("dt", 1.0),
    )

    df = model.run(method=params.get("method", "euler"))

    os.makedirs("output", exist_ok=True)
    with open(f"output/{choice}.json", "w") as f:
        json.dump(df.to_dict(orient="list"), f, indent=4)

    print(f"Saved results to output/{choice}.json")

    plot_results(df, title=f"SIR Dynamics: {choice}")



def multiple_scenario_simulation():
    print("\nRunning 3 demo scenarios...")

    scenarios = [
        {"beta": 0.3, "gamma": 0.1, "N": 500},
        {"beta": 0.5, "gamma": 0.1, "N": 500},
        {"beta": 0.2, "gamma": 0.2, "N": 500},
    ]

    results = run_multiple_scenarios(scenarios)
    save_to_csv(results, "output/multi_scenarios.csv")

    print("Saved CSV to output/multi_scenarios.csv")

def main():
    while True:
        choice = menu()
        if choice == "1":
            manual_simulation()
        elif choice == "2":
            predefined_simulation()
        elif choice == "3":
            multiple_scenario_simulation()
        elif choice == "4":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please select 1–4.")


if __name__ == "__main__":
    main()