from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, KeepTogether, Flowable, Image as RLImage)
from reportlab.pdfgen import canvas

OUT = r"C:\Users\TKE\Documents\Datasheet\SMD_Package_Size_Reference_Guide_v2.pdf"
ATTACHED_IMAGE = r"C:\Users\TKE\Documents\Datasheet\smd-components-and-their-package-size.jpg"
NAVY = colors.HexColor('#15324B')
BLUE = colors.HexColor('#1976A8')
PALE = colors.HexColor('#EAF3F8')
INK = colors.HexColor('#22313F')
MUTED = colors.HexColor('#5C6B75')
LINE = colors.HexColor('#C9D5DC')
GOLD = colors.HexColor('#E9AA42')

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Title2', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=25, leading=30, textColor=NAVY, alignment=TA_LEFT, spaceAfter=8))
styles.add(ParagraphStyle(name='Sub', parent=styles['Normal'], fontSize=11, leading=16, textColor=MUTED, spaceAfter=10))
styles.add(ParagraphStyle(name='H1x', parent=styles['Heading1'], fontSize=17, leading=21, textColor=NAVY, spaceBefore=1, spaceAfter=8))
styles.add(ParagraphStyle(name='H2x', parent=styles['Heading2'], fontSize=11, leading=14, textColor=BLUE, spaceBefore=7, spaceAfter=4))
styles.add(ParagraphStyle(name='Bodyx', parent=styles['BodyText'], fontSize=8.5, leading=12, textColor=INK, spaceAfter=5))
styles.add(ParagraphStyle(name='Smallx', parent=styles['BodyText'], fontSize=7.2, leading=9.2, textColor=INK))
styles.add(ParagraphStyle(name='Tinyx', parent=styles['BodyText'], fontSize=6.4, leading=8, textColor=INK))
styles.add(ParagraphStyle(name='CellHead', parent=styles['BodyText'], fontName='Helvetica-Bold', fontSize=7.1, leading=8.2, textColor=colors.white))
styles.add(ParagraphStyle(name='Callout', parent=styles['BodyText'], fontSize=8.3, leading=11.2, textColor=NAVY))

P = lambda s, st='Smallx': Paragraph(s, styles[st])

def header_footer(c, doc):
    c.saveState()
    w, h = letter
    c.setFillColor(NAVY)
    c.rect(0, h-8*mm, w, 8*mm, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont('Helvetica-Bold', 8)
    c.drawString(17*mm, h-5.4*mm, 'SMD PACKAGE SIZE REFERENCE | VERSION 2')
    c.setFillColor(MUTED)
    c.setFont('Helvetica', 7)
    c.drawString(17*mm, 10*mm, 'Typical body dimensions only | Always confirm the exact manufacturer drawing')
    c.drawRightString(w-17*mm, 10*mm, f'{doc.page}')
    c.setStrokeColor(LINE)
    c.line(17*mm, 14*mm, w-17*mm, 14*mm)
    c.restoreState()

def make_table(headers, rows, widths, font='Smallx', repeatRows=1):
    data = [[P(x,'CellHead') for x in headers]]
    data += [[P(str(x), font) for x in row] for row in rows]
    t = Table(data, colWidths=widths, repeatRows=repeatRows, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),0.35,LINE),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),
        ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ]))
    return t

