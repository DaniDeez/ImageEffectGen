# 🚀 Quick Start Guide

Get up and running with the Jigsaw Folk Art Filter in 2 minutes!

## 📦 Installation

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

That's it! All dependencies will be installed automatically.

### Step 2: Run the Demo

See the filter in action immediately:

```bash
python demo.py
```

This will:
- Create a sample image
- Apply the filter with 6 different settings
- Save all results to the `demo_output/` folder

**Expected output:**
```
demo_output/
├── 00_original.png          # Original sample image
├── 01_default.png           # Default settings
├── 02_small_pieces.png      # Small detailed pieces
├── 03_large_pieces.png      # Large bold pieces
├── 04_flower_border.png     # With flower border
├── 05_geometric_border.png  # With geometric border
└── 06_smooth.png            # Very smooth edges
```

## 🎨 Using with Your Own Images

### Simple Usage

Apply the filter to your image:

```bash
python run_filter.py your_image.jpg
```

Output will be saved as `your_image_jigsaw.png`

### Specify Output File

```bash
python run_filter.py input.jpg output.png
```

### Using Presets

**Small pieces (detailed):**
```bash
python run_filter.py photo.jpg --small
```

**Large pieces (bold):**
```bash
python run_filter.py photo.jpg --large
```

**Smooth edges:**
```bash
python run_filter.py photo.jpg --smooth
```

**Add decorative borders:**
```bash
python run_filter.py photo.jpg --borders flowers
python run_filter.py photo.jpg --borders geometric
```

### Custom Parameters

Fine-tune the effect:

```bash
python run_filter.py photo.jpg \
    --piece-size 40 \
    --colors 12 \
    --smoothness 5 \
    --borders flowers
```

**Parameters:**
- `--piece-size` (20-100): Size of puzzle pieces in pixels
- `--colors` (8-24): Number of colors to use
- `--smoothness` (1-10): How smooth the piece edges are
- `--borders` (flowers/geometric): Add decorative border

## 🐍 Using in Python Scripts

Create your own scripts:

```python
import sys
sys.path.insert(0, 'src')

from PIL import Image
from imageeffectgen import JigsawFolkFilter

# Load image
image = Image.open('photo.jpg')

# Apply filter (default settings)
filter = JigsawFolkFilter()
result = filter.apply(image)
result.save('output.png')
```

**With custom settings:**

```python
from PIL import Image
from imageeffectgen import JigsawFolkFilter

image = Image.open('photo.jpg')

# Customize the effect
filter = JigsawFolkFilter(
    piece_size=40,          # Smaller pieces
    n_colors=12,            # Fewer colors
    smoothness=5,           # Smoother edges
    add_borders=True,       # Add border
    border_pattern='flowers' # Flower pattern
)

result = filter.apply(image)
result.save('output.png')
```

## 🎯 Examples

### Example 1: Portrait Photo
```bash
python run_filter.py portrait.jpg --small --borders flowers
```
Best for portraits with lots of detail.

### Example 2: Landscape
```bash
python run_filter.py landscape.jpg --large
```
Bold, simplified landscape with large pieces.

### Example 3: Abstract Art
```bash
python run_filter.py art.jpg --piece-size 60 --colors 8 --smoothness 8
```
Very smooth, highly simplified with few colors.

### Example 4: With Borders
```bash
python run_filter.py photo.jpg --borders geometric
```
Add traditional folk art decorative border.

## 📊 Parameter Guide

| Parameter | Range | Effect |
|-----------|-------|--------|
| `piece_size` | 20-100 | Smaller = more pieces, more detail |
| `n_colors` | 8-24 | Fewer = more stylized folk art look |
| `smoothness` | 1-10 | Higher = more organic, rounded edges |

**Recommended Combinations:**

| Style | piece_size | n_colors | smoothness |
|-------|------------|----------|------------|
| Detailed | 30 | 20 | 3 |
| Default | 50 | 16 | 3 |
| Bold | 70 | 10 | 2 |
| Smooth | 55 | 16 | 8 |

## 🛠️ Troubleshooting

**Problem: "ModuleNotFoundError"**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Problem: "No module named imageeffectgen"**
```bash
# Solution: Make sure you're running from the ImageEffectGen directory
cd /path/to/ImageEffectGen
python run_filter.py image.jpg
```

**Problem: Image processing is slow**
- This is normal! The filter does complex processing
- Smaller images process faster
- Try resizing large images first: `--piece-size` larger values = faster

**Problem: Output looks too pixelated**
```bash
# Solution: Use smaller pieces and more colors
python run_filter.py image.jpg --piece-size 30 --colors 20
```

**Problem: Want more folk art style**
```bash
# Solution: Use larger pieces and fewer colors
python run_filter.py image.jpg --piece-size 70 --colors 10
```

## 💡 Tips

1. **Start with the demo** to see different styles
2. **Small images** (500-800px) process faster for testing
3. **Fewer colors** (8-12) = more folk art style
4. **More colors** (18-24) = more detail preserved
5. **Borders** work best with `piece_size` 40-50
6. **Save as PNG** for best quality

## 🎨 Best Practices

**For portraits:**
- Use small to medium pieces (30-50)
- More colors (16-20)
- Medium smoothness (3-5)

**For landscapes:**
- Use medium to large pieces (50-70)
- Moderate colors (12-16)
- Lower smoothness (2-4) for texture

**For abstract/artistic:**
- Use large pieces (60-80)
- Fewer colors (8-12)
- High smoothness (6-10)

## 📁 File Organization

```
ImageEffectGen/
├── demo.py              ← Run this first!
├── run_filter.py        ← Use this for your images
├── requirements.txt     ← Install these dependencies
├── demo_output/         ← Demo results appear here
└── src/                 ← Source code (don't need to touch)
```

## ✅ Next Steps

1. ✓ Run `python demo.py` to see examples
2. ✓ Try `python run_filter.py your_photo.jpg`
3. ✓ Experiment with different parameters
4. ✓ Check the full README.md for Python API details

## 🆘 Need Help?

- Check the full README.md for detailed documentation
- Run `python run_filter.py --help` for all options
- See `examples/example_usage.py` for more code examples

---

**Ready? Start here:**

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the demo
python demo.py

# 3. Use with your image
python run_filter.py your_image.jpg
```

Enjoy creating beautiful folk art! 🎨
