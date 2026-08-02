import json, math
from PIL import Image, ImageDraw, ImageFont
m = json.load(open('data/mascots.json'))
keys = sorted(m)
COLS, CELL, LBL = 6, 300, 38
rows = math.ceil(len(keys)/COLS)
sheet = Image.new('RGB', (COLS*CELL, rows*(CELL+LBL)), (245,245,247))
d = ImageDraw.Draw(sheet)
try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 19)
except: f = ImageFont.load_default()
for i,k in enumerate(keys):
    im = Image.open(m[k]['file']).convert('RGBA')
    im.thumbnail((CELL-24, CELL-24))
    x, y = (i%COLS)*CELL, (i//COLS)*(CELL+LBL)
    tile = Image.new('RGBA', (CELL, CELL), (255,255,255,255))
    tile.alpha_composite(im, ((CELL-im.width)//2, (CELL-im.height)//2))
    sheet.paste(tile.convert('RGB'), (x,y))
    d.rectangle([x,y,x+CELL-1,y+CELL+LBL-1], outline=(210,210,215))
    d.text((x+10, y+CELL+9), k, font=f, fill=(20,20,25))
sheet.save('out/mascot_contact_sheet.png')
print(sheet.size, len(keys))