class PackageSketch(Flowable):
    """Vector sample picture: generic package top view, side view and dimension callouts."""
    def __init__(self, width=178*mm, height=87*mm):
        Flowable.__init__(self); self.width=width; self.height=height
    def draw(self):
        c=self.canv; w=self.width; h=self.height
        c.setFillColor(PALE); c.roundRect(0,0,w,h,4*mm,stroke=0,fill=1)
        c.setFillColor(NAVY); c.setFont('Helvetica-Bold',9)
        c.drawString(6*mm,h-7*mm,'SAMPLE PACKAGE PICTURE - simplified views, not to scale')
        # Chip component top view, left
        x=21*mm; y=43*mm
        c.setFillColor(colors.HexColor('#445A6B')); c.roundRect(x,y,35*mm,17*mm,2*mm,stroke=0,fill=1)
        c.setFillColor(colors.HexColor('#C9D2D8')); c.rect(x-5*mm,y+1*mm,5*mm,15*mm,stroke=0,fill=1); c.rect(x+35*mm,y+1*mm,5*mm,15*mm,stroke=0,fill=1)
        c.setFillColor(colors.white); c.setFont('Helvetica-Bold',8); c.drawCentredString(x+17.5*mm,y+7*mm,'CHIP R / C')
        c.setFillColor(INK); c.setFont('Helvetica',7); c.drawCentredString(x+17.5*mm,y-5*mm,'TOP VIEW: length L x width W')
        # Dimension L arrow
        c.setStrokeColor(BLUE); c.setLineWidth(.8); c.line(x,y+20*mm,x+35*mm,y+20*mm)
        c.line(x,y+18.5*mm,x,y+21.5*mm); c.line(x+35*mm,y+18.5*mm,x+35*mm,y+21.5*mm)
        c.setFillColor(BLUE); c.drawCentredString(x+17.5*mm,y+21*mm,'L')
        # SOT side view
        sx=99*mm; sy=45*mm
        c.setFillColor(colors.HexColor('#445A6B')); c.roundRect(sx,sy,28*mm,14*mm,2*mm,stroke=0,fill=1)
        c.setFillColor(colors.HexColor('#C9D2D8'))
        for i in range(3):
            c.setStrokeColor(colors.HexColor('#A9B6BE')); c.setLineWidth(2)
            c.line(sx+2*mm+i*3*mm,sy,sx+2*mm+i*3*mm,sy-8*mm)
            c.line(sx+26*mm-i*3*mm,sy,sx+26*mm-i*3*mm,sy-8*mm)
        c.setFillColor(INK); c.setFont('Helvetica-Bold',8); c.drawCentredString(sx+14*mm,sy+5*mm,'SOT / IC')
        c.setFont('Helvetica',7); c.drawCentredString(sx+14*mm,sy-13*mm,'SIDE VIEW: height H')
        c.setStrokeColor(BLUE); c.line(sx+33*mm,sy,sx+33*mm,sy+14*mm); c.line(sx+31.5*mm,sy,sx+34.5*mm,sy); c.line(sx+31.5*mm,sy+14*mm,sx+34.5*mm,sy+14*mm)
        c.saveState(); c.translate(sx+36*mm,sy+7*mm); c.rotate(90); c.setFillColor(BLUE); c.drawCentredString(0,0,'H'); c.restoreState()
        # Pitch mini drawing
        px=22*mm; py=17*mm
        for i in range(5):
            c.setFillColor(BLUE); c.circle(px+i*6*mm,py,1.1*mm,stroke=0,fill=1)
        c.setStrokeColor(BLUE); c.line(px,py-4*mm,px+6*mm,py-4*mm); c.line(px,py-5*mm,px,py-3*mm); c.line(px+6*mm,py-5*mm,px+6*mm,py-3*mm)
        c.setFillColor(INK); c.drawString(px+44*mm,py-1*mm,'Pitch = center-to-center lead spacing (ICs)')
        c.setFont('Helvetica',7); c.setFillColor(MUTED); c.drawString(6*mm,5*mm,'Dimensions in this guide: package body L x W x H; pin pitch shown separately. PCB pads are not included.')

story=[]
story += [Spacer(1,5*mm), P('SMD PACKAGE<br/>SIZE REFERENCE GUIDE','Title2'),
          P('VERSION 2  |  Includes the supplied reference sheet, clearer cross-check notes, and common package dimensions for ICs, diodes, passives, transistors, MOSFETs, LEDs, and related parts.','Sub'),
          PackageSketch(), Spacer(1,4*mm)]
