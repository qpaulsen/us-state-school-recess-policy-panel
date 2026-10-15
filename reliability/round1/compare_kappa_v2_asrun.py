
import argparse, math, re, sys
from collections import Counter
from pathlib import Path
import pandas as pd

CAT_FIELDS = ["topic","policy_status","frequency","grade_bands","outdoor_specificity","withholding_recess","enforcement","source_type","confidence"]
NUM_FIELDS = ["minutes_required"]
DATE_FIELDS = ["enactment_date","effective_date","amended_date","repeal_date"]
SCHOOL_YEAR_FIELDS = ["implementation_school_year"]
MISSING_INSTRUMENT = "__missing_instrument__"; BLANK = "__blank__"
PARTIAL_DATE_RE = re.compile(r"^((?:18|19|20|21)\d{2})(?:-(0[1-9]|1[0-2]))?(?:-(0[1-9]|[12]\d|3[01]))?$")
SCHOOL_YEAR_RE = re.compile(r"^((?:18|19|20|21)\d{2})-((?:18|19|20|21)\d{2})$")

def clean_text(v):
    if v is None: return ""
    if isinstance(v,float) and math.isnan(v): return ""
    return str(v).strip()
def normalize_category(v):
    t=clean_text(v); return t.casefold() if t else BLANK
def normalize_number(v):
    t=clean_text(v)
    if not t: return None
    try: return float(t)
    except ValueError: return math.nan
def normalize_date(v):
    t=clean_text(v)
    if not t: return BLANK,None,True
    if isinstance(v,pd.Timestamp): return v.strftime("%Y-%m-%d"),int(v.year),True
    if isinstance(v,(int,float)) and not isinstance(v,bool):
        n=float(v)
        if n.is_integer() and 1800<=n<=2199: return str(int(n)),int(n),True
        if n.is_integer() and 1<=n<=200000:
            try:
                s=pd.Timestamp("1899-12-30")+pd.to_timedelta(int(n),unit="D")
                return s.strftime("%Y-%m-%d"),int(s.year),True
            except (OverflowError,ValueError): pass
        return f"__invalid_date__:{t}",None,False
    m=PARTIAL_DATE_RE.fullmatch(t)
    if not m: return f"__invalid_date__:{t}",None,False
    y=int(m.group(1)); mo,da=m.group(2),m.group(3)
    if da and not mo: return f"__invalid_date__:{t}",None,False
    return t,y,True
def normalize_school_year(v):
    t=clean_text(v)
    if not t: return BLANK,None,True
    m=SCHOOL_YEAR_RE.fullmatch(t)
    if not m or int(m.group(2))!=int(m.group(1))+1: return f"__invalid_school_year__:{t}",None,False
    return t,int(m.group(1)),True
def load_wb(path,sheet,states):
    df=pd.read_excel(path,sheet_name=sheet,keep_default_na=False)
    df=df.dropna(how="all").copy()
    df["row_id"]=df["row_id"].map(clean_text); df["state"]=df["state"].map(clean_text)
    df=df[df["state"].isin(states)].copy()
    if not df["row_id"].all(): raise ValueError(f"{path} blank row_id in scope")
    d=df.loc[df["row_id"].duplicated(keep=False),"row_id"].tolist()
    if d: raise ValueError(f"{path} duplicate row_ids: {d}")
    return df.set_index("row_id",drop=False)
def load_map(path,states):
    pm=pd.read_csv(path,keep_default_na=False,dtype=str)
    for c in ["state","row_id_A","row_id_B","instrument_label"]: pm[c]=pm[c].map(clean_text)
    if states: pm=pm[pm["state"].isin(states)].copy()
    return pm.reset_index(drop=True)
def validate(pm,a,b,labels):
    for exp,col,lab,frame in [(set(a.index),"row_id_A",labels[0],a),(set(b.index),"row_id_B",labels[1],b)]:
        mapped=set(pm.loc[pm[col]!="",col])
        unk=sorted(mapped-exp); om=sorted(exp-mapped)
        if unk: raise ValueError(f"{lab} unknown ids: {unk}")
        if om: raise ValueError(f"{lab} rows omitted: {om}")
def kappa(a,b):
    n=len(a)
    if n==0: return None
    po=sum(x==y for x,y in zip(a,b))/n
    ca,cb=Counter(a),Counter(b)
    pe=sum((ca[c]/n)*(cb[c]/n) for c in set(ca)|set(cb))
    if math.isclose(pe,1.0): return None
    return (po-pe)/(1.0-pe)
def fk(v): return "NA" if v is None or (isinstance(v,float) and math.isnan(v)) else f"{v:.3f}"
def pv(pm,a,b,field,incl):
    va,vb,det=[],[],[]
    for _,p in pm.iterrows():
        ra,rb=p["row_id_A"],p["row_id_B"]
        if not incl and (not ra or not rb): continue
        x=normalize_category(a.at[ra,field]) if ra else MISSING_INSTRUMENT
        y=normalize_category(b.at[rb,field]) if rb else MISSING_INSTRUMENT
        va.append(x); vb.append(y); det.append((p["instrument_label"],x,y))
    return va,vb,det
