"""Prepare inspected Drive activity photos and exact embedded report figures."""
from pathlib import Path
from PIL import Image, ImageOps
import fitz
import shutil

ROOT = Path(__file__).resolve().parents[1]
MEDIA = Path('/workspace/scratch/e43ad798ba81/leadership-update')
OUT = ROOT / 'dist/assets'
SOURCES = {
    'creativism-darahoa-teaching': 'darahoa/IMG_5418.JPG',
    'creativism-darahoa-workshop': 'darahoa/IMG_5484.JPG',
    'creativism-darahoa-stem-demo': 'darahoa/IMG_5577.JPG',
    'creativism-darahoa-gifts': 'darahoa/IMG_3273.JPG',
    'phyx-small-group-learning': 'phyx/IMG_0057.HEIC.jpg',
    'phyx-student-participation': 'phyx/IMG_0068.HEIC.jpg',
    'safeflow-model-building': 'suoi-tuong/20260809_100121.jpg',
    'safeflow-model-boat-test': 'suoi-tuong/20260809_100855.jpg',
    'safeflow-waterside-testing': 'suoi-tuong/20260809_100859.jpg',
    'safeflow-classroom-activity': 'suoi-tuong/20260809_102123.jpg',
    'safeflow-stem-demo': 'suoi-tuong/20260809_094934.jpg',
}
for name, relative in SOURCES.items():
    im = ImageOps.exif_transpose(Image.open(MEDIA / relative)).convert('RGB')
    im.thumbnail((1800, 1800), Image.Resampling.LANCZOS)
    im.save(OUT / f'{name}.webp', quality=87, method=6)
    im.thumbnail((800, 1000), Image.Resampling.LANCZOS)
    im.save(OUT / f'{name}-small.webp', quality=84, method=6)

drone = MEDIA / 'reports/Bao_cao_TRI (1).pdf'
vest = MEDIA / 'reports/SMARTVEST-SAR AN IOT AND AI-DRIVEN LIFE-SAVING SYSTEM FOR MARITIME RESCUE.pdf'
figures = [
    ('drone-pose-states', drone, 46),
    ('drone-monitoring-interface', drone, 48),
    ('smartvest-wearable-firmware', vest, 19),
    ('smartvest-relay-firmware', vest, 21),
]
for name, source, page_number in figures:
    with fitz.open(source) as report:
        # The principal figure is the largest visible raster; exclude page furniture.
        info = max(report[page_number - 1].get_image_info(xrefs=True),
                   key=lambda item: item['width'] * item['height'])
        data = report.extract_image(info['xref'])
        original = OUT / f'{name}.{data["ext"]}'
        original.write_bytes(data['image'])
    im = Image.open(original).convert('RGB')
    im.save(OUT / f'{name}.webp', lossless=True, method=6)
    im.thumbnail((800, 1000), Image.Resampling.LANCZOS)
    im.save(OUT / f'{name}-small.webp', quality=94, method=6)

shutil.copy2(drone, ROOT / 'dist/documents/Rescue-Drone-Project-Report.pdf')
shutil.copy2(vest, ROOT / 'dist/documents/SmartVest-SAR-Project-Report.pdf')
print('Prepared 11 activity photographs, 4 exact report figures, and 2 refreshed reports.')
