import sys; sys.path.insert(0,'.')
from style import *
from matplotlib.patches import Patch, FancyBboxPatch
from matplotlib.lines import Line2D
import datetime as dt
def yf(s):
    p=[int(x) for x in s.split('-')]; d=dt.date(p[0],p[1] if len(p)>1 else 1,p[2] if len(p)>2 else 1)
    return d.year+(d.timetuple().tm_yday-1)/365.25
END=2026.0
fig=plt.figure(figsize=(180/25.4,116/25.4))
# ---- a: MS timeline
rows=[('MS_PA_1998_K_40DAILY','1998 rule, 40 min daily',None,'1998-02','2012-08-19',None,'u'),
      ('MS_PA_2012_K_30DAILY','2012 rule, 30 min daily','2012-08-19',None,'2016-02-20',2012,'u'),
      ('MS_PA_2016_K_30DAILY_OUTDOOR','2016 rule, 30 min daily','2016-02-20',None,'2018-10-21',2016,'o'),
      ('MS_PA_2018_K_30DAILY_OUTDOOR','2018 rule, 30 min daily','2018-10-21',None,None,2019,'o')]
COL={'u':(BLUE[1],BLUE[4]),'o':(GREEN[1],GREEN[3])}
ax=fig.add_axes([0.27,0.63,0.70,0.30]); tx=fig.add_axes([0.0,0.63,0.27,0.30]); tx.axis('off')
n=len(rows)
ax.axvspan(1997.5,2000,color=TONE[0],zorder=0,lw=0); ax.text(1998.75,n-0.3,'Before\npanel',ha='center',va='center',fontsize=7,linespacing=1.2)
for i,(rid,desc,eff,en,amd,tsy,k) in enumerate(rows):
    y=n-1-i; s=yf(eff or en); e=yf(amd) if amd else END
    ax.add_patch(FancyBboxPatch((s,y-0.17),e-s,0.34,boxstyle='round,pad=0,rounding_size=0.17',mutation_aspect=1/6,fc=COL[k][0],ec=COL[k][1],lw=0.8,zorder=2))
    if not amd: ax.annotate('',xy=(END+0.6,y),xytext=(END,y),arrowprops=dict(arrowstyle='-|>',color=COL[k][1],lw=0.9,mutation_scale=7),annotation_clip=False)
    ax.plot(s,y,marker='D' if eff else 'o',ms=4.2,mfc='white',mec=INK,mew=0.7,zorder=4)
    if tsy:
        t=tsy+8/12; ax.plot([s,t],[y+0.3,y+0.3],color=INK,lw=0.6,ls=(0,(2,1.5)),zorder=3)
        ax.plot(t,y+0.3,marker='v',ms=4.5,color=INK,zorder=4); ax.text(t+0.35,y+0.3,f'{tsy}-{str(tsy+1)[2:]}',fontsize=7,va='center')
    tx.text(0.03,y,desc,fontsize=7,fontweight='bold',va='center')
tx.set_xlim(0,1); tx.set_ylim(-0.55,n-0.15); ax.set_ylim(-0.55,n-0.15); ax.set_xlim(1997.5,2027)
ax.set_yticks([]); ax.set_xticks(range(1998,2027,4)); ax.set_xlabel('Year')
for sp in ('top','right','left'): ax.spines[sp].set_visible(False)
ax.xaxis.grid(True,color=GRID,lw=0.5); ax.set_axisbelow(True)
fig.text(0.01,0.975,'a',fontsize=7,fontweight='bold'); fig.text(0.5,0.975,'Instrument versions and treatment timing: Mississippi kindergarten daily activity',fontsize=7,va='center',ha='center')
h=[Patch(fc=TONE[1],ec=TONE[3],label='No instrument'),Patch(fc=BLUE[1],ec=BLUE[4],label='Location unspecified'),Patch(fc=GREEN[1],ec=GREEN[3],label='Outdoors if feasible'),
   Line2D([],[],ls='none',marker='o',mfc='white',mec=INK,ms=4,label='Enactment date'),Line2D([],[],ls='none',marker='D',mfc='white',mec=INK,ms=4,label='Effective date'),
   Line2D([],[],ls='none',marker='v',color=INK,ms=4.5,label='Treatment school year starts')]
legend_box(h,fig,loc='lower center',ncol=6,bbox_to_anchor=(0.5,0.005),handlelength=1.4,columnspacing=1.2)
# ---- b: AR baseline -> mandate -> panel
bx=fig.add_axes([0,0.075,1,0.44]); bx.set_xlim(0,180); bx.set_ylim(0,50); bx.axis('off')
yrs=list(range(2000,2026)); X0,X1=46,150; cw=(X1-X0)/len(yrs)
def xy(y): return X0+(y-2000)*cw
y1,y2,y3=43,26,9
fig.text(0.01,0.53,'b',fontsize=7,fontweight='bold'); fig.text(0.5,0.53,'Silent baseline, supersession and the derived panel: Arkansas recess',fontsize=7,va='center',ha='center')
bx.text(2,y1,'Instrument rows',fontsize=7,fontweight='bold',va='center',linespacing=1.3)
node(bx,xy(2000),y1-3,xy(2019.56)-xy(2000),6,TONE[1],TONE[3],r=1.2)
bx.text(xy(2000)+2,y1,'Silent baseline, recess (2000 onward)',fontsize=7,va='center')
bx.text(xy(2019.56)-2.5,(y1+y2)/2,'Amended date\n2019-07-24',fontsize=7,ha='right',va='center',linespacing=1.3)
node(bx,xy(2019.56),y2-3,xy(2026)-xy(2019.56)+4,6,GREEN[1],GREEN[3],r=1.2)
bx.text(xy(2019.56)+3,y2,'Act 641 of 2019',fontsize=7,va='center')
arrow(bx,(xy(2019.56),y1-3),(xy(2019.56),y2+3.2)); bx.text(xy(2019.56)+2.5,(y1+y2)/2,'Superseded by',fontsize=7,va='center')
bx.plot(xy(2019.56),y2,marker='D',ms=4.2,mfc='white',mec=INK,mew=0.7,zorder=5)
bx.text(2,y3,'Derived panel\n(1 cell per school year)',fontsize=7,fontweight='bold',va='center',linespacing=1.3)
for y in yrs: node(bx,xy(y)+0.2,y3-3,cw-0.4,6,GREEN[1] if y>=2019 else TONE[1],GREEN[3] if y>=2019 else TONE[3],r=0.6,lw=0.6)
for y in (2000,2005,2010,2015,2019,2025): bx.text(xy(y)+cw/2,y3-4.2,f'{y}-{str(y+1)[2:]}',fontsize=7,ha='center',va='top')
bx.plot(xy(2019)+cw/2,y3+4.3,marker='v',ms=4.5,color=INK,zorder=5); bx.text(xy(2019)+cw/2+1.5,y3+4.6,'Treatment school year 2019-20',fontsize=7,va='center')
save(fig,'QAP_Fig2_data_model')
