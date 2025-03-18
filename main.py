import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons


def main():
    # Initial Parameters
    x0_values = np.linspace(-0.02, 0.02, 5)  # Beam width; Units in meters
    k = 1  # Controls divergence; radians per meter
    default_distances = [0.1, 0.05, 0.05]  # Default distance; Units in meters
    default_focal_lengths = [0.025, 0.025]  # Default lens focal length; Units in meters

    # Interactive Graph
    fig, ax = plt.subplots(figsize=(8, 4))
    plt.subplots_adjust(left=0.3, bottom=0.4)

    # Position of checkboxes / sliders
    ax_check = plt.axes((0.03, 0.5, 0.15, 0.1))
    check_buttons = CheckButtons(ax_check, ["Lens 1", "Lens 2"], [True, True])
    ax_d1 = plt.axes((0.25, 0.25, 0.65, 0.03))
    ax_f1 = plt.axes((0.25, 0.2, 0.65, 0.03))
    ax_d2 = plt.axes((0.25, 0.15, 0.65, 0.03))
    ax_f2 = plt.axes((0.25, 0.1, 0.65, 0.03))
    ax_d3 = plt.axes((0.25, 0.05, 0.65, 0.03))

    # Sliders
    slider_d1 = Slider(ax_d1, "Distance to 1st Lens (m)", 0.005, 0.2, valinit=default_distances[0])
    slider_f1 = Slider(ax_f1, "Focal Length 1 (m)", -0.05, 0.05, valinit=default_focal_lengths[0])
    slider_d2 = Slider(ax_d2, "Distance to 2nd Lens (m)", 0.005, 0.2, valinit=default_distances[1])
    slider_f2 = Slider(ax_f2, "Focal Length 2 (m)", -0.05, 0.05, valinit=default_focal_lengths[1])
    slider_d3 = Slider(ax_d3, "Final Distance (m)", 0.005, 0.2, valinit=default_distances[2])

    def update(val):
        """
            Function to update beam path, corresponding to the values on the sliders
        """
        ax.clear()

        lens1_enabled, lens2_enabled = check_buttons.get_status()
        distances = []
        focal_lengths = []

        if lens1_enabled:
            distances.append(slider_d1.val)
            focal_lengths.append(slider_f1.val)

        if lens2_enabled:
            distances.append(slider_d2.val)
            focal_lengths.append(slider_f2.val)

        distances.append(slider_d3.val)

        for x0 in x0_values:
            theta0 = k * x0
            z_vals, x_vals = simulate_beam_path(x0, theta0, distances, focal_lengths)
            ax.plot(z_vals, x_vals, "o-")

        ax.set_xlabel("Optical Axis (z) [m]")
        ax.set_ylabel("Transverse Position (x) [m]")
        ax.set_title("Interactive Beam Path")
        ax.grid()
        fig.canvas.draw_idle()

    # Update on slider and checkbox change
    check_buttons.on_clicked(update)
    slider_d1.on_changed(update)
    slider_f1.on_changed(update)
    slider_d2.on_changed(update)
    slider_f2.on_changed(update)
    slider_d3.on_changed(update)

    # Update for initial values to show the graph
    update(None)

    plt.show()


def free_space_matrix(d):
    """
        Free space matrix
    """
    return np.array([[1, d], [0, 1]])


def thin_lens_matrix(f):
    """
        Thin lens matrix
    """
    return np.array([[1, 0], [-1 / f, 1]])


# Function to simulate beam path
def simulate_beam_path(x0, theta0, distances, focal_lengths):
    """
        Calculating the beam path, depending on the given parameters
    """
    ray = np.array([x0, theta0])
    z_vals = [0]
    x_vals = [x0]
    z_current = 0

    for i, d in enumerate(distances):
        ray = np.dot(free_space_matrix(d), ray)
        z_current += d
        z_vals.append(z_current)
        x_vals.append(ray[0])

        if i < len(focal_lengths):
            ray = np.dot(thin_lens_matrix(focal_lengths[i]), ray)
            z_vals.append(z_current)
            x_vals.append(ray[0])

    return z_vals, x_vals


if __name__ == "__main__":
    main()
