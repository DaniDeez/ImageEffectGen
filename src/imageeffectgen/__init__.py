"""ImageEffectGen - Stylized image filter generator."""

from .filters.jigsaw_folk import JigsawFolkFilter
from .filters.pixel_filter import PixelFilter, RetroPixelFilter, MosaicFilter

__version__ = "0.1.0"
__all__ = ["JigsawFolkFilter", "PixelFilter", "RetroPixelFilter", "MosaicFilter"]
