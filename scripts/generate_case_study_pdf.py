"""One-page PDF case study for LinkedIn Featured media upload."""
from pathlib import Path

try:
    from fpdf import FPDF
except ImportError:
    raise SystemExit("Install fpdf2: pip install fpdf2")

OUT = Path(__file__).resolve().parent.parent / "assets" / "Case-Study-Google-Voice-Dispatch-Agent.pdf"
NAVY = (11, 31, 58)
AMBER = (245, 166, 35)
BLUE = (37, 99, 235)
SLATE = (51, 65, 85)
MUTED = (100, 116, 139)
WHITE = (255, 255, 255)
SOFT = (241, 245, 249)


class PDF(FPDF):
    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*MUTED)
        self.cell(
            0,
            8,
            "mafzalkalwardev.github.io/case-studies.html  |  WhatsApp +92 307 9670503  |  @mafzalkalwardev",
            align="C",
        )


def build() -> None:
    pdf = PDF("P", "mm", "A4")
    pdf.set_auto_page_break(auto=False)
    pdf.add_page()
    pdf.set_margins(16, 14, 16)

    pdf.set_fill_color(*NAVY)
    pdf.rect(0, 0, 210, 36, "F")
    pdf.set_fill_color(*AMBER)
    pdf.rect(0, 36, 210, 2, "F")

    pdf.set_xy(16, 10)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(*WHITE)
    pdf.cell(0, 7, "Case Study: AI Google Voice Dispatch Agent", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(16)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(226, 232, 240)
    pdf.cell(0, 6, "Muhammad Afzal Kalwar  |  @mafzalkalwardev  |  Problem -> Stack -> Result", new_x="LMARGIN", new_y="NEXT")

    pdf.set_y(46)

    def heading(text: str) -> None:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(*BLUE)
        pdf.cell(0, 7, text, new_x="LMARGIN", new_y="NEXT")

    def body(text: str) -> None:
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*SLATE)
        pdf.multi_cell(0, 5, text)
        pdf.ln(3)

    heading("Problem")
    body(
        "Dispatch and outbound sales teams needed a low-cost way to run Google Voice calling "
        "workflows with scripts, voicemail handling, and operator control - without buying an "
        "expensive dialer stack."
    )
    heading("Stack")
    body("Python, Selenium, FastAPI, Groq LLM, local TTS, operator console UI, CRM-style call logging.")
    heading("Result")
    body(
        "Shipped a production-ready outbound assistant that generates call scripts, drives Google Voice "
        "in the browser, handles voicemail paths, and gives operators a live console - reducing manual "
        "dialing friction for logistics/dispatch use cases."
    )
    heading("Audience")
    body("Dispatch teams, logistics ops, and outbound sales agencies.")

    y = pdf.get_y() + 2
    pdf.set_fill_color(*SOFT)
    pdf.rect(16, y, 178, 28, "F")
    pdf.set_xy(20, y + 4)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 6, "Hire / contact", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(20)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(*SLATE)
    pdf.cell(0, 5, "WhatsApp +92 307 9670503  |  GitHub/LinkedIn @mafzalkalwardev", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(20)
    pdf.cell(0, 5, "Portfolio: mafzalkalwardev.github.io/case-studies.html", new_x="LMARGIN", new_y="NEXT")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUT))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
