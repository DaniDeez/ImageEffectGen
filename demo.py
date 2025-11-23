#!/usr/bin/env python3
"""
Quick Demo - Generate sample images and apply Jigsaw Folk Filter
Run this script to see the filter in action immediately!
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from PIL import Image, ImageDraw
import numpy as np
from imageeffectgen import JigsawFolkFilter


def create_sample_image():
    """Create a colorful sample image for demonstration."""
    print("Creating sample image...")

    # Create a 600x600 image
    img = Image.new('RGB', (600, 600), color=(135, 206, 235))  # Sky blue background
    draw = ImageDraw.Draw(img)

    # Draw a simple scene
    # Ground
    draw.rectangle([0, 400, 600, 600], fill=(34, 139, 34))  # Green

    # Sun
    draw.ellipse([450, 50, 550, 150], fill=(255, 215, 0))  # Yellow

    # House
    draw.rectangle([150, 250, 350, 450], fill=(220, 47, 2))  # Red
    draw.polygon([(150, 250), (250, 150), (350, 250)], fill=(139, 69, 19))  # Brown roof

    # Door
    draw.rectangle([220, 350, 280, 450], fill=(101, 67, 33))  # Dark brown

    # Windows
    draw.rectangle([170, 280, 220, 330], fill=(255, 255, 255))  # White
    draw.rectangle([280, 280, 330, 330], fill=(255, 255, 255))  # White

    # Tree
    draw.ellipse([400, 200, 500, 300], fill=(34, 139, 34))  # Green leaves
    draw.rectangle([440, 300, 460, 400], fill=(101, 67, 33))  # Brown trunk

    # Flowers
    for x in [80, 120, 160, 500, 540]:
        y = 420
        # Flower head
        draw.ellipse([x-10, y-10, x+10, y+10], fill=(255, 105, 180))  # Pink
        # Center
        draw.ellipse([x-3, y-3, x+3, y+3], fill=(255, 215, 0))  # Yellow
        # Stem
        draw.line([(x, y+10), (x, y+30)], fill=(34, 139, 34), width=2)

    # Clouds
    draw.ellipse([50, 50, 150, 100], fill=(255, 255, 255))
    draw.ellipse([200, 80, 280, 130], fill=(255, 255, 255))

    return img


def main():
    """Run the demo."""
    print("=" * 70)
    print("JIGSAW FOLK ART FILTER - QUICK DEMO")
    print("=" * 70)
    print()

    # Create output directory
    output_dir = Path('demo_output')
    output_dir.mkdir(exist_ok=True)
    print(f"Output directory: {output_dir.absolute()}")
    print()

    # Create sample image
    sample_image = create_sample_image()
    sample_path = output_dir / '00_original.png'
    sample_image.save(sample_path)
    print(f"✓ Saved original sample image: {sample_path}")
    print()

    # Define variations to generate
    variations = [
        {
            'name': '01_default',
            'description': 'Default settings',
            'params': {}
        },
        {
            'name': '02_small_pieces',
            'description': 'Small pieces, more detail',
            'params': {'piece_size': 30, 'n_colors': 20}
        },
        {
            'name': '03_large_pieces',
            'description': 'Large pieces, bold look',
            'params': {'piece_size': 70, 'n_colors': 10}
        },
        {
            'name': '04_flower_border',
            'description': 'With flower border',
            'params': {'add_borders': True, 'border_pattern': 'flowers', 'piece_size': 45}
        },
        {
            'name': '05_geometric_border',
            'description': 'With geometric border',
            'params': {'add_borders': True, 'border_pattern': 'geometric', 'piece_size': 45}
        },
        {
            'name': '06_smooth',
            'description': 'Very smooth edges',
            'params': {'smoothness': 8, 'piece_size': 55}
        },
    ]

    print("Generating variations (this may take a minute)...")
    print("-" * 70)

    for i, var in enumerate(variations, 1):
        print(f"[{i}/{len(variations)}] {var['description']}...", end=' ', flush=True)

        try:
            # Create filter
            filter_obj = JigsawFolkFilter(**var['params'])

            # Apply filter
            result = filter_obj.apply(sample_image)

            # Save
            output_path = output_dir / f"{var['name']}.png"
            result.save(output_path)

            print(f"✓ Saved to {output_path.name}")

        except Exception as e:
            print(f"✗ Error: {e}")

    print("-" * 70)
    print()
    print("=" * 70)
    print("DEMO COMPLETE!")
    print("=" * 70)
    print()
    print(f"Check the '{output_dir}' folder to see all variations!")
    print()
    print("To use with your own images:")
    print("  1. Place your image in this directory")
    print("  2. Run: python run_filter.py your_image.jpg")
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
