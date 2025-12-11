import matplotlib.pyplot as plt
from sir.model import SIR
import pandas as pd
import os
from sir.variants import StochasticSIR, SEIR
from sir.visualization import animate_sir
from sir.visualization_dots import animate_sir_dots


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


def format_summary(model: SIR) -> str:
    lines = []
    lines.append(f"R0 (basic reproduction): {model.R0:.3f}")

    peak = model.peak_infections()
    lines.append(f"Peak infections at t = {peak['time']:.2f}")
    lines.append(f"I_max = {peak['I_max']:.2f}")

    final_size = model.final_size()
    lines.append(f"Final size: {final_size:.3f} of N")

    Rt_time = model.time_Rt_below_one()
    if Rt_time is None:
        lines.append("R(t) never < 1")
    else:
        lines.append(f"R(t) < 1 from t = {Rt_time:.2f}")

    duration = model.epidemic_duration()
    if duration is None:
        lines.append("Epidemic never ends (I >= threshold)")
    else:
        lines.append(f"Epidemic ends at t = {duration:.2f}")

    return "\n".join(lines)

def print_summary(model: SIR) -> None:
    print("\n************** EPIDEMIC SUMMARY **************")
    print(format_summary(model))
    print("*************************************************")

def plot_results(df, title="SIR Model Dynamics", summary_text : str | None = None):
    fig, ax = plt.subplots()

    ax.plot(df["time"], df["S"], label="Susceptible")
    ax.plot(df["time"], df["I"], label="Infected")
    ax.plot(df["time"], df["R"], label="Recovered")

    ax.set_xlabel("Time")
    ax.set_ylabel("Population")
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()

    if summary_text is not None:
        ax.text(
            0.02, 0.98,
            summary_text,
            transform = ax.transAxes,
            va = "top",
            ha = "left",
            fontsize = 8,
            bbox = dict(boxstyle = "round", alpha = 0.3)
        )
    plt.show()



def menu():
    print("\n******** MAIN MENU ********")
    print("1. Manual simulation")
    print("2. Run predefined scenario")
    print("3. Stochastic SIR Simulation")
    print("4. SEIR Simulation")
    print("5. Exit")
    return input("Choose (1–5): ").strip()

def choose_visualization(df, summary_text=None, country_name=None):
    print("\n**** Choose Visualization ****")
    print("1. Animated graph (lines)")
    print("2. Animated dots map (emoji dots)")
    print("3. Static graph (plot)")
    print("4. Show ALL visualizations")
    choice = input("Select (1–4): ").strip()

    title = "SIR Model Dynamics"
    if country_name:
        title = f"SIR Model Dynamics - {country_name}"

    if choice == "1":
        animate_sir(df)

    elif choice == "2":
        animate_sir_dots(df)

    elif choice == "3":
        plot_results(df, title=title, summary_text=summary_text)

    elif choice == "4":
        animate_sir_dots(df)
        animate_sir(df)
        plot_results(df, title=title, summary_text=summary_text)

    else:
        print("Invalid choice, showing animated graph by default.")
        animate_sir(df)



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
    summary_text = format_summary(model)
    print_summary(model)
    choose_visualization(df, summary_text=summary_text, country_name=None)


