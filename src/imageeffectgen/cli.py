"""Command-line interface for ImageEffectGen."""

import click
from pathlib import Path
from PIL import Image
import sys

from .filters.jigsaw_folk import JigsawFolkFilter


@click.group()
@click.version_option(version="0.1.0")
def main():
    """ImageEffectGen - Stylized image filter generator.

    Transform images into beautiful folk art styles.
    """
    pass


@main.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
@click.option(
    '--piece-size',
    default=50,
    help='Size of jigsaw pieces (default: 50)',
    type=int
)
@click.option(
    '--colors',
    default=16,
    help='Number of colors (default: 16)',
    type=int
)
@click.option(
    '--folk-palette/--no-folk-palette',
    default=True,
    help='Use traditional folk art color palette'
)
@click.option(
    '--smoothness',
    default=3,
    help='Smoothness of piece edges (default: 3)',
    type=int
)
@click.option(
    '--segmentation-scale',
    default=100,
    help='Segmentation scale (default: 100)',
    type=int
)
@click.option(
    '--add-borders',
    is_flag=True,
    help='Add decorative folk art borders'
)
@click.option(
    '--border-pattern',
    type=click.Choice(['flowers', 'geometric'], case_sensitive=False),
    help='Border pattern type (requires --add-borders)'
)
def jigsaw(
    input_path,
    output_path,
    piece_size,
    colors,
    folk_palette,
    smoothness,
    segmentation_scale,
    add_borders,
    border_pattern
):
    """Apply jigsaw folk art filter to an image.

    \b
    Examples:
        imageeffectgen jigsaw input.jpg output.png
        imageeffectgen jigsaw input.jpg output.png --piece-size 40 --colors 12
        imageeffectgen jigsaw input.jpg output.png --add-borders --border-pattern flowers
    """
    try:
        # Load image
        click.echo(f"Loading image from {input_path}...")
        image = Image.open(input_path)

        # Create filter
        click.echo("Applying jigsaw folk filter...")
        filter_obj = JigsawFolkFilter(
            piece_size=piece_size,
            n_colors=colors,
            use_folk_palette=folk_palette,
            smoothness=smoothness,
            segmentation_scale=segmentation_scale,
            add_borders=add_borders,
            border_pattern=border_pattern
        )

        # Apply filter
        result = filter_obj.apply(image)

        # Save result
        click.echo(f"Saving result to {output_path}...")
        result.save(output_path)

        click.echo(click.style("✓ Done!", fg="green", bold=True))

    except Exception as e:
        click.echo(click.style(f"Error: {str(e)}", fg="red"), err=True)
        sys.exit(1)


@main.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option(
    '--output-dir',
    default='output',
    help='Output directory for comparison images',
    type=click.Path()
)
def demo(input_path, output_dir):
    """Generate demo outputs with different settings.

    Creates multiple variations of the jigsaw folk filter to showcase
    different parameter combinations.
    """
    try:
        import os

        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Load image
        click.echo(f"Loading image from {input_path}...")
        image = Image.open(input_path)

        # Get base filename
        base_name = Path(input_path).stem

        # Generate variations
        variations = [
            {
                'name': 'default',
                'params': {}
            },
            {
                'name': 'small_pieces',
                'params': {'piece_size': 30, 'n_colors': 20}
            },
            {
                'name': 'large_pieces',
                'params': {'piece_size': 70, 'n_colors': 12}
            },
            {
                'name': 'with_flower_border',
                'params': {'add_borders': True, 'border_pattern': 'flowers'}
            },
            {
                'name': 'with_geometric_border',
                'params': {'add_borders': True, 'border_pattern': 'geometric'}
            },
        ]

        for var in variations:
            click.echo(f"Generating {var['name']} variation...")
            filter_obj = JigsawFolkFilter(**var['params'])
            result = filter_obj.apply(image)

            output_path = os.path.join(output_dir, f"{base_name}_{var['name']}.png")
            result.save(output_path)
            click.echo(f"  Saved to {output_path}")

        click.echo(click.style(f"\n✓ Generated {len(variations)} variations!", fg="green", bold=True))

    except Exception as e:
        click.echo(click.style(f"Error: {str(e)}", fg="red"), err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
