import math,json,random,sys
from shapely.geometry import shape,Polygon,box,MultiPolygon,Point
from shapely.ops import unary_union
import mg
from mg import *
GEO=json.load(open('geo/ne_10m_admin_0_countries.geojson'))
C={}
for ft in GEO['features']:
    n=ft['properties'].get('NAME') or ft['properties'].get('ADMIN')
    C[n]=shape(ft['geometry'])
def rings(g):
    gs=[g] if g.geom_type=='Polygon' else list(g.geoms)
    return [list(p.exterior.coords) for p in gs]
def merc(lat):
    lat=max(-80.0,min(84.0,lat)); return math.log(math.tan(math.pi/4+math.radians(lat)/2))
def proj(clon,clat,span):
    k=W/span;cy=merc(clat)
    return lambda ll:((ll[0]-clon)*k+W/2,H/2-(math.degrees(merc(ll[1])-cy))*k)
PW=proj(37,31.2,30);PZ=proj(36,32.3,9);PH=proj(35.15,32.4,1.8);PM=proj(35.0,31.4,3.6);PX=proj(25,38,90);PE=proj(22,49,80);PA=proj(36,31.5,16)
SQ=0.62
def sq(pf,s=SQ): return lambda ll:(lambda q:(640+(q[0]-640)*s,q[1]))(pf(ll))
EAREA=[(34.5,29.5),(36.0,31.3),(39,33),(42.5,32.8),(45,29.5),(41,26)]
SINAI=[(32.5,29.2),(34.6,30.4),(34.9,29.4),(33.5,28.0)]
def draw_land(f,pf,names=None,fill=LAND,outline=(60,52,36),w=1):
    f.d.rectangle([0,0,W,H],fill=SEA)
    for n,g in C.items():
        if names and n not in names: continue
        for r in rings(g):
            pts=[pf(c) for c in r]
            if max(p[0] for p in pts)<-50 or min(p[0] for p in pts)>W+50 or max(p[1] for p in pts)<-50 or min(p[1] for p in pts)>H+50: continue
            if len(pts)>2: f.d.polygon(pts,fill=fill,outline=outline)
def wide_base(f,pf,desert=0.0,labels=True):
    draw_land(f,pf)
    if desert>0:
        for poly in(EAREA,SINAI): f.d.polygon([pf(q) for q in poly],fill=mix(LAND,(7,6,5),desert))
    if labels:
        f.text(pf((29.5,26.2)),'EGYPT',f20,DIM);f.text(pf((44.3,33.9)),'MESOPOTAMIA',f20,DIM)
ROADLL=[(31.25,30.05),(32.3,31.1),(34.45,31.5),(34.85,32.1),(35.18,32.58),(35.6,33.4),(36.3,34.3),(37.15,36.2),(40.0,36.4),(43.1,36.35),(44.4,33.2)]
def rd(pf): return [pf(q) for q in ROADLL]
HILLS=[(35.0,31.7)]
random.seed(7);VILL=[(random.gauss(35.22,0.14),random.gauss(32.05,0.38)) for _ in range(50)]
def s_B001(p,t,du):
    f=Fr();s=lerp(1,SQ,ease(p));pf=sq(PW,s);wide_base(f,pf);f.line(rd(pf),(120,100,60),2,False)
    f.d.line([(640,60),(640,680)],fill=mix(OBS,GOLD,ease(seg(p,0.2,0.8))),width=2);return f.out()
def s_B004(p,t,du):
    f=Fr();pf=sq(PW);wide_base(f,pf,desert=ease(seg(p,0,0.4)));R=rd(pf)
    for side in(0,1):
        pts=R[:6] if side==0 else R[::-1][:6]
        for k in range(5):
            q=(p*1.3+k*0.2)%1.0;f.dot(at(pts,q),5,EMB if side else GOLD)
        f.line(partial(pts,ease(seg(p,0.1,1))),mix(OBS,EMB if side else GOLD,0.6),2,False)
    return f.out()
def s_B005(p,t,du):
    f=Fr();pf=sq(PW);wide_base(f,pf,desert=1.0);R=rd(pf);f.line(partial(R,ease(seg(p,0,0.6))),GOLD,5);return f.out()
def s_B006(p,t,du):
    f=Fr();draw_land(f,PM:=proj(35.0,32.1,2.4));a=PM((34.84,32.33));b=PM((35.04,32.33))
    f.line([PM(q) for q in[(34.6,31.3),(34.78,32.0),(34.84,32.33),(34.95,32.9),(35.1,33.3)]],GOLD,3)
    k=ease(seg(p,0.1,0.5));x2=lerp(a[0],b[0],k)
    f.d.line([a,(x2,a[1])],fill=LG,width=4);f.gd.line([a,(x2,a[1])],fill=GOLD,width=9)
    for x in(a[0],x2): f.d.line([(x,a[1]-14),(x,a[1]+14)],fill=LG,width=3)
    f.text((a[0]-18,a[1]),'sea',fi30,DIM,'rm',a=k);f.text((b[0]+18,a[1]),'hills',fi30,DIM,'lm',a=k)
    f.text((640,650),'Narrowest point, before 1967: about 9 miles.',fi36,PAR,a=seg(p,0.35,0.55)*(1-seg(p,0.88,1)));return f.out()
