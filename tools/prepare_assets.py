from pathlib import Path
from PIL import Image, ImageOps
import shutil

ROOT = Path(__file__).resolve().parents[1]
MEDIA = Path('/workspace/scratch/e43ad798ba81/drive_assets')
OUT = ROOT / 'dist/assets'
OUT.mkdir(parents=True, exist_ok=True)
sources = {
 'portrait':'Bản sao của Bản sao của IMG_8624 2.JPG',
 'drone-field':'drone2/rescue-drone-field-trial-hero.jpg',
 'drone-prototype':'drone/rescue-drone-field-trial-hero.jpg',
 'stem-gears':'stem/Bản sao của DSC06105.JPG',
 'stem-conversation':'stem2/Bản sao của DSC06115.JPG',
 'droneverse-speaker':'droneverse/20260828_110237.jpg',
 'droneverse-team':'droneverse2/20260828_134833.jpg',
 'safeflow-field':'safeflow/20260809_090452.jpg',
 'safeflow-yty':'yty/20260731_100422.jpg',
 'sviif-award':'sviif/Bản sao của IMG_8791 2.JPG',
 'wro':'wro/20260728_084106.jpg',
 'internship':'intern/Bản sao của IMG_7178.JPG',
 'phyx-teaching':'phyx/phyx.jpg',
 'smartvest':'vest/prototype-0.jpeg',
}
for name, source in sources.items():
 im=ImageOps.exif_transpose(Image.open(MEDIA/source)).convert('RGB')
 im.thumbnail((1700,1700),Image.Resampling.LANCZOS)
 im.save(OUT/(name+'.webp'),'WEBP',quality=87,method=6)
 im.thumbnail((800,900),Image.Resampling.LANCZOS)
 im.save(OUT/(name+'-small.webp'),'WEBP',quality=84,method=6)
shutil.copy2('/workspace/scratch/e43ad798ba81/final/brand/Thakorn_TT_Personal_Logo_Transparent.png',OUT/'thakorn-mark.png')
docs=ROOT/'dist/documents';docs.mkdir(exist_ok=True)
shutil.copy2('/workspace/scratch/e43ad798ba81/qa/resume_darahoa_final/Thakorn_Tangphadungrutch_Resume_UPDATED.pdf',docs/'Thakorn-Tangphadungrutch-Resume.pdf')
for folder,name in [('pdf1','SmartVest-SAR-Project-Report.pdf'),('pdf2','Rescue-Drone-Project-Report.pdf'),('pdf3','SVIIF-AI-Finance-Poster.pdf')]:
 shutil.copy2(next((MEDIA/folder).glob('*.pdf')),docs/name)
print('Prepared 14 photographs and project figures; 4 source documents.')
