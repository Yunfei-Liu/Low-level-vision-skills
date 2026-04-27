#!/usr/bin/env python3
import argparse
import base64
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Tuple

from openai import OpenAI


BASE_PROMPT = """You are performing a low-level vision pixel-to-pixel transformation.
Task: {task_id}

Input image is the only source of truth. Keep scene geometry, camera viewpoint, object identity, and composition unchanged unless task explicitly requires map rendering.

Primary objective:
{task_objective}

Hard constraints:
- No added or removed objects.
- No text, watermark, logo, or border.
- Keep global framing and perspective consistent with input.
- Preserve fine structures (hair, wires, edges, micro-texture) whenever compatible with the task.

Output specification:
{output_spec}

Quality bar:
{quality_bar}

If uncertain, prefer conservative edits over aggressive hallucination."""


@dataclass(frozen=True)
class TaskSpec:
    objective: str
    output_spec: str
    quality_bar: str


TASKS: Dict[str, TaskSpec] = {
    "denoise": TaskSpec("Remove sensor and chroma noise while preserving true texture and edge sharpness. Avoid plastic smoothing.", "Single realistic RGB image, same scene content.", "Texture-preserving denoising with no waxy skin or blotchy artifacts."),
    "deblur": TaskSpec("Recover sharp details from motion or defocus blur while avoiding ringing and over-sharpening.", "Single realistic RGB image, same framing.", "Sharper edges with minimal halos."),
    "super_resolution": TaskSpec("Increase perceived resolution and detail fidelity naturally without inventing new semantics.", "Single realistic RGB image, high detail appearance.", "Natural micro-details, stable identity and geometry."),
    "jpeg_artifact_removal": TaskSpec("Remove JPEG blocking and ringing artifacts while preserving gradients and details.", "Single realistic RGB image.", "No block noise, no banding amplification."),
    "dehaze": TaskSpec("Reduce atmospheric haze/fog and restore contrast with realistic color and depth cues.", "Single realistic RGB image.", "Natural colors, no aggressive saturation or halos."),
    "derain": TaskSpec("Remove rain streaks and rain veil while preserving scene details and lighting.", "Single realistic RGB image.", "Clean rain removal with stable textures."),
    "deweather": TaskSpec("Clean weather artifacts such as rain, snow, and fog with minimal scene drift.", "Single realistic RGB image.", "Conservative correction with consistent geometry."),
    "low_light_enhance": TaskSpec("Improve brightness and visibility in dark regions with controlled noise and realistic color.", "Single realistic RGB image.", "Brightened shadows without blown highlights."),
    "color_correction": TaskSpec("Correct color cast and restore natural tones while preserving materials.", "Single realistic RGB image.", "Neutral and plausible colors."),
    "white_balance": TaskSpec("Neutralize illumination color cast and maintain realistic neutral surfaces.", "Single realistic RGB image.", "Balanced whites and natural skin/material tones."),
    "exposure_correction": TaskSpec("Balance highlights and shadows; recover details while avoiding clipping.", "Single realistic RGB image.", "Controlled dynamic range with natural look."),
    "lens_distortion_correction": TaskSpec("Correct geometric lens distortion and preserve straight structures.", "Single realistic RGB image.", "Straight lines and stable proportions."),
    "vignette_removal": TaskSpec("Remove corner darkening smoothly while preserving natural illumination.", "Single realistic RGB image.", "Even luminance with no edge artifacts."),
    "reflection_removal": TaskSpec("Suppress reflections and reveal underlying scene as much as feasible.", "Single realistic RGB image.", "Reflection reduced without over-smearing."),
    "shadow_removal": TaskSpec("Reduce cast shadows while maintaining realistic boundaries and albedo.", "Single realistic RGB image.", "Shadow suppression with material consistency."),
    "moire_removal": TaskSpec("Suppress moire/interference patterns while retaining texture fidelity.", "Single realistic RGB image.", "Reduced moire and preserved detail."),
    "grayscale_to_color": TaskSpec("Colorize grayscale image with plausible and coherent natural colors.", "Single realistic RGB image.", "Color coherence across regions and objects."),
    "style_preserving_relight": TaskSpec("Adjust lighting only, preserving geometry and identity.", "Single realistic RGB image.", "Illumination change without content drift."),
    "rectification": TaskSpec("Correct perspective to fronto-parallel when appropriate without removing key content.", "Single realistic RGB image.", "Rectified geometry and minimal stretch artifacts."),
    "inpainting_structural": TaskSpec("Fill missing regions using nearby structure, texture, and illumination cues.", "Single realistic RGB image.", "Coherent fills with seamless boundaries."),
    "outpainting_local_context": TaskSpec("Extend local context with strong consistency to existing scene.", "Single realistic RGB image with slight contextual extension.", "Seamless local continuity."),
    "edge_map": TaskSpec("Generate a clean high-contrast edge map.", "Monochrome edge image, white edges on black background.", "Clear contours, low noise."),
    "line_art_clean": TaskSpec("Generate simplified clean line drawing preserving main contours.", "Monochrome line-art image.", "Crisp lines, minimal clutter."),
    "depth_map": TaskSpec("Generate relative depth map from the input scene.", "Grayscale depth map with near=bright, far=dark.", "Smooth depth with edge awareness."),
    "albedo_layer": TaskSpec("Decompose the image and output the intrinsic albedo (reflectance) layer with illumination removed as much as possible.", "Intrinsic albedo image emphasizing material color, with minimized shading and shadows.", "Uniform reflectance across same materials, minimal lighting imprint, clean boundaries."),
    "shading_layer": TaskSpec("Decompose the image and output the intrinsic shading/illumination layer while suppressing material color variations.", "Intrinsic shading image that captures light and shadow structure.", "Smooth illumination transitions, preserved shadow geometry, reduced texture/albedo leakage."),
    "surface_normals": TaskSpec("Generate surface normal map using standard RGB normal encoding.", "RGB normal map image.", "Consistent normal orientation and smooth surfaces."),
    "saliency_map": TaskSpec("Generate saliency map emphasizing visually important regions.", "Heatmap-like saliency image.", "Stable, interpretable salient regions."),
    "binary_mask_foreground": TaskSpec("Generate binary foreground mask.", "Binary image: foreground white, background black.", "Clean boundary and minimal holes."),
    "semantic_segmentation_map": TaskSpec("Generate semantic segmentation color map with separated classes.", "Color-coded segmentation map image.", "Distinct regions and coherent class boundaries."),
    "photo_to_sketch": TaskSpec("Convert photo into clean sketch while preserving structure.", "Sketch-like monochrome image.", "Recognizable structure and balanced stroke density."),
    "sketch_to_photo": TaskSpec("Render sketch into realistic photo while respecting line geometry.", "Photorealistic RGB image.", "Realistic materials with preserved structure."),
}


