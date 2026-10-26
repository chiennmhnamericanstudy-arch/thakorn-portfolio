"""Prepare the additional photographs and two supplied product diagrams."""
from pathlib import Path
from PIL import Image, ImageOps
import shutil

ROOT = Path(__file__).resolve().parents[1]
MEDIA = Path('/workspace/scratch/e43ad798ba81/drive_assets_update')
OUT = ROOT / 'dist/assets'
SOURCES = {
    'drone-flight-payload': 'drone-test/rescue-drone-field-trial-hero.jpg',
    'stem-model-maker': 'stem-model/DSC06088.JPG',
    'phyx-workshop': 'phyx-workshop/phyx-workshop.jpg',
    'internship-visit': 'intern-lab/Bản sao của IMG_7112.JPG',
    'droneverse-talk': 'droneverse-event/20260828_143807.jpg',
    'droneverse-exhibition': 'droneverse-audience/DSC06214.JPG',
    'safeflow-floating-village': 'safeflow-outreach/20260809_091846.jpg',
    'safeflow-school-group': 'safeflow-yty-activity/20260731_100339.jpg',
    'wro-collaboration': 'wro-team/20260728_084249.jpg',
    'sviif-delegation': 'sviif-team/Bản sao của Bản sao của IMG_8867.jpg',
}
for name, relative in SOURCES.items():
    im = ImageOps.exif_transpose(Image.open(MEDIA / relative)).convert('RGB')
    im.thumbnail((1700, 1700), Image.Resampling.LANCZOS)
    im.save(OUT / f'{name}.webp', quality=87, method=6)
    im.thumbnail((800, 900), Image.Resampling.LANCZOS)
    im.save(OUT / f'{name}-small.webp', quality=84, method=6)

diagrams = {
    'rescue-drone-operation': MEDIA / 'drone-diagram/rescue-drone-test-log-or-diagram.png',
    'smartvest-operation': Path('/workspace/scratch/e43ad798ba81/drive_assets/vest/smart-life-jacket-drone-workflow.svg.png'),
}
for name, path in diagrams.items():
    # Preserve the supplied PNG exactly for the full-size diagram link.
    shutil.copy2(path, OUT / f'{name}.png')
    im = Image.open(path).convert('RGB')
    im.save(OUT / f'{name}.webp', lossless=True, method=6)
    im.thumbnail((900, 900), Image.Resampling.LANCZOS)
    im.save(OUT / f'{name}-small.webp', quality=92, method=6)
print('Prepared 10 additional photographs and 2 original product diagrams.')
