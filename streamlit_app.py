#!/usr/bin/env python3
"""
Streamlit Web Interface for Jigsaw Folk Art Filter
Live demo: https://imageeffectgen.streamlit.app
"""

import streamlit as st
import sys
from pathlib import Path
from PIL import Image
import io

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from imageeffectgen import JigsawFolkFilter, PixelFilter, RetroPixelFilter, MosaicFilter


# Page configuration
st.set_page_config(
    page_title="Jigsaw Folk Art Filter",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');

    /* Antique paper background */
    .stApp {
        background: linear-gradient(to bottom,
            rgba(235, 220, 195, 0.9),
            rgba(225, 210, 180, 0.95)
        );
        background-image:
            linear-gradient(to bottom, rgba(235, 220, 195, 0.9), rgba(225, 210, 180, 0.95)),
            repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(150, 120, 80, 0.03) 2px, rgba(150, 120, 80, 0.03) 4px),
            repeating-linear-gradient(90deg, transparent, transparent 2px, rgba(150, 120, 80, 0.03) 2px, rgba(150, 120, 80, 0.03) 4px);
        background-color: #f4e8d8;
    }

    /* Paper texture overlay */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        opacity: 0.15;
        background-image:
            radial-gradient(circle at 20% 50%, transparent 0%, rgba(100, 80, 60, 0.1) 100%),
            radial-gradient(circle at 80% 80%, transparent 0%, rgba(100, 80, 60, 0.1) 100%);
        pointer-events: none;
        z-index: 0;
    }

    /* Main header with pixel font */
    .main-header {
        font-family: 'Press Start 2P', cursive;
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 0;
        color: #4a3520;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        padding: 1rem;
        background: rgba(255, 255, 255, 0.3);
        border: 3px solid #8b6f47;
        border-radius: 8px;
        box-shadow: inset 0 0 20px rgba(139, 111, 71, 0.1);
    }

    .sub-header {
        font-family: 'VT323', monospace;
        font-size: 1.8rem;
        text-align: center;
        color: #6b5438;
        margin-bottom: 2rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(to bottom,
            rgba(245, 235, 215, 0.95),
            rgba(235, 225, 205, 0.95)
        );
        border-right: 3px solid #8b6f47;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        font-family: 'Press Start 2P', cursive;
        color: #4a3520;
        font-size: 1rem;
        line-height: 1.5;
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        font-family: 'VT323', monospace;
        font-size: 1.3rem;
        color: #5a4530;
    }

    /* Main content headers */
    h1, h2, h3 {
        font-family: 'Press Start 2P', cursive;
        color: #4a3520;
        line-height: 1.6;
    }

    /* Regular text */
    p, div, span, label {
        font-family: 'VT323', monospace;
        font-size: 1.2rem;
        color: #5a4530;
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(to bottom, #d4a574, #b8935e);
        color: #2a1f15;
        font-family: 'Press Start 2P', cursive;
        font-size: 0.8rem;
        font-weight: bold;
        border: 3px solid #8b6f47;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        transition: all 0.3s;
    }

    .stButton>button:hover {
        background: linear-gradient(to bottom, #e4b584, #c8a36e);
        transform: translateY(-2px);
        box-shadow: 4px 4px 8px rgba(0,0,0,0.4);
    }

    /* Download button */
    .stDownloadButton>button {
        background: linear-gradient(to bottom, #a4c574, #88a95e);
        color: #1f2a15;
        font-family: 'Press Start 2P', cursive;
        font-size: 0.8rem;
        border: 3px solid #6b8f47;
        border-radius: 8px;
        box-shadow: 3px 3px 6px rgba(0,0,0,0.3);
    }

    /* File uploader */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.5);
        border: 3px dashed #8b6f47;
        border-radius: 8px;
        padding: 1rem;
    }

    /* Images */
    .example-image {
        border-radius: 8px;
        border: 3px solid #8b6f47;
        box-shadow: 4px 4px 8px rgba(0,0,0,0.3);
    }

    /* Info boxes */
    .stAlert {
        background: rgba(255, 255, 255, 0.6);
        border: 2px solid #8b6f47;
        border-radius: 8px;
        font-family: 'VT323', monospace;
    }

    /* Dividers */
    hr {
        border: 2px solid #8b6f47;
        opacity: 0.5;
    }

    /* Radio buttons and checkboxes */
    .stRadio label, .stCheckbox label {
        font-family: 'VT323', monospace;
        font-size: 1.2rem;
    }

    /* Selectbox */
    .stSelectbox label {
        font-family: 'VT323', monospace;
        font-size: 1.2rem;
    }

    /* Markdown links */
    a {
        color: #8b4513;
        font-family: 'VT323', monospace;
        text-decoration: underline;
    }

    a:hover {
        color: #a0522d;
    }
</style>
""", unsafe_allow_html=True)


def create_sample_image():
    """Create a colorful sample image for demonstration."""
    from PIL import ImageDraw

    img = Image.new('RGB', (400, 400), color=(135, 206, 235))
    draw = ImageDraw.Draw(img)

    # Ground
    draw.rectangle([0, 270, 400, 400], fill=(34, 139, 34))

    # Sun
    draw.ellipse([300, 30, 370, 100], fill=(255, 215, 0))

    # House
    draw.rectangle([100, 165, 230, 270], fill=(220, 47, 2))
    draw.polygon([(100, 165), (165, 100), (230, 165)], fill=(139, 69, 19))

    # Door
    draw.rectangle([145, 210, 185, 270], fill=(101, 67, 33))

    # Windows
    draw.rectangle([115, 180, 145, 210], fill=(255, 255, 255))
    draw.rectangle([185, 180, 215, 210], fill=(255, 255, 255))

    # Tree
    draw.ellipse([260, 135, 340, 215], fill=(34, 139, 34))
    draw.rectangle([290, 215, 310, 270], fill=(101, 67, 33))

    # Flowers
    for x in [50, 90, 320, 360]:
        y = 285
        draw.ellipse([x-7, y-7, x+7, y+7], fill=(255, 105, 180))
        draw.ellipse([x-2, y-2, x+2, y+2], fill=(255, 215, 0))

    return img


def main():
    """Main Streamlit app."""

    # Header
    st.markdown('<p class="main-header">🎨 Image Effect Generator</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform images with artistic filters!</p>', unsafe_allow_html=True)

    # Sidebar - Parameters
    with st.sidebar:
        st.header("⚙️ Filter Settings")

        # Filter type selection
        st.subheader("🎭 Filter Type")
        filter_type = st.radio(
            "Choose effect:",
            ["Jigsaw Folk Art", "Pixel Art"],
            help="Select which artistic filter to apply"
        )

        st.divider()

        # Show appropriate settings based on filter type
        if filter_type == "Jigsaw Folk Art":
            # Jigsaw presets
            st.subheader("Quick Presets")
            preset = st.radio(
                "Choose a preset:",
                ["Custom", "Default", "Small Pieces", "Large Pieces", "Smooth", "With Border"],
                help="Select a preset or choose 'Custom' to adjust parameters manually"
            )

            st.divider()

            # Parameters
            st.subheader("Custom Parameters")

            if preset == "Custom":
                piece_size = st.slider("Piece Size", 20, 100, 50, 5,
                                      help="Size of jigsaw pieces (larger = fewer pieces)")
                n_colors = st.slider("Number of Colors", 8, 24, 16, 1,
                                   help="More colors = more detail, fewer = more stylized")
                smoothness = st.slider("Smoothness", 1, 10, 3, 1,
                                     help="How smooth the piece edges are")
                use_folk_palette = st.checkbox("Use Folk Art Palette", True,
                                             help="Use traditional folk art colors")
                add_borders = st.checkbox("Add Decorative Border", False)

                if add_borders:
                    border_pattern = st.selectbox("Border Pattern",
                                                 ["flowers", "geometric"])
                else:
                    border_pattern = None
            else:
                # Apply presets
                presets = {
                    "Default": {"piece_size": 50, "n_colors": 16, "smoothness": 3,
                               "use_folk_palette": True, "add_borders": False, "border_pattern": None},
                    "Small Pieces": {"piece_size": 30, "n_colors": 20, "smoothness": 3,
                                    "use_folk_palette": True, "add_borders": False, "border_pattern": None},
                    "Large Pieces": {"piece_size": 70, "n_colors": 10, "smoothness": 2,
                                    "use_folk_palette": True, "add_borders": False, "border_pattern": None},
                    "Smooth": {"piece_size": 55, "n_colors": 16, "smoothness": 8,
                              "use_folk_palette": True, "add_borders": False, "border_pattern": None},
                    "With Border": {"piece_size": 45, "n_colors": 16, "smoothness": 3,
                                   "use_folk_palette": True, "add_borders": True, "border_pattern": "flowers"}
                }

                params = presets[preset]
                piece_size = params["piece_size"]
                n_colors = params["n_colors"]
                smoothness = params["smoothness"]
                use_folk_palette = params["use_folk_palette"]
                add_borders = params["add_borders"]
                border_pattern = params["border_pattern"]

                # Display preset values
                st.info(f"""
                **{preset} Settings:**
                - Piece Size: {piece_size}
                - Colors: {n_colors}
                - Smoothness: {smoothness}
                - Folk Palette: {'Yes' if use_folk_palette else 'No'}
                - Border: {border_pattern if add_borders else 'No'}
                """)

            st.divider()

            # Info
            st.subheader("ℹ️ About")
            st.markdown("""
            This filter transforms images into jigsaw folk art style with:
            - Organic puzzle piece shapes
            - Flat folk art colors
            - Traditional decorative borders

            **Tips:**
            - Small pieces = more detail
            - Fewer colors = more folk art style
            - Try different presets!
            """)

        else:  # Pixel Art filter
            # Pixel art presets
            st.subheader("Quick Presets")
            pixel_preset = st.radio(
                "Choose a preset:",
                ["Custom", "Retro Gaming", "Mosaic", "Large Pixels", "Tiny Pixels"],
                help="Select a preset or choose 'Custom' to adjust parameters manually"
            )

            st.divider()

            # Parameters
            st.subheader("Custom Parameters")

            if pixel_preset == "Custom":
                pixel_size = st.slider("Pixel Size", 2, 50, 10, 1,
                                      help="Size of each pixel block")
                quantize_colors = st.checkbox("Reduce Colors", True,
                                            help="Limit the color palette")
                if quantize_colors:
                    pixel_n_colors = st.slider("Number of Colors", 4, 32, 16, 1,
                                              help="Number of colors in the palette")
                else:
                    pixel_n_colors = 256

                outline = st.checkbox("Add Pixel Outlines", False,
                                    help="Add black borders around pixels")
                if outline:
                    outline_thickness = st.slider("Outline Thickness", 1, 3, 1, 1)
                else:
                    outline_thickness = 1

            else:
                # Apply pixel presets
                pixel_presets = {
                    "Retro Gaming": {"pixel_size": 16, "quantize_colors": True, "pixel_n_colors": 8,
                                    "outline": True, "outline_thickness": 1},
                    "Mosaic": {"pixel_size": 6, "quantize_colors": True, "pixel_n_colors": 24,
                              "outline": True, "outline_thickness": 1},
                    "Large Pixels": {"pixel_size": 25, "quantize_colors": True, "pixel_n_colors": 12,
                                    "outline": False, "outline_thickness": 1},
                    "Tiny Pixels": {"pixel_size": 4, "quantize_colors": True, "pixel_n_colors": 32,
                                   "outline": False, "outline_thickness": 1}
                }

                params = pixel_presets[pixel_preset]
                pixel_size = params["pixel_size"]
                quantize_colors = params["quantize_colors"]
                pixel_n_colors = params["pixel_n_colors"]
                outline = params["outline"]
                outline_thickness = params["outline_thickness"]

                # Display preset values
                st.info(f"""
                **{pixel_preset} Settings:**
                - Pixel Size: {pixel_size}
                - Quantize Colors: {'Yes' if quantize_colors else 'No'}
                - Colors: {pixel_n_colors if quantize_colors else 'Full'}
                - Outlines: {'Yes' if outline else 'No'}
                """)

            st.divider()

            # Info
            st.subheader("ℹ️ About")
            st.markdown("""
            This filter transforms images into pixel art style with:
            - Retro gaming aesthetic
            - Mosaic tile effects
            - Color quantization
            - Optional pixel grid outlines

            **Tips:**
            - Smaller pixels = more detail
            - Fewer colors = more retro
            - Outlines for authentic pixel art look!
            """)

        st.divider()

        # Links
        st.markdown("""
        **🔗 Links:**
        - [GitHub Repo](https://github.com/DaniDeez/ImageEffectGen)
        - [Documentation](https://github.com/DaniDeez/ImageEffectGen#readme)
        """)

    # Main content
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📤 Upload Image")

        # Image upload
        uploaded_file = st.file_uploader(
            "Choose an image...",
            type=["jpg", "jpeg", "png", "bmp"],
            help="Upload a JPG, PNG, or BMP image"
        )

        # Sample image button
        use_sample = st.button("🎨 Use Sample Image", help="Try with a demo image")

        if use_sample:
            input_image = create_sample_image()
            st.image(input_image, caption="Sample Image", use_container_width=True)
        elif uploaded_file is not None:
            input_image = Image.open(uploaded_file)
            st.image(input_image, caption="Original Image", use_container_width=True)

            # Show image info
            st.caption(f"Size: {input_image.size[0]}×{input_image.size[1]} pixels")
        else:
            input_image = None
            st.info("👆 Upload an image or use the sample image to get started!")

    with col2:
        st.header("🎨 Filtered Result")

        if input_image is not None:
            # Apply filter button
            if st.button("✨ Apply Filter", type="primary"):
                filter_name = "jigsaw folk" if filter_type == "Jigsaw Folk Art" else "pixel art"
                with st.spinner(f"🎨 Applying {filter_name} filter... This may take a moment..."):
                    try:
                        # Create filter based on type
                        if filter_type == "Jigsaw Folk Art":
                            filter_obj = JigsawFolkFilter(
                                piece_size=piece_size,
                                n_colors=n_colors,
                                use_folk_palette=use_folk_palette,
                                smoothness=smoothness,
                                add_borders=add_borders,
                                border_pattern=border_pattern
                            )
                        else:  # Pixel Art
                            filter_obj = PixelFilter(
                                pixel_size=pixel_size,
                                quantize_colors=quantize_colors,
                                n_colors=pixel_n_colors,
                                outline=outline,
                                outline_thickness=outline_thickness
                            )

                        # Apply filter
                        result_image = filter_obj.apply(input_image)

                        # Store in session state
                        st.session_state.result_image = result_image
                        st.session_state.filter_applied = True

                        st.success("✅ Filter applied successfully!")

                    except Exception as e:
                        st.error(f"❌ Error applying filter: {str(e)}")
                        st.session_state.filter_applied = False

            # Display result if available
            if hasattr(st.session_state, 'filter_applied') and st.session_state.filter_applied:
                result_image = st.session_state.result_image
                st.image(result_image, caption="Filtered Image", use_container_width=True)

                # Show result info
                st.caption(f"Size: {result_image.size[0]}×{result_image.size[1]} pixels")

                # Download button
                buf = io.BytesIO()
                result_image.save(buf, format="PNG")
                byte_im = buf.getvalue()

                filename = "jigsaw_folk_art.png" if filter_type == "Jigsaw Folk Art" else "pixel_art.png"
                st.download_button(
                    label="📥 Download Result",
                    data=byte_im,
                    file_name=filename,
                    mime="image/png",
                    help="Download the filtered image"
                )
        else:
            st.info("Upload an image to see the filtered result here!")

    # Examples section
    st.divider()
    st.header("🖼️ Examples")
    st.markdown("Here are some effects you can create:")

    example_cols = st.columns(3)

    with example_cols[0]:
        st.markdown("**Jigsaw Folk Art**")
        st.markdown("Organic puzzle pieces with folk colors")

    with example_cols[1]:
        st.markdown("**Retro Pixel Art**")
        st.markdown("8-bit gaming aesthetic")

    with example_cols[2]:
        st.markdown("**Mosaic Tiles**")
        st.markdown("Fine pixel mosaic effect")

    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>Made with ❤️ using Python, OpenCV, and Streamlit</p>
        <p>Transform your images with artistic filters! 🎨✨</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
