import re,io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from pypdf import PdfReader, PdfWriter, Transformation
import tables  # registers LS fonts, builds table PDFs

U=''
L=open(U+'QAP_figure_legends.txt').read().strip().split('\n\n'); leg={}
for b in L:
    m=re.match(r'(Figure \d|Supplementary Figure \d)\. (.*)',b,re.S); leg[m.group(1)]=m.group(2)
figs=[('Figure 1',U+'QAP_Fig1_overview.pdf'),('Figure 2',U+'QAP_Fig2_data_model.pdf'),
      ('Figure 3',U+'QAP_Fig3_rollout.pdf'),('Figure 4',U+'QAP_Fig4_validation.pdf')]
supp=[('Supplementary Figure 1','QAP_SuppFig1_state_year_grid.pdf')]
W,H=A4; M=18*mm; cw=W-2*M
st=ParagraphStyle('l',fontName='LS',fontSize=8.5,leading=11.5,alignment=TA_LEFT)
out=PdfWriter()
def fig_page(name,path):
    src=PdfReader(path).pages[0]; iw=float(src.mediabox.width); ih=float(src.mediabox.height)
    title,body=leg[name].split('. ',1)
    p=Paragraph(f'<b>{name} | {title}.</b> {body}',st); _,ph=p.wrap(cw,H)
    s=cw/iw; h=ih*s; maxh=H-2*M-ph-8*mm
    if h>maxh: s=maxh/ih; h=maxh
    w=iw*s; x=M+(cw-w)/2; y=H-M-h
    buf=io.BytesIO(); c=canvas.Canvas(buf,pagesize=A4); p.drawOn(c,M,y-6*mm-ph); c.showPage(); c.save()
    page=PdfReader(io.BytesIO(buf.getvalue())).pages[0]
    page.merge_transformed_page(src,Transformation().scale(s,s).translate(x,y))
    out.add_page(page)
for n,f in figs: fig_page(n,f)
for pg in PdfReader('QAP_Tables_combined.pdf').pages: out.add_page(pg)
for n,f in supp: fig_page(n,f)
out.add_metadata({'/Title':'QAP data descriptor: figures and tables'})
out.write('QAP_Figures_and_Tables_combined.pdf'); print('pages',len(out.pages))