def s_B021(p,t,du):
    f=Fr();draw_land(f,PZ);R=rd(PZ);f.line(partial(R,ease(seg(p,0,0.7))),GOLD,4)
    f.text(PZ((35.1,32.9)),'CANAAN',f34,GOLD,a=ease(seg(p,0.5,0.9)));return f.out()
def s_B025(p,t,du):
    f=Fr();draw_land(f,PH);car=[(34.88,32.78),(35.06,32.64),(35.13,32.57),(35.1,32.5),(34.95,32.58)];sam=[(35.22,32.5),(35.3,32.62),(35.7,32.5),(35.7,32.1),(35.3,32.2)]
    f.d.polygon([PH(q) for q in car],fill=(44,40,30));f.d.polygon([PH(q) for q in sam],fill=(44,40,30))
    m=PH((35.18,32.58));pulse=0.5+0.5*math.sin(t*6);f.dot(m,9+5*pulse,GOLD)
    for k in range(8):
        q=(p*1.1+k/8.0)%1.0
        f.dot(at([PH((34.75,31.95)),PH((34.95,32.35)),m],q),4,EMB);f.dot(at([PH((35.6,33.15)),PH((35.4,32.8)),m],q),4,EMB)
    f.text((m[0],m[1]+44),'MEGIDDO',f26,GOLD,a=ease(seg(p,0.2,0.5)));return f.out()
PHL=proj(35.2,32.0,3.2)
def s_B034(p,t,du):
    f=Fr();draw_land(f,PHL)
    for i,v in enumerate(VILL):
        a=ease(seg(p,i/60.0,i/60.0+0.25));f.dot(PHL(v),4,mix(OBS,GOLD,a),glow=a>0.5)
    f.text(PHL((35.2,32.65)),'ISRAEL',f44,GOLD,a=ease(seg(p,0.55,0.95)));return f.out()
def s_B040(p,t,du):
    f=Fr();draw_land(f,PHL)
    for i,v in enumerate(VILL):
        a=ease(seg(p,i/90.0,i/90.0+0.2));f.dot(PHL(v),4,mix(OBS,GOLD if v[1]>31.95 else LG,a),glow=a>0.5)
    y=PHL((35.0,31.95))[1];f.d.line([(300,y),(980,y)],fill=mix(OBS,DIM,ease(seg(p,0.25,0.4))),width=1)
    f.text(PHL((35.2,32.7)),'ISRAEL',f34,GOLD,a=ease(seg(p,0.3,0.45)));f.text(PHL((35.2,32.28)),'SAMARIA',f20,LG,a=ease(seg(p,0.45,0.55)))
    f.text(PHL((35.0,31.35)),'JUDAH',f34,GOLD,a=ease(seg(p,0.5,0.65)));j=PHL((35.22,31.78))
    f.text((j[0]+70,j[1]),'JERUSALEM',f20,LG,'lm',a=ease(seg(p,0.65,0.8)));f.d.ellipse([j[0]-10,j[1]-10,j[0]+10,j[1]+10],outline=mix(OBS,LG,ease(seg(p,0.65,0.8))),width=2);return f.out()
def s_B050(p,t,du):
    f=Fr();draw_land(f,PHL)
    for v in VILL:
        if v[1]>31.95:
            k=ease(seg(p,0.15,0.9));c=mix(GOLD,(90,90,90),ease(seg(p,0,0.4)));c=mix(c,OBS,seg(p,0.6,1));f.dot(PHL((v[0]+k*0.9,v[1])),4,c,glow=False)
        else: f.dot(PHL(v),4,LG)
    f.text(PHL((35.2,32.7)),'ISRAEL',f34,GOLD,a=1-ease(seg(p,0.1,0.5)));f.text(PHL((35.0,31.35)),'JUDAH',f34,GOLD);f.text((PHL((35.22,31.78))[0]+70,PHL((35.22,31.78))[1]),'JERUSALEM',f20,LG,'lm');return f.out()
def s_B082(p,t,du):
    f=Fr();draw_land(f,PA);c=PA((35.0,31.2))
    f.text(c,'JUDEA',f64,GOLD,a=1-ease(seg(p,0.05,0.35)))
    s='SYRIA PALAESTINA';n=int(len(s)*ease(seg(p,0.35,0.9)))
    if n: f.text((640,c[1]-90),s[:n],f44,GOLD)
    return f.out()
