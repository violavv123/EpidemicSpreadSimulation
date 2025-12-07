import pandas as pd

class SIR:
    def __init__(
        self,
        eons: int=300,
        N: int = 1000,
        I0: int = 10,
        R0: int = 0,
        beta: float = 0.3,
        gamma: float = 0.1,
    ):
        self.eons = eons
        self.N = N
        self.I0= I0
        self.R0 = R0
        self.S0 = N - I0 - R0

        self.beta = beta
        self.gamma = gamma

        self.results = None
        self.model_run = False