story.append(P('<b>How to read a package size:</b> L x W x H is the component body length, width, and maximum height in millimeters. For gull-wing and leaded parts, lead span can be wider than the body. For leadless parts, terminal dimensions are separate. Pin pitch is center-to-center spacing.','Callout'))
story.append(Spacer(1,2*mm))
story.append(P('<b>Important:</b> Package names are not perfectly uniform across brands. “Typical” dimensions below are nominal identification values, not production limits. Use the exact part datasheet for tolerances, pinout, orientation, thermal pad, and recommended PCB land pattern. IPC-7351 addresses land patterns, not a universal component-body catalog. [1]','Callout'))
story.append(P('Quick package family map','H2x'))
maprows=[
('Resistors / capacitors / small LEDs','Chip sizes: 01005 to 2512; MELF and arrays also common'),
('Diodes / rectifiers / TVS','SOD-323/123/523; SMA/SMB/SMC; SOT-23; DFN'),
('Small transistors / MOSFETs','SOT-23, SOT-323, SOT-89, SOT-223, DFN; power DPAK'),
('ICs / logic / analog / memory','SOIC, TSSOP, SSOP, QFN/DFN, LQFP, BGA, WLCSP'),
('Power / protection / RF / opto','DPAK/D2PAK, PowerSO, SMA/SMB/SMC, SOD, SOP-4, RF leadless')]
story.append(make_table(['Component group','Common package families'],maprows,[56*mm,122*mm]))
story.append(PageBreak())

story += [P('1. Chip passives and small indicators','H1x'), P('Resistors, MLCC capacitors, ferrite beads, and many LEDs share the familiar two-terminal chip-size codes. Imperial and metric codes can collide: EIA 0402 is 1.0 x 0.5 mm, while metric 0402 is 0.4 x 0.2 mm. Always confirm which numbering system is used. Murata lists the EIA/JIS mappings and representative MLCC dimensions. [2]','Bodyx')]
passive=[
('01005','0402 metric','0.40 x 0.20','0.13-0.23','Very small; check assembly capability'),
('0201','0603 metric','0.60 x 0.30','0.20-0.40','Common miniature passive'),
('0402','1005 metric','1.00 x 0.50','0.30-0.60','Very common; metric/EIA name confusion'),
('0603','1608 metric','1.60 x 0.80','0.35-0.80','General purpose'),
('0805','2012 metric','2.00 x 1.25','0.50-1.10','General purpose, larger ratings'),
('1206','3216 metric','3.20 x 1.60','0.55-1.40','Power and voltage vary by series'),
('1210','3225 metric','3.20 x 2.50','0.60-2.30','Wider body, common capacitor size'),
('1812','4532 metric','4.50 x 3.20','0.80-3.00','Bulkier passive / protection'),
('2010','5025 metric','5.00 x 2.50','0.60-1.20','Often resistor size code'),
('2512','6432 metric','6.30 x 3.20','0.60-1.20','Power resistor and shunt use')]
story.append(make_table(['EIA / inch code','JIS / metric code','Typical body L x W (mm)','Typical H (mm)','Notes'],passive,[22*mm,25*mm,32*mm,24*mm,75*mm]))
story += [Spacer(1,3*mm), P('Other passive package shapes','H2x')]
otherpass=[
('MELF / MiniMELF','Cylindrical 1.4-5.8 mm long; 1.0-2.2 mm diameter','Resistors and diodes; orientation can matter'),
('Resistor networks / arrays','Common bodies about 2.0-5.1 mm long; 2-8+ terminals','Check pin count, internal circuit, and terminal pitch'),
('Tantalum / polymer capacitor','A / B / C / D case families; roughly 3.2-7.3 mm long','Case code is not the same as chip-resistor code'),
('Power inductor','Broad range, often 2-15+ mm footprint','Size, height, saturation current, and shielding vary widely'),
('Crystal / oscillator','Common 2.0 x 1.6, 2.5 x 2.0, 3.2 x 2.5 mm bodies','Package body only; pad and keepout are device-specific')]
story.append(make_table(['Family','Representative dimensions','Where used / caution'],otherpass,[40*mm,63*mm,75*mm]))
story += [Spacer(1,2*mm), P('<b>Passive-size decoding:</b> The first two digits usually encode length and last two encode width in hundredths of an inch for EIA chip codes (e.g., 0603 ≈ 0.06 x 0.03 in). This is approximate; use the metric body dimensions for design. Capacitor thickness and resistor power rating vary by manufacturer and series. [2]','Callout'), PageBreak()]

