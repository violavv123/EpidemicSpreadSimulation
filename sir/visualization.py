import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def animate_sir(df):
    """
    df must contain: time, S, I, R
    Example: df = model.run(...)
    """

    fig, ax = plt.subplots()

    ax.set_xlim(df["time"].min(), df["time"].max())
    ax.set_ylim(0, max(df["S"].max(), df["I"].max(), df["R"].max()))

    line_S, = ax.plot([], [], label="Susceptible")
    line_I, = ax.plot([], [], label="Infected")
    line_R, = ax.plot([], [], label="Recovered")

    ax.legend()

    def update(frame):
        line_S.set_data(df["time"][:frame], df["S"][:frame])
        line_I.set_data(df["time"][:frame], df["I"][:frame])
        line_R.set_data(df["time"][:frame], df["R"][:frame])
        return line_S, line_I, line_R

    ani = FuncAnimation(fig, update, frames=len(df), interval=50, blit=True)
    plt.show()
