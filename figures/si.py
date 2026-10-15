from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
H=ParagraphStyle('h',fontName='Helvetica-Bold',fontSize=13,leading=16,spaceAfter=6)
N=ParagraphStyle('n',fontName='Helvetica',fontSize=9.5,leading=13)
doc=SimpleDocTemplate('QAP_Supplementary_Information.pdf',pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=18*mm,bottomMargin=18*mm,title='Supplementary Information',author='Quinn A. Paulsen, Chase A. Ludwig')
T='State policy status by school year, 2000-2001 to 2025-2026'
s=[Paragraph('Supplementary Information',H),
   Paragraph('State policies on school recess, physical activity, and outdoor time in the United States, 2000-2025',N),Spacer(1,3),
   Paragraph('Quinn A. Paulsen and Chase A. Ludwig',N),Spacer(1,14),
   Paragraph('Contents',ParagraphStyle('c',parent=H,fontSize=11)),
   Table([['Figure S1. '+T,'2']],colWidths=[150*mm,20*mm],style=[('FONT',(0,0),(-1,-1),'Helvetica',9.5),('ALIGN',(1,0),(1,0),'RIGHT')]),PageBreak()]
w=174*mm
s+=[Image('QAP_SuppFig1_state_year_grid.png',width=w,height=w*195/180),Spacer(1,6),
    Paragraph(f'<b>Figure S1. {T}.</b> <b>a</b>, Recess. <b>b</b>, PE and daily physical activity time. Each cell shows the strongest K-12 instrument in force; within each panel, jurisdictions are ordered by the school year of their first mandate, then of their first recommendation, then alphabetically, so the row order differs between panels. Derivation and exclusions as in Figure 3 of the main article.',N)]
doc.build(s)
