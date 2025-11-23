"""Pixel/Mosaic Filter - transforms images into pixelated art."""

import numpy as np
import cv2
from PIL import Image
from typing import Optional

from ..core.base_filter import BaseFilter


class PixelFilter(BaseFilter):
    """
    Transforms images into pixelated/mosaic art.

    Creates a retro pixel art effect by reducing image resolution
    and optionally applying color quantization.

    Parameters:
        pixel_size: Size of each pixel block (default: 10)
        quantize_colors: Whether to reduce colors (default: True)
        n_colors: Number of colors if quantizing (default: 16)
        outline: Add black outlines to pixels (default: False)
        outline_thickness: Thickness of outlines (default: 1)
    """

    def __init__(
        self,
        pixel_size: int = 10,
        quantize_colors: bool = True,
        n_colors: int = 16,
        outline: bool = False,
        outline_thickness: int = 1,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.pixel_size = max(1, pixel_size)
        self.quantize_colors = quantize_colors
        self.n_colors = n_colors
        self.outline = outline
        self.outline_thickness = outline_thickness

    def apply(self, image: Image.Image) -> Image.Image:
        """
        Apply the pixel filter to an image.

        Args:
            image: Input PIL Image

        Returns:
            Pixelated PIL Image
        """
        self.validate_image(image)

        # Convert to numpy array
        img_array = self.to_numpy(image)
        h, w = img_array.shape[:2]

        # Step 1: Pixelate by downscaling and upscaling
        pixelated = self._pixelate(img_array)

        # Step 2: Optionally quantize colors
        if self.quantize_colors:
            pixelated = self._quantize_colors(pixelated)

        # Step 3: Optionally add outlines
        if self.outline:
            pixelated = self._add_pixel_outlines(pixelated)

        return self.to_pil(pixelated)

    def _pixelate(self, image: np.ndarray) -> np.ndarray:
        """
        Create pixelated effect by downsampling and upsampling.

        Args:
            image: Input image array

        Returns:
            Pixelated image array
        """
        h, w = image.shape[:2]

        # Calculate new dimensions
        small_h = max(1, h // self.pixel_size)
        small_w = max(1, w // self.pixel_size)

        # Downscale using area interpolation (averages pixels)
        small = cv2.resize(image, (small_w, small_h), interpolation=cv2.INTER_AREA)

        # Upscale using nearest neighbor (creates sharp pixels)
        pixelated = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

        return pixelated

    def _quantize_colors(self, image: np.ndarray) -> np.ndarray:
        """
        Reduce number of colors using color quantization.

        Args:
            image: Input image array

        Returns:
            Color-quantized image
        """
        from sklearn.cluster import KMeans

        h, w, c = image.shape
        pixels = image.reshape(-1, 3)

        # Use k-means to find dominant colors
        kmeans = KMeans(n_clusters=self.n_colors, random_state=42, n_init=10)
        labels = kmeans.fit_predict(pixels)
        centers = kmeans.cluster_centers_.astype(np.uint8)

        # Replace each pixel with its cluster center
        quantized = centers[labels]
        return quantized.reshape(h, w, c)

    def _add_pixel_outlines(self, image: np.ndarray) -> np.ndarray:
        """
        Add black outlines around pixel blocks.

        Args:
            image: Input image array

        Returns:
            Image with pixel outlines
        """
        h, w = image.shape[:2]
        result = image.copy()

        # Draw vertical lines
        for x in range(0, w, self.pixel_size):
            cv2.line(
                result,
                (x, 0),
                (x, h),
                (0, 0, 0),
                self.outline_thickness
            )

        # Draw horizontal lines
        for y in range(0, h, self.pixel_size):
            cv2.line(
                result,
                (0, y),
                (w, y),
                (0, 0, 0),
                self.outline_thickness
            )

        return result


class RetroPixelFilter(PixelFilter):
    """
    Preset: Retro gaming pixel art style.

    Large pixels with limited colors for authentic retro look.
    """

    def __init__(self, **kwargs):
        super().__init__(
            pixel_size=16,
            quantize_colors=True,
            n_colors=8,
            outline=True,
            outline_thickness=1,
            **kwargs
        )


class MosaicFilter(PixelFilter):
    """
    Preset: Fine mosaic tile effect.

    Small pixels with more colors for detailed mosaic look.
    """

    def __init__(self, **kwargs):
        super().__init__(
            pixel_size=6,
            quantize_colors=True,
            n_colors=24,
            outline=True,
            outline_thickness=1,
            **kwargs
        )
