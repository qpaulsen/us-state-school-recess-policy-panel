import json,collections,re
d=json.load(open('rows.json'));H=d['H'];ix={h:i for i,h in enumerate(H)};R=d['data']
g=lambda r,f:r[ix[f]]
YEARS=list(range(2000,2026))  # school year start: 2000-01 .. 2025-26
ABBR={}
import csv
def sy_of_date(s):
    m=re.match(r'(\d{4})(?:-(\d{2}))?',s); y=int(m.group(1)); mo=int(m.group(2) or 1)
    return y if mo>=8 else y-1
skipped=[]
def intervals(topic):
    out=collections.defaultdict(list)
    for r in R:
        if g(r,'topic')!=topic: continue
        if g(r,'instrument_class') not in ('time_dose','structural_recess'): continue
        gb=(g(r,'grade_bands') or '')
        if gb.strip() in ('Pre-K','PK'): continue
        db=g(r,'date_basis') or ''; tsy=g(r,'treatment_school_year')
        if tsy: start=int(tsy[:4])
        elif 'left_censored' in db: start=1900
        else: skipped.append((topic,g(r,'row_id'),db)); continue
        rd=g(r,'repeal_date')
        if rd and 'must not be read as treatment ending' in (g(r,'notes_ambiguities') or ''): rd=None
        ends=[sy_of_date(x) for x in (g(r,'amended_date'),rd) if x]
        end=min(ends) if ends else 9999
        ps=g(r,'policy_status'); os_=g(r,'outdoor_specificity')
        cat=1 if ps=='recommendation' else (3 if os_ in('outdoor_if_feasible','explicit_outdoor') else 2)
        out[g(r,'state')].append((start,end,cat,g(r,'row_id')))
    return out
states=sorted(set(g(r,'state') for r in R))
res={}
for t in ('recess','daily_PA_minutes'):
    iv=intervals(t); M={}
    for s in states:
        M[s]=[max([c for a,b,c,_ in iv[s] if a<=y<=b] or [0]) for y in YEARS]
    res[t]=M
json.dump({'states':states,'years':YEARS,'res':res},open('panel.json','w'))
print('skipped',len(skipped)); [print(x) for x in skipped]
for t in res:
    print(t)
    for y_i,y in enumerate(YEARS):
        c=collections.Counter(res[t][s][y_i] for s in states)
        print(y,dict(sorted(c.items())))
