# Demos

## Input assets

Put source images in:
- `demos/input/`

Recommended starter set:
- portrait with sensor noise
- night street
- hazy landscape
- document/building perspective scene
- texture-rich scene (fabric, foliage, bricks)

## Gallery assets

Put showcase pairs in:
- `demos/gallery/`

Naming suggestion:
- `{task}_input.jpg`
- `{task}_output.png`

## Batch run example

```bash
python .cursor/skills/low-level-vision-p2p/scripts/run_task.py --input demos/input/portrait.jpg --task denoise
python .cursor/skills/low-level-vision-p2p/scripts/run_task.py --input demos/input/street.jpg --task low_light_enhance
python .cursor/skills/low-level-vision-p2p/scripts/run_task.py --input demos/input/haze.jpg --task dehaze
python .cursor/skills/low-level-vision-p2p/scripts/run_task.py --input demos/input/city.jpg --task depth_map
```
