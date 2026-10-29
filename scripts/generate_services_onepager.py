"""Generate a one-page services sheet for LinkedIn / WhatsApp sharing."""
from pathlib import Path

try:
    from fpdf import FPDF
except ImportError:
    raise SystemExit("Install fpdf2: pip install fpdf2")

OUT = Path(__file__).resolve().parent.parent / "assets" / "Muhammad-Afzal-Kalwar-Services.pdf"

NAVY = (11, 31, 58)
AMBER = (245, 166, 35)
BLUE = (37, 99, 235)
SLATE = (51, 65, 85)
MUTED = (100, 116, 139)
WHITE = (255, 255, 255)
SOFT = (241, 245, 249)


class OnePager(FPDF):
    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*MUTED)
        self.cell(
            0,
            8,
            "GitHub/LinkedIn @mafzalkalwardev  |  mafzalkalwardev.github.io/#hire-me  |  WhatsApp +92 307 9670503",
            align="C",
        )


def build() -> None:
    pdf = OnePager("P", "mm", "A4")
    pdf.set_auto_page_break(auto=False)
    pdf.add_page()
    pdf.set_margins(14, 12, 14)

    # Header bar
    pdf.set_fill_color(*NAVY)
    pdf.rect(0, 0, 210, 42, "F")
    pdf.set_fill_color(*AMBER)
    pdf.rect(0, 42, 210, 2.2, "F")

    pdf.set_xy(14, 10)
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(*WHITE)
    pdf.cell(0, 8, "Muhammad Afzal Kalwar", ln=True)

    pdf.set_x(14)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(226, 232, 240)
    pdf.cell(0, 6, "Full-Stack Developer  |  Python Automation Engineer", ln=True)

    pdf.set_x(14)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(
        0,
        5,
        "Islamabad, Pakistan  ·  Remote worldwide  ·  Freelance / contract / hire",
        ln=True,
    )

    pdf.set_y(50)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 7, "Services one-pager", ln=True)

    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(*SLATE)
    pdf.multi_cell(
        0,
        4.8,
        "I build production automation for real businesses: auto dialers, scrapers, email/CRM platforms, "
        "dispatch tools, and AI call workflows. 70+ public projects on GitHub.",
    )
    pdf.ln(2)

    services = [
        (
            "01  Auto dialers & voice AI",
            "Google Voice / iPECS dialers, AI call scripts, operator consoles, Windows outbound tools for dispatch & sales.",
        ),
        (
            "02  Scrapers & carrier data",
            "Playwright/Selenium pipelines, FMCSA SAFER extractors, logistics lead systems, site capture/clone toolkits.",
        ),
        (
            "03  Email & CRM platforms",
            "Bulk email verification, SMTP automation, lead CRMs, admin dashboards, outreach ops tooling.",
        ),
        (
            "04  Full-stack product builds",
            "React/Next.js/Blazor frontends, Node/FastAPI/Go backends, Docker deploys, client websites & SaaS.",
        ),
    ]

    for title, desc in services:
        y = pdf.get_y()
        pdf.set_fill_color(*SOFT)
        pdf.rect(14, y, 182, 22, style="F")
        pdf.set_xy(18, y + 3)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(*BLUE)
        pdf.cell(0, 5, title, ln=True)
        pdf.set_x(18)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*SLATE)
        pdf.multi_cell(174, 4.4, desc)
        pdf.set_y(y + 24)

    pdf.ln(1)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 6, "Best fit / engagement", ln=True)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*SLATE)
    pdf.multi_cell(
        0,
        4.5,
        "Dialers · scrapers · email ops · CRM · dispatch/logistics sites · AI call workflows. "
        "Fixed-scope builds or weekly contract. Remote-first.",
    )
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 6, "Flagship proof", ln=True)
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(*SLATE)
    proofs = [
        "google-voice-dispatch-agent  ·  python-auto-dialer-pro  ·  fiverr-lead-extractor-crm",
        "safer-web-scraper  ·  email-verification-platform  ·  playwright-website-scraper-pro",
        "Case studies: github.com/mafzalkalwardev  ->  each repo / CASE_STUDY.md",
    ]
    for line in proofs:
        pdf.cell(0, 4.2, line, ln=True)

    pdf.ln(3)
    # CTA box
    y = pdf.get_y()
    pdf.set_fill_color(*NAVY)
    pdf.rect(14, y, 182, 36, style="F")
    pdf.set_xy(18, y + 4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*AMBER)
    pdf.cell(0, 6, "Hire / contact", ln=True)
    pdf.set_x(18)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(*WHITE)
    pdf.cell(0, 5, "WhatsApp  +92 307 9670503   ·   wa.me/923079670503", ln=True)
    pdf.set_x(18)
    pdf.cell(0, 5, "GitHub  @mafzalkalwardev   ·   LinkedIn  @mafzalkalwardev", ln=True)
    pdf.set_x(18)
    pdf.cell(0, 5, "Email  kalwarmuhammadafzal3@gmail.com   ·   Portfolio  mafzalkalwardev.github.io/#hire-me", ln=True)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUT))
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
