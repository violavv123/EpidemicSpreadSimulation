import numpy as np
from sir.model import SIR   


class StochasticSIR(SIR):
    
    def run_stochastic(self, steps=160):
        S, I, R = [self.S0], [self.I0], [self.R0]

        for t in range(steps):
            S_prev, I_prev, R_prev = S[-1], I[-1], R[-1]

            p_inf = self.beta * I_prev / self.N       
            p_rec = self.gamma                        

            new_infections = np.random.binomial(int(S_prev), min(max(p_inf, 0), 1))
            new_recoveries = np.random.binomial(int(I_prev), min(max(p_rec, 0), 1))

            S_new = S_prev - new_infections
            I_new = I_prev + new_infections - new_recoveries
            R_new = R_prev + new_recoveries

            S.append(S_new)
            I.append(I_new)
            R.append(R_new)

        return np.array(S), np.array(I), np.array(R)
    

class SEIR:

    def __init__(self, N, S0, E0, I0, R0, beta, gamma, sigma):
        self.N = N
        self.S0 = S0
        self.E0 = E0
        self.I0 = I0
        self.R0 = R0
        self.beta = beta     
        self.gamma = gamma   
        self.sigma = sigma   

    def run(self, steps=160):
        S, E, I, R = [self.S0], [self.E0], [self.I0], [self.R0]

        for t in range(steps):
            S_prev, E_prev, I_prev, R_prev = S[-1], E[-1], I[-1], R[-1]

            new_exposed = self.beta * S_prev * I_prev / self.N
            new_infected = self.sigma * E_prev
            new_recovered = self.gamma * I_prev

            S_new = S_prev - new_exposed
            E_new = E_prev + new_exposed - new_infected
            I_new = I_prev + new_infected - new_recovered
            R_new = R_prev + new_recovered

            S.append(S_new)
            E.append(E_new)
            I.append(I_new)
            R.append(R_new)

        return np.array(S), np.array(E), np.array(I), np.array(R)

