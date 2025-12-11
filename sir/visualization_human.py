import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

def animate_sir_human(df, save_path=None):
    """
    Animate SIR with moving colored dots.
    df must contain: time, S, I, R
    """
    # Total population
    N = int(df["S"].iloc[0] + df["I"].iloc[0] + df["R"].iloc[0])
    
    # Initial random positions
    x = np.random.rand(N)
    y = np.random.rand(N)

    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("SIR Simulation (Dynamic)")

    # Initial scatter (all susceptible)
    colors = ["blue"] * N
    scatter = ax.scatter(x, y, c=colors, s=50)

    # Velocity for each individual for movement
    vx = (np.random.rand(N) - 0.5) * 0.01
    vy = (np.random.rand(N) - 0.5) * 0.01

    def update(frame):
        nonlocal x, y

        # Move people
        x += vx
        y += vy

        # Bounce off walls
        x = np.clip(x, 0, 1)
        y = np.clip(y, 0, 1)

        # Get current counts
        S_count = int(df["S"].iloc[frame])
        I_count = int(df["I"].iloc[frame])
        R_count = int(df["R"].iloc[frame])

        # Build colors array
        frame_colors = ["blue"]*S_count + ["red"]*I_count + ["green"]*R_count

        # Pad/truncate to N
        if len(frame_colors) < N:
            frame_colors += ["blue"]*(N - len(frame_colors))
        elif len(frame_colors) > N:
            frame_colors = frame_colors[:N]

        # Update scatter
        scatter.set_offsets(np.c_[x, y])
        scatter.set_color(frame_colors)
        ax.set_title(f"Time: {df['time'].iloc[frame]:.0f} | S:{S_count} I:{I_count} R:{R_count}")
        return scatter,

    ani = FuncAnimation(fig, update, frames=len(df), interval=200, blit=True)

    if save_path:
        ani.save(save_path, writer="imagemagick", fps=5)

    plt.show()
