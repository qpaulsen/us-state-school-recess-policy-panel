import sys,re,collections; sys.path.insert(0,'.')
from style import *
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import numpy as np, openpyxl
# a: agreement by field, from Technical Validation text (calibration: AK, AZ, AR; production: 6 states)
fields=['Topic','Policy status','Required minutes','Frequency','Outdoor specificity','Recess withholding','Grade band','Enforcement']
# kappa from reliability/round1/kappa_report_FINAL_2026-07-23.txt and the Technical Validation text; 'p' = proportion in exact agreement where kappa is undefined
cal ={'Topic':(1.00,'k'),'Policy status':(0.818,'k'),'Required minutes':(1.00,'p'),'Frequency':(1.00,'k'),'Outdoor specificity':(1.00,'k'),'Recess withholding':(1.00,'p'),'Grade band':(0.916,'k'),'Enforcement':(0.30,'k')}
prod={'Topic':(1.00,'k'),'Policy status':(1.00,'k'),'Required minutes':(24/27,'p'),'Outdoor specificity':(0.90,'k'),'Recess withholding':(1.00,'k'),'Enforcement':(0.52,'k')}
fig=plt.figure(figsize=(180/25.4,86/25.4))
a=fig.add_axes([0.17,0.33,0.26,0.57])
y=np.arange(len(fields))
for i,f in enumerate(fields):
    if f in cal and f in prod: a.plot([cal[f][0],prod[f][0]],[i,i],color=GREY[2],lw=1,zorder=1)
    for d,c,off in ((cal,BLUE[1],0),(prod,BLUE[4],0)):
        if f in d:
            v,k=d[f]
            if k=='k': a.plot(v,i,marker='o',ms=5,mfc=c,mec='white',mew=0.6,ls='none',zorder=3)
            else: a.plot(v,i,marker='o',ms=4.4,mfc='white',mec=c,mew=1.2,ls='none',zorder=3)
a.set_yticks(y); a.set_yticklabels([f+'*' if f=='Enforcement' else f for f in fields]); a.invert_yaxis(); a.set_xlim(0.2,1.02); a.set_xticks([0.2,0.4,0.6,0.8,1.0])
a.set_xlabel("Cohen's kappa or exact agreement"); clean(a,grid='x'); a.tick_params(axis='y',length=0); a.spines['left'].set_visible(False)
a.axvline(0.8,color=GREY[4],lw=0.6,ls=(0,(2,1.5)),zorder=0)
fig.text(0.02,0.175,'*Coders differed on when a requirement counts as monitored; the convention was\nfixed by codebook rules 11 and 25 (v1.2) and applied to the full panel.',fontsize=6,va='top',color=GREY[4],linespacing=1.25)
fig.text(0.01,0.95,'a',fontsize=7,fontweight='bold'); fig.text(0.26,0.95,'Inter-coder agreement by field',fontsize=7,va='center',ha='center')
h=[Line2D([],[],ls='none',marker='o',mfc=BLUE[1],mec='white',ms=5,label='Calibration round (3 states)'),Line2D([],[],ls='none',marker='o',mfc=BLUE[4],mec='white',ms=5,label='Production round (6 states)'),
   Line2D([],[],ls='none',marker='o',mfc=GREY[3],mec='white',ms=5,label="Cohen's kappa"),Line2D([],[],ls='none',marker='o',mfc='white',mec=GREY[3],mew=1.2,ms=4.4,label='Exact agreement')]
lg=fig.legend(handles=h,loc='lower left',bbox_to_anchor=(0.02,0.0),ncol=2,frameon=False,handletextpad=0.4,columnspacing=1.2,labelspacing=0.3)
# b: audit candidates by check, stacked by final outcome (AUDIT_CANDIDATES 'outcome' column)
wb=openpyxl.load_workbook(sys.argv[1],read_only=True,data_only=True)
R=list(wb['AUDIT_CANDIDATES'].iter_rows(values_only=True)); H=list(R[0])
iL,iO=H.index('log_id'),H.index('outcome')
D=[r for r in R[1:] if r[0]]
def chk(l):
    cs=set(re.findall(r'-C(\d)\b',str(l))); return int(cs.pop()) if len(cs)==1 else (6 if cs else 5)
LAB={1:'Rules with minutes',2:'Repealed or superseded',3:'State board actions',4:'Outdoor or withholding text',6:'Two or more checks',5:'Later review'}
OUT=[('new_row','New row',BLUE[4]),('existing_revised','Existing row revised',BLUE[2]),('note_added','Note added',BLUE[0]),('closed_no_change','Closed, no change',TONE[1])]
bad=[r[0] for r in D if r[iO] not in {o for o,_,_ in OUT}]
assert not bad, f'missing or invalid outcome: {bad[:5]}'
cnt=collections.Counter((chk(r[iL]),r[iO]) for r in D)
ks=[1,2,3,4,6,5]
b=fig.add_axes([0.70,0.33,0.28,0.47])
left=np.zeros(6)
for o,lab,c in OUT:
    v=np.array([cnt[(k,o)] for k in ks])
    b.barh(range(6),v,left=left,color=c,height=0.62,edgecolor='white',linewidth=0.4)
    for i,(l,x) in enumerate(zip(left,v)):
        if x>=8: b.text(l+x/2,i,str(x),va='center',ha='center',fontsize=6,color='white' if o in('new_row','existing_revised') else INK)
    left+=v
for i,x in enumerate(left): b.text(x+1.5,i,str(int(x)),va='center',fontsize=7)
b.set_yticks(range(6)); b.set_yticklabels([LAB[k] for k in ks]); b.invert_yaxis(); b.set_xlim(0,100); b.set_xticks(range(0,101,25)); b.set_xlabel('Candidates (n)')
clean(b,grid='x'); b.tick_params(axis='y',length=0); b.spines['left'].set_visible(False)
fig.text(0.52,0.95,'b',fontsize=7,fontweight='bold'); fig.text(0.76,0.95,f'Audit candidates by check and outcome (n = {len(D)})',fontsize=7,va='center',ha='center')
fig.legend(handles=[Patch(fc=c,ec='none',label=lab) for _,lab,c in OUT],loc='lower left',bbox_to_anchor=(0.52,0.0),ncol=2,frameon=False,handlelength=1.0,handletextpad=0.4,columnspacing=1.2,labelspacing=0.3)
save(fig,'QAP_Fig4_validation')
