import sys,json; sys.path.insert(0,'.')
from style import *
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
import numpy as np
P=json.load(open('panel.json')); states=sorted(P['states'],key=lambda s:AB[s]); years=P['years']
cols=STATUS; cmap=ListedColormap(cols)
fig,axes=plt.subplots(1,2,figsize=(180/25.4,195/25.4))
fig.subplots_adjust(left=0.05,right=0.975,top=0.955,bottom=0.1,wspace=0.22)
def first_mandate(t,s):
    v=P['res'][t][s]
    return next((years[i] for i,x in enumerate(v) if x>=2), 9999)
def first_rec(t,s):
    v=P['res'][t][s]
    return next((years[i] for i,x in enumerate(v) if x>=1), 9999)
for ax,(t,lab,ttl) in zip(axes,[('recess','a','Recess'),('daily_PA_minutes','b','PE and daily physical activity time')]):
    order=sorted(states,key=lambda s:(first_mandate(t,s),first_rec(t,s),AB[s]))
    M=np.array([P['res'][t][s] for s in order])
    ax.set_yticks(range(len(order))); ax.set_yticklabels([AB[s] for s in order],fontsize=7)
    # vector cells (pcolormesh) instead of an embedded bitmap, so the grid stays sharp at any zoom
    ax.pcolormesh(np.arange(-0.5,len(years)),np.arange(-0.5,len(order)),M,cmap=cmap,vmin=-0.5,vmax=3.5,shading='flat',edgecolors='none',antialiased=False)
    ax.set_xlim(-0.5,len(years)-0.5); ax.set_ylim(len(order)-0.5,-0.5)
    ax.set_xticks(np.arange(-0.5,len(years),1),minor=True); ax.set_yticks(np.arange(-0.5,len(states),1),minor=True)
    ax.grid(which='minor',color='white',linewidth=0.6); ax.tick_params(which='minor',length=0); ax.tick_params(axis='y',length=0)
    xt=[i for i,y in enumerate(years) if y%5==0]
    ax.set_xticks(xt); ax.set_xticklabels([f'{years[i]}-{str(years[i]+1)[2:]}' for i in xt])
    ax.set_xlabel('School year')
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_title(ttl,loc='center',pad=4)
    ax.text(-0.09,1.012,lab,transform=ax.transAxes,fontsize=7,fontweight='bold',va='bottom',ha='left')
labels=['No state instrument','Recommendation only','Mandate','Mandate, outdoors if feasible']
legend_box([Patch(fc=c,ec='none',lw=0.4,label=l) for c,l in zip(cols,labels)],fig,loc='lower center',ncol=4,bbox_to_anchor=(0.52,0.0),handlelength=1.2,columnspacing=1.6)
save(fig,'QAP_SuppFig1_state_year_grid')
