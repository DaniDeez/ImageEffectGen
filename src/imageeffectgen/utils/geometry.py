"""Geometric utilities for creating jigsaw patterns."""

import numpy as np
from typing import List, Tuple
import cv2


def create_jigsaw_piece(
    x: int,
    y: int,
    width: int,
    height: int,
    tab_size: float = 0.3,
    tabs: Tuple[bool, bool, bool, bool] = (False, False, False, False)
) -> np.ndarray:
    """
    Create an interlocking jigsaw puzzle piece with tabs and blanks.

    Each piece has rounded protrusions (tabs) and indentations (blanks) that
    interlock with adjacent pieces, mimicking real puzzle pieces.

    Args:
        x, y: Top-left corner position
        width, height: Piece dimensions
        tab_size: Size of tab/blank as fraction of piece size (default: 0.3)
        tabs: Tuple of (top, right, bottom, left) booleans
              True = tab (protrusion out), False = blank (indentation in)
              None values result in flat edge (for border pieces)

    Returns:
        Array of polygon points defining the piece shape
    """
    points = []

    # Tab/blank dimensions
    tab_depth = min(width, height) * tab_size
    tab_width = min(width, height) * 0.4  # Width of the tab/blank along the edge

    # Number of points for smooth curves
    num_curve_points = 12

    # Corner radius for rounded corners (more prominent rounding)
    corner_radius = min(width, height) * 0.2

    def add_rounded_corner(px, py, radius, start_angle, end_angle):
        """Add a rounded corner."""
        angles = np.linspace(start_angle, end_angle, 8)
        for angle in angles:
            points.append([
                px + radius * np.cos(angle),
                py + radius * np.sin(angle)
            ])

    def add_tab_or_blank(edge_start, edge_end, is_tab, perpendicular_out):
        """Add a tab (protrusion) or blank (indentation) to an edge."""
        # Edge direction
        edge_vec = np.array(edge_end) - np.array(edge_start)
        edge_length = np.linalg.norm(edge_vec)
        edge_dir = edge_vec / edge_length if edge_length > 0 else np.array([1, 0])

        # Perpendicular direction (pointing out from piece)
        perp_dir = np.array(perpendicular_out)

        # Start of edge
        start_pt = np.array(edge_start)

        # Position along edge where tab/blank starts and ends
        tab_start_t = 0.5 - (tab_width / edge_length) / 2
        tab_end_t = 0.5 + (tab_width / edge_length) / 2

        # Points before tab/blank
        t_before = np.linspace(0, tab_start_t, 3)
        for t in t_before[:-1]:  # Exclude last to avoid duplicate
            pt = start_pt + t * edge_vec
            points.append(pt)

        # Tab/blank center position
        center_t = 0.5
        center_pt = start_pt + center_t * edge_vec

        # Create tab (outward) or blank (inward)
        depth = tab_depth if is_tab else -tab_depth

        # Base points where tab/blank meets the edge
        tab_start_pt = start_pt + tab_start_t * edge_vec
        tab_end_pt = start_pt + tab_end_t * edge_vec

        # Control point for the curve (tip of tab or deepest point of blank)
        control_pt = center_pt + depth * perp_dir

        # Create smooth curve using circular arc approximation
        # Left side of tab/blank
        angles_left = np.linspace(0, np.pi / 2, num_curve_points // 2)
        for i, angle in enumerate(angles_left):
            # Bezier-like curve from tab_start to control point
            t = i / (len(angles_left) - 1)
            # Smooth interpolation
            curve_pt = (1 - t)**2 * tab_start_pt + 2 * (1 - t) * t * (tab_start_pt + control_pt) / 2 + t**2 * control_pt
            points.append(curve_pt)

        # Right side of tab/blank (mirror)
        angles_right = np.linspace(np.pi / 2, np.pi, num_curve_points // 2)
        for i, angle in enumerate(angles_right):
            t = i / (len(angles_right) - 1)
            curve_pt = (1 - t)**2 * control_pt + 2 * (1 - t) * t * (tab_end_pt + control_pt) / 2 + t**2 * tab_end_pt
            points.append(curve_pt)

        # Points after tab/blank
        t_after = np.linspace(tab_end_t, 1.0, 3)
        for t in t_after[1:]:  # Skip first to avoid duplicate
            pt = start_pt + t * edge_vec
            points.append(pt)

    # Define the four corners with rounded edges
    top_left = (x + corner_radius, y + corner_radius)
    top_right = (x + width - corner_radius, y + corner_radius)
    bottom_right = (x + width - corner_radius, y + height - corner_radius)
    bottom_left = (x + corner_radius, y + height - corner_radius)

    # TOP EDGE (with optional tab/blank)
    has_top = tabs[0] if tabs[0] is not None else None
    if has_top is None:
        # Flat edge
        points.append([x + corner_radius, y])
        points.append([x + width - corner_radius, y])
    else:
        add_tab_or_blank(
            [x + corner_radius, y],
            [x + width - corner_radius, y],
            is_tab=has_top,
            perpendicular_out=[0, -1]  # Up
        )

    # Top-right corner
    add_rounded_corner(x + width - corner_radius, y + corner_radius, corner_radius, -np.pi/2, 0)

    # RIGHT EDGE (with optional tab/blank)
    has_right = tabs[1] if tabs[1] is not None else None
    if has_right is None:
        points.append([x + width, y + corner_radius])
        points.append([x + width, y + height - corner_radius])
    else:
        add_tab_or_blank(
            [x + width, y + corner_radius],
            [x + width, y + height - corner_radius],
            is_tab=has_right,
            perpendicular_out=[1, 0]  # Right
        )

    # Bottom-right corner
    add_rounded_corner(x + width - corner_radius, y + height - corner_radius, corner_radius, 0, np.pi/2)

    # BOTTOM EDGE (with optional tab/blank)
    has_bottom = tabs[2] if tabs[2] is not None else None
    if has_bottom is None:
        points.append([x + width - corner_radius, y + height])
        points.append([x + corner_radius, y + height])
    else:
        add_tab_or_blank(
            [x + width - corner_radius, y + height],
            [x + corner_radius, y + height],
            is_tab=has_bottom,
            perpendicular_out=[0, 1]  # Down
        )

    # Bottom-left corner
    add_rounded_corner(x + corner_radius, y + height - corner_radius, corner_radius, np.pi/2, np.pi)

    # LEFT EDGE (with optional tab/blank)
    has_left = tabs[3] if tabs[3] is not None else None
    if has_left is None:
        points.append([x, y + height - corner_radius])
        points.append([x, y + corner_radius])
    else:
        add_tab_or_blank(
            [x, y + height - corner_radius],
            [x, y + corner_radius],
            is_tab=has_left,
            perpendicular_out=[-1, 0]  # Left
        )

    # Top-left corner
    add_rounded_corner(x + corner_radius, y + corner_radius, corner_radius, np.pi, 3*np.pi/2)

    return np.array(points, dtype=np.float32).astype(np.int32)


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

            piece = create_jigsaw_piece(x, y, w, h, tab_size=0.25, tabs=tuple(tabs))
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