story += [P('2. Diodes, LEDs, and discrete semiconductors','H1x'), P('The same outline can contain different electrical functions. SOD/SMA names describe package families, not whether a part is a signal diode, Schottky, Zener, TVS, or rectifier. Check polarity markings and pin configuration in the part datasheet. Diodes Incorporated maintains outline drawings for many SOD, SOT, and DFN variants; Vishay lists typical rectifier package dimensions. [3][4]','Bodyx')]
discrete=[
('SOD-523','Small diode','1.6 x 0.8 x 0.6','-','Tiny signal / Zener'),
('SOD-323','Small diode','1.7 x 1.25 x 0.95','-','Signal diode / low-power Zener'),
('SOD-123','Small diode','2.65 x 1.6 x 1.1','-','Common signal, Schottky, Zener'),
('SOD-123F','Flat-lead diode','2.6 x 1.6 x 0.7','-','Low profile; variants differ'),
('SOT-23 / SOT-23-3','3-lead transistor','2.9 x 1.3 x 1.0','0.95','BJT, MOSFET, dual diode/regulator'),
('SOT-23-5 / -6','5/6-lead device','2.9 x 1.6 x 1.1','0.95','ICs, dual FETs, transistor arrays'),
('SOT-323 / SC-70','3-lead small outline','2.0 x 1.25 x 0.9','0.65','Small signal transistor/diode'),
('SOT-363 / SC-70-6','6-lead small outline','2.0 x 1.25 x 0.9','0.65','Dual transistor / array'),
('SOT-89','Power transistor','4.5 x 2.5 x 1.5','1.5','BJT / regulator / small power FET'),
('SOT-223','Power outline','6.5 x 3.5 x 1.6','2.3 typical','Regulator / transistor / MOSFET; large tab'),
('SMA / DO-214AC','Rectifier / TVS','5.1 x 2.7 x 2.1','—','Common 1 A-class rectifier outline'),
('SMB / DO-214AA','Rectifier / TVS','5.4 x 3.6 x 2.3','—','Larger diode / protection device'),
('SMC / DO-214AB','Rectifier / TVS','7.9 x 5.9 x 2.3','—','Higher power protection / rectifier'),
('SMF / DO-219AB','Slim diode','3.7 x 1.8 x 1.0','—','Compact TVS / rectifier family'),
('MicroSMP / DO-219AD','Tiny diode','2.5 x 1.3 x 0.65','—','Low profile / TVS families')]
story.append(make_table(['Package','Typical role','Typical body L x W x H (mm)','Pitch (mm)','Common use'],discrete,[32*mm,32*mm,37*mm,20*mm,57*mm],font='Tinyx'))
story += [Spacer(1,3*mm), P('LEDs and photoelectric parts','H2x')]
leds=[('Chip LED','0201 / 0402 / 0603 / 0805','0.6x0.3 through 2.0x1.25 mm','Check anode/cathode and lens height'),('PLCC-2 / PLCC-4','2 or 4 pads','~3.2x2.8 to 5.0x5.0 mm','Common indicator and RGB LED'),('SMD IR / photodiode','SOD, side-view, leadless','Varies by optics and window','Optical face and pinout matter')]
story.append(make_table(['Family','Common size / outline','Representative body size','Check'],leds,[32*mm,39*mm,51*mm,56*mm]))
story += [Spacer(1,2*mm), P('<b>Dimension note:</b> SOD-123 is a representative outline. For example, Diodes Inc. specifies a typical 2.65 mm body length, 1.55 mm body width, and 1.05 mm height (with min/max limits); another maker’s drawing may differ slightly. SMA/SMB/SMC values above are rounded representative outlines. [3][4]','Callout'), PageBreak()]

