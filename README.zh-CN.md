# Low-Level Vision P2P Skill（GPT-Image）

语言： [English](./README.md) | **中文**

只需一张输入图和一个任务名，即可完成面向 low-level vision / pixel-to-pixel 的图像转换。

本仓库提供：
- 一个可直接使用的 Cursor Skill（图像到图像的低层视觉任务）
- 一套标准化任务体系与 Prompt 约束
- 基于前沿图像模型（默认 `gpt-image-2`）的自动化脚本
- 适合 GitHub 展示的 Demo/Gallery 目录结构
- 支持批量运行的一键脚本
- 提供跨 IDE 集成文档（Cursor、Claude 工作流、通用终端 IDE）

## 这个项目解决了什么

- **统一入口**：输入参数固定为 `--input` + `--task`
- **可控质量**：统一 hard constraints，降低 hallucination 风险
- **可复现**：每次输出都保存 prompt / model / size 元数据
- **易发布**：Skill 文件、说明文档、展示模板已齐备

## 支持的任务类别

- 图像恢复增强：去噪、去模糊、超分、去雾、去雨、低照增强、压缩伪影去除等
- 稠密预测图输出：边缘图、深度图、法线图、显著图、mask、分割图
- 几何保持变换：透视矫正、结构化补全、局部外扩
- 领域转换（尽量像素对齐）：照片/素描互转、地图/遥感风格互转

完整任务清单见：
- `.cursor/skills/low-level-vision-p2p/SKILL.md`

<details>
<summary><strong>支持的 low-level vision 任务（点击展开）</strong></summary>

### 图像恢复与增强

- `denoise`：去除传感器噪声/色噪，尽量保留纹理
- `deblur`：从运动模糊/离焦模糊中恢复清晰细节
- `super_resolution`：提升感知分辨率并保持结构一致
- `jpeg_artifact_removal`：去除压缩块效应与振铃伪影
- `dehaze`：去雾并恢复自然对比度
- `derain`：去除雨丝和雨幕
- `deweather`：去除雨/雪/雾等复合天气干扰
- `low_light_enhance`：低照度增强并控制噪声
- `color_correction`：纠正全局或局部偏色
- `white_balance`：白平衡校正，消除光照色偏
- `exposure_correction`：平衡高光和阴影细节
- `lens_distortion_correction`：校正桶形/枕形畸变
- `vignette_removal`：去除暗角
- `reflection_removal`：抑制玻璃/镜面反射
- `shadow_removal`：减弱投影阴影并保持材质真实
- `moire_removal`：去除摩尔纹/干涉纹

### 色彩与光照映射

- `grayscale_to_color`：灰度图自然上色
- `day_to_night`：白天场景转夜景风格
- `night_to_day`：夜景转白天外观
- `style_preserving_relight`：保持结构身份不变，仅改变光照
- `hdr_like_tone_mapping`：提升局部动态范围观感

### 几何与视角保持变换

- `rectification`：文档/建筑等透视矫正
- `inpainting_structural`：基于周边结构的缺失区域补全
- `outpainting_local_context`：在局部上下文一致前提下外扩

### 稠密预测风格输出

- `edge_map`：黑底白边的边缘图
- `line_art_clean`：轮廓为主的干净线稿
- `depth_map`：相对深度图（近亮远暗）
- `surface_normals`：RGB 法线图
- `saliency_map`：显著性热度图
- `binary_mask_foreground`：前景白、背景黑的二值 mask
- `semantic_segmentation_map`：语义分割彩色区域图

### 领域转换（偏像素对齐）

- `photo_to_sketch`：照片转结构保持的素描
- `sketch_to_photo`：素描转写实图像
- `map_to_satellite_like`：地图风格转遥感风格
- `satellite_like_to_map`：遥感风格转地图风格
- `thermal_like_render`：热成像风格可视化

</details>

## 快速开始

### 1）安装依赖

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2）配置 API Key

```bash
export OPENAI_API_KEY="your_key_here"
```

### 3）运行单个任务

```bash
python .cursor/skills/low-level-vision-p2p/scripts/run_task.py \
  --input demos/input/example.jpg \
  --task dehaze \
  --model gpt-image-2 \
  --size 1024x1024
```

输出文件：
- `outputs/dehaze/example__dehaze.png`
- `outputs/dehaze/example__dehaze.json`

### 4）批量生成 Demo

```bash
python .cursor/skills/low-level-vision-p2p/scripts/run_batch.py \
  --manifest demos/tasks.example.json \
  --model gpt-image-2 \
  --size 1024x1024
```

## IDE 兼容性

| IDE / Agent | 状态 | 使用方式 |
|---|---|---|
| Cursor | 已就绪 | 使用 `.cursor/skills/low-level-vision-p2p/` 原生 skill |
| Claude 风格 IDE 工作流 | 已就绪 | 使用 `adapters/claude/` 适配文档并调用共享 CLI |
| 其他 IDE | 已就绪 | 在终端/任务系统直接调用 CLI |

集成文档入口：
- `docs/IDE_INTEGRATION.md`
- `adapters/claude/SKILL.md`
- `adapters/claude/PROMPT_TEMPLATE.md`

## Gallery 预览

### Denoise

<table>
  <tr>
    <th>输入</th>
    <th>输出</th>
  </tr>
  <tr>
    <td><img src="./demos/input/denoise_input.png" alt="denoise input" style="width:320px;height:220px;object-fit:cover;"></td>
    <td><img src="./outputs/gallery/denoise_output.png" alt="denoise output" style="width:320px;height:220px;object-fit:cover;"></td>
  </tr>
</table>

### Deblur

<table>
  <tr>
    <th>输入</th>
    <th>输出</th>
  </tr>
  <tr>
    <td><img src="./demos/input/deblur_input.png" alt="deblur input" style="width:320px;height:220px;object-fit:cover;"></td>
    <td><img src="./outputs/gallery/deblur_output.png" alt="deblur output" style="width:320px;height:220px;object-fit:cover;"></td>
  </tr>
</table>

### Low-light Enhance

<table>
  <tr>
    <th>输入</th>
    <th>输出</th>
  </tr>
  <tr>
    <td><img src="./demos/input/low_light_input.jpeg" alt="low-light input" style="width:320px;height:220px;object-fit:cover;"></td>
    <td><img src="./outputs/gallery/low_light_output.png" alt="low-light output" style="width:320px;height:220px;object-fit:cover;"></td>
  </tr>
</table>

## Skill 触发示例

当用户提出如下需求时，skill 应被触发：
- “把这张图做去噪”
- “基于这张图生成 depth map”
- “对这张图做 pixel-to-pixel dehaze”
- “把这张照片变成干净线稿”

## 仓库结构

```text
.cursor/skills/low-level-vision-p2p/
  SKILL.md
  reference.md
  examples.md
  scripts/run_task.py
  scripts/run_batch.py
demos/
  input/
  gallery/
outputs/
```

## 建议的开源发布清单

- 准备 8-12 组代表性样例（室内/室外/人像/夜景/复杂纹理）
- 增加失败案例说明（边界能力和预期管理）
- 补充质量和时延说明（主观评估 + 运行耗时）
- 视需求锁定依赖版本（`requirements.txt`）
- 按需增加 `LICENSE` 与 `CITATION`

## 后续可扩展方向

- 增加自动质量评估（如 SSIM、LPIPS、边缘一致性）
- 增加任务档位预设（`fast` / `balanced` / `quality`）
- 增加自动生成 Markdown Gallery 的脚本
- 增加多后端适配层（不同图像模型供应商）
