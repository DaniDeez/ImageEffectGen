# ImageEffectGen

Transform images into beautiful jigsaw folk art patterns! ImageEffectGen applies stylized filters that turn photos into interlocking puzzle-piece folk art with flat colors and organic shapes.

## 🌐 Try It Online (No Installation!)

**[→ Launch Web Demo](https://imageeffectgen.streamlit.app)** ← Click here to try it in your browser!

Upload an image and transform it into folk art instantly - no installation or coding required!

---

## 🚀 Quick Start (2 minutes!)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the demo (see it in action!)
python demo.py

# 3. Use with your own image
python run_filter.py your_image.jpg
```

**That's it!** Check `demo_output/` folder for results. See [QUICKSTART.md](QUICKSTART.md) for detailed guide.

## Features

- **🌐 Web Demo**: Try it instantly in your browser - no installation needed!
- **Jigsaw Folk Art Filter**: Transform any image into a folk art style with organic, interlocking puzzle piece shapes
- **Color Quantization**: Reduce images to vibrant folk art color palettes
- **Customizable Parameters**: Adjust piece size, color count, smoothness, and more
- **Decorative Borders**: Add traditional folk art borders with flower or geometric patterns
- **CLI Interface**: Easy-to-use command-line tool
- **Python API**: Integrate into your own projects
- **Streamlit App**: Beautiful web interface with real-time previews

## Installation

```bash
# Clone the repository
git clone https://github.com/DaniDeez/ImageEffectGen.git
cd ImageEffectGen

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Quick Start

### Command Line Usage

Basic usage:
```bash
imageeffectgen jigsaw input.jpg output.png
```

With custom parameters:
```bash
imageeffectgen jigsaw input.jpg output.png \
    --piece-size 40 \
    --colors 12 \
    --smoothness 5
```

Add decorative borders:
```bash
imageeffectgen jigsaw input.jpg output.png \
    --add-borders \
    --border-pattern flowers
```

Generate demo variations:
```bash
imageeffectgen demo input.jpg --output-dir ./output
```

### Python API Usage

```python
from PIL import Image
from imageeffectgen import JigsawFolkFilter

# Load image
image = Image.open('input.jpg')

# Create filter with custom parameters
filter = JigsawFolkFilter(
    piece_size=50,
    n_colors=16,
    use_folk_palette=True,
    smoothness=3,
    add_borders=True,
    border_pattern='flowers'
)

# Apply filter
result = filter.apply(image)

# Save result
result.save('output.png')
```

## Filter Parameters

### JigsawFolkFilter

- **piece_size** (int, default=50): Size of individual jigsaw pieces in pixels
- **n_colors** (int, default=16): Number of colors to reduce the image to
- **use_folk_palette** (bool, default=True): Use traditional folk art color palette
- **smoothness** (int, default=3): Smoothness level of piece edges (higher = smoother)
- **segmentation_scale** (int, default=100): Number of segments for image analysis
- **add_borders** (bool, default=False): Add decorative borders around the image
- **border_pattern** (str, optional): Border pattern type - 'flowers' or 'geometric'

## Examples

The filter transforms images with these characteristics:

- **Organic Shapes**: Soft, interlocking blob shapes resembling puzzle pieces
- **Flat Colors**: Solid colors with no gradients, creating a hand-painted feel
- **Folk Art Palette**: Vibrant traditional colors (reds, oranges, yellows, greens, blues)
- **Simplified Forms**: Subjects are abstracted into puzzle-like shapes
- **Optional Decorative Borders**: Traditional folk art border patterns

## CLI Commands

### `jigsaw`
Apply the jigsaw folk art filter to an image.

```bash
imageeffectgen jigsaw [OPTIONS] INPUT_PATH OUTPUT_PATH

Options:
  --piece-size INTEGER          Size of jigsaw pieces (default: 50)
  --colors INTEGER              Number of colors (default: 16)
  --folk-palette / --no-folk-palette
                                Use traditional folk art color palette
  --smoothness INTEGER          Smoothness of piece edges (default: 3)
  --segmentation-scale INTEGER  Segmentation scale (default: 100)
  --add-borders                 Add decorative folk art borders
  --border-pattern [flowers|geometric]
                                Border pattern type
  --help                        Show help message
```

### `demo`
Generate multiple variations with different settings.

```bash
imageeffectgen demo [OPTIONS] INPUT_PATH

Options:
  --output-dir PATH  Output directory for comparison images
  --help             Show help message
```

## 🌐 Web Interface

### Run Locally

Start the Streamlit web interface on your machine:

```bash
streamlit run streamlit_app.py
```

Then open your browser to `http://localhost:8501`

Features:
- 📤 Drag-and-drop image upload
- ⚙️ Interactive parameter controls
- 🎨 Real-time preview
- 📥 One-click download
- 🎯 Quick presets (Small, Large, Smooth, etc.)
- 🖼️ Before/after comparison

### Deploy Your Own

Deploy for free on Streamlit Cloud:

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Deploy `streamlit_app.py`
5. Get a shareable URL like `https://your-app.streamlit.app`

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## How It Works

The Jigsaw Folk Filter uses a multi-step process:

1. **Color Simplification**: Reduces colors using k-means clustering and bilateral filtering
2. **Image Segmentation**: Uses SLIC superpixels to identify distinct regions
3. **Jigsaw Pattern Generation**: Creates organic, interlocking blob shapes across the image
4. **Color Mapping**: Assigns flat folk art colors to each piece based on the underlying image
5. **Edge Refinement**: Smooths piece edges for an organic, hand-painted look
6. **Border Addition**: Optionally adds decorative folk art borders

## Requirements

- Python 3.8+
- NumPy
- Pillow (PIL)
- OpenCV
- scikit-image
- SciPy
- Click

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

MIT License - See LICENSE file for details

## Project Structure

```
ImageEffectGen/
├── src/
│   └── imageeffectgen/
│       ├── __init__.py
│       ├── cli.py              # Command-line interface
│       ├── core/
│       │   ├── __init__.py
│       │   └── base_filter.py  # Base filter class
│       ├── filters/
│       │   ├── __init__.py
│       │   └── jigsaw_folk.py  # Jigsaw folk art filter
│       └── utils/
│           ├── __init__.py
│           ├── color.py        # Color manipulation utilities
│           └── geometry.py     # Geometric shape utilities
├── tests/
├── examples/
├── output/
├── requirements.txt
├── setup.py
└── README.md
```

## Acknowledgments

Inspired by traditional folk art patterns and puzzle piece aesthetics from various cultures around the world.
