"""Base class for all image filters."""

from abc import ABC, abstractmethod
from typing import Any, Dict
import numpy as np
from PIL import Image


class BaseFilter(ABC):
    """Abstract base class for image filters."""

    def __init__(self, **kwargs):
        """
        Initialize the filter with optional parameters.

        Args:
            **kwargs: Filter-specific parameters
        """
        self.params = kwargs

    @abstractmethod
    def apply(self, image: Image.Image) -> Image.Image:
        """
        Apply the filter to an image.

        Args:
            image: Input PIL Image

        Returns:
            Filtered PIL Image
        """
        pass

    def validate_image(self, image: Image.Image) -> None:
        """
        Validate input image.

        Args:
            image: Input PIL Image

        Raises:
            ValueError: If image is invalid
        """
        if not isinstance(image, Image.Image):
            raise ValueError("Input must be a PIL Image")

        if image.size[0] < 1 or image.size[1] < 1:
            raise ValueError("Image dimensions must be positive")

    def to_numpy(self, image: Image.Image) -> np.ndarray:
        """
        Convert PIL Image to numpy array.

        Args:
            image: Input PIL Image

        Returns:
            NumPy array (H, W, C)
        """
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        return np.array(image)

    def to_pil(self, array: np.ndarray) -> Image.Image:
        """
        Convert numpy array to PIL Image.

        Args:
            array: NumPy array (H, W, C)

        Returns:
            PIL Image
        """
        # Ensure uint8 type
        if array.dtype != np.uint8:
            array = np.clip(array, 0, 255).astype(np.uint8)
        return Image.fromarray(array, mode='RGB')

    def get_param(self, key: str, default: Any = None) -> Any:
        """
        Get a parameter value.

        Args:
            key: Parameter name
            default: Default value if not found

        Returns:
            Parameter value
        """
        return self.params.get(key, default)
