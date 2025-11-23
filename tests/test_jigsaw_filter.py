"""Tests for the Jigsaw Folk Filter."""

import unittest
import numpy as np
from PIL import Image
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from imageeffectgen import JigsawFolkFilter


class TestJigsawFolkFilter(unittest.TestCase):
    """Test cases for JigsawFolkFilter."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a simple test image
        self.test_image = Image.new('RGB', (200, 200), color=(255, 0, 0))
        # Add some color variation
        pixels = self.test_image.load()
        for i in range(100):
            for j in range(100):
                pixels[i, j] = (0, 255, 0)
        for i in range(100, 200):
            for j in range(100, 200):
                pixels[i, j] = (0, 0, 255)

    def test_filter_initialization(self):
        """Test filter can be initialized with default parameters."""
        filter_obj = JigsawFolkFilter()
        self.assertEqual(filter_obj.piece_size, 50)
        self.assertEqual(filter_obj.n_colors, 16)
        self.assertTrue(filter_obj.use_folk_palette)

    def test_filter_initialization_custom(self):
        """Test filter can be initialized with custom parameters."""
        filter_obj = JigsawFolkFilter(
            piece_size=30,
            n_colors=20,
            use_folk_palette=False,
            smoothness=5
        )
        self.assertEqual(filter_obj.piece_size, 30)
        self.assertEqual(filter_obj.n_colors, 20)
        self.assertFalse(filter_obj.use_folk_palette)
        self.assertEqual(filter_obj.smoothness, 5)

    def test_filter_apply(self):
        """Test filter can be applied to an image."""
        filter_obj = JigsawFolkFilter(piece_size=40, n_colors=8)
        result = filter_obj.apply(self.test_image)

        # Check result is a PIL Image
        self.assertIsInstance(result, Image.Image)

        # Check dimensions are same or larger (if borders added)
        self.assertGreaterEqual(result.size[0], self.test_image.size[0])
        self.assertGreaterEqual(result.size[1], self.test_image.size[1])

    def test_filter_with_borders(self):
        """Test filter with decorative borders."""
        filter_obj = JigsawFolkFilter(
            add_borders=True,
            border_pattern='flowers'
        )
        result = filter_obj.apply(self.test_image)

        # Result should be larger due to borders
        self.assertGreater(result.size[0], self.test_image.size[0])
        self.assertGreater(result.size[1], self.test_image.size[1])

    def test_validate_image(self):
        """Test image validation."""
        filter_obj = JigsawFolkFilter()

        # Valid image should not raise
        filter_obj.validate_image(self.test_image)

        # Invalid input should raise
        with self.assertRaises(ValueError):
            filter_obj.validate_image("not an image")

    def test_to_numpy_conversion(self):
        """Test PIL to numpy conversion."""
        filter_obj = JigsawFolkFilter()
        array = filter_obj.to_numpy(self.test_image)

        self.assertIsInstance(array, np.ndarray)
        self.assertEqual(array.shape[:2], self.test_image.size[::-1])
        self.assertEqual(array.shape[2], 3)  # RGB

    def test_to_pil_conversion(self):
        """Test numpy to PIL conversion."""
        filter_obj = JigsawFolkFilter()
        array = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        image = filter_obj.to_pil(array)

        self.assertIsInstance(image, Image.Image)
        self.assertEqual(image.size, (100, 100))

    def test_different_piece_sizes(self):
        """Test filter with different piece sizes."""
        for piece_size in [20, 40, 60, 80]:
            filter_obj = JigsawFolkFilter(piece_size=piece_size)
            result = filter_obj.apply(self.test_image)
            self.assertIsInstance(result, Image.Image)

    def test_different_color_counts(self):
        """Test filter with different color counts."""
        for n_colors in [8, 12, 16, 24]:
            filter_obj = JigsawFolkFilter(n_colors=n_colors)
            result = filter_obj.apply(self.test_image)
            self.assertIsInstance(result, Image.Image)


if __name__ == '__main__':
    unittest.main()