def s_B085(p,t,du):
    f=Fr();draw_land(f,PX);o=PX((35.2,32.0));f.dot(o,7,GOLD)
    T=[('BABYLON',(44.4,32.5)),('NORTH AFRICA',(10.2,34.0)),('SPAIN',(-3.7,40.4)),('EUROPE',(14.0,48.0))]
    for i,(n,ll) in enumerate(T):
        xy=PX(ll);k=ease(seg(p,0.05+i*0.12,0.5+i*0.12));f.line(partial([o,xy],k),GOLD,2);a=ease(seg(p,0.5+i*0.1,0.8+i*0.1))
        if k>0.99: f.dot(xy,6,mix(OBS,GOLD,a))
        f.text((xy[0],xy[1]+26),n,f20,GOLD,a=a)
    return f.out()
EUR_N=['Portugal','Spain','France','United Kingdom','Ireland','Germany','Italy','Poland','Sweden','Norway','Finland','Denmark','Netherlands','Belgium','Switzerland','Austria','Czechia','Hungary','Romania','Bulgaria','Greece','Serbia','Ukraine','Belarus','Lithuania','Latvia','Estonia','Slovakia','Slovenia','Croatia','Bosnia and Herz.','Albania','Russia','Turkey']
random.seed(11);PAL=[(120,70,60),(70,90,130),(90,120,90),(130,110,60),(100,70,120),(60,110,120),(130,80,90),(80,80,110),(110,100,60),(120,90,60)]
EORD=EUR_N[:];random.shuffle(EORD)
def s_B107(p,t,du):
    f=Fr();draw_land(f,PE,names=set(EUR_N)|{'Morocco','Algeria','Tunisia','Libya','Egypt','Syria','Israel','Palestine','Lebanon','Jordan','Iraq','Iran','Georgia','Armenia','Azerbaijan','Moldova','North Macedonia','Montenegro','Kosovo','Luxembourg','Cyprus','Saudi Arabia','Kazakhstan'},fill=(22,20,15))
    for i,n in enumerate(EORD):
        k=ease(seg(p,i*0.022,i*0.022+0.12))
        for r in rings(C[n]):
            pts=[PE(c) for c in r]
            if k>0 and len(pts)>2: f.d.polygon(pts,fill=mix((22,20,15),PAL[i%10],k),outline=(30,28,22))
    k=ease(seg(p,0.78,0.95))
    if k>0: f.dot(PE((35.2,31.8)),6+6*(0.5+0.5*math.sin(t*5)),GOLD)
    return f.out()
PXX=proj(28,38,70)
def s_B118(p,t,du):
    f=Fr();draw_land(f,PXX);dst=PXX((34.75,32.05));k=ease(seg(p,0.05,0.85))
    for s0 in((30.5,50.0),(40.5,22.0)): f.line(partial([PXX(s0),dst],k),GOLD,3)
    f.dot(dst,6+(5*ease(seg(p,0.85,1))),LG);return f.out()
MAND=unary_union([C['Israel'],C['Palestine']])
def patch(f,cx,cy,sc,col,w=2,fill=None):
    pf=lambda ll:(cx+(ll[0]-35.0)*sc,cy-(ll[1]-31.4)*sc*1.18)
    for r in rings(MAND): f.d.polygon([pf(c) for c in r],outline=col,fill=fill)
def s_B120(p,t,du):
    f=Fr();labels=['LETTERS TO ARAB LEADERS','DIVIDED BY A SECRET LINE','A NATIONAL HOME FOR THE JEWISH PEOPLE'];cols=[(70,66,52),(84,62,42),(58,72,62)]
    for i in range(3):
        k=ease(seg(p,i*0.22,i*0.22+0.3));x=lerp(1500 if i%2 else -300,500+i*140,k);y0=110+i*30
        f.d.rectangle([x-230,y0,x+230,y0+380],outline=mix(OBS,GOLD,0.7*k),width=2,fill=mix(OBS,cols[i],0.55*k))
        patch(f,x,y0+190,150,mix(OBS,LG,k))
        if i==1: f.d.line([(x-120,y0+330),(x+120,y0+60)],fill=mix(OBS,EMB,k),width=3)
        f.text((640,590+i*34),labels[i],f20,GOLD,a=seg(p,0.25+i*0.2,0.45+i*0.2))
    f.text((640,60),'MEANING DISPUTED',f34,EMB,a=ease(seg(p,0.5,0.7)));return f.out()
def mand_map(f,pf,fillc=(54,52,46)):
    draw_land(f,pf,fill=(24,22,17))
    for r in rings(MAND): f.d.polygon([pf(c) for c in r],fill=fillc,outline=(80,74,60))
