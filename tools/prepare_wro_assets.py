"""Prepare the user-selected WRO banner and inspected supporting photographs."""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
MEDIA = Path('/workspace/scratch/e43ad798ba81')
ASSETS = {
    'wro-award-banner': MEDIA / 'upload/01-20260729_180650.jpg',
    'wro-robot-field': MEDIA / 'wro-update/20260728_094114.jpg',
    'wro-team-stage': MEDIA / 'wro-update/20260729_180826.jpg',
    'wro-first-place-portrait': MEDIA / 'wro-update/20260729_181519.jpg',
}
for name, source in ASSETS.items():
    im = ImageOps.exif_transpose(Image.open(source)).convert('RGB')
    im.thumbnail((2000, 2000), Image.Resampling.LANCZOS)
    im.save(ROOT / 'dist/assets' / f'{name}.webp', quality=89, method=6)
    im.thumbnail((900, 1000), Image.Resampling.LANCZOS)
    im.save(ROOT / 'dist/assets' / f'{name}-small.webp', quality=85, method=6)
print('Prepared the selected WRO banner and three supporting photographs.')
