import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# --- CONFIGURATION ---
surf = None
wire = None
ASSET_COUNT = 30  # Number of assets (X/Y grid size)
LANDSCAPE_SCALE = 2.5  # Controls Z height scaling
ANIMATION_INTERVAL = 40  # ms per frame

# --- DATA GENERATION ---
def generate_correlation_energy(t):
    """
    Generate a synthetic correlation energy landscape.
    Args:
        t (float): Time parameter for animation.
    Returns:
        X, Y, Z: Meshgrid arrays for surface plot.
    """
    x = np.linspace(-1, 1, ASSET_COUNT)
    y = np.linspace(-1, 1, ASSET_COUNT)
    X, Y = np.meshgrid(x, y)
    # Simulate evolving cross-asset correlation energy
    # Use a sum of smooth waves modulated by time
    Z = (
        np.sin(2 * np.pi * X + t * 0.7) * np.cos(2 * np.pi * Y - t * 0.5) +
        0.5 * np.sin(3 * np.pi * X * Y + t * 0.3) +
        0.3 * np.cos(4 * np.pi * Y - t * 0.9)
    ) * LANDSCAPE_SCALE
    # Add a slow global morph for realism
    Z += 0.7 * np.sin(t * 0.2 + X * Y)
    return X, Y, Z

# --- PLOT INITIALIZATION ---
def init_plot():
    """
    Set up the 3D plot with black background and neon accents.
    Returns:
        fig, ax, surf: Figure, axis, and surface objects.
    """
    fig = plt.figure(figsize=(10, 8), facecolor='black')
    ax = fig.add_subplot(111, projection='3d', facecolor='black')
    # Set black background for the whole plot
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    # White wireframe box/grid
    ax.grid(True, color='white', linewidth=0.5, alpha=0.3)
    # Set axis line colors (modern matplotlib)
    ax.xaxis._axinfo['grid']['color'] =  (1,1,1,0.3)
    ax.yaxis._axinfo['grid']['color'] =  (1,1,1,0.3)
    ax.zaxis._axinfo['grid']['color'] =  (1,1,1,0.3)
    # Set axis labels
    ax.set_xlabel('Asset X', color='white', fontsize=12)
    ax.set_ylabel('Asset Y', color='white', fontsize=12)
    ax.set_zlabel('Correlation Energy', color='white', fontsize=12)
    # Set tick params
    ax.tick_params(colors='white', which='both')
    # Set axis limits
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-LANDSCAPE_SCALE * 2, LANDSCAPE_SCALE * 2)
    # No initial surface; will be drawn in update()
    surf = None
    wire = None
    # Remove panes and spines for a clean look
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.xaxis.pane.set_edgecolor('white')
    ax.yaxis.pane.set_edgecolor('white')
    ax.zaxis.pane.set_edgecolor('white')
    ax.xaxis.pane.set_alpha(0.0)
    ax.yaxis.pane.set_alpha(0.0)
    ax.zaxis.pane.set_alpha(0.0)
    # Title
    ax.set_title('Correlation Energy Landscape', color='#C800FF', fontsize=16, pad=20)
    return fig, ax, surf

# --- ANIMATION UPDATE ---
def update(frame):
    """
    Update the surface for each animation frame.
    Args:
        frame (int): Frame number.
    """
    global surf, wire, ax
    t = frame * 0.07
    X, Y, Z = generate_correlation_energy(t)
    if surf is not None:
        surf.remove()
    if wire is not None:
        wire.remove()
    # Draw new surface
    surf = ax.plot_surface(
        X, Y, Z,
        rstride=1, cstride=1,
        cmap=cm.magma,
        edgecolor='none',
        antialiased=True,
        alpha=0.7
    )
    # Neon wireframe accent
    wire = ax.plot_wireframe(X, Y, Z, color='#C800FF', linewidth=0.2, alpha=0.25)
    return surf,

# --- MAIN EXECUTION ---
surf = None
wire = None

if __name__ == "__main__":
    fig, ax, _ = init_plot()
    ani = FuncAnimation(
        fig, update, frames=1000, interval=ANIMATION_INTERVAL, blit=False
    )
    plt.show()
