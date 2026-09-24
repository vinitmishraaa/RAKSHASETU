import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    DARK_BLUE = RGBColor(10, 25, 47)      # #0A192F
    NAVY_CARD = RGBColor(14, 37, 55)      # #0E2537
    LIGHT_BG = RGBColor(248, 250, 252)    # #F8FAFC
    CARD_BG = RGBColor(241, 245, 249)     # #F1F5F9
    BORDER_COL = RGBColor(203, 213, 225)  # #CBD5E1
    TEXT_DARK = RGBColor(15, 23, 42)      # #0F172A
    TEXT_MUTED = RGBColor(100, 116, 139)  # #64748B
    PRIMARY_CYAN = RGBColor(0, 150, 214)  # #0096D6
    ACCENT_RED = RGBColor(229, 72, 77)    # #E5484D
    ACCENT_GREEN = RGBColor(16, 185, 129) # #10B981
    ACCENT_ORANGE = RGBColor(245, 158, 11)# #F59E0B
    WHITE = RGBColor(255, 255, 255)
    PLACEHOLDER_FILL = RGBColor(234, 242, 250)
    PLACEHOLDER_BORDER = RGBColor(56, 139, 210)

    def add_header(slide, title_text, slide_num):
        # Top Header Banner
        header_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.25), Inches(10.5), Inches(0.6))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = "Calibri"
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = DARK_BLUE

        # NOVACORE Pill Badge top-left
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(0.9), Inches(1.8), Inches(0.35))
        badge.fill.solid()
        badge.fill.fore_color.rgb = DARK_BLUE
        badge.line.color.rgb = DARK_BLUE
        btf = badge.text_frame
        btf.margin_top = btf.margin_bottom = btf.margin_left = btf.margin_right = 0
        bp = btf.paragraphs[0]
        bp.text = "NOVACORE"
        bp.alignment = PP_ALIGN.CENTER
        bp.font.name = "Calibri"
        bp.font.size = Pt(11)
        bp.font.bold = True
        bp.font.color.rgb = WHITE

        # SIH 2026 Logo placeholder / text top-right
        sih_box = slide.shapes.add_textbox(Inches(10.8), Inches(0.25), Inches(2.0), Inches(0.65))
        stf = sih_box.text_frame
        stf.margin_left = stf.margin_top = stf.margin_right = stf.margin_bottom = 0
        sp = stf.paragraphs[0]
        sp.text = "SMART INDIA\nHACKATHON 2026"
        sp.alignment = PP_ALIGN.RIGHT
        sp.font.name = "Calibri"
        sp.font.size = Pt(11)
        sp.font.bold = True
        sp.font.color.rgb = DARK_BLUE

        # Bottom Slide Number Footer
        footer_box = slide.shapes.add_textbox(Inches(0.6), Inches(7.15), Inches(12.13), Inches(0.3))
        ftf = footer_box.text_frame
        ftf.margin_left = ftf.margin_top = ftf.margin_right = ftf.margin_bottom = 0
        fp = ftf.paragraphs[0]
        fp.text = f"@SIH Idea submission - Template | Slide {slide_num}"
        fp.alignment = PP_ALIGN.CENTER
        fp.font.name = "Calibri"
        fp.font.size = Pt(10)
        fp.font.color.rgb = TEXT_MUTED

    def add_placeholder_box(slide, left, top, width, height, title, instruction):
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        box.fill.solid()
        box.fill.fore_color.rgb = PLACEHOLDER_FILL
        box.line.color.rgb = PLACEHOLDER_BORDER
        box.line.width = Pt(1.5)
        
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.2)
        tf.margin_bottom = Inches(0.2)
        
        p = tf.paragraphs[0]
        p.text = f"📷 [PLACE PHOTO HERE]"
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Calibri"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = PRIMARY_CYAN
        
        p2 = tf.add_paragraph()
        p2.text = title
        p2.alignment = PP_ALIGN.CENTER
        p2.font.name = "Calibri"
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = DARK_BLUE
        
        p3 = tf.add_paragraph()
        p3.text = f"👉 Screenshot: {instruction}"
        p3.alignment = PP_ALIGN.CENTER
        p3.font.name = "Calibri"
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)

    # Top SIH Header
    t_box = slide1.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.3), Inches(0.8))
    t_tf = t_box.text_frame
    p = t_tf.paragraphs[0]
    p.text = "SMART INDIA HACKATHON 2026"
    p.font.name = "Calibri"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE

    # Details Left Box
    d_box = slide1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(7.5), Inches(5.0))
    d_tf = d_box.text_frame
    d_tf.word_wrap = True
    
    lines = [
        ("• Problem Statement ID – ", "SIH26191"),
        ("• Problem Statement Title – ", "Intelligent Identification of Hazard-Based Red Zones, Carrying Capacity Assessment, and Immediate Relocation Needs for Vulnerable Habitations."),
        ("• Organization – ", "Ministry of Home Affairs (MHA) / NDRF"),
        ("• Theme – ", "Disaster Management"),
        ("• PS Category – ", "Software"),
        ("• Team ID – ", "170297"),
        ("• Team Name – ", "NOVACORE"),
    ]
    
    for i, (label, val) in enumerate(lines):
        p = d_tf.paragraphs[0] if i == 0 else d_tf.add_paragraph()
        p.space_after = Pt(14)
        run1 = p.add_run()
        run1.text = label
        run1.font.name = "Calibri"
        run1.font.size = Pt(17)
        run1.font.bold = True
        run1.font.color.rgb = DARK_BLUE
        
        run2 = p.add_run()
        run2.text = val
        run2.font.name = "Calibri"
        run2.font.size = Pt(17)
        run2.font.bold = (i in [0, 1, 6])
        run2.font.color.rgb = PRIMARY_CYAN if i in [0, 6] else TEXT_DARK

    # Right Logo/Illustration Card Placeholder
    r_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.8), Inches(3.8), Inches(4.8))
    r_card.fill.solid()
    r_card.fill.fore_color.rgb = CARD_BG
    r_card.line.color.rgb = BORDER_COL
    rtf = r_card.text_frame
    rtf.word_wrap = True
    rtf.margin_top = Inches(0.8)
    rp = rtf.paragraphs[0]
    rp.text = "🛡️ RAKSHASETU (रक्षासेतु)"
    rp.alignment = PP_ALIGN.CENTER
    rp.font.name = "Calibri"
    rp.font.size = Pt(20)
    rp.font.bold = True
    rp.font.color.rgb = DARK_BLUE

    rp2 = rtf.add_paragraph()
    rp2.text = "MHA / NDRF Decision-Support Platform"
    rp2.alignment = PP_ALIGN.CENTER
    rp2.font.name = "Calibri"
    rp2.font.size = Pt(12)
    rp2.font.color.rgb = PRIMARY_CYAN
    rp2.space_after = Pt(14)

    rp3 = rtf.add_paragraph()
    rp3.text = "📷 [PLACE SIH LOGO / TEAM LOGO HERE]"
    rp3.alignment = PP_ALIGN.CENTER
    rp3.font.name = "Calibri"
    rp3.font.size = Pt(11)
    rp3.font.bold = True
    rp3.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 2: PROPOSED SOLUTION
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "PROPOSED SOLUTION: RAKSHASETU (AI-GIS Disaster Decision Platform)", 2)

    # Left Column: 3 Pillar Feature Cards
    card_w = Inches(5.8)
    left_x = Inches(0.6)
    
    # Pillar 1: Red Zones
    c1 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, Inches(1.4), card_w, Inches(1.75))
    c1.fill.solid()
    c1.fill.fore_color.rgb = WHITE
    c1.line.color.rgb = ACCENT_RED
    c1.line.width = Pt(1.5)
    tf1 = c1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = Inches(0.12)
    p = tf1.paragraphs[0]
    p.text = "🔴 1. Dynamic Hazard-Based Red-Zone Delineation"
    p.font.name = "Calibri"
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_RED
    
    b_items1 = [
        "Identifies zones Unsuitable for Permanent Habitation via live multi-hazard feeds.",
        "4 Explicit Hazard Models: Floods, Landslides, Coastal Erosion, and Cloudbursts.",
        "GIS Animated Buffers: Pulsating blowout rings pinpoint danger perimeter on map.",
    ]
    for bi in b_items1:
        bp = tf1.add_paragraph()
        bp.text = f" {bi}"
        bp.font.name = "Calibri"
        bp.font.size = Pt(9.5)
        bp.font.color.rgb = TEXT_DARK

    # Pillar 2: 3-Tier Relocation Needs
    c2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, Inches(3.25), card_w, Inches(1.75))
    c2.fill.solid()
    c2.fill.fore_color.rgb = WHITE
    c2.line.color.rgb = PRIMARY_CYAN
    c2.line.width = Pt(1.5)
    tf2 = c2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = tf2.margin_top = tf2.margin_bottom = Inches(0.12)
    p = tf2.paragraphs[0]
    p.text = "⏱️ 2. 3-Tier Relocation Need Prioritization (Immediate to Long-Term)"
    p.font.name = "Calibri"
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_CYAN
    
    b_items2 = [
        "🔴 Immediate (0–48 Hours): Rapid tactical evacuation for acute life-threats.",
        "🟠 Short-Term (1–3 Months): Pre-monsoon planned relocation before floods/slides.",
        "🟡 Medium-Term (6–12 Months): Sustainable rehabilitation & permanent housing.",
    ]
    for bi in b_items2:
        bp = tf2.add_paragraph()
        bp.text = f" {bi}"
        bp.font.name = "Calibri"
        bp.font.size = Pt(9.5)
        bp.font.color.rgb = TEXT_DARK

    # Pillar 3: Carrying Capacity & Zero Cost
    c3 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, Inches(5.1), card_w, Inches(1.75))
    c3.fill.solid()
    c3.fill.fore_color.rgb = WHITE
    c3.line.color.rgb = ACCENT_GREEN
    c3.line.width = Pt(1.5)
    tf3 = c3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = tf3.margin_right = tf3.margin_top = tf3.margin_bottom = Inches(0.12)
    p = tf3.paragraphs[0]
    p.text = "🏢 3. Carrying Capacity Assessment & Overcrowding Mitigation"
    p.font.name = "Calibri"
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    
    b_items3 = [
        "Evaluates Total Capacity, Pre-Occupancy, and Net Absorption Headroom.",
        "Automated Multi-Site Split: Prevents secondary disaster outbreak when stress >85%.",
        "100% Zero Operating Cost: Powered by free open-source data (Open-Meteo, USGS, OSM).",
    ]
    for bi in b_items3:
        bp = tf3.add_paragraph()
        bp.text = f" {bi}"
        bp.font.name = "Calibri"
        bp.font.size = Pt(9.5)
        bp.font.color.rgb = TEXT_DARK

    # Right Column: Project Links Box + 2 Photo Placeholders
    right_x = Inches(6.7)
    right_w = Inches(6.0)

    # Links Box
    lbox = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x, Inches(1.4), right_w, Inches(0.85))
    lbox.fill.solid()
    lbox.fill.fore_color.rgb = NAVY_CARD
    lbox.line.color.rgb = DARK_BLUE
    ltf = lbox.text_frame
    ltf.margin_top = Inches(0.08)
    lp = ltf.paragraphs[0]
    lp.text = "🔗 PROJECT REPOSITORY & LIVE LINKS (Click to Open):"
    lp.font.name = "Calibri"
    lp.font.size = Pt(11)
    lp.font.bold = True
    lp.font.color.rgb = PRIMARY_CYAN
    
    lp2 = ltf.add_paragraph()
    lp2.text = "• GitHub Code Repository: https://github.com/vinitmishraaa/RAKSHASETU"
    lp2.font.name = "Calibri"
    lp2.font.size = Pt(9.5)
    lp2.font.color.rgb = WHITE
    
    lp3 = ltf.add_paragraph()
    lp3.text = "• Live Web Dashboard: http://localhost:5173  |  SIH PS-26191"
    lp3.font.name = "Calibri"
    lp3.font.size = Pt(9.5)
    lp3.font.color.rgb = WHITE

    # Photo Placeholder 1: Main GIS Map
    add_placeholder_box(
        slide2, right_x, Inches(2.35), right_w, Inches(2.25),
        "Main Dashboard: Multi-Hazard Red-Zone GIS Map",
        "Take screenshot of your Home Dashboard showing the map, West Bengal state-district cascade, pulsating red blowout rings, and safe shelters."
    )

    # Photo Placeholder 2: Carrying Capacity Stress Meter
    add_placeholder_box(
        slide2, right_x, Inches(4.7), right_w, Inches(2.15),
        "Carrying Capacity Assessment & Stress Gauge Card",
        "Take screenshot of Relocation or SafeSites page showing the carrying capacity progress bar (headroom slots, stress %, and absorption metrics)."
    )

    # =========================================================================
    # SLIDE 3: TECHNICAL APPROACH
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "TECHNICAL APPROACH: End-to-End System Workflow & Architecture", 3)

    # 5 Step Horizontal Flow Boxes across the top
    steps = [
        ("Step 1: Ingest", "Live Open Telemetry\n• Open-Meteo (Rain/Wind)\n• USGS (Seismology)\n• NDMA SACHET CAP"),
        ("Step 2: Engine", "3-Pillar Risk Engine\n• Hazard Intensity (40%)\n• Vulnerability (35%)\n• Disaster History (25%)"),
        ("Step 3: Red Zones", "Red-Zone Delineation\n• Multi-hazard unsuitability\n• 4 Hazards: Flood, Slide,\n  Erosion, Cloudburst"),
        ("Step 4: Safe Sites", "Capacity Assessment\n• Headroom & stress %\n• Overcrowding split\n• OSRM road routing"),
        ("Step 5: Action", "SDMA Action Corridor\n• 4-Step guided flow\n• Google Maps driving\n• 🖨️ Printable brief"),
    ]
    step_w = Inches(2.3)
    step_gap = Inches(0.15)
    top_y = Inches(1.4)
    
    for i, (stitle, sdesc) in enumerate(steps):
        sx = Inches(0.6) + i * (step_w + step_gap)
        sbox = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sx, top_y, step_w, Inches(1.45))
        sbox.fill.solid()
        sbox.fill.fore_color.rgb = WHITE
        sbox.line.color.rgb = PRIMARY_CYAN if i % 2 == 0 else ACCENT_RED
        sbox.line.width = Pt(1.5)
        stf = sbox.text_frame
        stf.margin_left = stf.margin_right = stf.margin_top = stf.margin_bottom = Inches(0.08)
        sp1 = stf.paragraphs[0]
        sp1.text = stitle
        sp1.font.name = "Calibri"
        sp1.font.size = Pt(11)
        sp1.font.bold = True
        sp1.font.color.rgb = DARK_BLUE
        
        sp2 = stf.add_paragraph()
        sp2.text = sdesc
        sp2.font.name = "Calibri"
        sp2.font.size = Pt(8.5)
        sp2.font.color.rgb = TEXT_DARK

    # Bottom Left: Tech Stack & Features
    t_card = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(3.0), Inches(5.8), Inches(3.85))
    t_card.fill.solid()
    t_card.fill.fore_color.rgb = WHITE
    t_card.line.color.rgb = BORDER_COL
    tt_tf = t_card.text_frame
    tt_tf.margin_left = tt_tf.margin_right = tt_tf.margin_top = tt_tf.margin_bottom = Inches(0.14)
    tp = tt_tf.paragraphs[0]
    tp.text = "💻 TECHNOLOGY STACK & SMART CAPABILITIES:"
    tp.font.name = "Calibri"
    tp.font.size = Pt(13)
    tp.font.bold = True
    tp.font.color.rgb = DARK_BLUE
    
    tech_bullets = [
        "Frontend: React 18, TypeScript, Vite, Leaflet.js, Recharts, Custom Glassmorphism UI.",
        "Backend & Optimization: Python 3.12, FastAPI, In-Memory Administrative Directory (36 States/UTs).",
        "Road Network Routing: Open Source Routing Machine (OSRM) driving route geometry & live ETA.",
        "Multi-Hazard Risk Engine: Real-time calculation integrating Floods, Landslides, Coastal Erosion, and Cloudbursts.",
        "Disaster History Recurrence: Historical incident penalty directly elevates chronic hazard scores.",
        "SDMA Action Suite: 4-step guided evacuation corridor, turn-by-turn driver instructions, and official order export.",
        "GitHub Link: https://github.com/vinitmishraaa/RAKSHASETU",
    ]
    for tb in tech_bullets:
        tbp = tt_tf.add_paragraph()
        tbp.text = f"• {tb}"
        tbp.font.name = "Calibri"
        tbp.font.size = Pt(9.5)
        tbp.font.color.rgb = TEXT_DARK

    # Bottom Right: 2 Screenshot Placeholders
    add_placeholder_box(
        slide3, Inches(6.7), Inches(3.0), Inches(6.0), Inches(1.85),
        "4-Step Guided Relocation Corridor & OSRM Route",
        "Take screenshot of Relocation page showing Step 1 to Step 4, road distance, ETA, and turn-by-turn road instructions."
    )
    add_placeholder_box(
        slide3, Inches(6.7), Inches(4.95), Inches(6.0), Inches(1.9),
        "Official SDMA Relocation Order Print Preview",
        "Click 'Print SDMA Action Brief' on Relocation page and take screenshot of the print-ready official evacuation order."
    )

    # =========================================================================
    # SLIDE 4: FEASIBILITY AND VIABILITY
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "FEASIBILITY & VIABILITY: Operational & Comparative Assessment", 4)

    # Comparison Table on Left
    table_shape = slide4.shapes.add_table(6, 4, Inches(0.6), Inches(1.4), Inches(7.0), Inches(3.3))
    table = table_shape.table
    table.columns[0].width = Inches(1.6)
    table.columns[1].width = Inches(1.8)
    table.columns[2].width = Inches(2.0)
    table.columns[3].width = Inches(1.6)

    table_data = [
        ["Operational Dimension", "Traditional Reactive Method", "RakshaSetu Proactive AI-GIS", "Key Advantage"],
        ["Response Timing", "Post-disaster rescue (Panic & delay)", "Proactive pre-disaster tiers (0-48h, 1-3m, 6-12m)", "Zero panic & loss"],
        ["Hazard Delineation", "Manual, localized post-event survey", "Dynamic GIS Multi-Hazard Red-Zone mapping", "High precision"],
        ["Safe Site Allocation", "Ad-hoc intake (Severe overcrowding)", "Carrying capacity headroom stress % analysis", "Prevents stampede"],
        ["Evacuation Routing", "Unverified paths (often blocked)", "OSRM real road network & Google Maps handoff", "Guaranteed ETA"],
        ["Financial Cost", "Expensive proprietary GIS licenses", "100% Open-source zero-key architecture", "₹0 Software Bills"],
    ]

    for row_idx, row in enumerate(table_data):
        for col_idx, cell_value in enumerate(row):
            cell = table.cell(row_idx, col_idx)
            cell.text = cell_value
            cp = cell.text_frame.paragraphs[0]
            cp.font.name = "Calibri"
            cp.font.size = Pt(8.5 if row_idx > 0 else 9.5)
            cp.font.bold = (row_idx == 0 or col_idx == 0)
            if row_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = DARK_BLUE
                cp.font.color.rgb = WHITE
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = WHITE if row_idx % 2 == 0 else CARD_BG
                cp.font.color.rgb = TEXT_DARK

    # Bottom Left: 3 Reasons Box
    rbox = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(4.85), Inches(7.0), Inches(2.0))
    rbox.fill.solid()
    rbox.fill.fore_color.rgb = WHITE
    rbox.line.color.rgb = ACCENT_ORANGE
    rbox.line.width = Pt(1.5)
    rtf = rbox.text_frame
    rtf.margin_left = rtf.margin_right = rtf.margin_top = rtf.margin_bottom = Inches(0.12)
    rp = rtf.paragraphs[0]
    rp.text = "🎯 3 REASONS WHY RAKSHASETU IS 100% FEASIBLE & VIABLE:"
    rp.font.name = "Calibri"
    rp.font.size = Pt(11.5)
    rp.font.bold = True
    rp.font.color.rgb = ACCENT_ORANGE
    
    reasons = [
        "Zero Key Operating Cost: Relies on public Open-Meteo, USGS, NDMA CAP and OpenStreetMap with no cloud bills.",
        "Deterministic & Explainable AI: Formulated on clear mathematical equations (40% Hazard, 35% Vulnerability, 25% History) avoiding black-box errors.",
        "Pan-India Immediate Deployment: All 28 States and 8 UTs pre-indexed; instantly scalable to every SDMA and DDMA.",
    ]
    for r in reasons:
        rr = rtf.add_paragraph()
        rr.text = f" {r}"
        rr.font.name = "Calibri"
        rr.font.size = Pt(9.0)
        rr.font.color.rgb = TEXT_DARK

    # Right: Photo Placeholders
    add_placeholder_box(
        slide4, Inches(7.8), Inches(1.4), Inches(4.9), Inches(2.6),
        "Safe Sites Infrastructure & Headroom Stress Meter",
        "Take screenshot of the Safe Sites page showing multiple shelter cards with occupancy %, absorption headroom, and verified facilities."
    )
    add_placeholder_box(
        slide4, Inches(7.8), Inches(4.15), Inches(4.9), Inches(2.7),
        "Multi-Site Split Allocation to Prevent Overcrowding",
        "Take screenshot showing the Relocation page recommendation when high population is allocated safely across shelters."
    )

    # =========================================================================
    # SLIDE 5: IMPACT AND BENEFITS
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "IMPACT & BENEFITS: Saving Lives, Preventing Overcrowding & Empowering SDMA", 5)

    # Left Column: 3 Impact Cards
    card_w5 = Inches(5.8)
    
    # Impact 1
    im1 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.4), card_w5, Inches(1.2))
    im1.fill.solid()
    im1.fill.fore_color.rgb = WHITE
    im1.line.color.rgb = ACCENT_RED
    itf1 = im1.text_frame
    itf1.margin_left = itf1.margin_right = itf1.margin_top = itf1.margin_bottom = Inches(0.1)
    ip1 = itf1.paragraphs[0]
    ip1.text = "🛡️ 1. Life & Infrastructure Protection (Shifting Reactive to Proactive)"
    ip1.font.name = "Calibri"
    ip1.font.size = Pt(11.5)
    ip1.font.bold = True
    ip1.font.color.rgb = ACCENT_RED
    ib1 = itf1.add_paragraph()
    ib1.text = "Eliminates repeated loss of life and property in perennial flood, landslide, erosion, and cloudburst belts by moving vulnerable habitations BEFORE disaster strikes."
    ib1.font.name = "Calibri"
    ib1.font.size = Pt(9.0)
    ib1.font.color.rgb = TEXT_DARK

    # Impact 2
    im2 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(2.7), card_w5, Inches(1.2))
    im2.fill.solid()
    im2.fill.fore_color.rgb = WHITE
    im2.line.color.rgb = PRIMARY_CYAN
    itf2 = im2.text_frame
    itf2.margin_left = itf2.margin_right = itf2.margin_top = itf2.margin_bottom = Inches(0.1)
    ip2 = itf2.paragraphs[0]
    ip2.text = "🏢 2. Prevention of Secondary Disasters & Post-Evacuation Overcrowding"
    ip2.font.name = "Calibri"
    ip2.font.size = Pt(11.5)
    ip2.font.bold = True
    ip2.font.color.rgb = PRIMARY_CYAN
    ib2 = itf2.add_paragraph()
    ib2.text = "Mathematical carrying capacity assessment caps intake at safe thresholds, preventing sanitation collapse, epidemic outbreaks, and resource exhaustion at relief centres."
    ib2.font.name = "Calibri"
    ib2.font.size = Pt(9.0)
    ib2.font.color.rgb = TEXT_DARK

    # Impact 3
    im3 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(4.0), card_w5, Inches(1.2))
    im3.fill.solid()
    im3.fill.fore_color.rgb = WHITE
    im3.line.color.rgb = ACCENT_GREEN
    itf3 = im3.text_frame
    itf3.margin_left = itf3.margin_right = itf3.margin_top = itf3.margin_bottom = Inches(0.1)
    ip3 = itf3.paragraphs[0]
    ip3.text = "📋 3. Empowering SDMA, DDMA & Incident Commanders with Action Orders"
    ip3.font.name = "Calibri"
    ip3.font.size = Pt(11.5)
    ip3.font.bold = True
    ip3.font.color.rgb = ACCENT_GREEN
    ib3 = itf3.add_paragraph()
    ib3.text = "Generates signed official relocation briefs, driver turn-by-turn routes, and automated SMS/Email alert dispatch to pre-configured disaster response officers."
    ib3.font.name = "Calibri"
    ib3.font.size = Pt(9.0)
    ib3.font.color.rgb = TEXT_DARK

    # Proved Measurable Results Box
    pbox = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(5.3), card_w5, Inches(1.55))
    pbox.fill.solid()
    pbox.fill.fore_color.rgb = NAVY_CARD
    pbox.line.color.rgb = DARK_BLUE
    ptf = pbox.text_frame
    ptf.margin_left = ptf.margin_right = ptf.margin_top = ptf.margin_bottom = Inches(0.1)
    pp = ptf.paragraphs[0]
    pp.text = "📊 PROVED MEASURABLE OUTCOMES (Per Vulnerable District):"
    pp.font.name = "Calibri"
    pp.font.size = Pt(11)
    pp.font.bold = True
    pp.font.color.rgb = PRIMARY_CYAN
    
    outcomes = [
        "0–48 Hours Evacuation Window: Immediate alerts for high-risk red-zone communities.",
        "85% Carrying Capacity Threshold: Triggers multi-site diversion to protect shelter safety.",
        "100% Open Data Transparency: Zero recurring software or mapping license burden.",
        "36 States & UTs Pre-Indexed: Ready for instant pan-India adoption by NDRF / MHA.",
    ]
    for o in outcomes:
        op = ptf.add_paragraph()
        op.text = f"• {o}"
        op.font.name = "Calibri"
        op.font.size = Pt(8.5)
        op.font.color.rgb = WHITE

    # Right Column: 2 Screenshot Placeholders
    add_placeholder_box(
        slide5, Inches(6.7), Inches(1.4), Inches(6.0), Inches(2.65),
        "Recharts Live Analytics: 3-Tier Distribution & 4-Hazard Profile",
        "Take screenshot of the Analytics page showing the 3-Tier Relocation Need Pie Chart, 4-Hazard Bar Chart, and Red Zone habitant KPI stats."
    )
    add_placeholder_box(
        slide5, Inches(6.7), Inches(4.2), Inches(6.0), Inches(2.65),
        "Officer Alert Desk & Dual-Tone Emergency Siren Tester",
        "Take screenshot of the Alerts page showing the 5 designated response officers (email/sms triggers) and the interactive 'TEST SIREN' button."
    )

    # =========================================================================
    # SLIDE 6: RESEARCH, PROJECT LINKS & FUTURE ROADMAP
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "RESEARCH, PROJECT LINKS & FUTURE ROADMAP", 6)

    # Top Links Box
    top_links = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.4), Inches(12.13), Inches(0.9))
    top_links.fill.solid()
    top_links.fill.fore_color.rgb = WHITE
    top_links.line.color.rgb = PRIMARY_CYAN
    top_links.line.width = Pt(1.5)
    tltf = top_links.text_frame
    tltf.margin_top = Inches(0.08)
    tlp = tltf.paragraphs[0]
    tlp.text = "📱 OFFICIAL PROJECT DELIVERABLES & REPOSITORIES:"
    tlp.font.name = "Calibri"
    tlp.font.size = Pt(12)
    tlp.font.bold = True
    tlp.font.color.rgb = PRIMARY_CYAN
    
    tlp2 = tltf.add_paragraph()
    tlp2.text = "• GitHub Code Repository: https://github.com/vinitmishraaa/RAKSHASETU  |  Branch: main (Tested & Verified)"
    tlp2.font.name = "Calibri"
    tlp2.font.size = Pt(10)
    tlp2.font.color.rgb = TEXT_DARK

    tlp3 = tltf.add_paragraph()
    tlp3.text = "• Local Command Center: http://localhost:5173  |  FastAPI Backend REST Endpoints: http://127.0.0.1:8000/docs"
    tlp3.font.name = "Calibri"
    tlp3.font.size = Pt(10)
    tlp3.font.color.rgb = TEXT_DARK

    # 3 Columns for Sources
    col_w = Inches(3.9)
    col_gap = Inches(0.2)
    
    # Col 1: Government Sources
    c1 = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(2.45), col_w, Inches(3.4))
    c1.fill.solid()
    c1.fill.fore_color.rgb = WHITE
    c1.line.color.rgb = DARK_BLUE
    c1tf = c1.text_frame
    c1tf.margin_left = c1tf.margin_right = c1tf.margin_top = c1tf.margin_bottom = Inches(0.12)
    cp1 = c1tf.paragraphs[0]
    cp1.text = "🏛️ Official Government Sources"
    cp1.font.name = "Calibri"
    cp1.font.size = Pt(12)
    cp1.font.bold = True
    cp1.font.color.rgb = DARK_BLUE
    
    gov_sources = [
        ("Ministry of Home Affairs (MHA)", "https://mha.gov.in"),
        ("National Disaster Response Force (NDRF)", "https://ndrf.gov.in"),
        ("NDMA SACHET (CAP Early Warning)", "https://sachet.ndma.gov.in"),
        ("India Meteorological Department (IMD)", "https://mausam.imd.gov.in"),
        ("Geological Survey of India (GSI - Landslides)", "https://gsi.gov.in"),
        ("Central Water Commission (CWC - Floods)", "https://cwc.gov.in"),
        ("Census of India (Village Demographics)", "https://censusindia.gov.in"),
    ]
    for name, url in gov_sources:
        p = c1tf.add_paragraph()
        p.text = f"• {name}\n  {url}"
        p.font.name = "Calibri"
        p.font.size = Pt(8.0)
        p.font.color.rgb = TEXT_MUTED

    # Col 2: Open / Technical Sources
    c2 = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6) + col_w + col_gap, Inches(2.45), col_w, Inches(3.4))
    c2.fill.solid()
    c2.fill.fore_color.rgb = WHITE
    c2.line.color.rgb = PRIMARY_CYAN
    c2tf = c2.text_frame
    c2tf.margin_left = c2tf.margin_right = c2tf.margin_top = c2tf.margin_bottom = Inches(0.12)
    cp2 = c2tf.paragraphs[0]
    cp2.text = "🌐 Open Technical Data Sources"
    cp2.font.name = "Calibri"
    cp2.font.size = Pt(12)
    cp2.font.bold = True
    cp2.font.color.rgb = PRIMARY_CYAN
    
    tech_sources = [
        ("Open-Meteo API (Live Weather & Wind)", "https://open-meteo.com"),
        ("USGS Seismology (Earthquake Hypocenters)", "https://earthquake.usgs.gov"),
        ("OpenStreetMap (Roads & Critical Buildings)", "https://openstreetmap.org"),
        ("OSRM Project (Road Routing Engine)", "http://project-osrm.org"),
        ("GDACS (Global Disaster Alert & Coordination)", "https://gdacs.org"),
        ("NASA GIBS (Satellite True-Color Imagery)", "https://earthdata.nasa.gov"),
        ("Leaflet.js & Recharts (Visualization)", "https://leafletjs.com"),
    ]
    for name, url in tech_sources:
        p = c2tf.add_paragraph()
        p.text = f"• {name}\n  {url}"
        p.font.name = "Calibri"
        p.font.size = Pt(8.0)
        p.font.color.rgb = TEXT_MUTED

    # Col 3: Research & Development Sources
    c3 = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6) + 2 * (col_w + col_gap), Inches(2.45), col_w, Inches(3.4))
    c3.fill.solid()
    c3.fill.fore_color.rgb = WHITE
    c3.line.color.rgb = ACCENT_RED
    c3tf = c3.text_frame
    c3tf.margin_left = c3tf.margin_right = c3tf.margin_top = c3tf.margin_bottom = Inches(0.12)
    cp3 = c3tf.paragraphs[0]
    cp3.text = "📚 Research & Standards"
    cp3.font.name = "Calibri"
    cp3.font.size = Pt(12)
    cp3.font.bold = True
    cp3.font.color.rgb = ACCENT_RED
    
    res_sources = [
        ("UNDRR Sendai Framework 2015–2030", "Target 4: Disaster Resilient Infrastructure"),
        ("IPCC AR6 Vulnerability Guidelines", "Climate-induced resettlement standards"),
        ("Smart India Hackathon 2026 Portal", "Problem Statement ID: SIH26191"),
        ("NDMA SOP on Disaster Relocation", "Standard capacity allocations per person"),
        ("Team NOVACORE Research Paper", "Proactive GIS Carrying Capacity Models"),
        ("Open Source MIT License", "Fully libre software for public good"),
    ]
    for name, desc in res_sources:
        p = c3tf.add_paragraph()
        p.text = f"• {name}\n  {desc}"
        p.font.name = "Calibri"
        p.font.size = Pt(8.0)
        p.font.color.rgb = TEXT_MUTED

    # Bottom Banner: How these references ground our solution
    bot_banner = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(6.0), Inches(12.13), Inches(0.95))
    bot_banner.fill.solid()
    bot_banner.fill.fore_color.rgb = CARD_BG
    bot_banner.line.color.rgb = BORDER_COL
    btf = bot_banner.text_frame
    btf.margin_top = Inches(0.08)
    bp = btf.paragraphs[0]
    bp.text = "🌟 HOW THESE SCIENTIFIC & TECHNICAL REFERENCES VALIDATE RAKSHASETU:"
    bp.font.name = "Calibri"
    bp.font.size = Pt(10.5)
    bp.font.bold = True
    bp.font.color.rgb = DARK_BLUE
    
    bp2 = btf.add_paragraph()
    bp2.text = "✅ Reliable Open Data: Official government and live sensor feeds ensure real-time hazard detection without manual delay.\n✅ Proven Mathematical Methodology: 3-Pillar risk formula and carrying capacity headroom calculations ensure zero subjective bias.\n✅ Immediate Administrative Adoption: Structured to fit directly into SDMA / DDMA standard operating procedures for MHA / NDRF."
    bp2.font.name = "Calibri"
    bp2.font.size = Pt(8.5)
    bp2.font.color.rgb = TEXT_DARK

    # Save presentation
    output_path = r"D:\sih\rakshasetu\rakshasetu\RAKSHASETU_SIH26191_Presentation.pptx"
    prs.save(output_path)
    print(f"Successfully generated presentation at: {output_path}")

if __name__ == "__main__":
    create_presentation()
