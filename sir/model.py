import pandas as pd
import numpy as np

"""
Implementing the SIR model using discrete-time numerical integration of
the differential equations:
dS/dt = -beta * S * I / N
dI/dt = beta * S * I / N - gamma * I
dR/dt = gamma * I

Using algorithms:
Euler forward method 
Runge-Kutta 4 (RK4) high-accuracy solver

Inputs: 
N - total population
I0 - initial infected
R0 - initial recovered/removed
beta - transmission rate
gamma - recovery rate 
dt - time step of numerical integration
T - total simulation time

Outputs:
Pandas DataFrame with columns: time, S, I , R
"""

class SIR:
    def __init__(
            self,
            N: int = 1000,
            I0: int = 10,
            R0: int = 0,
            beta: float = 0.3,
            gamma: float = 0.1,
            dt: float = 1.0,
            T: float = 300.0,
    ):
        """
        Initializing model parameters
        """
        self.N = N
        self.I0 = I0
        self.S0 = N - I0 - R0

        self.beta = beta
        self.gamma = gamma

        self.dt = dt
        self.T = T
        self.steps = int(T / dt)

        self.results: pd.DataFrame | None = None
        self.model_run: bool = False

    @property
    def R0(self) -> float:
        return self.beta/self.gamma

    """
    Euler Solver
    """
    def run_euler(self) -> pd.DataFrame:
        S = [self.S0]
        I = [self.I0]
        R = [self.R0]

        for __ in range(1, self.steps):
            S_prev, I_prev, R_prev = S[-1], I[-1], R[-1]

            dS = -self.beta * S_prev * I_prev/ self.N
            dI = self.beta * S_prev * I_prev / self.N - self.gamma * I_prev
            dR = self.gamma * I_prev

            S_new = S_prev + dS * self.dt
            I_new = I_prev + dI * self.dt
            R_new = R_prev + dR  * self.dt

            S.append(S_new)
            I.append(I_new)
            R.append(R_new)

        t = np.arange(0, self.steps * self.dt, self.dt)

        self.results = pd.DataFrame({"time": t, "S": S, "I" : I, "R": R})
        self.model_run = True
        return self.results

    """
    RK4 Solver
    """
    def run_rk4(self) -> pd.DataFrame:
        def f(S,I,R) -> tuple[float, float, float]:
            dS = -self.beta * S * I / self.N
            dI = self.beta * S * I / self.N - self.gamma * I
            dR = self.gamma * I
            return dS, dI, dR

        S = [self.S0]
        I = [self.I0]
        R = [self.R0]

        for __ in range(1, self.steps):
            S_prev, I_prev, R_prev = S[-1], I[-1], R[-1]

            k1 = f(S_prev, I_prev, R_prev)
            k2 = f(S_prev + 0.5 * self.dt * k1[0], I_prev + 0.5 * self.dt * k1[1], R_prev + 0.5 * self.dt * k1[2])
            k3 = f(S_prev + 0.5 * self.dt * k2[0], I_prev + 0.5 * self.dt * k2[1], R_prev + 0.5 * self.dt * k2[2])
            k4 = f(S_prev + self.dt * k3[0], I_prev + self.dt * k3[1], R_prev + self.dt * k3[2])

            S_new = S_prev + (self.dt / 6) * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
            I_new = I_prev + (self.dt / 6) * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
            R_new = R_prev + (self.dt / 6) * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])

            S.append(S_new)
            I.append(I_new)
            R.append(R_new)

        t = np.arange(0, self.steps * self.dt, self.dt)

        self.results = pd.DataFrame({"time": t, "S": S, "I": I, "R": R})
        self.model_run = True
        return self.results


    def run(self, method="euler"):
        if method == "euler":
            return self.run_euler()
        elif method == "rk4":
            return self.run_rk4()
        else:
            raise ValueError("Method must be either 'euler' or 'rk4'.")

    """
    When does the number of infected people reach its maximum, and how many people 
    are infected at that moment?
    """
    def peak_infections(self) -> dict:
        if not self.model_run:
            raise RuntimeError("Run the model first.")
        idx = self.results["I"].idxmax()
        return{
            "time": float(self.results["time"][idx]),
            "I_max": float(self.results["I"][idx])
        }


    """
    What proportion of the population ends up recovered at the end of the epidemic?
    """
    def final_size(self) -> float:
        if not self.model_run:
            raise RuntimeError("Run the model first.")
        return float(self.results["R"].iloc[-1]/ self.N)


    """
    When does the epidemic start to decline? - each infected person infects less than
    on person on average
    """
    def time_Rt_below_one(self) -> float | None:
        Rt = self.effective_Rt()
        below_one = Rt[Rt < 1]
        if below_one.empty:
            return None
        idx = below_one.index[0]
        return float(self.results["time"][idx])


    """
    How long does the epidemic last?
    """
    def epidemic_duration(self, threshold: float = 1.0) -> float:
        if not self.model_run:
            raise RuntimeError("Run the model first.")
        df = self.results
        ending = df[df["I"] < threshold]

        if ending.empty:
            return None

        return float(ending["time"].iloc[0])


    """
    How many people one infected person infects at each moment of the epidemic?
    """
    def effective_Rt(self) -> pd.Series:
        if not self.model_run:
            raise RuntimeError("Run the model first.")
        Rt = self.R0 * (self.results["S"] / self.N)
        return Rt
