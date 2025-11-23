"""Geometric utilities for creating jigsaw patterns."""

import numpy as np
from typing import List, Tuple
import cv2


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


def create_jigsaw_grid(
    width: int,
    height: int,
    piece_size: int = 40,
    overlap: float = 0.2
) -> List[np.ndarray]:
    """
    Create a grid of overlapping jigsaw-like shapes.

    Args:
        width: Image width
        height: Image height
        piece_size: Approximate size of each piece
        overlap: Overlap factor (0-1)

    Returns:
        List of polygon arrays
    """
    polygons = []
    step = int(piece_size * (1 - overlap))
    base_radius = piece_size / 2

    rows = (height // step) + 2
    cols = (width // step) + 2

    for row in range(rows):
        for col in range(cols):
            # Offset every other row for organic feel
            offset_x = step // 2 if row % 2 == 1 else 0
            cx = col * step + offset_x
            cy = row * step

            # Skip if completely outside image
            if cx > width + piece_size or cy > height + piece_size:
                continue
            if cx < -piece_size or cy < -piece_size:
                continue

            # Create organic blob
            blob = create_organic_blob(
                (cx, cy),
                base_radius,
                num_points=6 + (row + col) % 3,  # Vary number of points
                randomness=0.4
            )
            polygons.append(blob)

    return polygons


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