story += [P('3. IC packages with leads','H1x'), P('A package may be sold in multiple pin counts and body widths. The dimensions below are representative body dimensions; “span” means the overall outside-to-outside lead dimension when useful. Pitch is the center spacing of adjacent pins along a row. TI’s package finder provides exact body, pitch, height, and drawings for its package variants. [5]','Bodyx')]
ic_leaded=[
('SOT-23-5 / 6','5-6','2.9 x 1.6 x 1.1','0.95','Small analog IC, logic, regulator'),
('SOIC narrow','8-16','~4.9 x 3.9 x 1.75','1.27','Op amp, memory, controller'),
('SOIC wide','8-16','~10.3 x 7.5 x 1.75','1.27','Wide-body isolation / power'),
('SOP / SSOP','8-28+','~3-10 x 3-8 x 1.5-2.0','1.0 / 0.65','Compact logic and analog'),
('TSSOP','8-56','~3-12 x 3-8 x 1.0-1.2','0.65 / 0.5','Thin, higher pin density'),
('MSOP / VSSOP','8-16','~3.0 x 3.0 x 1.1','0.65 / 0.5','Small analog and power control'),
('QSOP','16-28','~6-10 x 3.8 x 1.5','0.635','Shrink small outline'),
('LQFP / TQFP','32-256','~7-28 square x 1.0-1.6','0.8 / 0.5 / 0.4','MCUs, DSPs, ASICs'),
('PLCC','20-84','~9-30 square x 3.0-4.6','1.27','J-lead, socketable variants'),
('PowerSO / HSOP','8-28','~5-16 x 5-11 x 1.7-3.0','0.65-1.27','Power IC, driver, heat spreading')]
story.append(make_table(['Package family','Typical pins','Representative body L x W x H (mm)','Pitch (mm)','Typical applications'],ic_leaded,[34*mm,18*mm,48*mm,22*mm,56*mm],font='Tinyx'))
story += [Spacer(1,3*mm), P('Common shorthand and aliases','H2x')]
aliases=[('SOIC','Small outline IC; also SO / SOP depending on vendor'),('TSSOP','Thin shrink small-outline; pin count, body width, and pitch define variant'),('MSOP / VSSOP','Miniature / very thin small-outline; names overlap across vendors'),('LQFP / TQFP','Low-profile / thin quad flat package; lead count and pitch vary widely'),('PLCC','Plastic leaded chip carrier; J-shaped leads')]
story.append(make_table(['Short name','Meaning / note'],aliases,[42*mm,136*mm]))
story += [Spacer(1,2*mm), P('<b>Read the part number suffix:</b> manufacturers often encode package and tape/reel options at the end of an IC order code. Similar device names can be offered in several outlines. Match the full ordering code to the outline drawing before making a PCB footprint.','Callout'), PageBreak()]

