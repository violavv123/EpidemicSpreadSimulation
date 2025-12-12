import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sir.model import SIR

OUTPUT_DIR = Path("experiments_output")
OUTPUT_DIR.mkdir(exist_ok=True)
