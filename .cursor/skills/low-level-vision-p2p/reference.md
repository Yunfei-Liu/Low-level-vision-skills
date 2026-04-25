# Reference

## Canonical Task Mapping

Use exact task IDs from this table. Alias should map to canonical ID before execution.

| Canonical ID | Common Aliases |
|---|---|
| denoise | noise removal, 去噪 |
| deblur | 去模糊, sharpen blur |
| super_resolution | sr, 超分辨率, upscaling |
| jpeg_artifact_removal | 去压缩伪影, deblock |
| dehaze | 去雾 |
| derain | 去雨 |
| deweather | 去天气干扰 |
| low_light_enhance | 夜景增强, brighten dark image |
| color_correction | 色彩校正 |
| white_balance | 白平衡 |
| exposure_correction | 曝光校正 |
| lens_distortion_correction | 畸变校正 |
| vignette_removal | 暗角校正 |
| reflection_removal | 去反光 |
| shadow_removal | 去阴影 |
| moire_removal | 去摩尔纹 |
| grayscale_to_color | 黑白上色, colorization |
| style_preserving_relight | relight |
| rectification | 透视矫正 |
| inpainting_structural | 结构化补全 |
| outpainting_local_context | 局部外扩 |
| edge_map | 边缘图 |
| line_art_clean | 线稿提取 |
| depth_map | 深度图 |
| surface_normals | 法线图 |
| saliency_map | 显著图 |
| binary_mask_foreground | 前景二值 mask |
| semantic_segmentation_map | 语义分割图 |
| photo_to_sketch | 照片转素描 |
| sketch_to_photo | 素描转照片 |

## API Pattern (OpenAI Images Edit)

Python SDK example shape:

```python
from openai import OpenAI

client = OpenAI()
with open("input.png", "rb") as f:
    result = client.images.edit(
        model="gpt-image-2",
        image=f,
        prompt="...",
        size="1024x1024",
    )
```

Persist output as PNG and keep JSON metadata for reproducibility.

## Output Convention

- Image: `outputs/{task_id}/{input_stem}__{task_id}.png`
- Metadata: `outputs/{task_id}/{input_stem}__{task_id}.json`

Metadata fields:
- `task_id`
- `task_alias` (if any)
- `model`
- `size`
- `input_image`
- `output_image`
- `prompt`
- `created_at`

## Safety and Quality Guidelines

- For restoration tasks, avoid semantic hallucination.
- For map outputs (`depth_map`, `edge_map`, masks), prioritize structural consistency over artistic style.
- Reject unsupported task IDs with a clear error listing valid options.