def predefined_simulation():
    file_path = "covid_data/country_wise_latest.csv" 

    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    df = pd.read_csv(file_path)

    df.columns = [col.strip().replace(" ", "_").replace("/", "_").lower() for col in df.columns]

    total_confirmed = df['confirmed'].sum()
    total_deaths = df['deaths'].sum()
    total_recovered = df['recovered'].sum()
    total_active = df['active'].sum()

    print("\n--- Global COVID-19 Stats ---")
    print(f"Total Confirmed Cases: {total_confirmed}")
    print(f"Total Deaths: {total_deaths}")
    print(f"Total Recovered: {total_recovered}")
    print(f"Total Active Cases: {total_active}")

    country = input("\nEnter a country name to see stats: ").strip()

    country_data = df[df['country_region'].str.lower() == country.lower()]

    if country_data.empty:
        print(f"No data found for '{country}'.")
        return

    country_data = country_data.iloc[0]

    confirmed = int(country_data['confirmed'])
    active = int(country_data['active'])
    recovered = int(country_data['recovered'])
    deaths = int(country_data['deaths'])
    population = int(country_data["population"])

    new_infections = int(active * 0.05)
    predicted_active = active + new_infections - int(recovered * 0.01) - int(deaths * 0.01)

    fatality_rate = (deaths / confirmed) * 100 if confirmed > 0 else 0
    recovery_rate = (recovered / confirmed) * 100 if confirmed > 0 else 0

    choice = input("\nUse predicted active as initial infected for SIR? (y/n): ").strip().lower()
    if choice == "y":
        I0 = predicted_active
        print(f"Using predicted active = {predicted_active} as I0 for SIR.")
    else:
        I0 = active
        print(f"Using current active = {active} as I0 for SIR.")

    print(f"\n--- COVID-19 Stats for {country_data['country_region']} ---")
    print(f"Confirmed Cases: {confirmed}")
    print(f"Active Cases: {active}")
    print(f"Recovered: {recovered}")
    print(f"Deaths: {deaths}")
    print(f"Fatality Rate: {fatality_rate:.2f}%")
    print(f"Recovery Rate: {recovery_rate:.2f}%")
    print(f"Predicted New Infections Next Period: {new_infections}")
    print(f"Predicted Active Cases Next Period: {predicted_active}")

    N = population
    R0_init = recovered + deaths
    S0_check = N - I0 - R0_init

    if S0_check < 0:
        print("Warning: N < I0 + R0 (data inconsistent with SR). Adjust N or input data.")
        return

    beta = 0.3
    gamma = 1.0 / 14.0

    T = 160.0
    dt = 1.0

    method = input("Numerical method ('euler' or 'rk4') [euler]: ").strip().lower()
    if method not in ("euler", "rk4"):
        method = "euler"

    model = SIR(N = N, I0 = I0, R0 = R0_init, beta = beta, gamma = gamma, T = T, dt = dt)

    df_sir = model.run(method = method)
    base_summary = format_summary(model)
    extra = (
        f"\nNew infections (simple model): {new_infections}"
        f"\nPredicted active (simple model): {predicted_active}"
    )
    summary_text = base_summary + extra
    print_summary(model)
    print(extra)
    plot_results(df_sir, title=f"SIR Model Dynamics - {country_data['country_region']}", summary_text=summary_text)



def run_stochastic_simulation():
    print("\n***** Stochastic SIR Simulation *****")

    N = get_int_input("Total population N", 1000)
    I0 = get_int_input("Initial infected I0", 10)
    R0 = get_int_input("Initial recovered R0", 0)

    beta = get_float_input("Transmission rate beta", 0.3)
    gamma = get_float_input("Recovery rate gamma", 0.1)

    steps = get_int_input("Simulation steps", 160)

    model = StochasticSIR(N=N, I0=I0, R0=R0, beta=beta, gamma=gamma)

    S, I, R = model.run_stochastic(steps=steps)

    df = pd.DataFrame({"time": range(len(S)), "S": S, "I": I, "R": R})
    
    choose_visualization(df, summary_text=None, country_name="Stochastic SIR Model")



def run_seir_simulation():
    print("\n***** SEIR Simulation *****")

    N = get_int_input("Total population N", 1000)
    S0 = get_int_input("Initial susceptible S0", 990)
    E0 = get_int_input("Initial exposed E0", 5)
    I0 = get_int_input("Initial infected I0", 5)
    R0 = get_int_input("Initial recovered R0", 0)

    beta = get_float_input("Transmission rate beta", 0.3)
    gamma = get_float_input("Recovery rate gamma", 0.1)
    sigma = get_float_input("Incubation rate sigma", 0.2)

    steps = get_int_input("Simulation steps", 160)

    model = SEIR(N, S0, E0, I0, R0, beta, gamma, sigma)

    S, E, I, R = model.run(steps=steps)

    df = pd.DataFrame({"time": range(len(S)), "S": S, "E": E, "I": I, "R": R})
    
    choose_visualization(df, summary_text=None, country_name="SEIR Model Dynamics")

    


def main():
    while True:
        choice = menu()
        if choice == "1":
            manual_simulation()
        elif choice == "2":
            predefined_simulation()
        elif choice == "3":
            run_stochastic_simulation()

        elif choice == "4":
            run_seir_simulation()

        elif choice == "5":
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Please select 1–5.")


if __name__ == "__main__":
    main()