import sys,json; sys.path.insert(0,'.')
from style import *
from matplotlib.patches import Polygon, Patch
import numpy as np
P=json.load(open('panel.json')); years=P['years']; states=P['states']
G=json.load(open(sys.argv[1]))  # US state boundaries GeoJSON (see README)
fig=plt.figure(figsize=(180/25.4,158/25.4))
ax=fig.add_axes([0.07,0.735,0.74,0.235])
rec=[sum(P['res']['recess'][s][i]>=2 for s in states) for i in range(len(years))]
pa=[sum(P['res']['daily_PA_minutes'][s][i]>=2 for s in states) for i in range(len(years))]
of=[sum(max(P['res']['recess'][s][i],P['res']['daily_PA_minutes'][s][i])==3 for s in states) for i in range(len(years))]
x=np.arange(len(years))
for ys,c,m,l in ((pa,GREY[2],'s','PE or activity\nmandate'),(rec,BLUE[4],'o','Recess\nmandate'),(of,GREEN[3],'^','Outdoors-if-feasible\nmandate')):
    ax.plot(x,ys,color=c,lw=1.3,zorder=3,clip_on=False)
    ax.annotate('',xy=(x[-1]+0.6,ys[-1]),xytext=(x[-1],ys[-1]),arrowprops=dict(arrowstyle='-|>',color=c,lw=1.3,mutation_scale=7),annotation_clip=False)
    ax.text(x[-1]+1.3,ys[-1]+(1.2 if c==BLUE[4] else 0),l,color=INK,fontsize=7,va='center',linespacing=1.15)
ax.set_xlim(-0.5,len(years)-0.5); ax.set_ylim(0,35); ax.set_yticks(range(0,36,5))
xt=[i for i,y in enumerate(years) if y%5==0]
ax.set_xticks(xt); ax.set_xticklabels([f'{years[i]}-{str(years[i]+1)[2:]}' for i in xt])
ax.set_ylabel('Jurisdictions (n)'); ax.set_xlabel('School year'); clean(ax)
ax.text(-0.08,1.02,'a',transform=ax.transAxes,fontsize=7,fontweight='bold',va='bottom')
pick=[2000,2008,2016,2025]
def draw(axm,t,yr):
    i=years.index(yr)
    for f in G['features']:
        c=STATUS[P['res'][t][f['properties']['name']][i]]
        geo=f['geometry']; polys=geo['coordinates'] if geo['type']=='MultiPolygon' else [geo['coordinates']]
        for poly in polys: axm.add_patch(Polygon(np.array(poly[0]),closed=True,fc=c,ec='white',lw=0.35))
    node(axm,915,425,40,40,STATUS[P['res'][t]['District of Columbia'][i]],'white',r=6,lw=0.35)
    axm.text(935,473,'DC',fontsize=7,ha='center',va='top')
    axm.set_xlim(0,975); axm.set_ylim(615,-5); axm.set_aspect('equal'); axm.axis('off')
wm=0.235
for t,lab,title,y0 in (('recess','b','Recess',0.385),('daily_PA_minutes','c','PE and daily physical activity time',0.10)):
    for j,yr in enumerate(pick):
        axm=fig.add_axes([0.015+j*(wm+0.01),y0,wm,0.195]); draw(axm,t,yr); axm.set_title(f'{yr}-{str(yr+1)[2:]}',pad=2)
    fig.text(0.015,y0+0.225,lab,fontsize=7,fontweight='bold',va='bottom'); fig.text(0.5,y0+0.225,title,fontsize=7,va='bottom',ha='center')
legend_box([Patch(fc=c,ec='none',label=l) for c,l in zip(STATUS,['No state instrument','Recommendation only','Mandate','Mandate, outdoors if feasible'])],fig,loc='lower center',ncol=4,bbox_to_anchor=(0.5,0.0),handlelength=1.2,columnspacing=1.6)
save(fig,'QAP_Fig3_rollout')
