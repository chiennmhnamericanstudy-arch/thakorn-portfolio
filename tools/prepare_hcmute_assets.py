"""Prepare website copies of the supplied HCMUTE photos and certificate."""
from pathlib import Path
import shutil
import subprocess
import tempfile

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
UPLOAD = Path('/workspace/scratch/e43ad798ba81/upload')
ASSETS = ROOT / 'dist/assets'
DOCUMENTS = ROOT / 'dist/documents'


def web_versions(source, name):
    with Image.open(source) as original:
        frame = ImageOps.exif_transpose(original).convert('RGB')
        frame.thumbnail((2000, 2000), Image.Resampling.LANCZOS)
        frame.save(ASSETS / f'{name}.webp', quality=89, method=6)
        frame.thumbnail((900, 1000), Image.Resampling.LANCZOS)
        frame.save(ASSETS / f'{name}-small.webp', quality=85, method=6)


for filename, name in [
    ('02-20250828_155941.jpg', 'hcmute-vehicle-controls'),
    ('03-20251231_102054.jpg', 'hcmute-drone-electronics'),
    ('04-20250828_155937.jpg', 'hcmute-campus-vehicle'),
]:
    web_versions(UPLOAD / filename, name)

certificate = UPLOAD / '01-Scan2025-12-24_164259.pdf'
DOCUMENTS.mkdir(exist_ok=True)
shutil.copyfile(certificate, DOCUMENTS / 'HCMUTE-AI-Embedded-Systems-Certificate.pdf')
with tempfile.TemporaryDirectory() as temporary:
    prefix = Path(temporary) / 'certificate'
    subprocess.run([
        'pdftoppm', '-f', '1', '-singlefile', '-scale-to', '2000',
        '-png', str(certificate), str(prefix),
    ], check=True)
    web_versions(prefix.with_suffix('.png'), 'hcmute-certificate')
print('Prepared three photos, certificate preview, and unchanged certificate PDF.')