PMP=proj(35.0,31.6,4.2)
def s_B129(p,t,du):
    f=Fr();mand_map(f,PMP);line=[PMP(q) for q in[(34.9,33.0),(35.35,32.2),(35.1,31.7),(35.25,31.0),(34.9,30.0)]]
    k=ease(seg(p,0.05,0.5));f.line(partial(line,k),GOLD,10)
    if p>0.55:
        c=ease(seg(p,0.55,1));random.seed(3)
        for j in range(16):
            a=at(line,j/16.0);ln=[a];x,y=a
            for _ in range(4): x+=random.uniform(-18,18);y+=random.uniform(6,20);ln.append((x,y))
            f.d.line(partial(ln,c),fill=OBS,width=2)
    f.text((1180,60),'29 November 1947',fi36,PAR,'rm',a=ease(seg(p,0.1,0.3)));return f.out()
WG=Polygon([(35.0,33.1),(35.55,33.05),(35.5,32.75),(35.1,32.7),(34.95,32.9)])
ARAB=unary_union([C['Palestine'],WG.intersection(C['Israel'])]).buffer(0)
JEW=MAND.difference(ARAB).buffer(0)
def shade(f,pf,geo,col):
    for r in rings(geo) if geo.geom_type in('Polygon','MultiPolygon') else []: f.d.polygon([pf(c) for c in r],fill=col)
def s_B130(p,t,du):
    f=Fr();draw_land(f,PMP,fill=(24,22,17));k=ease(seg(p,0.05,0.4));shade(f,PMP,JEW,mix((24,22,17),SH_A,k));shade(f,PMP,ARAB,mix((24,22,17),SH_B,k))
    j=PMP((35.22,31.78))
    for dx in range(-26,27,8): f.d.line([(j[0]+dx-18,j[1]+22),(j[0]+dx+18,j[1]-22)],fill=mix(OBS,PAR,0.8*k),width=1)
    f.d.ellipse([j[0]-26,j[1]-26,j[0]+26,j[1]+26],outline=mix(OBS,PAR,0.8*k),width=2)
    f.text((1020,300),'A JEWISH STATE',f26,SH_A,a=ease(seg(p,0.4,0.6)));f.text((1020,360),'AN ARAB STATE',f26,SH_B,a=ease(seg(p,0.55,0.75)))
    f.text((1020,430),'JERUSALEM UNDER',f20,PAR,a=ease(seg(p,0.7,0.9)));f.text((1020,458),'INTERNATIONAL RULE',f20,PAR,a=ease(seg(p,0.7,0.9)));return f.out()
PCT=proj(38.0,31.2,14)
def s_B138(p,t,du):
    f=Fr();draw_land(f,PCT);tgt=PCT((34.75,32.0))
    for r in rings(MAND): f.d.polygon([PCT(c) for c in r],fill=(60,56,46))
    S=[('EGYPT',(31.0,29.5)),('TRANSJORDAN',(36.5,30.7)),('SYRIA',(38.0,34.5)),('IRAQ',(43.0,33.0)),('LEBANON',(35.9,34.0))]
    for i,(n,ll) in enumerate(S):
        xy=PCT(ll);k=ease(seg(p,0.1+i*0.08,0.85));pt=at([xy,tgt],k*0.9);f.line([xy,pt],(150,140,120),2,False);f.dot(pt,5,(190,180,150),False)
        f.text((xy[0],xy[1]-24),n,f20,PAR,a=ease(seg(p,i*0.08,0.2+i*0.08)))
    return f.out()
def s_B140(p,t,du):
    f=Fr();draw_land(f,PMP,fill=(24,22,17));shade(f,PMP,JEW,SH_A);shade(f,PMP,ARAB,SH_B)
    k=ease(seg(p,0.65,0.95));ex=JEW.symmetric_difference(C['Israel']).intersection(C['Israel'])
    if k>0: shade(f,PMP,C['Israel'].difference(JEW),mix((90,90,90),GOLD,0.55*k))
    for r in rings(C['Israel']): f.line(partial([PMP(c) for c in r],ease(seg(p,0.1,0.65))),GOLD,2,False)
    f.text((1180,60),'1949',fi36,PAR,'rm',a=ease(seg(p,0.05,0.2)));return f.out()
def s_B152(p,t,du):
    f=Fr();pf=sq(PW);f.line(rd(pf),GOLD,5);im=f.out();return Image.blend(im,Image.new('RGB',(W,H),OBS),ease(seg(p,0.66,1)))
for k,v in list(globals().items()):
    if k.startswith('s_B'): mg.SC[k[2:]]=v
if __name__=='__main__':
    jobs=json.loads(sys.argv[1])
    from multiprocessing import Pool
    with Pool(4) as pool: print(pool.starmap(mg.render,jobs))
