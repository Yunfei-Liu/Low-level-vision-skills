# Low-Level Vision P2P Skill（GPT-Image）

语言： [English](./README.md) | **中文**

只需一张输入图和一个任务名，即可完成面向 low-level vision / pixel-to-pixel 的图像转换。

本仓库提供：
- 一个可直接使用的 Cursor Skill（图像到图像的低层视觉任务）
- 一套标准化任务体系与 Prompt 约束
- 基于前沿图像模型（默认 `gpt-image-2`）的自动化脚本
- 适合 GitHub 展示的 Demo/Gallery 目录结构
- 支持批量运行的一键脚本

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

## Gallery 展示模板

将你筛选后的输入/输出样例放到 `demos/gallery/`，并维护如下表格：

| 任务 | 输入图 | 输出图 | 说明 |
|---|---|---|---|
| `denoise` | `demos/gallery/denoise_input.jpg` | `demos/gallery/denoise_output.png` | 纹理保真 |
| `deblur` | `demos/gallery/deblur_input.jpg` | `demos/gallery/deblur_output.png` | 抗光晕 |
| `low_light_enhance` | `demos/gallery/low_light_input.jpg` | `demos/gallery/low_light_output.png` | 暗部可见性 |
| `dehaze` | `demos/gallery/dehaze_input.jpg` | `demos/gallery/dehaze_output.png` | 自然色彩 |
| `edge_map` | `demos/gallery/edge_input.jpg` | `demos/gallery/edge_output.png` | 黑底白边 |
| `depth_map` | `demos/gallery/depth_input.jpg` | `demos/gallery/depth_output.png` | 近亮远暗 |
| `semantic_segmentation_map` | `demos/gallery/seg_input.jpg` | `demos/gallery/seg_output.png` | 区域一致性 |

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
