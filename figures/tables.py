"""Tables 1 and 2 for the QAP data descriptor, in Scientific Reports house style
(full thin grid, bold shaded header row, sans 7.5 pt, double-column 180 mm width)."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import Table, TableStyle, Paragraph, SimpleDocTemplate, Spacer, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

F='/usr/share/fonts/truetype/liberation/'
pdfmetrics.registerFont(TTFont('LS',F+'LiberationSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LS-B',F+'LiberationSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('LS-I',F+'LiberationSans-Italic.ttf'))
pdfmetrics.registerFontFamily('LS',normal='LS',bold='LS-B',italic='LS-I')

HEAD=colors.HexColor('#D9D9D9'); RULE=colors.HexColor('#000000')
cell=ParagraphStyle('c',fontName='LS',fontSize=7.5,leading=9.2)
cellb=ParagraphStyle('cb',parent=cell,fontName='LS-B')
cap=ParagraphStyle('cap',fontName='LS',fontSize=8.5,leading=11.5,alignment=TA_LEFT,spaceBefore=4*mm)
cw=180*mm

def grid(nrows,ncols,extra=()):
    st=[('FONTNAME',(0,0),(-1,-1),'LS'),('FONTSIZE',(0,0),(-1,-1),7.5),
        ('GRID',(0,0),(-1,-1),0.5,RULE),('BACKGROUND',(0,0),(-1,0),HEAD),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),3),('RIGHTPADDING',(0,0),(-1,-1),3),
        ('TOPPADDING',(0,0),(-1,-1),1.6),('BOTTOMPADDING',(0,0),(-1,-1),1.6)]
    return TableStyle(st+list(extra))

P=lambda s,b=False:Paragraph(s,cellb if b else cell)

# ---------- Table 1 ----------
T1=[('row_id','text','Stable unique identifier; also names the corresponding source files'),
('level','state','Issuing level of government (all rows are state-level in this release)'),
('state; state_fips; jurisdiction_name','text; 2-digit code','Jurisdiction name and FIPS code for linkage'),
('nces_leaid','7-digit code','Reserved for district rows; blank in this release'),
('topic','recess, daily_PA_minutes, outdoor_time, none','Policy domain; PE minutes are coded under daily_PA_minutes'),
('policy_status','mandate, recommendation, silent','Legal strength from operative language'),
('instrument_class','time_dose, structural_recess, umbrella_subject, credit_unit, withholding_policy, baseline_none','Analytic class; defaults use time_dose and structural_recess'),
('minutes_required; frequency','number; daily, weekly, per_week_minutes, other, NA','Dose and cadence'),
('grade_bands','text','Controlled short form of grades covered'),
('outdoor_specificity','explicit_outdoor, outdoor_if_feasible, indoor_permitted, unspecified, NA','Required location of covered time'),
('withholding_recess','prohibited, restricted, permitted, silent','Use of recess withholding as discipline'),
('enforcement','accreditation_condition, monitored, statutory_soft, none, unknown','Enforcement mechanism attached to the requirement'),
('enactment_date; effective_date; amended_date; repeal_date','YYYY, YYYY-MM, or YYYY-MM-DD','Raw dates from primary sources'),
('implementation_school_year','YYYY-YYYY','First applicable school year, recorded only when stated'),
('superseded_by','row_id list','Successor rows'),
('treatment_school_year; date_basis','YYYY-YYYY; text flag','Derived treatment timing and the rule applied'),
('citation; source_type; source_url; source_excerpt; source_file','text','Provenance for each row'),
('coder; date_coded; confidence; notes_ambiguities','text','Coding metadata and free-text notes')]
rows1=[[P('Field',1),P('Values or format',1),P('Description',1)]]+[[P(a),P(b),P(c)] for a,b,c in T1]
t1=Table(rows1,colWidths=[52*mm,58*mm,70*mm],repeatRows=1); t1.setStyle(grid(len(rows1),3))
cap1=Paragraph('<b>Table 1.</b> Panel fields. The 32 fields of the state panel, grouped where fields share a format. '
 'Controlled vocabularies are listed in full; derived fields (treatment_school_year, date_basis) are computed from the raw date fields under the codebook rules.',cap)

# ---------- Table 2 ----------
T2=[('time_dose',115,78,None,193),('umbrella_subject',85,15,None,100),('credit_unit',59,1,None,60),
('structural_recess',23,10,None,33),('withholding_policy',4,7,None,11),('baseline_none',None,None,153,153)]
f=lambda v:'' if v is None else str(v)
rows2=[[P('Instrument class',1),P('Mandate',1),P('Recommendation',1),P('Silent',1),P('Total',1)]]
rows2+=[[P(a),P(f(b)),P(f(c)),P(f(d)),P(f(e))] for a,b,c,d,e in T2]
rows2+=[[P('Total',1),P('286',1),P('111',1),P('153',1),P('550',1)]]
t2=Table(rows2,colWidths=[44*mm,34*mm,34*mm,34*mm,34*mm])
t2.setStyle(grid(len(rows2),5,[('ALIGN',(1,1),(-1,-1),'RIGHT'),('LINEABOVE',(0,-1),(-1,-1),0.9,RULE)]))
cap2=Paragraph('<b>Table 2.</b> Panel rows by instrument class and legal strength. Counts are from the frozen release file '
 '(550 rows; 397 policy instruments and 153 silent baselines across 50 states and the District of Columbia, 4 to 21 rows per jurisdiction, median 11). '
 'Silent baselines are coded only in the baseline_none class and carry no legal strength.',cap)

def build(path,items):
    doc=SimpleDocTemplate(path,pagesize=A4,leftMargin=(A4[0]-cw)/2,rightMargin=(A4[0]-cw)/2,topMargin=18*mm,bottomMargin=18*mm,
                          title='QAP data descriptor tables')
    doc.build(items)
build('QAP_Table1_fields.pdf',[t1,cap1])
build('QAP_Table2_rows.pdf',[t2,cap2])
build('QAP_Tables_combined.pdf',[KeepTogether([t1,cap1]),Spacer(1,10*mm),KeepTogether([t2,cap2])])
print('ok')
