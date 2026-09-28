#!/usr/bin/env python3
"""
Compiles an Executive Master PDF Playbook for Short-Form Video Script Architecture.
Uses ReportLab to create vector-rendered A4 typography and structured AV tables.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm

def create_playbook_pdf(output_path="short_form_script_engineering_playbook.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Brand Palette
    c_primary = colors.HexColor("#1E1B4B")     # Deep Indigo
    c_accent = colors.HexColor("#4F46E5")      # Vibrant Indigo
    c_dark = colors.HexColor("#0F172A")        # Slate 900
    c_muted = colors.HexColor("#475569")       # Slate 600
    c_light_bg = colors.HexColor("#F8FAFC")    # Slate 50
    c_border = colors.HexColor("#E2E8F0")      # Slate 200
    c_gold = colors.HexColor("#B45309")        # Amber 700

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_primary,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=c_muted,
        spaceAfter=14
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_accent,
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_dark
    )

    cell_bold = ParagraphStyle(
        'CellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=c_primary
    )

    cell_normal = ParagraphStyle(
        'CellNormal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_dark
    )

    cell_muted = ParagraphStyle(
        'CellMuted',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.5,
        leading=10,
        textColor=c_muted
    )

    story = []

    # Title & Metadata Header
    story.append(Paragraph("SHORT-FORM SCRIPT ARCHITECTURE & 60S RETENTION BLUEPRINT", title_style))
    story.append(Paragraph("Unified Audio-Visual (AV) Production Specification, WPM Telemetry & Cognitive Pacing Framework", subtitle_style))
    story.append(Spacer(1, 4))

    # Specification Matrix
    spec_data = [
        [Paragraph("<b>Author / Lead Architect</b>", cell_bold), Paragraph("Muhammad Khoiruzzadittaqwa (Zadit) - PT Prisma Digital Kreatif", cell_normal)],
        [Paragraph("<b>Target Channels</b>", cell_bold), Paragraph("TikTok, Instagram Reels, YouTube Shorts (Vertical 9:16)", cell_normal)],
        [Paragraph("<b>Duration & Word Limits</b>", cell_bold), Paragraph("Max 60 Seconds | 130 - 145 Spoken Words (135-150 WPM Natural Pace)", cell_normal)],
        [Paragraph("<b>Visual Reset Protocol</b>", cell_bold), Paragraph("Max 4.0 Seconds interval per B-roll, camera reframing, or text cue", cell_normal)],
        [Paragraph("<b>Theoretical Grounding</b>", cell_bold), Paragraph("Cognitive Load Theory (Sweller), Dual Coding (Paivio), ACL ScriptWriter (DaoD et al.)", cell_normal)],
    ]
    t_spec = Table(spec_data, colWidths=[140, 380])
    t_spec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_light_bg),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_spec)
    story.append(Spacer(1, 12))

    # Section 1: The 60-Second Retention Timeline
    story.append(Paragraph("1. The 6-Beat Retention Timeline Architecture", h2_style))
    story.append(Paragraph("Every high-performing 60-second vertical video adheres to six deterministic cognitive milestones. Violating this timeline triggers immediate swipe-away actions:", body_style))
    story.append(Spacer(1, 6))

    timeline_data = [
        [Paragraph("Timeline", cell_bold), Paragraph("Narrative Milestone", cell_bold), Paragraph("Cognitive Mechanism", cell_bold), Paragraph("Production Execution Target", cell_bold)],
        [
            Paragraph("00:00 - 00:03", cell_bold),
            Paragraph("<b>Pattern Interrupt Hook</b>", cell_normal),
            Paragraph("System 1 heuristic appraisal; breaks habitual scrolling inertia.", cell_muted),
            Paragraph("Visually provocative gesture + direct accusation or paradox.", cell_normal)
        ],
        [
            Paragraph("00:04 - 00:15", cell_bold),
            Paragraph("<b>Agitation & Loss Aversion</b>", cell_normal),
            Paragraph("Validates viewer struggle; introduces tangible cost of inaction.", cell_muted),
            Paragraph("Screen recording of failure, red warning stats, fast cut.", cell_normal)
        ],
        [
            Paragraph("00:16 - 00:25", cell_bold),
            Paragraph("<b>The Re-Hook Inflection</b>", cell_normal),
            Paragraph("Resets dopamine decay right at the 20-second retention drop.", cell_muted),
            Paragraph("Angle shift / overhead shot + 'Aturan 4 Detik' bold text.", cell_normal)
        ],
        [
            Paragraph("00:26 - 00:44", cell_bold),
            Paragraph("<b>High-Density Solution</b>", cell_normal),
            Paragraph("Cognitive clarity; Paivio's dual coding (audio + matching text).", cell_muted),
            Paragraph("3-part bulleted takeaway, 1 idea per sentence, zero filler.", cell_normal)
        ],
        [
            Paragraph("00:45 - 00:54", cell_bold),
            Paragraph("<b>Proof & Payoff</b>", cell_normal),
            Paragraph("Validates the premise; resolves narrative tension.", cell_muted),
            Paragraph("Inspectable master template preview, clean final artifact.", cell_normal)
        ],
        [
            Paragraph("00:55 - 01:00", cell_bold),
            Paragraph("<b>Seamless Loop CTA</b>", cell_normal),
            Paragraph("Micro-action trigger; loop phrase bridges back to 00:00.", cell_muted),
            Paragraph("Incomplete bridge phrase ('...karena') driving >100% loop.", cell_normal)
        ],
    ]
    t_timeline = Table(timeline_data, colWidths=[65, 120, 160, 175])
    t_timeline.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EEF2F6")),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_timeline)
    story.append(Spacer(1, 14))

    # Section 2: Turnkey AV Production Script
    story.append(Paragraph("2. Turnkey AV Production Master Script (Case Study Implementation)", h2_style))
    story.append(Paragraph("Script Title: <b>Stop Wasting Your First 3 Seconds</b> | Target Time: 60s | Spoken Words: 138 | Visual Cuts: 12", body_style))
    story.append(Spacer(1, 6))

    script_data = [
        [Paragraph("Timecode", cell_bold), Paragraph("Visual & B-Roll Cue (Editor)", cell_bold), Paragraph("Spoken Audio & Voiceover (Talent)", cell_bold), Paragraph("SFX & Mood", cell_bold)],
        [
            Paragraph("00:00-00:03", cell_bold),
            Paragraph("Medium close-up. Talent stares intensely at camera holding empty jar upside down. Snap zoom + bold text: <i>'STOP BUANG 60 DETIK LO'</i>.", cell_normal),
            Paragraph("\"90% video pendek gagal bukan karena visualnya buram, tapi karena scriptnya kelamaan basa-basi di 3 detik awal.\"", cell_normal),
            Paragraph("Sub-bass drop + glass impact", cell_muted)
        ],
        [
            Paragraph("00:04-00:14", cell_bold),
            Paragraph("Split screen. Left: talking head video. Right: analytics graph showing retention cliff drop at 00:03.", cell_normal),
            Paragraph("\"Begitu lo buka dengan kalimat 'Hai guys balik lagi sama gue', 70 persen jempol penonton udah geser ke video orang lain.\"", cell_normal),
            Paragraph("Vinyl scratch + whoosh", cell_muted)
        ],
        [
            Paragraph("00:15-00:25", cell_bold),
            Paragraph("Overhead desk angle. Hand circles digital timer at 4.0s. High contrast title: <i>'ATURAN 4 DETIK'</i>.", cell_normal),
            Paragraph("\"Rahasianya ada di aturan 4 detik. Otak manusia di mobile feed butuh kejutan visual baru setiap 4 detik sebelum dopaminnya turun.\"", cell_normal),
            Paragraph("Mechanical ticking riser", cell_muted)
        ],
        [
            Paragraph("00:26-00:44", cell_bold),
            Paragraph("Three-part graphical stack slides in synchronously with speech cadence: 1. Action Hook, 2. Contrarian Data, 3. Micro-Payoff.", cell_normal),
            Paragraph("\"Bagi naskah lo jadi dua kolom: apa yang didengar talent, dan apa yang dilihat editor. Jangan biarkan talent ngomong tanpa ada B-roll pendukung atau teks penegas.\"", cell_normal),
            Paragraph("Typewriter tick per bullet", cell_muted)
        ],
        [
            Paragraph("00:45-00:54", cell_bold),
            Paragraph("Full-screen AV script table preview showing color-coded columns for talent and editor.", cell_normal),
            Paragraph("\"Dengan format ini, video 60 detik lo bukan cuma ditonton sampai tuntas, tapi memandu editor motong klip dengan presisi frame.\"", cell_normal),
            Paragraph("Clean bell chime", cell_muted)
        ],
        [
            Paragraph("00:55-01:00", cell_bold),
            Paragraph("Talent points down. Prompt sticker: <i>'Simpan buat syuting besok'</i>. Quick snap back to opening frame.", cell_normal),
            Paragraph("\"Simpan video ini buat acuan syuting lo besok, karena...\"", cell_normal),
            Paragraph("Whoosh loop to start", cell_muted)
        ],
    ]

    t_script = Table(script_data, colWidths=[65, 175, 205, 75])
    t_script.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EEF2F6")),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_script)
    story.append(Spacer(1, 14))

    # Footer note
    story.append(Paragraph("Direct Inquiries & Architecture Review: <b>devapenseo@gmail.com</b> | Live Prototype: <b>zadevpenseo.github.io/demos/short-form-script-engine/</b>", cell_muted))

    doc.build(story)
    print(f"Master PDF compiled successfully: {output_path}")

if __name__ == "__main__":
    create_playbook_pdf()
