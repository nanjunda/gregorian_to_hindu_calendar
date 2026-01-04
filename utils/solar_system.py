"""
Solar System View Generator for Hindu Panchanga v4.0 Cosmic Context
Generates a heliocentric (Sun-centered) top-down view of the solar system.

This module visualizes planetary alignments by plotting their positions 
on a normalized ecliptic plane.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import hashlib
import os
from pathlib import Path
from utils.astronomy import eph, sun, ts

planets_map = {
    "Mercury": eph['mercury'],
    "Venus": eph['venus'],
    "Earth": eph['earth'],
    "Mars": eph['mars'],
    "Jupiter": eph['jupiter barycenter'],
    "Saturn": eph['saturn barycenter']
}

CACHE_DIR = Path("static/solar_systems")

def get_cache_key(date_str: str, time_str: str):
    """Heliocentric view only depends on date/time, not observer location."""
    data = f"solar-{date_str}-{time_str}"
    return hashlib.md5(data.encode()).hexdigest()[:12]

def get_cached_image(cache_key: str):
    image_path = CACHE_DIR / f"{cache_key}.png"
    if image_path.exists():
        return str(image_path)
    return None

def generate_solar_system(utc_dt, output_path, event_title=None):
    """
    Generate a top-down heliocentric view of the solar system.
    """
    # Ensure cache directory exists
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    t = ts.from_datetime(utc_dt)
    
    positions = {}
    for name, body in planets_map.items():
        # Get position relative to sun
        astrometric = sun.at(t).observe(body)
        # We want the x, y in the ecliptic plane
        # skyfield's ecliptic_position() returns distance in AU, and angles
        # We can also get cartesian coordinates in the ecliptic frame
        from skyfield.framelib import ecliptic_frame
        pos = astrometric.frame_xyz(ecliptic_frame).au
        positions[name] = (pos[0], pos[1]) # X, Y coordinates

    # Setup Plot - Thread Safe
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    
    fig = Figure(figsize=(15.0, 15.0), facecolor='#0a0a0f')
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111, facecolor='#0a0a0f')
    
    # Sun at center with glow
    import matplotlib.patches as patches
    for r_glow in [0.2, 0.1]:
        glow = patches.Circle((0, 0), r_glow, color='#ffcc00', alpha=0.3, zorder=9)
        ax.add_patch(glow)
    ax.plot(0, 0, 'o', markersize=24, color='#ffcc00', 
            markeredgecolor='#ffffff', markeredgewidth=1.5, label='Sun', zorder=10)
    ax.text(0, -0.5, 'SUN', color='#ffffff', ha='center', fontsize=14, fontweight='bold')

    # Orbit Radii for visualization
    colors = {
        "Mercury": "#9b9b9b",
        "Venus": "#f3d299",
        "Earth": "#4a90d9",
        "Mars": "#e94560",
        "Jupiter": "#d39c7e",
        "Saturn": "#c5ab6e"
    }
    
    symbols = {
        "Mercury": "☿", "Venus": "♀", "Earth": "⊕", 
        "Mars": "♂", "Jupiter": "♃", "Saturn": "♄"
    }

    # Normalize distances for a better visual (inner vs outer)
    def scale_pos(x, y):
        dist = np.sqrt(x**2 + y**2)
        if dist == 0: return 0, 0
        # Refined scaling for better inner planetary visibility
        scaled_dist = 1.2 * (dist ** 0.55) 
        factor = scaled_dist / dist
        return x * factor, y * factor

    # Draw Orbits and Planets
    max_r = 0
    for name, (x, y) in positions.items():
        sx, sy = scale_pos(x, y)
        r = np.sqrt(sx**2 + sy**2)
        max_r = max(max_r, r)
        
        # Draw Orbit circle - more prominent
        circle = patches.Circle((0, 0), r, color='#444455', fill=False, linestyle='-', alpha=0.2, linewidth=1)
        ax.add_patch(circle)
        
        # Add Colored Symbol as the Marker (Replacement for circle)
        ax.text(sx, sy, symbols[name], color=colors[name], ha='center', va='center', 
                fontsize=24, fontweight='bold', zorder=15)
        
        # Add Name label next to symbol - Adaptive offsetting
        # If planet is on the right half, label to the right. If left, label to the left.
        ha = 'left' if sx >= 0 else 'right'
        offset = 0.4 if sx >= 0 else -0.4
        ax.text(sx + offset, sy, name.upper(), color=colors[name], 
                ha=ha, va='center', fontsize=14, fontweight='bold', zorder=15)

    # Styling
    padding = 1.2
    ax.set_xlim(-max_r * padding, max_r * padding)
    ax.set_ylim(-max_r * padding, max_r * padding)
    ax.set_aspect('equal')
    ax.axis('off')

    # Grid background (faint stars) - 50 random points
    np.random.seed(42)
    stars_x = np.random.uniform(-max_r*padding, max_r*padding, 50)
    stars_y = np.random.uniform(-max_r*padding, max_r*padding, 50)
    ax.scatter(stars_x, stars_y, s=1, color='#ffffff', alpha=0.2, zorder=1)

    # Titles
    fig.suptitle("PLANETARY ALIGNMENTS AT BIRTH", color='#ffffff', fontsize=20, fontweight='bold', y=0.94, fontfamily='sans-serif')
    if event_title:
        fig.text(0.5, 0.90, f'"{event_title}"', color='#ff9100', fontsize=13, ha='center', fontfamily='sans-serif')
    
    # Save the figure with padding
    fig.savefig(output_path, dpi=130, bbox_inches='tight', facecolor='#0a0a0f', pad_inches=0.5)
    return output_path
