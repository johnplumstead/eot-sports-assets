import os, re, glob, json
from PIL import Image
from rembg import remove, new_session

SRC = glob.glob('/mnt/user-data/uploads/Downloads/Week1_graphics_part*/*.png') + \
      glob.glob('/mnt/user-data/uploads/Downloads/01_Riverview_vs_Spoto_Week1_FINAL_4.png')
os.makedirs('assets/mascots', exist_ok=True)
sess = new_session('u2net')

# generous band above the team-name text, split left/right of the VS divider
BAND = (470, 900)
LEFT  = (25, 505)
RIGHT = (575, 1055)

def slug(s):
    return re.sub(r'(?<!^)(?=[A-Z])', '-', s).lower()

manifest = {}
for path in sorted(SRC):
    base = os.path.basename(path)
    m = re.match(r'\d+_(.+?)_vs_(.+?)_Week1_FINAL', base)
    if not m: continue
    img = Image.open(path).convert('RGB')
    for school, xr in ((m.group(1), LEFT), (m.group(2), RIGHT)):
        key = slug(school)
        if key in manifest: continue
        crop = img.crop((xr[0], BAND[0], xr[1], BAND[1]))
        cut = remove(crop, session=sess)
        bb = cut.getbbox()
        if bb: cut = cut.crop(bb)
        out = f'assets/mascots/{key}.png'
        cut.save(out)
        manifest[key] = {'school': school, 'file': out, 'size': cut.size, 'src': base}
json.dump(manifest, open('data/mascots.json','w'), indent=1)
print(f'{len(manifest)} mascots extracted')
