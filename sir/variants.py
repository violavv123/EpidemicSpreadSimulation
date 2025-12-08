import numpy as np
from sir.model import SIR   


class StochasticSIR(SIR):
    """
    Stochastic SIR model using binomial Monte Carlo transitions.
    """
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
