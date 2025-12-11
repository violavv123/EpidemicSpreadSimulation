Epidemic Spread Simulation – SIR Model

This project implements epidemic-spread simulations using SIR, SEIR, and stochastic models. It includes numerical solvers such as Euler and Runge-Kutta 4, multiple visualization methods, an interactive command-line interface, COVID-19 data-based scenarios, and six algorithmic experiments used for analyzing convergence, complexity, and parameter sensitivity.

Project Structure

The project is organized into the following folders:

sir/
This folder contains all core modules of the simulation:
model.py – Implements the deterministic SIR model with Euler and RK4 numerical solvers. Includes functions for peak infection time, final epidemic size, recovery dynamics, Rt calculation, and epidemic duration. The model outputs a DataFrame containing time, S, I, and R values.
variants.py – Contains additional model variants. StochasticSIR introduces randomness using binomial sampling. SEIR implements the four-compartment model S → E → I → R.
visualization.py – Provides animated line-graph visualization of S, I, and R over time.
visualization_dots.py – Provides a dot-based human-style visualization where each individual is represented by a colored dot (susceptible, infected, recovered).
experiments.py – Contains six predefined experiments used for numerical and algorithmic analysis. These include convergence studies, time complexity evaluation, parameter sweeps, beta and gamma influence demonstrations, and herd-immunity scenarios. The results are automatically saved into the experiments_output folder.

covid_data/
This folder contains the dataset country_wise_latest.csv, used for predefined simulation scenarios where the user selects a country and a corresponding SIR model is built from real-world data.

experiments_output/
This folder holds all generated outputs from the experiments module. Files include CSV tables of computed values and PNG visualizations for convergence, time complexity, parameter sweeps, beta and gamma effects, and herd-immunity results.

main.py
This is the entry point of the project and provides an interactive menu interface. It allows the user to run:
Manual SIR simulations with user-specified parameters
Predefined scenarios using COVID-19 data
Stochastic SIR simulations
SEIR model simulations
Different visualization options such as animated graphs, dot visualizations, and static plots are available through the menu.

Description of the Six Experiments

The experiments implemented in sir/experiments.py are the following:

Convergence Study
Compares Euler and RK4 solvers for multiple time-step sizes. Shows how both methods behave as dt becomes smaller and how RK4 converges faster than Euler.

Time Complexity Experiment
Measures runtime against the number of numerical steps. Demonstrates that the simulation complexity grows linearly with respect to T/dt.

Parameter Sweep
Runs the SIR model across a grid of beta and gamma values. Records peak infection counts and generates a heatmap to visualize how outbreak severity depends on model parameters.

Effect of Beta
Shows how increasing the transmission rate causes earlier and stronger outbreaks.

Effect of Gamma
Shows how increasing the recovery rate reduces outbreak intensity and lowers the infection peak.

Herd Immunity Scenario
Varies the initial recovered population to demonstrate how pre-existing immunity can prevent or weaken outbreaks.

How to Run the Project

Install dependencies by using:
pip install numpy pandas matplotlib

Run the main interactive program:
python main.py

Run all six experiments:
python sir/experiments.py

All experiment results will appear in the experiments_output folder.

Purpose of the Project

The project is designed to study:
Differences between numerical solvers such as Euler and RK4
Convergence and accuracy of epidemic models
Algorithmic time complexity of numerical integration
Parameter sensitivity of epidemiological systems
Deterministic versus stochastic epidemic dynamics
Real-world applicability using COVID-19 data

It provides both theoretical and practical insight into epidemic modeling and numerical algorithm behavior for educational and research use.