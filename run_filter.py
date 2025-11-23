#!/usr/bin/env python3
"""
Simple script to apply Jigsaw Folk Filter to your images.

Usage:
    python run_filter.py input.jpg
    python run_filter.py input.jpg output.png
    python run_filter.py input.jpg --small
    python run_filter.py input.jpg --large
    python run_filter.py input.jpg --borders flowers
"""

import sys
from pathlib import Path
import argparse

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from PIL import Image
from imageeffectgen import JigsawFolkFilter


def main():
    """Run the filter on an input image."""
    parser = argparse.ArgumentParser(
        description='Apply Jigsaw Folk Art Filter to images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_filter.py photo.jpg
  python run_filter.py photo.jpg --output result.png
  python run_filter.py photo.jpg --small
  python run_filter.py photo.jpg --large --borders flowers
  python run_filter.py photo.jpg --piece-size 40 --colors 12
        """
    )

    parser.add_argument('input', help='Input image file')
    parser.add_argument('output', nargs='?', help='Output image file (default: input_jigsaw.png)')
    parser.add_argument('--piece-size', type=int, help='Size of jigsaw pieces (default: 50)')
    parser.add_argument('--colors', type=int, help='Number of colors (default: 16)')
    parser.add_argument('--smoothness', type=int, help='Edge smoothness 1-10 (default: 3)')
    parser.add_argument('--borders', choices=['flowers', 'geometric'], help='Add decorative border')

    # Preset shortcuts
    parser.add_argument('--small', action='store_true', help='Small pieces preset (30px, 20 colors)')
    parser.add_argument('--large', action='store_true', help='Large pieces preset (70px, 10 colors)')
    parser.add_argument('--smooth', action='store_true', help='Very smooth edges preset')

    args = parser.parse_args()

    # Determine output filename
    if args.output:
        output_path = args.output
    else:
        input_path = Path(args.input)
        output_path = input_path.stem + '_jigsaw.png'

    # Build filter parameters
    params = {}

    # Apply presets
    if args.small:
        params['piece_size'] = 30
        params['n_colors'] = 20
    elif args.large:
        params['piece_size'] = 70
        params['n_colors'] = 10
    elif args.smooth:
        params['smoothness'] = 8

    # Override with explicit parameters
    if args.piece_size:
        params['piece_size'] = args.piece_size
    if args.colors:
        params['n_colors'] = args.colors
    if args.smoothness:
        params['smoothness'] = args.smoothness
    if args.borders:
        params['add_borders'] = True
        params['border_pattern'] = args.borders

    # Print configuration
    print("=" * 60)
    print("JIGSAW FOLK ART FILTER")
    print("=" * 60)
    print(f"Input:  {args.input}")
    print(f"Output: {output_path}")
    if params:
        print("\nParameters:")
        for key, value in params.items():
            print(f"  {key}: {value}")
    print("=" * 60)
    print()

    try:
        # Load image
        print("Loading image...", end=' ', flush=True)
        image = Image.open(args.input)
        print(f"✓ ({image.size[0]}x{image.size[1]})")

        # Create filter
        print("Creating filter...", end=' ', flush=True)
        filter_obj = JigsawFolkFilter(**params)
        print("✓")

        # Apply filter
        print("Applying jigsaw folk filter (this may take a moment)...", end=' ', flush=True)
        result = filter_obj.apply(image)
        print("✓")

        # Save result
        print("Saving result...", end=' ', flush=True)
        result.save(output_path, quality=95)
        print("✓")

        print()
        print("=" * 60)
        print(f"SUCCESS! Output saved to: {output_path}")
        print("=" * 60)

    except FileNotFoundError:
        print(f"\n✗ Error: File not found: {args.input}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
