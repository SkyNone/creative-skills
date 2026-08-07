#!/usr/bin/env python3
"""Prepare, restore, and verify a protected photo panel for rightward image extension."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageOps


def parse_hex_color(value: str) -> tuple[int, int, int]:
    value = value.strip().lstrip("#")
    if len(value) != 6:
        raise argparse.ArgumentTypeError("color must be a six-digit hex value")
    try:
        return tuple(int(value[index : index + 2], 16) for index in (0, 2, 4))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("color must be hexadecimal") from exc


def load_rgb(path: Path) -> Image.Image:
    with Image.open(path) as image:
        return ImageOps.exif_transpose(image).convert("RGB")


def hex_color(rgb: tuple[int, int, int]) -> str:
    return "#%02x%02x%02x" % rgb


def luminance(rgb: tuple[int, int, int]) -> float:
    red, green, blue = rgb
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def chroma(rgb: tuple[int, int, int]) -> int:
    return max(rgb) - min(rgb)


def color_distance(first: tuple[int, int, int], second: tuple[int, int, int]) -> float:
    return sum((a - b) ** 2 for a, b in zip(first, second)) ** 0.5


def extract_palette(image: Image.Image, count: int = 5) -> list[tuple[int, int, int]]:
    sample = image.copy()
    sample.thumbnail((160, 160), Image.Resampling.LANCZOS)
    quantized = sample.quantize(colors=16, method=Image.Quantize.MEDIANCUT).convert("RGB")
    ranked = sorted(quantized.getcolors(maxcolors=256) or [], reverse=True)

    candidates: list[tuple[int, int, int]] = []
    for _frequency, color in ranked:
        if luminance(color) < 18 or luminance(color) > 245:
            continue
        if all(color_distance(color, chosen) >= 34 for chosen in candidates):
            candidates.append(color)
        if len(candidates) >= 10:
            break

    if not candidates:
        candidates = [(128, 128, 128)]

    atmospheric = max(candidates, key=lambda value: luminance(value) - chroma(value) * 0.4)
    environmental = max(candidates, key=lambda value: chroma(value) * 0.35 + 255 - abs(luminance(value) - 120))
    accent = max(candidates, key=lambda value: chroma(value) * 1.6 + abs(luminance(value) - 128) * 0.15)
    dark = min(candidates, key=luminance)

    selected: list[tuple[int, int, int]] = []
    for color in (atmospheric, environmental, accent, dark, *candidates):
        if all(color_distance(color, chosen) >= 24 for chosen in selected):
            selected.append(color)
        if len(selected) == count:
            break
    return selected


def auto_extension_ratio(width: int, height: int) -> float:
    ratio = width / height
    if ratio >= 1.2:
        return 0.62
    if ratio >= 0.9:
        return 0.78
    if ratio >= 0.62:
        return 0.92
    return 0.98


def pixel_digest(image: Image.Image) -> str:
    return hashlib.sha256(image.tobytes()).hexdigest()


def prepare(args: argparse.Namespace) -> None:
    source = load_rgb(args.source)
    source_width, source_height = source.size
    extension_ratio = args.extension_ratio
    if extension_ratio is None:
        extension_ratio = auto_extension_ratio(source_width, source_height)

    extension_width = max(1, round(source_width * extension_ratio))
    seam_pixels = max(1, round(source_width * args.seam_ratio))
    canvas_width = source_width + extension_width
    palette = extract_palette(source)

    canvas = Image.new("RGB", (canvas_width, source_height), args.paper_color)
    canvas.paste(source, (0, 0))
    canvas.save(args.output)

    protected_width = source_width - seam_pixels
    manifest = {
        "source_width": source_width,
        "source_height": source_height,
        "canvas_width": canvas_width,
        "canvas_height": source_height,
        "extension_width": extension_width,
        "extension_ratio": extension_ratio,
        "seam_pixels": seam_pixels,
        "protected_width": protected_width,
        "paper_color": hex_color(args.paper_color),
        "source_palette": [hex_color(color) for color in palette],
        "protected_sha256": pixel_digest(source.crop((0, 0, protected_width, source_height))),
    }
    args.manifest.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def restore(args: argparse.Namespace) -> None:
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    source = load_rgb(args.source)
    generated = load_rgb(args.generated)
    expected_source_size = (manifest["source_width"], manifest["source_height"])
    expected_canvas_size = (manifest["canvas_width"], manifest["canvas_height"])

    if source.size != expected_source_size:
        raise ValueError(f"source size {source.size} does not match manifest {expected_source_size}")
    if generated.size != expected_canvas_size:
        generated = generated.resize(expected_canvas_size, Image.Resampling.LANCZOS)

    seam_pixels = int(manifest["seam_pixels"])
    seam_start = source.width - seam_pixels
    result = generated.copy()
    result.paste(source.crop((0, 0, seam_start, source.height)), (0, 0))

    source_seam = source.crop((seam_start, 0, source.width, source.height))
    generated_seam = generated.crop((seam_start, 0, source.width, source.height))
    mask = Image.new("L", (seam_pixels, source.height))
    mask.putdata(
        [
            round(255 * x / max(1, seam_pixels - 1))
            for _y in range(source.height)
            for x in range(seam_pixels)
        ]
    )
    result.paste(Image.composite(generated_seam, source_seam, mask), (seam_start, 0))
    result.save(args.output)


def verify(args: argparse.Namespace) -> None:
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    source = load_rgb(args.source)
    final = load_rgb(args.final)
    protected_width = int(manifest["protected_width"])
    source_region = source.crop((0, 0, protected_width, source.height))
    final_region = final.crop((0, 0, protected_width, source.height))
    source_digest = pixel_digest(source_region)
    final_digest = pixel_digest(final_region)
    expected_digest = manifest["protected_sha256"]
    if source_digest != expected_digest or final_digest != expected_digest:
        raise SystemExit("verification failed: protected photo pixels changed")
    print(f"verified: {protected_width} protected columns are pixel-identical")


def add_common_paths(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare_parser = subparsers.add_parser("prepare")
    add_common_paths(prepare_parser)
    prepare_parser.add_argument("--output", type=Path, required=True)
    prepare_parser.add_argument("--extension-ratio", type=float)
    prepare_parser.add_argument("--seam-ratio", type=float, default=0.055)
    prepare_parser.add_argument("--paper-color", type=parse_hex_color, default=parse_hex_color("#eee7db"))
    prepare_parser.set_defaults(func=prepare)

    restore_parser = subparsers.add_parser("restore")
    add_common_paths(restore_parser)
    restore_parser.add_argument("--generated", type=Path, required=True)
    restore_parser.add_argument("--output", type=Path, required=True)
    restore_parser.set_defaults(func=restore)

    verify_parser = subparsers.add_parser("verify")
    add_common_paths(verify_parser)
    verify_parser.add_argument("--final", type=Path, required=True)
    verify_parser.set_defaults(func=verify)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    for attribute in ("output", "manifest"):
        path = getattr(args, attribute, None)
        if path is not None:
            path.parent.mkdir(parents=True, exist_ok=True)
    args.func(args)


if __name__ == "__main__":
    main()
