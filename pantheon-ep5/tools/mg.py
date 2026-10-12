import math,random,sys,subprocess,json
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageChops
W,H=1280,720
OBS=(10,9,8);GOLD=(201,168,76);LG=(232,201,122);EMB=(196,90,32);PAR=(240,232,208);DIM=(70,64,52);LAND=(26,24,18);SEA=(14,22,24)
FD='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf';FB='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf';FI='/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf'
def F(p,s): return ImageFont.truetype(p,s)
f20,f26,f34,f44,f64=F(FD,20),F(FD,26),F(FD,34),F(FD,44),F(FD,64)
fb54,fb90=F(FB,54),F(FB,92)
fi30,fi36=F(FI,30),F(FI,36)
def cl(x,a=0,b=1): return max(a,min(b,x))
def ease(p): p=cl(p); return p*p*(3-2*p)
def lerp(a,b,t): return a+(b-a)*t
def mix(c1,c2,t): return tuple(int(lerp(c1[i],c2[i],cl(t))) for i in range(3))
def seg(p,a,b): return cl((p-a)/(b-a))
ROAD=[(300,520),(380,450),(470,370),(540,300),(600,235),(690,190),(800,180),(910,225),(990,300),(1040,390)]
SEAP=[(0,0),(1280,0),(1280,140),(820,150),(700,175),(600,215),(520,290),(440,360),(340,450),(260,520),(0,560)]
DESERT=[(430,430),(640,330),(900,330),(930,700),(430,700)]
def partial(pts,p):
    p=cl(p)
    if p<=0: return pts[:1]
    L=[math.dist(pts[i],pts[i+1]) for i in range(len(pts)-1)];T=sum(L);tgt=T*p;out=[pts[0]];acc=0
    for i,l in enumerate(L):
        if acc+l>=tgt:
            r=(tgt-acc)/l if l else 0;out.append((lerp(pts[i][0],pts[i+1][0],r),lerp(pts[i][1],pts[i+1][1],r)));return out
        acc+=l;out.append(pts[i+1])
    return out
def at(pts,p):
    q=partial(pts,p);return q[-1]
