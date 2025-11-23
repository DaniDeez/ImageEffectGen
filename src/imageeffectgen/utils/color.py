"""Color manipulation utilities."""

import numpy as np
from typing import List, Tuple
from sklearn.cluster import KMeans


def quantize_colors(image: np.ndarray, n_colors: int = 16) -> np.ndarray:
    """
    Reduce the number of colors in an image using k-means clustering.

    Args:
        image: Input image array (H, W, 3)
        n_colors: Number of colors to reduce to

    Returns:
        Quantized image array
    """
    h, w, c = image.shape
    pixels = image.reshape(-1, 3)

    # Use k-means to find dominant colors
    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
    labels = kmeans.fit_predict(pixels)
    centers = kmeans.cluster_centers_.astype(np.uint8)

    # Replace each pixel with its cluster center
    quantized = centers[labels]
    return quantized.reshape(h, w, c)


def get_dominant_color(pixels: np.ndarray) -> Tuple[int, int, int]:
    """
    Get the dominant color from a set of pixels.

    Args:
        pixels: Array of pixel values (N, 3)

    Returns:
        RGB tuple of dominant color
    """
    if len(pixels) == 0:
        return (128, 128, 128)  # Gray default

    # Calculate mean color
    mean_color = np.mean(pixels, axis=0).astype(int)
    return tuple(mean_color)


def flatten_colors(image: np.ndarray, threshold: int = 30) -> np.ndarray:
    """
    Flatten similar colors to create a folk art effect.

    Args:
        image: Input image array (H, W, 3)
        threshold: Color difference threshold

    Returns:
        Image with flattened colors
    """
    # Apply bilateral filter to reduce noise while preserving edges
    from cv2 import bilateralFilter
    filtered = bilateralFilter(image, 9, 75, 75)
    return filtered


def create_folk_palette() -> List[Tuple[int, int, int]]:
    """
    Create a folk art color palette.

    Returns:
        List of RGB tuples
    """
    return [
        (220, 47, 2),      # Red
        (255, 138, 0),     # Orange
        (255, 215, 0),     # Yellow
        (34, 139, 34),     # Green
        (41, 128, 185),    # Blue
        (142, 68, 173),    # Purple
        (231, 76, 60),     # Bright red
        (192, 57, 43),     # Dark red
        (211, 84, 0),      # Dark orange
        (241, 196, 15),    # Gold
        (39, 174, 96),     # Emerald
        (22, 160, 133),    # Turquoise
        (52, 152, 219),    # Sky blue
        (255, 255, 255),   # White
        (236, 240, 241),   # Light gray
        (189, 195, 199),   # Gray
        (149, 165, 166),   # Dark gray
        (127, 140, 141),   # Darker gray
    ]


def map_to_palette(image: np.ndarray, palette: List[Tuple[int, int, int]]) -> np.ndarray:
    """
    Map image colors to a specific palette.

    Args:
        image: Input image array (H, W, 3)
        palette: List of RGB tuples

    Returns:
        Image with colors mapped to palette
    """
    h, w, c = image.shape
    pixels = image.reshape(-1, 3).astype(float)
    palette_array = np.array(palette, dtype=float)

    # Find closest palette color for each pixel
    distances = np.sum((pixels[:, np.newaxis, :] - palette_array[np.newaxis, :, :]) ** 2, axis=2)
    closest_indices = np.argmin(distances, axis=1)
    mapped = palette_array[closest_indices].astype(np.uint8)

    return mapped.reshape(h, w, c)
