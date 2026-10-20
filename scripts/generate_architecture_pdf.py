"""
Generates the official Architecture Diagram PDF:
docs/Architecture_Diagram.pdf
for Happiest Health Digital Twin Challenge 2026.
"""

import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def build_pdf():
    os.makedirs("docs", exist_ok=True)
    pdf_path = os.path.join("docs", "Architecture_Diagram.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=landscape(letter),
        leftMargin=36,
        rightMargin=36,
        topMargin=32,
        bottomMargin=32
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'ArchTitle',
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#0F172A"),
        alignment=1,
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'ArchSubtitle',
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#0284C7"),
        alignment=1,
        spaceAfter=20
    )
    col_head = ParagraphStyle(
        'ColHead',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#0F172A"),
        alignment=1
    )
    card_body = ParagraphStyle(
        'CardBody',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155")
    )

    story = []
    story.append(Paragraph("🫁 PulmoTwin System Architecture Diagram", title_style))
    story.append(Paragraph("Multimodal Cardiopulmonary Digital Twin: Continuous Ingestion, Dynamic Simulation, Safety Rails & Clinical Decision Support", subtitle_style))

    # Architecture Columns (5 stages)
    stage1 = Paragraph(
        "<b>1. MULTIMODAL INGESTION</b><br/><br/>"
        "• <b>Longitudinal EHR (ABDM / FHIR R4)</b><br/>"
        "  - Baseline Spirometry (FEV1, FVC, PEF)<br/>"
        "  - Biomarkers (FeNO, Blood Eosinophils, IgE)<br/>"
        "  - Documented Allergens & Exacerbation History<br/><br/>"
        "• <b>Wearable Telemetry Stream</b><br/>"
        "  - Continuous PPG: Heart Rate & HRV (rMSSD)<br/>"
        "  - Blood Oxygen Saturation (SpO2 %)<br/>"
        "  - Respiratory Rate & Skin Temperature<br/>"
        "  - BLE Smart Inhaler Doses & Actuation Log<br/><br/>"
        "• <b>Environmental Dispersion API</b><br/>"
        "  - Open-Meteo 48h Hourly PM2.5, NO2, SO2, O3<br/>"
        "  - Thermal Inversion & Weather Telemetry",
        card_body
    )

    stage2 = Paragraph(
        "<b>2. DIGITAL TWIN SIMULATOR</b><br/><br/>"
        "• <b>Physiological State Modeling</b><br/>"
        "  - Airway Resistance Raw (cmH2O/(L/s))<br/>"
        "  - Dynamic Lung Compliance Cdyn (mL/cmH2O)<br/>"
        "  - Alveolar-Arterial O2 Gradient (A-a DO2)<br/>"
        "  - Autonomic Sympathetic Tone Index<br/><br/>"
        "• <b>24-Hour Forward Projection</b><br/>"
        "  - Differential Equations of Airway Narrowing<br/>"
        "  - Particulate Inhalation Kinetics<br/>"
        "  - Exacerbation Risk Index (ERI) Curve<br/>"
        "  - Estimated Time to Decompensation",
        card_body
    )

    stage3 = Paragraph(
        "<b>3. COUNTERFACTUAL WHAT-IF</b><br/><br/>"
        "• <b>Virtual Intervention Sandbox</b><br/>"
        "  - Test interventions in silico before execution<br/>"
        "  - Scenario A: Indoor HEPA air filtration<br/>"
        "  - Scenario B: Proactive SMART inhaler puff<br/>"
        "  - Scenario C: Activity rescheduling<br/><br/>"
        "• <b>Comparative Efficacy</b><br/>"
        "  - ΔERI Peak Risk Reduction %<br/>"
        "  - ΔPEF Airway Improvement<br/>"
        "  - Optimal Personalized Protocol",
        card_body
    )

    stage4 = Paragraph(
        "<b>4. SAFETY & GOVERNANCE</b><br/><br/>"
        "• <b>Deterministic Safety Rails</b><br/>"
        "  - Dual-layer: Regex & GINA Step-5 boundaries<br/>"
        "  - Red-Flag Distress Interceptor (Bypasses LLM)<br/>"
        "  - Output Sanitizer: Blocks dosage changes<br/>"
        "  - Bilingual Emergency 108/112 SOS Protocols<br/><br/>"
        "• <b>Human-in-the-Loop Approval</b><br/>"
        "  - Zero-Trust External Action Queue<br/>"
        "  - Gated Caregiver SMS / n8n Webhook<br/>"
        "  - Tamper-evident SQLite Audit Log",
        card_body
    )

    stage5 = Paragraph(
        "<b>5. ACTION & INTERACTION</b><br/><br/>"
        "• <b>Patient Experience (Web UI)</b><br/>"
        "  - Editorial Design System (Warm Ivory & Glass)<br/>"
        "  - Bilingual English / Hindi Voice & Text<br/>"
        "  - 24h Safest Clean Air Window Finder<br/><br/>"
        "• <b>Clinician Decision Support</b><br/>"
        "  - Instant 30-Day GINA Summary PDF<br/>"
        "  - Reliever puff frequency & PEF dynamics<br/>"
        "  - GDPR / DPDP Full Data Portability",
        card_body
    )

    data = [
        [
            Paragraph("<b>Stage 1: SENSE & INGEST</b>", col_head),
            Paragraph("<b>Stage 2: SIMULATE & TWIN</b>", col_head),
            Paragraph("<b>Stage 3: WHAT-IF REASONING</b>", col_head),
            Paragraph("<b>Stage 4: SAFETY GOVERNANCE</b>", col_head),
            Paragraph("<b>Stage 5: ACT & SUPPORT</b>", col_head)
        ],
        [stage1, stage2, stage3, stage4, stage5]
    ]

    t = Table(data, colWidths=[140, 140, 140, 140, 140])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284C7")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    footer_text = Paragraph(
        "<font size=8 color='#64748B'><b>PulmoTwin Architecture:</b> Certified for Digital Twin Challenge 2026 • Happiest Health Summit, Bengaluru • Open-Source License: MIT • Team Kabir Roy (rakeshkabir@gmail.com)</font>",
        ParagraphStyle('Foot', fontName='Helvetica', alignment=1)
    )
    story.append(footer_text)

    doc.build(story)
    print(f"Architecture diagram PDF successfully generated: {pdf_path}")

if __name__ == "__main__":
    build_pdf()
