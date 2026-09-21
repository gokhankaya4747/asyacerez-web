import json,subprocess,io,concurrent.futures as cf
from PIL import Image
u=json.load(open('src/unsplash_urls.json'))
# (unsplash id, output name, width, crop ratio w/h or None)
PLAN=[
("tDKsvBRFFKc","ceviz-1",1600,1.0),("IbL3Zd62Q7Q","ceviz-2",1400,1.0),("3w6qAk35xAg","ceviz-3",1400,1.0),
("auHN-_HBc8Q","badem-1",1600,1.0),("kAWWYOq1cIs","badem-2",1400,1.0),("vkuNgNf2VNk","badem-3",1400,1.0),
("ES9YQ5HAwPI","antep-fistigi-1",1600,1.0),("Zo0TZax87Cc","antep-fistigi-2",1400,1.0),("oPsaQVRaXKI","antep-fistigi-3",1400,1.0),("fiquoT6JZKE","antep-fistigi-4",1400,1.0),
("Su__nb7MsEo","kaju-1",1600,1.0),("FG29J5efMYQ","kaju-2",1400,1.0),("xWRwCmhcWDM","kaju-3",1400,1.0),
("Xku7nuvaM4A","ay-cekirdegi-1",1600,1.0),("k_3Lzjqm_TE","ay-cekirdegi-2",1400,1.0),
("-5xwN7UJEdo","kabak-cekirdegi-1",1600,1.0),
("13lLAWadKwU","yer-fistigi-1",1600,1.0),("TysS85XkjgI","yer-fistigi-2",1400,1.0),("8LbcvCZnmyw","yer-fistigi-3",1400,1.0),
("9-7vSSswKtU","kuru-kayisi-1",1600,1.0),
("E1AAFoR0C80","kuru-incir-1",1600,1.0),
("2-gYuTl3in4","kuru-uzum-1",1600,1.0),
("Ey5nIlYiPYg","hurma-1",1600,1.0),("5t6D43cwOcY","hurma-2",1400,1.0),("_fc9yOAZa3Y","hurma-3",1400,1.0),
("Fr4lk6RdnFg","leblebi-1",1600,1.0),("Mcly3OmxrhI","leblebi-2",1400,1.0),
("pUa1On18Jno","karisik-kuruyemis-1",1600,1.0),("PHIJC0jpx9U","karisik-kuruyemis-2",1400,1.0),
# site imagery
("tDKsvBRFFKc","hero",2400,None),("pUa1On18Jno","hero-mix",2400,None),("jOqJbvo1P9g","ship",2000,None),
("1cqIcrWFQBI","ship-aerial",2000,None),("tjX_sniNzgQ","containers",1600,None),("oBcWSFDYo-0","market",1800,None),
("LoVkcaZbUQw","market-2",1400,None),("4N0dLUmdLAY","bowls",1800,None),("Ql_SWytd1C4","tasting",1400,None),("AMXFr97d00c","ship-sunset",2000,None),
]
def run(p):
    k,name,w,ratio=p
    url=f"https://images.unsplash.com/{u[k]}?w={w*2 if ratio else w}&q=85&fm=jpg"
    data=subprocess.run(['curl','-sL',url],capture_output=True).stdout
    im=Image.open(io.BytesIO(data)).convert('RGB')
    if ratio:
        W,H=im.size; s=min(W,H)
        im=im.crop(((W-s)//2,(H-s)//2,(W-s)//2+s,(H-s)//2+s)).resize((w,w),Image.LANCZOS)
    elif im.width>w: im=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
    out=f"site/assets/img/{'products/' if ratio else ''}{name}.webp"
    im.save(out,'WEBP',quality=80,method=6)
    if ratio: im.resize((640,640),Image.LANCZOS).save(out.replace('.webp','-sm.webp'),'WEBP',quality=78,method=6)
    return name,im.size
for r in cf.ThreadPoolExecutor(10).map(run,PLAN): print(r)