ALIASES = {
    "sr": "super_resolution",
    "deblock": "jpeg_artifact_removal",
    "relight": "style_preserving_relight",
    "mask": "binary_mask_foreground",
    "seg_map": "semantic_segmentation_map",
    "albedo": "albedo_layer",
    "shading": "shading_layer",
}


def normalize_task(task: str) -> Tuple[str, str]:
    task_raw = task.strip().lower()
    canonical = ALIASES.get(task_raw, task_raw)
    if canonical not in TASKS:
        available = ", ".join(sorted(TASKS.keys()))
        raise ValueError(f"Unsupported task '{task}'. Available tasks: {available}")
    return canonical, task_raw


def build_prompt(task_id: str) -> str:
    spec = TASKS[task_id]
    return BASE_PROMPT.format(
        task_id=task_id,
        task_objective=spec.objective,
        output_spec=spec.output_spec,
        quality_bar=spec.quality_bar,
    )


def save_output_png(output_b64: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(base64.b64decode(output_b64))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run low-level vision pixel-to-pixel task with GPT image model.")
    parser.add_argument("--input", required=True, help="Path to input image.")
    parser.add_argument("--task", required=True, help="Canonical task id or alias.")
    parser.add_argument("--model", default=os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-2"))
    parser.add_argument("--size", default=os.getenv("OPENAI_IMAGE_SIZE", "1024x1024"))
    parser.add_argument("--output-root", default="outputs")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Input image not found: {input_path}")

    task_id, task_raw = normalize_task(args.task)
    prompt = build_prompt(task_id)

    client = OpenAI()
    with input_path.open("rb") as image_file:
        result = client.images.edit(
            model=args.model,
            image=image_file,
            prompt=prompt,
            size=args.size,
        )

    output_root = Path(args.output_root)
    output_image = output_root / task_id / f"{input_path.stem}__{task_id}.png"
    output_meta = output_root / task_id / f"{input_path.stem}__{task_id}.json"

    b64_data = result.data[0].b64_json
    save_output_png(b64_data, output_image)

    metadata = {
        "task_id": task_id,
        "task_alias": task_raw if task_raw != task_id else None,
        "model": args.model,
        "size": args.size,
        "input_image": str(input_path),
        "output_image": str(output_image.resolve()),
        "prompt": prompt,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    output_meta.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Done: {output_image}")
    print(f"Metadata: {output_meta}")


if __name__ == "__main__":
    main()
