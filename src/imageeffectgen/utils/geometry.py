"""Geometric utilities for creating jigsaw patterns."""

import numpy as np
from typing import List, Tuple
import cv2


def create_jigsaw_piece(
    x: int,
    y: int,
    width: int,
    height: int,
    tab_size: float = 0.2,
    tabs: Tuple[bool, bool, bool, bool] = (False, False, False, False)
) -> np.ndarray:
    """
    Create a single jigsaw puzzle piece with interlocking tabs and blanks.

    Args:
        x, y: Top-left corner position
        width, height: Piece dimensions
        tab_size: Size of tabs/blanks as fraction of piece size (default: 0.2)
        tabs: (top, right, bottom, left) - True for tab (out), False for blank (in)

    Returns:
        Array of polygon points defining the piece shape
    """
    points = []
    tab_top, tab_right, tab_bottom, tab_left = tabs

    # Tab parameters - make them more circular/rounded
    tab_radius_w = width * tab_size
    tab_radius_h = height * tab_size

    # Helper function to create a rounded tab or blank
    def create_semicircle(cx, cy, radius, angle_start, angle_end, num_points=10):
        """Create points for a semicircular tab or blank."""
        angles = np.linspace(angle_start, angle_end, num_points)
        pts = []
        for angle in angles:
            px = cx + radius * np.cos(angle)
            py = cy + radius * np.sin(angle)
            pts.append([px, py])
        return pts

    # TOP EDGE
    points.append([x, y])

    if tab_top:
        # Tab sticks UP (semicircle above the edge)
        points.append([x + width * 0.35, y])
        # Semicircle going up
        tab_center_x = x + width * 0.5
        tab_center_y = y - tab_radius_h * 0.5
        circle_pts = create_semicircle(tab_center_x, tab_center_y, tab_radius_h, np.pi, 2*np.pi, 12)
        points.extend(circle_pts)
        points.append([x + width * 0.65, y])
    else:
        # Blank cuts DOWN (semicircle below the edge)
        points.append([x + width * 0.35, y])
        # Semicircle going down
        tab_center_x = x + width * 0.5
        tab_center_y = y + tab_radius_h * 0.5
        circle_pts = create_semicircle(tab_center_x, tab_center_y, tab_radius_h, 0, np.pi, 12)
        points.extend(circle_pts)
        points.append([x + width * 0.65, y])

    points.append([x + width, y])

    # RIGHT EDGE
    if tab_right:
        # Tab sticks RIGHT
        points.append([x + width, y + height * 0.35])
        tab_center_x = x + width + tab_radius_w * 0.5
        tab_center_y = y + height * 0.5
        circle_pts = create_semicircle(tab_center_x, tab_center_y, tab_radius_w, np.pi * 0.5, np.pi * 1.5, 12)
        points.extend(circle_pts)
        points.append([x + width, y + height * 0.65])
    else:
        # Blank cuts LEFT
        points.append([x + width, y + height * 0.35])
        tab_center_x = x + width - tab_radius_w * 0.5
        tab_center_y = y + height * 0.5
        circle_pts = create_semicircle(tab_center_x, tab_center_y, tab_radius_w, -np.pi * 0.5, np.pi * 0.5, 12)
        points.extend(circle_pts)
        points.append([x + width, y + height * 0.65])

    points.append([x + width, y + height])

    # BOTTOM EDGE
    if tab_bottom:
        # Tab sticks DOWN
        points.append([x + width * 0.65, y + height])
        tab_center_x = x + width * 0.5
        tab_center_y = y + height + tab_radius_h * 0.5
        circle_pts = create_semicircle(tab_center_x, tab_center_y, tab_radius_h, 2*np.pi, 3*np.pi, 12)
        points.extend(circle_pts)
        points.append([x + width * 0.35, y + height])
    else:
        # Blank cuts UP
        points.append([x + width * 0.65, y + height])
        tab_center_x = x + width * 0.5
        tab_center_y = y + height - tab_radius_h * 0.5
        circle_pts = create_semicircle(tab_center_x, tab_center_y, tab_radius_h, np.pi, 2*np.pi, 12)
        points.extend(circle_pts)
        points.append([x + width * 0.35, y + height])

    points.append([x, y + height])

    # LEFT EDGE
    if tab_left:
        # Tab sticks LEFT
        points.append([x, y + height * 0.65])
        tab_center_x = x - tab_radius_w * 0.5
        tab_center_y = y + height * 0.5
        circle_pts = create_semicircle(tab_center_x, tab_center_y, tab_radius_w, -np.pi * 0.5, np.pi * 0.5, 12)
        points.extend(circle_pts)
        points.append([x, y + height * 0.35])
    else:
        # Blank cuts RIGHT
        points.append([x, y + height * 0.65])
        tab_center_x = x + tab_radius_w * 0.5
        tab_center_y = y + height * 0.5
        circle_pts = create_semicircle(tab_center_x, tab_center_y, tab_radius_w, np.pi * 0.5, np.pi * 1.5, 12)
        points.extend(circle_pts)
        points.append([x, y + height * 0.35])

    return np.array(points, dtype=np.int32)


