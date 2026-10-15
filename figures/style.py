import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# Nature house palette, sampled from the Nature artwork guide swatches
TONE  = ['#F7F5EE','#E4DFCD','#C6C2A6','#A7A386','#888365','#605D48']
GREY  = ['#E6E6ED','#C8CDDA','#98A3B4','#6E7A90','#47556C','#212F45']
RED   = ['#FACFCD','#EDA4A7','#DE6765','#C93C3D','#9B2422','#73130E']
BLUE  = ['#C8E7FB','#9CCBEC','#5699D1','#0071B2','#004D90','#00285B']
GREEN = ['#D9E7C6','#A0CA78','#60B345','#449332','#1D702C','#113A18']
YEL   = ['#FFF1C2','#F6DC89','#EBC74F','#CC9F28','#9C7710','#6A540B']

INK='#000000'; LINE=GREY[4]; GRID='#E3E3E3'
# status encoding used in every data figure
S_NONE, S_REC, S_MAN, S_OUT = TONE[1], BLUE[1], BLUE[4], GREEN[3]
STATUS=[S_NONE,S_REC,S_MAN,S_OUT]
STATUS_LAB=['No state instrument','Recommendation only','Mandate','Mandate, outdoors if feasible']

plt.rcParams.update({'font.family':'Liberation Sans','font.size':7,'axes.titlesize':7,'axes.labelsize':7,
 'xtick.labelsize':7,'ytick.labelsize':7,'legend.fontsize':7,'axes.linewidth':0.6,
 'xtick.major.width':0.6,'ytick.major.width':0.6,'xtick.major.size':2.5,'ytick.major.size':2.5,
 'axes.edgecolor':INK,'text.color':INK,'axes.labelcolor':INK,'xtick.color':INK,'ytick.color':INK,
 'pdf.fonttype':42,'ps.fonttype':42,'savefig.facecolor':'white','lines.solid_capstyle':'round'})

def clean(ax,grid='y'):
    for s in ('top','right'): ax.spines[s].set_visible(False)
    if grid: getattr(ax,grid+'axis').grid(True,color=GRID,lw=0.5); ax.set_axisbelow(True)
def legend_box(handles,fig,**kw):
    lg=fig.legend(handles=handles,frameon=True,fancybox=False,edgecolor=INK,**kw); lg.get_frame().set_linewidth(0.5); return lg
def node(ax,x,y,w,h,fill,edge,r=1.6,lw=0.8,z=2):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle=f'round,pad=0,rounding_size={r}',fc=fill,ec=edge,lw=lw,zorder=z))
def arrow(ax,p1,p2,c=LINE,lw=0.9,head=True,ls='-',rad=0,z=1):
    ax.add_patch(FancyArrowPatch(p1,p2,arrowstyle='-|>' if head else '-',mutation_scale=7,lw=lw,color=c,ls=ls,
                 connectionstyle=f'arc3,rad={rad}',shrinkA=0,shrinkB=0,zorder=z))
def save(fig,name):
    # Vector PDF for submission; 600 dpi lossless rasters for anything that needs pixels
    fig.savefig(name+'.pdf')
    fig.savefig(name+'.png',dpi=600)
    fig.savefig(name+'.tiff',dpi=600,pil_kwargs={'compression':'tiff_lzw'})
AB={'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA','Colorado':'CO','Connecticut':'CT','Delaware':'DE','District of Columbia':'DC','Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS','Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV','New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM','New York':'NY','North Carolina':'NC','North Dakota':'ND','Ohio':'OH','Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA','Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY'}
