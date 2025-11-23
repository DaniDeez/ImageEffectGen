#!/usr/bin/env python3
"""
Example usage of ImageEffectGen Jigsaw Folk Filter.

This script demonstrates various ways to use the filter with different parameters.
"""

from PIL import Image
from pathlib import Path
import sys

# Add parent directory to path to import the package
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from imageeffectgen import JigsawFolkFilter


def example_basic():
    """Basic usage example."""
    print("Example 1: Basic usage with default parameters")

    # Load an image (you'll need to provide your own)
    # image = Image.open('your_image.jpg')

    # Create filter with default parameters
    filter_obj = JigsawFolkFilter()

    # Apply filter
    # result = filter_obj.apply(image)

    # Save result
    # result.save('output_basic.png')

    print("  Filter created with default parameters")
    print(f"  - piece_size: 50")
    print(f"  - n_colors: 16")
    print(f"  - use_folk_palette: True\n")


def example_custom_parameters():
    """Example with custom parameters."""
    print("Example 2: Custom parameters for different artistic effects")

    # Small pieces, more colors
    filter_detailed = JigsawFolkFilter(
        piece_size=30,
        n_colors=20,
        smoothness=5
    )
    print("  Detailed version:")
    print(f"  - Smaller pieces (30px)")
    print(f"  - More colors (20)")
    print(f"  - Smoother edges (5)\n")

    # Large pieces, fewer colors
    filter_bold = JigsawFolkFilter(
        piece_size=70,
        n_colors=10,
        smoothness=2
    )
    print("  Bold version:")
    print(f"  - Larger pieces (70px)")
    print(f"  - Fewer colors (10)")
    print(f"  - Less smooth edges (2)\n")


def example_with_borders():
    """Example with decorative borders."""
    print("Example 3: Adding decorative folk art borders")

    # Flower border
    filter_flowers = JigsawFolkFilter(
        add_borders=True,
        border_pattern='flowers'
    )
    print("  Flower border version")

    # Geometric border
    filter_geometric = JigsawFolkFilter(
        add_borders=True,
        border_pattern='geometric'
    )
    print("  Geometric border version\n")


def example_no_folk_palette():
    """Example without folk art palette."""
    print("Example 4: Using original image colors (no folk palette)")

    filter_original_colors = JigsawFolkFilter(
        use_folk_palette=False,
        n_colors=24
    )
    print("  This maintains more of the original image's color scheme")
    print("  while still applying the jigsaw pattern effect\n")


def example_batch_processing():
    """Example of processing multiple images."""
    print("Example 5: Batch processing multiple images")
    print("""
    # Process all images in a directory
    import os
    from pathlib import Path

    input_dir = Path('input_images')
    output_dir = Path('output_images')
    output_dir.mkdir(exist_ok=True)

    filter_obj = JigsawFolkFilter(piece_size=40)

    for image_path in input_dir.glob('*.jpg'):
        image = Image.open(image_path)
        result = filter_obj.apply(image)

        output_path = output_dir / f"{image_path.stem}_jigsaw.png"
        result.save(output_path)
        print(f"Processed: {image_path.name}")
    """)


def example_complete_workflow():
    """Complete workflow example."""
    print("Example 6: Complete workflow with error handling")
    print("""
    from PIL import Image
    from imageeffectgen import JigsawFolkFilter
    import sys

    try:
        # Load image
        image = Image.open('input.jpg')
        print(f"Loaded image: {image.size}")

        # Create filter
        filter_obj = JigsawFolkFilter(
            piece_size=50,
            n_colors=16,
            use_folk_palette=True,
            smoothness=3,
            add_borders=True,
            border_pattern='flowers'
        )

        # Apply filter
        print("Applying filter...")
        result = filter_obj.apply(image)

        # Save result
        result.save('output.png', quality=95)
        print("✓ Success! Saved to output.png")

    except FileNotFoundError:
        print("Error: Input file not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    """)


if __name__ == '__main__':
    print("=" * 60)
    print("ImageEffectGen - Jigsaw Folk Filter Examples")
    print("=" * 60)
    print()

    example_basic()
    example_custom_parameters()
    example_with_borders()
    example_no_folk_palette()
    example_batch_processing()
    example_complete_workflow()

    print("=" * 60)
    print("To use these examples with actual images:")
    print("1. Place your images in the examples directory")
    print("2. Modify the code to use your image files")
    print("3. Run: python examples/example_usage.py")
    print("=" * 60)
