import json, colorsys, numpy as np
from PIL import Image
m=json.load(open('data/mascots.json')); schools={}
def hexof(rgb): return '#%02x%02x%02x'%tuple(int(c) for c in rgb)
for k,v in m.items():
    im=Image.open(v['file']).convert('RGBA').resize((90,90))
    a=np.array(im); px=a[a[:,:,3]>200][:,:3].astype(float)
    if len(px)<40: px=np.array([[30,45,80]],dtype=float)
    hsv=np.array([colorsys.rgb_to_hsv(*(p/255)) for p in px])
    # brand hue = most saturated, reasonably bright pixels
    sel=px[(hsv[:,1]>0.32)&(hsv[:,2]>0.22)]
    base=sel.mean(0) if len(sel)>25 else px.mean(0)
    h,s,val=colorsys.rgb_to_hsv(*(base/255))
    s=min(max(s,.55),.95)
    dark =np.array(colorsys.hsv_to_rgb(h,min(s+.10,1),max(val*0.30,0.09)))*255
    mid  =np.array(colorsys.hsv_to_rgb(h,s,          min(max(val*0.78,0.34),0.62)))*255
    ink  =np.array(colorsys.hsv_to_rgb(h,max(s-.18,.35),min(max(val*1.35,0.62),0.92)))*255
    schools[k]={'name':v['school'].replace('-',' '),'mascot':'','c1':hexof(dark),'c2':hexof(mid),'ink':hexof(ink),'img':v['file']}
json.dump(schools,open('data/schools.json','w'),indent=1)
print(len(schools),'schools with derived palettes')