def cat_results(title,pm,a,b,labels,incl):
    print(f"\n{title}")
    print(f"{'field':22s} {'kappa':>7s} {'agreement':>14s}")
    for f in CAT_FIELDS:
        va,vb,det=pv(pm,a,b,f,incl)
        ag=sum(x==y for x,y in zip(va,vb)); n=len(va)
        print(f"{f:22s} {fk(kappa(va,vb)):>7s} {ag:>3d}/{n:<3d} ({(ag/n if n else float('nan')):6.1%})")
        for lab,x,y in det:
            if x!=y: print(f"    DISAGREE [{lab}]: {labels[0]}={x!r}; {labels[1]}={y!r}")
def num_results(pm,a,b,labels,tol):
    m=pm[(pm["row_id_A"]!="")&(pm["row_id_B"]!="")]
    print("\nNUMERIC AGREEMENT - MATCHED")
    for f in NUM_FIELDS:
        ex=0; dis=[]
        for _,p in m.iterrows():
            x=normalize_number(a.at[p["row_id_A"],f]); y=normalize_number(b.at[p["row_id_B"],f])
            bb=x is None and y is None
            eq=x is not None and y is not None and not math.isnan(x) and not math.isnan(y) and x==y
            ex+=int(bb or eq)
            if not (bb or eq): dis.append((p["instrument_label"],x,y))
        print(f"{f:22s} exact={ex}/{len(m)}")
        for lab,x,y in dis: print(f"    DISAGREE [{lab}]: {labels[0]}={x!r}; {labels[1]}={y!r}")
def date_results(pm,a,b,labels):
    m=pm[(pm["row_id_A"]!="")&(pm["row_id_B"]!="")]
    print("\nDATE AGREEMENT - MATCHED")
    for f in DATE_FIELDS:
        ex=sy=0; inv=[]; dis=[]
        for _,p in m.iterrows():
            ta,ya,va=normalize_date(a.at[p["row_id_A"],f]); tb,yb,vb=normalize_date(b.at[p["row_id_B"],f])
            em=ta==tb and va and vb
            sm=em if (ya is None and yb is None) else (ya is not None and ya==yb)
            ex+=int(em); sy+=int(sm)
            if not va: inv.append((p["instrument_label"],labels[0],ta))
            if not vb: inv.append((p["instrument_label"],labels[1],tb))
            if not em: dis.append((p["instrument_label"],ta,tb))
        print(f"{f:22s} exact={ex}/{len(m)}; same-year={sy}/{len(m)}")
        for lab,c,r in inv: print(f"    INVALID [{lab}] {c}={r!r}")
        for lab,x,y in dis: print(f"    DISAGREE [{lab}]: {labels[0]}={x!r}; {labels[1]}={y!r}")
    for f in SCHOOL_YEAR_FIELDS:
        ex=0; dis=[]
        for _,p in m.iterrows():
            ta,_,va=normalize_school_year(a.at[p["row_id_A"],f]); tb,_,vb=normalize_school_year(b.at[p["row_id_B"],f])
            em=ta==tb and va and vb; ex+=int(em)
            if not em: dis.append((p["instrument_label"],ta,tb))
        print(f"{f:22s} exact={ex}/{len(m)}")
        for lab,x,y in dis: print(f"    DISAGREE [{lab}]: {labels[0]}={x!r}; {labels[1]}={y!r}")
def run(fa,fb,mapf,states,labels):
    pm=load_map(mapf,states)
    a=load_wb(fa,"Coding Template",states); b=load_wb(fb,"Coding Template",states)
    validate(pm,a,b,labels)
    m=pm[(pm["row_id_A"]!="")&(pm["row_id_B"]!="")]
    oa=pm[(pm["row_id_A"]!="")&(pm["row_id_B"]=="")]; ob=pm[(pm["row_id_A"]=="")&(pm["row_id_B"]!="")]
    print("="*70)
    print("INSTRUMENT DETECTION | states:", ", ".join(sorted(states)))
    print(f"Universe {len(pm)} | both {len(m)} | only-{labels[0]} {len(oa)} | only-{labels[1]} {len(ob)} | Jaccard {len(m)}/{len(pm)} = {len(m)/len(pm):.3f}")
    for _,p in oa.iterrows(): print(f"    {labels[0]}-only [{p['instrument_label']}]: {p['row_id_A']}")
    for _,p in ob.iterrows(): print(f"    {labels[1]}-only [{p['instrument_label']}]: {p['row_id_B']}")
    cat_results("CATEGORICAL KAPPA - MATCHED",pm,a,b,labels,False)
    cat_results("INCLUSIVE SENSITIVITY - MISSING AS CATEGORY",pm,a,b,labels,True)
    num_results(pm,a,b,labels,0.0)
    date_results(pm,a,b,labels)

if __name__ == "__main__":
    # Round 1 (calibration), as run 2026-07-23. Inputs sit beside this script.
    # Usage: python compare_kappa_v2_asrun.py [QAP_file] [CL_file] [pair_map]
    import sys
    here = Path(__file__).resolve().parent
    fa = sys.argv[1] if len(sys.argv) > 1 else str(here / "QAP_coder_file_asrun.xlsx")
    fb = sys.argv[2] if len(sys.argv) > 2 else str(here / "CoderB_CL_four_states.xlsx")
    mp = sys.argv[3] if len(sys.argv) > 3 else str(here / "pair_map.csv")
    run(fa, fb, mp, {"Alaska", "Arizona", "Arkansas"}, ["QAP", "CL"])
    run(fa, fb, mp, {"Alabama"}, ["QAP", "CL"])