story += [P('4. Leadless, array, power, and special packages','H1x'), P('Leadless packages use pads under or around the body rather than visible gull-wing leads. The exposed thermal pad is an electrical and thermal feature; its dimensions and via guidance must come from the individual datasheet. BGA and wafer-level packages are specified by body size, ball/pad count, and pitch rather than gull-wing lead pitch. [5][6]','Bodyx')]
leadless=[
('DFN / SON','6-16','~2-6 x 2-6 x 0.5-1.0','0.4-0.8','Small leadless; optional exposed pad'),
('QFN / VQFN','16-100+','~3-12 square x 0.5-1.0','0.4-0.8','Logic, MCU, RF, power; exposed pad common'),
('WSON','6-16','~2-5 x 2-5 x 0.5-0.8','0.4-0.65','Very thin small-outline no-lead'),
('LGA','varies','~2-15+ x 2-15+ x 0.5-2','0.4-1.0','Sensors, RF, modules; land grid'),
('BGA / FBGA','25-1000+','~3-40 square x 0.5-3','0.5-1.27 ball pitch','Processors, memory, FPGA'),
('WLCSP / CSP','4-200+','die-sized, often 0.5-5 square','0.3-0.8 ball pitch','Tiny mobile / power / sensor IC'),
('DPAK / TO-252','3-7','~6.5 x 6.1 x 2.3','2.28-2.54','Power MOSFET, regulator, rectifier'),
('D2PAK / TO-263','3-7','~10 x 15.4 x 4.4','2.54-5.08','Higher power MOSFET / rectifier'),
('PowerPAK / LFPAK','varies','~3-10 x 3-11 x 0.8-2.5','vendor-specific','Low-resistance FET; footprint varies'),
('SMA/SMB/SMC','2','5.1x2.7x2.1 / 5.4x3.6x2.3 / 7.9x5.9x2.3','—','Rectifiers, TVS and surge protection')]
story.append(make_table(['Package family','Typical terminals','Representative body L x W x H (mm)','Pitch / spacing','Typical use'],leadless,[31*mm,21*mm,51*mm,31*mm,44*mm],font='Tinyx'))
story += [Spacer(1,3*mm), P('Small cross-reference: package family by component','H2x')]
category=[
('Resistor','Chip (01005-2512), MELF, array, power resistor'),
('Capacitor','Chip MLCC, tantalum/polymer case, aluminum can, feedthrough'),
('Inductor / ferrite','Chip, molded/shielded power inductor, bead, common-mode choke'),
('Diode / TVS / rectifier','SOD, SMA/SMB/SMC, DFN, bridge and power leadless packages'),
('BJT / small MOSFET','SOT-23, SOT-323, SOT-363, SOT-89, SOT-223, DFN'),
('Power MOSFET / regulator','DPAK, D2PAK, PowerSO, PowerPAK, LFPAK, QFN'),
('IC / logic / analog / MCU','SOIC, TSSOP, QFN/DFN, LQFP, BGA, WLCSP'),
('LED / optocoupler / sensor','Chip LED, PLCC, SOD/SOT, SOP-4, LGA, QFN')]
story.append(make_table(['Part type','Common SMD families (examples, not a complete catalog)'],category,[47*mm,131*mm]))
story += [Spacer(1,3*mm), P('Other SMD parts found on boards','H2x')]
related=[
('Board connectors','FPC/FFC, board-to-board, USB, card, RF coax','Body sizes and contact pitch are connector-specific; inspect mating side and retention features.'),
('Switches / buttons','Tact switch, slide switch, encoder','Body and actuator dimensions matter as much as solder terminals.'),
('Fuse / protection','Chip fuse, resettable PTC, ESD array','Check current rating, voltage rating, polarity, and thermal limits.'),
('Relays / optocouplers','SMD relay, SOP-4/6/8 optocoupler','Often taller and larger; observe isolation and keepout requirements.')]
story.append(make_table(['Group','Examples','Key check'],related,[35*mm,57*mm,86*mm],font='Tinyx'))
story.append(PageBreak())

