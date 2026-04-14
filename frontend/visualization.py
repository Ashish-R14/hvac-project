import matplotlib.pyplot as plt
import numpy as np

def draw_room(length, width, placement):
    fig, ax = plt.subplots()

    # Create grid
    x = np.linspace(0, length, 50)
    y = np.linspace(0, width, 50)
    X, Y = np.meshgrid(x, y)

    # AC position based on placement
    if placement == "Top Wall":
        ac_x, ac_y = length / 2, width
    elif placement == "Bottom Wall":
        ac_x, ac_y = length / 2, 0
    elif placement == "Left Wall":
        ac_x, ac_y = 0, width / 2
    else:
        ac_x, ac_y = length, width / 2

    # Distance from AC (cooling strength)
    distance = np.sqrt((X - ac_x)**2 + (Y - ac_y)**2)

    # Invert distance to simulate cooling
    cooling_effect = np.exp(-distance / (length/2))

    # Heat map (cool = blue, hot = red)
    heatmap = ax.contourf(X, Y, cooling_effect, cmap='coolwarm')

    # Draw room border
    room = plt.Rectangle((0, 0), length, width, fill=None, edgecolor='black', linewidth=2)
    ax.add_patch(room)

    # Mark AC
    ax.plot(ac_x, ac_y, 'ko')
    ax.text(ac_x, ac_y, " AC", color='black')

    ax.set_xlim(0, length)
    ax.set_ylim(0, width)
    ax.set_title(f"Cooling Distribution ({placement})")

    plt.colorbar(heatmap, ax=ax, label="Cooling Intensity")

    return fig