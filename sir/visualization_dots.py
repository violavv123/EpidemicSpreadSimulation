import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


def animate_sir_dots(df, save_path=None):
    """
    Animate SIR using colored dots to represent people.
    df must contain: time, S, I, R
    """
    # Total population (rounded to int)
    N = int(df["S"].iloc[0] + df["I"].iloc[0] + df["R"].iloc[0])
    
    # Random positions for each individual
    x = np.random.rand(N)
    y = np.random.rand(N)

    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    ax.set_xticks([])
    ax.set_yticks([])

    # Initial scatter plot (all susceptible)
    colors = ["blue"] * N
    scatter = ax.scatter(x, y, c=colors, s=50)

    def update(frame):
        # Get current counts
        S_count = int(df["S"].iloc[frame])
        I_count = int(df["I"].iloc[frame])
        R_count = int(df["R"].iloc[frame])

        # Build new colors array for this frame
        frame_colors = ["blue"]*S_count + ["red"]*I_count + ["green"]*R_count

        # Pad with blue if due to rounding we have fewer than N
        if len(frame_colors) < N:
            frame_colors += ["blue"]*(N - len(frame_colors))
        elif len(frame_colors) > N:
            frame_colors = frame_colors[:N]

        # Update scatter colors
        scatter.set_color(frame_colors)

        # 🔵 ADD COMPLEXITY HERE
        complexity = f"O({S_count + I_count + R_count})"   # O(N)

        ax.set_title(
            f"S (blue):{S_count} I(red):{I_count}| "
            f"Complexity: {complexity}"
        )

        return scatter,

    ani = FuncAnimation(fig, update, frames=len(df), interval=200, blit=True)

    # Optionally save as GIF
    if save_path:
        ani.save(save_path, writer="imagemagick", fps=5)

    plt.show()