class Fr:
    def __init__(s):
        s.im=Image.new('RGB',(W,H),OBS);s.d=ImageDraw.Draw(s.im)
        s.g=Image.new('RGB',(W,H),(0,0,0));s.gd=ImageDraw.Draw(s.g)
    def out(s):
        sm=s.g.resize((W//4,H//4)).filter(ImageFilter.GaussianBlur(3)).resize((W,H))
        return ImageChops.add(s.im,sm)
    def line(s,pts,col=GOLD,w=3,glow=True):
        if len(pts)>1:
            s.d.line(pts,fill=col,width=w,joint='curve')
            if glow: s.gd.line(pts,fill=tuple(int(c*0.8) for c in col),width=w+6,joint='curve')
    def dot(s,xy,r,col=GOLD,glow=True):
        x,y=xy;s.d.ellipse([x-r,y-r,x+r,y+r],fill=col)
        if glow: s.gd.ellipse([x-r*2,y-r*2,x+r*2,y+r*2],fill=tuple(int(c*0.7) for c in col))
    def text(s,xy,t,font,col=GOLD,anchor='mm',a=1.0):
        c=mix(OBS,col,a);s.d.text(xy,t,font=font,fill=c,anchor=anchor)
def mapbase(f,tf,desert=0.0,labels=True,landcol=LAND):
    P=lambda pts:[tf(p) for p in pts]
    f.d.polygon(P([(0,0),(1280,0),(1280,720),(0,720)]),fill=landcol)
    f.d.polygon(P(SEAP),fill=SEA)
    if desert>0: f.d.polygon(P(DESERT),fill=mix(landcol,(8,7,6),desert))
    f.d.line(P([(0,560),(260,520),(340,450),(440,360),(520,290),(600,215),(700,175),(820,150),(1280,140)]),fill=(60,52,36),width=2)
    if labels:
        f.text(tf((190,640)),'EGYPT',f20,DIM);f.text(tf((1090,560)),'MESOPOTAMIA',f20,DIM)
def sqz(s): return lambda xy:(640+(xy[0]-640)*s,xy[1])
def zoom(k=1.9,c=(600,235)): return lambda xy:(640+(xy[0]-c[0])*k,360+(xy[1]-c[1])*k)
IDT=lambda xy:xy
NAMES=['EGYPT','ASSYRIA','BABYLON','MACEDON','ROME','THE CALIPHS','THE CRUSADERS','THE MAMLUKS','THE OTTOMANS','BRITAIN']
def ledger(f,lit,road=0.0,date=None):
    for i,n in enumerate(NAMES):
        f.text((640,70+i*58),n,f34,GOLD,a=cl(0.18+0.82*lit[i]))
        if lit[i]>0.5: f.d.line([(470,70+i*58+27),(810,70+i*58+27)],fill=mix(OBS,GOLD,0.25*lit[i]),width=1)
    if road>0: f.line(partial([(240,690),(1040,690)],road),GOLD,3)
    if date: f.text((1180,60),date,fi36,PAR,anchor='rm')
# ---- scenes: fn(p,t,dur)->Image
def s_B001(p,t,du):
    f=Fr();s=lerp(1,0.62,ease(p));tf=sqz(s);mapbase(f,tf);f.line([tf(q) for q in ROAD],(120,100,60),2,False)
    f.d.line([(640,60),(640,680)],fill=mix(OBS,GOLD,ease(seg(p,0.2,0.8))),width=2);return f.out()
def s_B004(p,t,du):
    f=Fr();tf=sqz(0.62);mapbase(f,tf,desert=ease(seg(p,0,0.4)));R=[tf(q) for q in ROAD]
    for side in(0,1):
        pts=R[:6] if side==0 else R[::-1][:5]
        for k in range(5):
            q=(p*1.3+k*0.2)%1.0;pt=at(pts,q);f.dot(pt,5,EMB if side else GOLD)
        f.line(partial(pts,ease(seg(p,0.1,1))),mix(OBS,EMB if side else GOLD,0.6),2,False)
    f.d.line([(640,60),(640,680)],fill=(60,52,36),width=1);return f.out()
def s_B005(p,t,du):
    f=Fr();tf=sqz(0.62);mapbase(f,tf,desert=1.0);R=[tf(q) for q in ROAD]
    f.line(partial(R,ease(seg(p,0,0.6))),GOLD,5);f.line(R,GOLD,2,False) if p>0.6 else None
    return f.out()
def s_B006(p,t,du):
    f=Fr();tf=sqz(0.62);mapbase(f,tf,desert=1.0);R=[tf(q) for q in ROAD];f.line(R,GOLD,3)
    a,b=tf((500,300)),tf((690,300));k=ease(seg(p,0.1,0.5));x2=lerp(a[0],b[0],k)
    f.d.line([a,(x2,a[1])],fill=LG,width=4);f.gd.line([a,(x2,a[1])],fill=GOLD,width=9)
    for x in(a[0],x2): f.d.line([(x,a[1]-12),(x,a[1]+12)],fill=LG,width=3)
    f.text((a[0]-14,a[1]),'sea',fi30,DIM,'rm',a=k);f.text((b[0]+14,a[1]),'hills',fi30,DIM,'lm',a=k)
    f.text((640,640),'Narrowest point, before 1967: about 9 miles.',fi36,PAR,a=seg(p,0.35,0.55)*(1-seg(p,0.88,1)));return f.out()
def s_B012(p,t,du):
    lit=[1-ease(seg(p,i*0.085,i*0.085+0.1)) for i in range(10)];f=Fr();ledger(f,lit,road=ease(seg(p,0.7,1)));return f.out()
def s_B017(p,t,du):
    f=Fr();k=ease(seg(p,0,0.55));f.line(partial([(240,470),(1040,470)],k),GOLD,4)
    f.text((640,lerp(380,350,ease(seg(p,0.3,0.8)))),'THE LAND EVERY',fb54,GOLD,a=ease(seg(p,0.3,0.8)))
    f.text((640,lerp(445,415,ease(seg(p,0.3,0.8)))),'EMPIRE WANTED',fb54,GOLD,a=ease(seg(p,0.35,0.85)));return f.out()
def s_B021(p,t,du):
    tf=zoom(1.9);f=Fr();mapbase(f,tf,labels=False);R=[tf(q) for q in ROAD];f.line(partial(R,ease(seg(p,0,0.7))),GOLD,4)
    f.text((640,470),'CANAAN',f34,GOLD,a=ease(seg(p,0.5,0.9)));return f.out()
HILLS_A=[(380,240),(560,250),(570,170),(430,150)];HILLS_B=[(620,240),(780,250),(800,160),(640,150)]
def s_B025(p,t,du):
    tf=zoom(2.2);f=Fr();mapbase(f,tf,labels=False);R=[tf(q) for q in ROAD];f.line(R,(120,100,60),2,False)
    for hp in(HILLS_A,HILLS_B): pass
    f.d.polygon([tf(q) for q in [(330,140),(595,150),(600,60),(330,40)]],fill=(40,36,26));f.d.polygon([tf(q) for q in [(615,150),(900,140),(900,40),(610,60)]],fill=(40,36,26))
    m=tf((600,235));pulse=0.5+0.5*math.sin(t*6);f.dot(m,8+4*pulse,GOLD)
    for k in range(8):
        q=(p*1.1+k/8.0)%1.0;pt=at([tf((300,520)),tf((470,370)),m],q);f.dot(pt,4,EMB)
        pt2=at([tf((1040,390)),tf((910,225)),tf((800,180)),m],q);f.dot(pt2,4,EMB)
    f.text((m[0],m[1]+40),'MEGIDDO',f26,GOLD,a=ease(seg(p,0.2,0.5)));return f.out()
random.seed(7);VIL=[(random.gauss(600,60),random.gauss(300,45)) for _ in range(46)]
def s_B034(p,t,du):
    tf=zoom(2.0,(600,300));f=Fr();mapbase(f,tf,labels=False);f.line([tf(q) for q in ROAD],(90,78,48),2,False)
    for i,v in enumerate(VIL):
        a=ease(seg(p,i/60.0,i/60.0+0.25));f.dot(tf(v),4,mix(OBS,GOLD,a),glow=a>0.5)
    f.text(tf((600,215)),'ISRAEL',f44,GOLD,a=ease(seg(p,0.55,0.95)));return f.out()
def s_B040(p,t,du):
    tf=zoom(2.0,(600,300));f=Fr();mapbase(f,tf,labels=False);f.line([tf(q) for q in ROAD],(90,78,48),2,False)
    for i,v in enumerate(VIL):
        a=ease(seg(p,i/90.0,i/90.0+0.2));f.dot(tf((v[0],v[1]-30*(1 if v[1]<300 else -1)*0+0)),4,mix(OBS,GOLD if v[1]<300 else LG,a),glow=a>0.5)
    f.d.line([tf((470,300)),tf((730,300))],fill=mix(OBS,DIM,ease(seg(p,0.25,0.4))),width=1)
    f.text(tf((600,205)),'ISRAEL',f34,GOLD,a=ease(seg(p,0.3,0.45)));f.text(tf((600,245)),'SAMARIA',f20,LG,a=ease(seg(p,0.45,0.55)))
    f.text(tf((600,375)),'JUDAH',f34,GOLD,a=ease(seg(p,0.5,0.65)));f.text(tf((600,340)),'JERUSALEM',f20,LG,a=ease(seg(p,0.65,0.8)))
    j=tf((600,325));f.d.ellipse([j[0]-12,j[1]-12,j[0]+12,j[1]+12],outline=mix(OBS,LG,ease(seg(p,0.65,0.8))),width=2);return f.out()
def s_B050(p,t,du):
    tf=zoom(2.0,(600,300));f=Fr();mapbase(f,tf,labels=False);f.line([tf(q) for q in ROAD],(90,78,48),2,False)
    for v in VIL:
        if v[1]<300:
            k=ease(seg(p,0.15,0.9));x=v[0]+k*260;c=mix(GOLD,(90,90,90),ease(seg(p,0,0.4)));c=mix(c,OBS,seg(p,0.6,1));f.dot(tf((x,v[1])),4,c,glow=False)
        else: f.dot(tf(v),4,LG)
    f.text(tf((600,205)),'ISRAEL',f34,GOLD,a=1-ease(seg(p,0.1,0.5)));f.text(tf((600,375)),'JUDAH',f34,GOLD);f.text(tf((600,340)),'JERUSALEM',f20,LG);return f.out()
def s_B055(p,t,du):
    lit=[0.0,1-ease(seg(p,0,0.35)),ease(seg(p,0.25,0.6))]+[0.0]*7;f=Fr();ledger(f,lit,date=None)
    f.text((1180,60),'586 BCE',fi36,PAR,'rm',a=ease(seg(p,0.5,0.7)));return f.out()
def s_B082(p,t,du):
    tf=zoom(1.9);f=Fr();mapbase(f,tf,labels=False);f.line([tf(q) for q in ROAD],(90,78,48),2,False)
    f.text((640,360),'JUDEA',f64,GOLD,a=1-ease(seg(p,0.05,0.35)))
    s='SYRIA PALAESTINA';n=int(len(s)*ease(seg(p,0.35,0.9)));f.text((640,360),s[:n],f44,GOLD,anchor='mm') if n else None
    return f.out()
def s_B085(p,t,du):
    f=Fr();mapbase(f,IDT,labels=False);o=(640,300);f.dot(o,7,GOLD)
    T=[('BABYLON',(1020,360)),('NORTH AFRICA',(300,600)),('SPAIN',(110,410)),('EUROPE',(560,40))]
    for i,(n,xy) in enumerate(T):
        k=ease(seg(p,0.05+i*0.12,0.5+i*0.12));f.line(partial([o,xy],k),GOLD,2)
        a=ease(seg(p,0.5+i*0.1,0.8+i*0.1))
        if k>0.99: f.dot(xy,6,mix(OBS,GOLD,a))
        f.text((xy[0],xy[1]+(22 if n!='EUROPE' else 26)),n,f20,GOLD,a=a)
    return f.out()
def s_B094(p,t,du):
    f=Fr();c=(640,360)
    for i,r in enumerate((70,135,200)):
        k=ease(seg(p,i*0.06,0.6+i*0.06));rr=r*k
        if rr>1: f.d.ellipse([c[0]-rr,c[1]-rr,c[0]+rr,c[1]+rr],outline=GOLD,width=3);f.gd.ellipse([c[0]-rr,c[1]-rr,c[0]+rr,c[1]+rr],outline=GOLD,width=7)
    f.dot(c,5,LG);return f.out()
EUR={'iberia':[(300,470),(420,440),(430,530),(330,560)],'france':[(430,380),(560,360),(580,450),(450,470)],'british':[(380,260),(440,240),(450,330),(390,350)],
'germany':[(560,320),(660,310),(670,400),(570,410)],'italy':[(590,430),(650,420),(700,560),(650,570)],'scand':[(560,150),(660,110),(700,250),(600,270)],
'poland':[(680,300),(790,290),(800,380),(690,390)],'russia':[(800,200),(1010,180),(1030,420),(810,400)],'balkans':[(680,410),(760,400),(780,520),(700,530)],'turkey':[(790,450),(930,440),(940,520),(800,530)]}
ECOL=[(120,70,60),(70,90,130),(90,120,90),(130,110,60),(100,70,120),(60,110,120),(130,80,90),(80,80,110),(110,100,60),(120,90,60)]
def s_B107(p,t,du):
    f=Fr()
    for i,(n,pts) in enumerate(EUR.items()):
        k=ease(seg(p,i*0.07,i*0.07+0.15));f.d.polygon(pts,fill=mix(OBS,ECOL[i],k))
    k=ease(seg(p,0.78,0.95));pt=(1180,560);f.dot(pt,6+6*(0.5+0.5*math.sin(t*5)),GOLD) if k>0 else None
    return f.out()
def s_B118(p,t,du):
    f=Fr();mapbase(f,IDT,labels=False);dst=(560,300);k=ease(seg(p,0.05,0.85))
    for s0 in((250,690),(1000,690)):
        f.line(partial([s0,dst],k),GOLD,3)
    f.dot(dst,6+(5*ease(seg(p,0.85,1))),LG);return f.out()
def s_B120(p,t,du):
    f=Fr()
    labels=['LETTERS TO ARAB LEADERS','DIVIDED BY A SECRET LINE','A NATIONAL HOME FOR THE JEWISH PEOPLE']
    cols=[(70,66,52),(84,62,42),(58,72,62)]
    for i in range(3):
        k=ease(seg(p,i*0.22,i*0.22+0.3));x=lerp(1500 if i%2 else -300,500+i*140,k);y0=110+i*30
        f.d.rectangle([x-230,y0,x+230,y0+380],outline=mix(OBS,GOLD,0.7*k),width=2,fill=mix(OBS,cols[i],0.55*k))
        patch=[(x-120,y0+150),(x-40,y0+90),(x+60,y0+120),(x+110,y0+230),(x+20,y0+330),(x-90,y0+300)]
        if k>0.5: f.d.polygon([(500+q[0]-x+0,q[1]-i*30+0) if False else q for q in patch],outline=mix(OBS,LG,k))
        if i==1: f.d.line([(x-180,y0+330),(x+190,y0+90)],fill=mix(OBS,EMB,k),width=3)
        f.text((640,590+i*34),labels[i],f20,GOLD,a=seg(p,0.25+i*0.2,0.45+i*0.2))
    f.text((640,60),'MEANING DISPUTED',f34,EMB,a=ease(seg(p,0.5,0.7)));return f.out()
COAST=[(300,300),(420,250),(520,260),(610,330),(640,430),(620,560),(540,640),(430,640),(340,520)]
def s_B129(p,t,du):
    f=Fr();f.d.polygon(COAST,fill=(54,52,46))
    k=ease(seg(p,0.05,0.5));line=[(380,230),(560,330),(520,450),(600,600)]
    f.line(partial(line,k),GOLD,10)
    if p>0.55:
        c=ease(seg(p,0.55,1));random.seed(3)
        for j in range(12):
            a=at(line,j/12.0);ln=[a];x,y=a
            for _ in range(4): x+=random.uniform(-22,22);y+=random.uniform(8,24);ln.append((x,y))
            f.d.line(partial(ln,c),fill=OBS,width=2)
    f.text((1180,60),'29 November 1947',fi36,PAR,'rm',a=ease(seg(p,0.1,0.3)));return f.out()
SH_A=(86,98,112);SH_B=(112,102,88)
def s_B130(p,t,du):
    f=Fr();f.d.polygon(COAST,fill=(40,38,32))
    a=[(300,300),(420,250),(520,260),(610,330),(580,420),(450,420),(400,330)];b=[(580,420),(640,430),(620,560),(540,640),(430,640),(340,520),(450,420)]
    k=ease(seg(p,0.05,0.4))
    f.d.polygon(a,fill=mix(OBS,SH_A,k));f.d.polygon(b,fill=mix(OBS,SH_B,k))
    jr=[(500,400),(560,400),(560,450),(500,450)]
    f.d.polygon(jr,fill=mix(OBS,(150,150,150),0.3*k))
    for x in range(500,562,8): f.d.line([(x,450),(x+50,400)] if False else [(x,400),(x-10,450)],fill=mix(OBS,PAR,0.7*k),width=1)
    f.text((900,300),'A JEWISH STATE',f26,mix((255,255,255),SH_A,0.2),a=ease(seg(p,0.4,0.6)));f.text((900,360),'AN ARAB STATE',f26,mix((255,255,255),SH_B,0.2),a=ease(seg(p,0.55,0.75)))
    f.text((900,420),'JERUSALEM UNDER',f20,PAR,a=ease(seg(p,0.7,0.9)));f.text((900,448),'INTERNATIONAL RULE',f20,PAR,a=ease(seg(p,0.7,0.9)));return f.out()
def s_B131(p,t,du):
    f=Fr();vals=[(33,'FOR'),(13,'AGAINST'),(10,'ABSTAINED')];base=560
    for i,(v,l) in enumerate(vals):
        x=380+i*260;k=ease(seg(p,i*0.1,0.7+i*0.05));h=v*10*k
        f.d.rectangle([x-60,base-h,x+60,base],fill=(120,110,90));f.text((x,base+34),f'{v} {l}',f26,PAR,a=seg(p,0.7,0.9))
    return f.out()
def s_B138(p,t,du):
    f=Fr();f.d.polygon(COAST,fill=(40,38,32));tgt=(560,360)
    S=[('EGYPT',(200,640)),('TRANSJORDAN',(980,430)),('SYRIA',(900,130)),('IRAQ',(1180,260)),('LEBANON',(640,90))]
    for i,(n,xy) in enumerate(S):
        k=ease(seg(p,0.1+i*0.08,0.85));pt=at([xy,tgt],k*0.9);f.line([xy,pt],(150,140,120),2,False);f.dot(pt,5,(190,180,150),False)
        f.text((xy[0],xy[1]-24),n,f20,PAR,a=ease(seg(p,i*0.08,0.2+i*0.08)))
    return f.out()
def counter(f,value,label,p,prefix=''):
    n=int(value*ease(seg(p,0.05,0.4)));s=prefix+f'{n:,}'
    f.text((640,330),s,fb90,GOLD);f.text((640,440),label,f34,PAR,a=ease(seg(p,0.0,0.15)))
def s_B139(p,t,du): f=Fr();counter(f,650000,'JEWISH INHABITANTS',p,'ABOUT ');return f.out()
def s_B141(p,t,du): f=Fr();counter(f,700000,'PALESTINIAN ARABS',p,'ROUGHLY ');f.text((640,520),'Nakba',fi36,PAR,a=ease(seg(p,0.5,0.7)));return f.out()
def s_B145(p,t,du):
    f=Fr();f.text((640,330),'HUNDREDS OF THOUSANDS',fb54,GOLD,a=ease(seg(p,0,0.3)));return f.out()
def s_B140(p,t,du):
    f=Fr();f.d.polygon(COAST,fill=(40,38,32))
    a=[(300,300),(420,250),(520,260),(610,330),(580,420),(450,420),(400,330)];b=[(580,420),(640,430),(620,560),(540,640),(430,640),(340,520),(450,420)]
    f.d.polygon(a,fill=SH_A);f.d.polygon(b,fill=SH_B)
    arm=[(300,300),(420,250),(530,262),(625,335),(600,430),(650,445),(630,575),(545,650),(425,650),(330,520),(300,300)]
    f.line(partial(arm,ease(seg(p,0.1,0.65))),GOLD,2)
    k=ease(seg(p,0.65,0.95));ex=[(610,330),(650,360),(660,430),(600,430)];f.d.polygon(ex,fill=mix((90,90,90),GOLD,0.5*k)) if k>0 else None
    f.text((1180,60),'1949',fi36,PAR,'rm',a=ease(seg(p,0.05,0.2)));return f.out()
def s_B147(p,t,du):
    lit=[]
    for i in range(10):
        a=ease(seg(p,i*0.06,i*0.06+0.1))*(1-ease(seg(p,0.5+i*0.04,0.58+i*0.04)));lit.append(a)
    f=Fr();ledger(f,lit,road=ease(seg(p,0.85,1)));return f.out()
def s_B152(p,t,du):
    f=Fr();tf=sqz(0.62);R=[tf(q) for q in ROAD];f.line(R,GOLD,5);im=f.out()
    return Image.blend(im,Image.new('RGB',(W,H),OBS),ease(seg(p,0.66,1)))
SC={k[2:]:v for k,v in globals().items() if k.startswith('s_B')}
def render(bid,dur,out):
    fps=25;n=int(round(dur*fps));fn=SC[bid]
    pr=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(fps),'-i','-','-an',
        '-vf','noise=alls=6:allf=t,vignette=PI/5','-c:v','libx264','-preset','veryfast','-crf','26','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
    for i in range(n):
        p=i/max(n-1,1);pr.stdin.write(fn(p,i/fps,dur).tobytes())
    pr.stdin.close();pr.wait();return bid
if __name__=='__main__':
    jobs=json.loads(sys.argv[1])
    from multiprocessing import Pool
    with Pool(4) as pool: print(pool.starmap(render,jobs))
