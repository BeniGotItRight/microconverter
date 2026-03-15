"""Image conversions: JPG, PNG, Image to PDF."""

from pathlib import Path

from PIL import Image


def _ensure_rgb(img: Image.Image, background: tuple[int, int, int] = (255, 255, 255)) -> Image.Image:
    """
    Convert image to RGB. For images with transparency (RGBA, LA, P),
    composite onto the given background (default white) instead of black.
    """
    if img.mode == "RGB":
        return img
    if img.mode == "P":
        img = img.convert("RGBA")
    if img.mode in ("RGBA", "LA"):
        background_img = Image.new("RGB", img.size, background)
        alpha = img.split()[-1]
        background_img.paste(img, mask=alpha)
        return background_img
    return img.convert("RGB")


def convert_image(
    input_path: Path, output_path: Path, target_ext: str
) -> None:
    """
    Convert between image formats (JPG/PNG) or image to PDF.
    Uses high-quality settings for best output.
    PNG transparency is composited onto white when converting to PDF or JPG.
    """
    img = Image.open(input_path)
    target_ext = target_ext.lower()

    if target_ext in (".jpg", ".jpeg") or target_ext == ".pdf":
        img = _ensure_rgb(img)

    if target_ext in (".jpg", ".jpeg"):
        img.save(
            output_path,
            "JPEG",
            quality=95,
            optimize=True,
            progressive=True,
        )
    elif target_ext == ".png":
        img.save(
            output_path,
            "PNG",
            optimize=True,
            compress_level=6,
        )
    elif target_ext == ".pdf":
        # Pillow saves images as PDF with embedded raster
        img.save(
            output_path,
            "PDF",
            resolution=150.0,
            quality=95,
            optimize=True,
        )
    else:
        raise ValueError(f"Unsupported image output format: {target_ext}")