story += [P('5. Use this guide safely','H1x'), P('A package label narrows the search; it does not uniquely identify the part. Many outlines have competing names, variants, or manufacturer-specific body dimensions. Package dimensions below are rounded common examples for recognition and rough planning. Use the manufacturer mechanical drawing before ordering boards or footprints.','Bodyx')]
story.append(P('PCB footprint checklist','H2x'))
check=[
('1','Confirm the full orderable part number and package code.'),
('2','Open its package drawing: body size, lead/pad size, tolerances, height, pin-1 mark, polarity.'),
('3','Read the pin map and numbering orientation from the top-view drawing.'),
('4','Copy or derive PCB land pattern from the datasheet or an applicable IPC-7351 land-pattern recommendation.'),
('5','For thermal/power parts, follow exposed-pad, copper, via, and heat-dissipation guidance.'),
('6','Check stencil, solder mask, courtyard, and assembly capabilities for very small parts.')]
story.append(make_table(['Step','Check'],check,[18*mm,160*mm]))
story += [Spacer(1,4*mm), P('Units and abbreviations','H2x')]
units=[('L x W x H','Body length x body width x maximum height, millimeters unless stated'),('Pitch','Center-to-center spacing between adjacent terminals'),('EIA / imperial chip code','Common resistor/capacitor size code such as 0603'),('JIS / metric code','Metric outline code such as 1608 for 1.6 x 0.8 mm'),('DFN / QFN / SON / WSON','Leadless package families; terminal geometry is underside/edge-specific'),('BGA / WLCSP','Ball array / wafer-level chip-scale package')]
story.append(make_table(['Term','Meaning'],units,[42*mm,136*mm]))
story += [Spacer(1,4*mm), P('References and package outline sources','H2x')]
refs=[
('[1] IPC-7351','Generic requirements and guidance for PCB surface-mount land patterns.','https://www.ipc.org/TOC/IPC-7351.pdf'),
('[2] Murata MLCC size table','EIA/JIS size mapping and representative body dimensions for chip capacitors.','https://www.murata.com/en-us/tool/data/sparameterdata/sparameter-mlcc/condition'),
('[3] Diodes Incorporated package outlines','Package drawings and pad layouts for SOD, SOT, DFN and related packages.','https://www.diodes.com/design/support/packaging/diodes-packaging/diodes-package-outlines-and-pad-layouts'),
('[4] Vishay eSMP dimensions','Representative SMA, SMB, SMC, SMF, MicroSMP, DPAK and power package sizes.','https://www.vishay.com/en/landingpage/tradeshows/diodes/esmppackages.html'),
('[5] Texas Instruments package finder','Manufacturer package dimensions, pitches, heights, and drawings for IC packages.','https://www.ti.com/packaging/docs/searchalltipackages.tsp'),
('[6] NXP package search','Package family descriptions, JEDEC outline references, dimensions, and drawings.','https://www.nxp.com/packages/search')]
for name, desc, url in refs:
    story.append(P(f'<b>{name}</b> - {desc} <link href="{url}" color="#1976A8">Open source</link>','Tinyx'))
story.append(Spacer(1,4*mm))
story.append(P('Prepared as a practical overview of widely used SMD families. Dimensions are rounded typical identification values and may differ by vendor, tolerance, lead style, and subfamily. Source pages accessed 28 October 2026.','Tinyx'))

story.append(PageBreak())
story += [P('Appendix: supplied SMD reference sheet','H1x'),
          P('The image below is included as provided. It is useful as a visual index of package families and PCB terminology. Some component dimensions are rounded or differ from the representative standard sizes used in the tables earlier in this guide. For example, its passive table gives 0603 as 1.5 x 0.8 mm and 1206 as 3.0 x 1.5 mm; the common nominal EIA sizes are 1.6 x 0.8 mm and 3.2 x 1.6 mm. Use the exact component datasheet for package dimensions.','Bodyx'),
          P('<b>Separate board-design data from package data:</b> track width/current, drill holes, vias, and pitch are PCB design references, not package body dimensions. Track current capacity depends on copper thickness, temperature rise, stackup, and design rules; hole and via sizes depend on the board manufacturer and design.','Callout'),
          Spacer(1,2*mm)]
img=RLImage(ATTACHED_IMAGE, width=178*mm, height=118.7*mm)
img.hAlign='CENTER'
story.append(img)
story += [Spacer(1,2*mm), P('User-provided image: smd-components-and-their-package-size.jpg. This graphic is preserved for visual reference; numeric entries have not been adopted as universal package specifications.','Tinyx')]

doc=SimpleDocTemplate(OUT,pagesize=letter,rightMargin=17*mm,leftMargin=17*mm,topMargin=14*mm,bottomMargin=18*mm,title='SMD Package Size Reference Guide - Version 2',author='OpenAI')
doc.build(story,onFirstPage=header_footer,onLaterPages=header_footer)
print(OUT)
