"""Jigsaw Folk Art Filter - transforms images into puzzle-piece folk art style."""

import numpy as np
import cv2
from PIL import Image, ImageDraw
from typing import Optional, Tuple, List
from skimage import segmentation, color
from scipy import ndimage

from ..core.base_filter import BaseFilter
from ..utils.color import (
    quantize_colors,
    flatten_colors,
    create_folk_palette,
    map_to_palette,
    get_dominant_color
)
from ..utils.geometry import (
    create_jigsaw_grid,
    smooth_polygon,
    create_organic_blob
)


class JigsawFolkFilter(BaseFilter):
    """
    Transforms images into jigsaw puzzle folk art style.

    The filter creates organic, interlocking blob shapes with flat colors
    reminiscent of hand-painted folk art merged with puzzle piece aesthetics.

    Parameters:
        piece_size: Size of jigsaw pieces (default: 50)
        n_colors: Number of colors to reduce to (default: 16)
        use_folk_palette: Use traditional folk art colors (default: True)
        smoothness: Smoothness of piece edges (default: 3)
        segmentation_scale: Scale for image segmentation (default: 100)
        add_borders: Add decorative folk art borders (default: False)
        border_pattern: Border pattern type ('flowers', 'geometric', None)
    """

    def __init__(
        self,
        piece_size: int = 50,
        n_colors: int = 16,
        use_folk_palette: bool = True,
        smoothness: int = 3,
        segmentation_scale: int = 100,
        add_borders: bool = False,
        border_pattern: Optional[str] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.piece_size = piece_size
        self.n_colors = n_colors
        self.use_folk_palette = use_folk_palette
        self.smoothness = smoothness
        self.segmentation_scale = segmentation_scale
        self.add_borders = add_borders
        self.border_pattern = border_pattern

    def apply(self, image: Image.Image) -> Image.Image:
        """
        Apply the jigsaw folk filter to an image.

        Args:
            image: Input PIL Image

        Returns:
            Filtered PIL Image with jigsaw folk art style
        """
        self.validate_image(image)

        # Convert to numpy array
        img_array = self.to_numpy(image)
        h, w = img_array.shape[:2]

        # Step 1: Simplify colors
        simplified = self._simplify_colors(img_array)

        # Step 2: Segment image to identify regions
        segments = self._segment_image(simplified)

        # Step 3: Create jigsaw pieces
        result = self._create_jigsaw_pieces(simplified, segments, w, h)

        # Step 4: Add borders if requested
        if self.add_borders:
            result = self._add_decorative_border(result)

        return self.to_pil(result)

    def _simplify_colors(self, image: np.ndarray) -> np.ndarray:
        """
        Simplify and flatten colors for folk art effect.

        Args:
            image: Input image array

        Returns:
            Color-simplified image
        """
        # First flatten similar colors
        flattened = flatten_colors(image)

        # Quantize to limited palette
        if self.use_folk_palette:
            # Create a larger quantized version first
            quantized = quantize_colors(flattened, n_colors=self.n_colors)
            # Then map to folk palette
            palette = create_folk_palette()
            result = map_to_palette(quantized, palette)
        else:
            result = quantize_colors(flattened, n_colors=self.n_colors)

        return result

    def _segment_image(self, image: np.ndarray) -> np.ndarray:
        """
        Segment image into regions using SLIC superpixels.

        Args:
            image: Input image array

        Returns:
            Segmentation map
        """
        # Use SLIC to create superpixels
        segments = segmentation.slic(
            image,
            n_segments=self.segmentation_scale,
            compactness=10,
            sigma=1,
            start_label=1
        )
        return segments

    def _create_jigsaw_pieces(
        self,
        image: np.ndarray,
        segments: np.ndarray,
        width: int,
        height: int
    ) -> np.ndarray:
        """
        Create jigsaw puzzle piece effect.

        Args:
            image: Color-simplified image
            segments: Segmentation map
            width: Image width
            height: Image height

        Returns:
            Image with jigsaw pieces
        """
        # Create output image
        output = np.ones((height, width, 3), dtype=np.uint8) * 240  # Light background

        # Generate jigsaw grid
        polygons = create_jigsaw_grid(
            width,
            height,
            piece_size=self.piece_size,
            overlap=0.15
        )

        # Create PIL Image for drawing
        pil_output = Image.fromarray(output)
        draw = ImageDraw.Draw(pil_output)

        # Draw each jigsaw piece
        for poly in polygons:
            # Smooth the polygon
            smoothed = smooth_polygon(poly, iterations=self.smoothness)

            # Create mask for this piece
            mask = np.zeros((height, width), dtype=np.uint8)
            cv2.fillPoly(mask, [smoothed], 255)

            # Find pixels in this piece
            piece_pixels = image[mask > 0]

            if len(piece_pixels) == 0:
                continue

            # Get dominant color
            piece_color = get_dominant_color(piece_pixels)

            # Draw filled polygon
            poly_list = [(int(x), int(y)) for x, y in smoothed]
            draw.polygon(poly_list, fill=piece_color, outline=None)

        # Convert back to array
        result = np.array(pil_output)

        # Add subtle outlines to pieces
        result = self._add_piece_outlines(result, polygons)

        return result

    def _add_piece_outlines(
        self,
        image: np.ndarray,
        polygons: List[np.ndarray],
        outline_color: Tuple[int, int, int] = (80, 80, 80),
        outline_width: int = 1
    ) -> np.ndarray:
        """
        Add subtle outlines to jigsaw pieces.

        Args:
            image: Input image
            polygons: List of polygon shapes
            outline_color: Color for outlines
            outline_width: Width of outlines

        Returns:
            Image with outlines
        """
        result = image.copy()

        for poly in polygons:
            smoothed = smooth_polygon(poly, iterations=self.smoothness)
            # Draw outline
            cv2.polylines(
                result,
                [smoothed],
                isClosed=True,
                color=outline_color,
                thickness=outline_width
            )

        return result

    def _add_decorative_border(
        self,
        image: np.ndarray,
        border_width: int = 60
    ) -> np.ndarray:
        """
        Add decorative folk art border around the image.

        Args:
            image: Input image
            border_width: Width of border

        Returns:
            Image with decorative border
        """
        h, w = image.shape[:2]
        new_h = h + 2 * border_width
        new_w = w + 2 * border_width

        # Create bordered image with light background
        bordered = np.ones((new_h, new_w, 3), dtype=np.uint8) * 245
        bordered[border_width:border_width + h, border_width:border_width + w] = image

        # Add simple decorative elements
        if self.border_pattern == 'flowers':
            bordered = self._add_flower_border(bordered, border_width)
        elif self.border_pattern == 'geometric':
            bordered = self._add_geometric_border(bordered, border_width)

        return bordered

    def _add_flower_border(
        self,
        image: np.ndarray,
        border_width: int
    ) -> np.ndarray:
        """
        Add flower pattern border.

        Args:
            image: Input image with border space
            border_width: Width of border

        Returns:
            Image with flower border
        """
        h, w = image.shape[:2]
        pil_img = Image.fromarray(image)
        draw = ImageDraw.Draw(pil_img)

        # Color palette
        colors = [
            (220, 47, 2),      # Red
            (255, 138, 0),     # Orange
            (255, 215, 0),     # Yellow
            (34, 139, 34),     # Green
            (231, 76, 60),     # Bright red
        ]

        # Draw simple flower shapes along top and bottom
        flower_size = border_width // 3
        spacing = flower_size * 2

        for position in range(0, w, spacing):
            # Top border
            cx = position + spacing // 2
            cy = border_width // 2

            # Draw simple 4-petal flower
            petal_color = colors[int(position / spacing) % len(colors)]
            center_color = (255, 215, 0)  # Yellow center

            # Create organic flower blob
            blob = create_organic_blob(
                (cx, cy),
                flower_size / 2,
                num_points=4,
                randomness=0.3
            )
            poly_list = [(int(x), int(y)) for x, y in blob]
            draw.polygon(poly_list, fill=petal_color)

            # Center
            draw.ellipse(
                [cx - flower_size//4, cy - flower_size//4,
                 cx + flower_size//4, cy + flower_size//4],
                fill=center_color
            )

            # Bottom border
            cy = h - border_width // 2
            blob = create_organic_blob(
                (cx, cy),
                flower_size / 2,
                num_points=4,
                randomness=0.3
            )
            poly_list = [(int(x), int(y)) for x, y in blob]
            draw.polygon(poly_list, fill=petal_color)
            draw.ellipse(
                [cx - flower_size//4, cy - flower_size//4,
                 cx + flower_size//4, cy + flower_size//4],
                fill=center_color
            )

        # Add vine-like elements
        vine_color = (34, 139, 34)  # Green
        for y_pos in [border_width // 2, h - border_width // 2]:
            points = []
            for x in range(0, w, 10):
                wave = int(10 * np.sin(x / 30))
                points.append((x, y_pos + wave))
            if len(points) > 1:
                draw.line(points, fill=vine_color, width=3)

        return np.array(pil_img)

    def _add_geometric_border(
        self,
        image: np.ndarray,
        border_width: int
    ) -> np.ndarray:
        """
        Add geometric pattern border.

        Args:
            image: Input image with border space
            border_width: Width of border

        Returns:
            Image with geometric border
        """
        h, w = image.shape[:2]
        pil_img = Image.fromarray(image)
        draw = ImageDraw.Draw(pil_img)

        colors = [(220, 47, 2), (255, 138, 0), (34, 139, 34)]
        shape_size = border_width // 2

        # Draw alternating shapes
        for i, position in enumerate(range(0, w, shape_size)):
            color = colors[i % len(colors)]

            # Top border
            x = position + shape_size // 2
            y = border_width // 2
            blob = create_organic_blob((x, y), shape_size // 3, num_points=6, randomness=0.2)
            poly_list = [(int(px), int(py)) for px, py in blob]
            draw.polygon(poly_list, fill=color)

            # Bottom border
            y = h - border_width // 2
            blob = create_organic_blob((x, y), shape_size // 3, num_points=6, randomness=0.2)
            poly_list = [(int(px), int(py)) for px, py in blob]
            draw.polygon(poly_list, fill=color)

        return np.array(pil_img)