def create_jigsaw_grid(
    width: int,
    height: int,
    piece_size: int = 50,
    overlap: float = 0
) -> List[Tuple[np.ndarray, Tuple[int, int, int, int]]]:
    """
    Create a grid of interlocking jigsaw puzzle pieces.

    Args:
        width: Image width
        height: Image height
        piece_size: Size of each puzzle piece
        overlap: Not used for jigsaw, kept for compatibility

    Returns:
        List of (polygon, bbox) tuples where bbox is (x, y, w, h)
    """
    pieces = []

    # Calculate grid dimensions
    cols = max(2, width // piece_size)
    rows = max(2, height // piece_size)

    # Calculate actual piece dimensions
    piece_w = width / cols
    piece_h = height / rows

    # Create tab pattern (deterministic but varied)
    np.random.seed(42)  # Fixed seed for consistency
    tab_pattern = np.random.choice([True, False], size=(rows, cols, 4))

    # Ensure interlocking: if one piece has a tab, neighbor must have a blank
    for row in range(rows):
        for col in range(cols):
            # Check right neighbor
            if col < cols - 1:
                if tab_pattern[row, col, 1]:  # If this has right tab
                    tab_pattern[row, col + 1, 3] = False  # Neighbor must have left blank
                else:
                    tab_pattern[row, col + 1, 3] = True  # Neighbor must have left tab

            # Check bottom neighbor
            if row < rows - 1:
                if tab_pattern[row, col, 2]:  # If this has bottom tab
                    tab_pattern[row + 1, col, 0] = False  # Neighbor must have top blank
                else:
                    tab_pattern[row + 1, col, 0] = True  # Neighbor must have top tab

    # Generate pieces
    for row in range(rows):
        for col in range(cols):
            x = int(col * piece_w)
            y = int(row * piece_h)
            w = int(piece_w)
            h = int(piece_h)

            # Edge pieces don't have tabs on edges
            tabs = list(tab_pattern[row, col])
            if row == 0:
                tabs[0] = False  # No top tab on top edge
            if col == cols - 1:
                tabs[1] = False  # No right tab on right edge
            if row == rows - 1:
                tabs[2] = False  # No bottom tab on bottom edge
            if col == 0:
                tabs[3] = False  # No left tab on left edge

            piece = create_jigsaw_piece(x, y, w, h, tab_size=0.15, tabs=tuple(tabs))
            bbox = (x, y, w, h)
            pieces.append((piece, bbox))

    return pieces


def create_organic_blob(
    center: Tuple[int, int],
    base_radius: float,
    num_points: int = 8,
    randomness: float = 0.3
) -> np.ndarray:
    """
    Create an organic blob shape resembling a jigsaw piece.

    Args:
        center: (x, y) center point
        base_radius: Base radius of the blob
        num_points: Number of control points
        randomness: Amount of randomness (0-1)

    Returns:
        Array of polygon points
    """
    cx, cy = center
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)

    # Add randomness to radius
    np.random.seed(int(cx * cy) % 10000)  # Deterministic randomness based on position
    radii = base_radius * (1 + randomness * (np.random.rand(num_points) - 0.5))

    # Create points
    points = []
    for angle, radius in zip(angles, radii):
        x = cx + radius * np.cos(angle)
        y = cy + radius * np.sin(angle)
        points.append([x, y])

    return np.array(points, dtype=np.int32)


def smooth_polygon(points: np.ndarray, iterations: int = 2) -> np.ndarray:
    """
    Smooth a polygon by averaging adjacent points.

    Args:
        points: Array of polygon points
        iterations: Number of smoothing iterations

    Returns:
        Smoothed polygon points
    """
    smoothed = points.copy().astype(float)

    for _ in range(iterations):
        new_points = np.zeros_like(smoothed)
        n = len(smoothed)
        for i in range(n):
            prev_pt = smoothed[(i - 1) % n]
            curr_pt = smoothed[i]
            next_pt = smoothed[(i + 1) % n]
            # Average with neighbors
            new_points[i] = (prev_pt + 2 * curr_pt + next_pt) / 4
        smoothed = new_points

    return smoothed.astype(np.int32)


def create_wavy_edge(
    start: Tuple[int, int],
    end: Tuple[int, int],
    num_waves: int = 3,
    amplitude: float = 5.0
) -> np.ndarray:
    """
    Create a wavy line between two points.

    Args:
        start: Start point (x, y)
        end: End point (x, y)
        num_waves: Number of waves
        amplitude: Wave amplitude

    Returns:
        Array of points forming the wavy line
    """
    x1, y1 = start
    x2, y2 = end

    # Calculate perpendicular direction
    dx = x2 - x1
    dy = y2 - y1
    length = np.sqrt(dx**2 + dy**2)

    if length == 0:
        return np.array([[x1, y1]], dtype=np.int32)

    # Perpendicular unit vector
    perp_x = -dy / length
    perp_y = dx / length

    # Create points along the line
    num_points = max(int(length / 5), 10)
    t_values = np.linspace(0, 1, num_points)

    points = []
    for t in t_values:
        # Base point on line
        x = x1 + t * dx
        y = y1 + t * dy

        # Add wave offset
        wave = amplitude * np.sin(t * num_waves * 2 * np.pi)
        x += wave * perp_x
        y += wave * perp_y

        points.append([x, y])

    return np.array(points, dtype=np.int32)


def create_puzzle_piece_shape(
    bounds: Tuple[int, int, int, int],
    seed: int = 0
) -> np.ndarray:
    """
    Create a puzzle piece shape with interlocking tabs.

    Args:
        bounds: (x, y, width, height) bounding box
        seed: Random seed for reproducibility

    Returns:
        Array of polygon points
    """
    x, y, w, h = bounds
    np.random.seed(seed)

    # Define corners
    corners = [
        (x, y),
        (x + w, y),
        (x + w, y + h),
        (x, y + h)
    ]

    points = []
    for i in range(4):
        start = corners[i]
        end = corners[(i + 1) % 4]

        # Create wavy edge
        edge_points = create_wavy_edge(
            start, end,
            num_waves=2 + i % 2,
            amplitude=3 + np.random.rand() * 3
        )
        points.extend(edge_points[:-1])  # Exclude last point to avoid duplicates

    return smooth_polygon(np.array(points, dtype=np.int32), iterations=1)

