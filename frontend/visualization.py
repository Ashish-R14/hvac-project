import matplotlib.pyplot as plt
import numpy as np

def draw_room(length, width, placement):
    fig, ax = plt.subplots(figsize=(6, 4))

    # Create smoother grid
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

    # Distance (cooling strength)
    distance = np.sqrt((X - ac_x)**2 + (Y - ac_y)**2)

    # Cooling effect (smooth decay)
    cooling_effect = np.exp(-distance / (length / 2))

    # Heatmap
    contour = ax.contourf(X, Y, cooling_effect, levels=25, cmap='coolwarm')

    # Room border
    ax.add_patch(plt.Rectangle(
        (0, 0), length, width,
        fill=False, edgecolor='black', linewidth=2
    ))

    # 🔵 AC Marker (improved)
    ax.scatter(ac_x, ac_y, color='blue', s=120)
    ax.text(ac_x, ac_y, " AC", color='white', fontsize=10, weight='bold')

    # ➡️ Airflow arrows (visual clarity)
    for i in range(3):
        dx = (length/6) if ac_x == 0 else -(length/6) if ac_x == length else 0
        dy = (width/6) if ac_y == 0 else -(width/6) if ac_y == width else 0

        ax.arrow(
            ac_x, ac_y,
            dx*(i+1), dy*(i+1),
            head_width=0.3,
            color='white'
        )

    # Labels
    ax.set_title(f"{placement} - Cooling Distribution", fontsize=12)
    ax.set_xlabel("Room Length")
    ax.set_ylabel("Room Width")

    # Color bar
    cbar = fig.colorbar(contour)
    cbar.set_label("Cooling Intensity")

    # Better layout
    ax.set_xlim(0, length)
    ax.set_ylim(0, width)
    ax.set_aspect('equal')

    return fig