import matplotlib.pyplot as plt
import numpy as np


# ================= STATIC VISUAL =================
def draw_room(length, width, placement):
    fig, ax = plt.subplots(figsize=(6, 4))

    x = np.linspace(0, length, 80)
    y = np.linspace(0, width, 80)
    X, Y = np.meshgrid(x, y)

    # AC position
    if placement == "Top Wall":
        ac_x, ac_y = length / 2, width
    elif placement == "Bottom Wall":
        ac_x, ac_y = length / 2, 0
    elif placement == "Left Wall":
        ac_x, ac_y = 0, width / 2
    else:
        ac_x, ac_y = length, width / 2

    distance = np.sqrt((X - ac_x)**2 + (Y - ac_y)**2)
    cooling_effect = np.exp(-distance / (length / 2))

    contour = ax.contourf(X, Y, cooling_effect, levels=25, cmap='coolwarm')

    # Room border
    ax.add_patch(plt.Rectangle((0, 0), length, width,
                               fill=False, edgecolor='black', linewidth=2))

    # AC marker
    ax.scatter(ac_x, ac_y, color='blue', s=120)
    ax.text(ac_x, ac_y, " AC", color='white', fontsize=10, weight='bold')

    # Airflow arrows
    for i in range(3):
        dx = (length/6) if ac_x == 0 else -(length/6) if ac_x == length else 0
        dy = (width/6) if ac_y == 0 else -(width/6) if ac_y == width else 0

        ax.arrow(ac_x, ac_y, dx*(i+1), dy*(i+1),
                 head_width=0.3, color='white')

    ax.set_title(f"{placement} - Cooling Distribution")
    ax.set_xlim(0, length)
    ax.set_ylim(0, width)
    ax.set_aspect('equal')

    cbar = fig.colorbar(contour)
    cbar.set_label("Cooling Intensity")

    return fig


# ================= SIMULATION MODE =================
def draw_room(length, width, placement):
    fig, ax = plt.subplots(figsize=(6, 4))

    # High resolution grid
    x = np.linspace(0, length, 100)
    y = np.linspace(0, width, 100)
    X, Y = np.meshgrid(x, y)

    # AC position + airflow direction
    if placement == "Top Wall":
        ac_x, ac_y = length / 2, width
        dir_x, dir_y = 0, -1
    elif placement == "Bottom Wall":
        ac_x, ac_y = length / 2, 0
        dir_x, dir_y = 0, 1
    elif placement == "Left Wall":
        ac_x, ac_y = 0, width / 2
        dir_x, dir_y = 1, 0
    else:  # Right Wall
        ac_x, ac_y = length, width / 2
        dir_x, dir_y = -1, 0

    # Vector from AC to each point
    dx = X - ac_x
    dy = Y - ac_y

    # Distance
    distance = np.sqrt(dx**2 + dy**2)

    # Normalize vectors
    norm = np.sqrt(dx**2 + dy**2) + 1e-6
    vx = dx / norm
    vy = dy / norm

    # Dot product (alignment with airflow direction)
    alignment = vx * dir_x + vy * dir_y

    # Keep only forward airflow (cone effect)
    alignment = np.maximum(alignment, 0)

    # Cooling model:
    # Strong forward flow + decay + slight spread
    cooling = alignment * np.exp(-distance / (length / 1.5))

    # Add small diffusion (side spread)
    diffusion = np.exp(-distance / (length))
    cooling = 0.7 * cooling + 0.3 * diffusion

    # Heatmap
    contour = ax.contourf(X, Y, cooling, levels=30, cmap="coolwarm")

    # Room border
    ax.add_patch(plt.Rectangle((0, 0), length, width,
                               fill=False, edgecolor="black", linewidth=2))

    # AC marker
    ax.scatter(ac_x, ac_y, color="blue", s=120)
    ax.text(ac_x, ac_y, " AC", color="white", fontsize=9, weight="bold")

    # Direction arrow (main airflow)
    ax.arrow(ac_x, ac_y,
             dir_x * length/3,
             dir_y * width/3,
             head_width=0.5,
             color="white", linewidth=2)

    # Labels
    ax.set_title(f"{placement} - Real Airflow Simulation")
    ax.set_xlabel("Room Length")
    ax.set_ylabel("Room Width")

    # Color bar
    cbar = fig.colorbar(contour)
    cbar.set_label("Cooling Intensity")

    ax.set_xlim(0, length)
    ax.set_ylim(0, width)
    ax.set_aspect('equal')

    return fig