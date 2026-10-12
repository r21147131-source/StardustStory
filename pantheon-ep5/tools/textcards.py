import sys,json
sys.path.insert(0,'.')
import mg
from mg import *
exec(open('labels.py').read())
beats=json.load(open('beats.json')); st=json.load(open('align1.json'))['starts']; T=978.94
IDS=['B071','B108','B109','B110','B111','B132','B133','B144']
LABEL={'B071':"Herod's Temple, scale model",'B108':'Pogroms in the Russian Empire','B109':'The degradation of Dreyfus, 1895','B110':'Theodor Herzl','B111':'The First Zionist Congress, Basel','B132':'Jerusalem after the vote','B133':'Arab leaders reject the plan','B144':'Jewish community of the Arab world'}
DATE={'B071':'','B108':'1880s','B109':'','B110':'','B111':'1897','B132':'30 November 1947','B133':'1947','B144':''}
def card(bid):
    def f_(p,t,du):
        f=Fr();k=ease(seg(p,0,0.2))*(1-ease(seg(p,0.85,1)))
        f.d.line([(440,400),(840,400)],fill=mix(OBS,GOLD,k*0.7),width=1)
        f.text((640,350),LABEL[bid],f34,GOLD,a=k)
        if DATE[bid]: f.text((640,445),DATE[bid],fi36,PAR,a=k)
        return f.out()
    return f_
LET=["His Majesty's Government view with favour the","establishment in Palestine of a national home for the","Jewish people, and will use their best endeavours to","facilitate the achievement of this object, it being","clearly understood that nothing shall be done which","may prejudice the civil and religious rights of","existing non-Jewish communities in Palestine, or the","rights and political status enjoyed by Jews in any","other country"]
FT=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',28)
def letter(p,t,du):
    f=Fr();f.d.rectangle([260,40,1020,690],fill=(30,28,22),outline=(70,64,52))
    f.d.text((640,90),'Foreign Office, November 2nd, 1917.',font=FT,fill=mix(OBS,PAR,0.8),anchor='mm')
    f.d.text((640,150),'Dear Lord Rothschild,',font=FT,fill=mix(OBS,PAR,0.8),anchor='mm')
    for i,l in enumerate(LET): f.d.text((300,230+i*44),l,font=FT,fill=mix(OBS,PAR,0.85),anchor='lm')
    k=ease(seg(p,0.45,0.8));y=230+4*44+20;x2=lerp(300,300+len(LET[4])*17,k)
    f.line([(300,y+6),(x2,y+6)],LG,3);f.line([(300,y+50),(300+ease(seg(p,0.5,0.9))*len(LET[6])*17,y+50)],LG,3)
    f.text((640,655),'Balfour Declaration, 2 November 1917',fi30,PAR,a=ease(seg(p,0.1,0.3)));return f.out()
mg.SC['B121']=letter
for b in IDS: mg.SC[b]=card(b)
jobs=[]
idx={x['id']:i for i,x in enumerate(beats)}
for b in IDS+['B121']:
    i=idx[b];d=(st[i+1] if i+1<len(st) else T)-st[i];jobs.append((b,round(d,3),f'txtseg/{b}.mp4'))
from multiprocessing import Pool
with Pool(4) as pl: print(pl.starmap(mg.render,jobs))
