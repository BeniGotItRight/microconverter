"""Image conversions: JPG, PNG, WEBP, BMP, TIFF, GIF, ICO, Image to PDF."""

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
    Convert between image formats or image to PDF.
    Supports: JPG, JPEG, PNG, WEBP, BMP, TIFF, TIF, GIF, ICO.
    PNG/WEBP transparency is composited onto white when converting to JPG or PDF.
    """
    img = Image.open(input_path)
    target_ext = target_ext.lower()

    # For GIF, take the first frame
    if getattr(img, "is_animated", False):
        img.seek(0)

    # Ensure RGB for formats that don't support transparency
    if target_ext in (".jpg", ".jpeg", ".bmp", ".pdf"):
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
        # Keep RGBA if source has it
        if img.mode not in ("RGB", "RGBA", "L", "LA", "P"):
            img = img.convert("RGBA")
        img.save(
            output_path,
            "PNG",
            optimize=True,
            compress_level=6,
        )
    elif target_ext == ".webp":
        img.save(
            output_path,
            "WEBP",
            quality=90,
            method=4,
        )
    elif target_ext == ".bmp":
        img = _ensure_rgb(img)
        img.save(output_path, "BMP")
    elif target_ext in (".tiff", ".tif"):
        img.save(output_path, "TIFF", compression="tiff_lzw")
    elif target_ext == ".gif":
        # Convert to palette mode for GIF
        if img.mode == "RGBA":
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[-1])
            img = bg
        img = img.convert("P", palette=Image.ADAPTIVE, colors=256)
        img.save(output_path, "GIF")
    elif target_ext == ".ico":
        img = _ensure_rgb(img)
        # ICO typically needs small sizes
        img.thumbnail((256, 256), Image.LANCZOS)
        img.save(output_path, "ICO", sizes=[(img.width, img.height)])
    elif target_ext == ".pdf":
        img.save(
            output_path,
            "PDF",
            resolution=150.0,
            quality=95,
            optimize=True,
        )
    else:
        raise ValueError(f"Unsupported image output format: {target_ext}")
