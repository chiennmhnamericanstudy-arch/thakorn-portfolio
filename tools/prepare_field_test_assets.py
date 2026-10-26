"""Prepare responsive website copies of the eight user-selected test photos."""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
UPLOAD = Path('/workspace/scratch/e43ad798ba81/upload')
ASSETS = ROOT / 'dist/assets'
PHOTOS = [
    ('01-20260815_102434.jpg', 'drone-coastal-water-test'),
    ('02-20260815_120704.jpg', 'drone-coastal-prototype'),
    ('03-20260809_110837.jpg', 'drone-waterside-prototype'),
    ('04-20260809_103038.jpg', 'drone-field-student-guidance'),
    ('05-20260809_103448.jpg', 'drone-community-demonstration'),
    ('06-20260809_105952.jpg', 'smartvest-rowing-test'),
    ('07-20260809_104414.jpg', 'smartvest-wearable-demonstration'),
    ('08-20260809_110012.jpg', 'smartvest-boat-closeup'),
]

for filename, name in PHOTOS:
    with Image.open(UPLOAD / filename) as original:
        frame = ImageOps.exif_transpose(original).convert('RGB')
        frame.thumbnail((2000, 2000), Image.Resampling.LANCZOS)
        frame.save(ASSETS / f'{name}.webp', quality=89, method=6)
        frame.thumbnail((900, 1000), Image.Resampling.LANCZOS)
        frame.save(ASSETS / f'{name}-small.webp', quality=85, method=6)
    print(f'Prepared {name}')
