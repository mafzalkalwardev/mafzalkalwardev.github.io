"""Generate professional CV PDF for portfolio download."""
from pathlib import Path

try:
    from fpdf import FPDF
except ImportError:
    raise SystemExit("Install fpdf2: pip install fpdf2")

OUT = Path(__file__).resolve().parent.parent / "assets" / "Muhammad-Afzal-Kalwar-CV.pdf"


class CV(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, "Muhammad Afzal Kalwar - CV", align="C")


def build() -> None:
    pdf = CV("P", "mm", "A4")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()
    pdf.set_margins(18, 18, 18)

    # Name & title
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 10, "Muhammad Afzal Kalwar", ln=True)

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(29, 78, 216)
    pdf.cell(0, 7, "Full-Stack Developer & Automation Engineer", ln=True)

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 5, "Islamabad, Pakistan  |  Remote worldwide  |  Available for freelance & contract", ln=True)
    pdf.cell(0, 5, "Email: kalwarmuhammadafzal3@gmail.com", ln=True)
    pdf.cell(0, 5, "GitHub: github.com/mafzalkalwardev  |  LinkedIn: linkedin.com/in/muhammad-afzal-2670b527b", ln=True)
    pdf.ln(4)

    def reset_x() -> None:
        pdf.set_x(pdf.l_margin)

    def section(title: str) -> None:
        pdf.ln(3)
        reset_x()
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(15, 23, 42)
        pdf.set_draw_color(29, 78, 216)
        pdf.cell(0, 7, title.upper(), ln=True)
        pdf.set_line_width(0.4)
        y = pdf.get_y()
        pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
        pdf.ln(3)
        reset_x()

    def body(text: str) -> None:
        reset_x()
        pdf.set_font("Helvetica", "", 9.5)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(0, 5, text)
        pdf.ln(1)

    def entry(role: str, org: str, period: str, desc: str) -> None:
        reset_x()
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(0, 5, role, ln=True)
        reset_x()
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(0, 5, f"{org}  |  {period}", ln=True)
        reset_x()
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(0, 4.5, desc)
        pdf.ln(2)

    section("Professional Summary")
    body(
        "Software developer specializing in full-stack web applications, Python desktop software, "
        "and browser automation. I build production-grade tools including auto dialers, CRM platforms, "
        "email verification systems, and web scrapers. 40+ open source repositories on GitHub. "
        "Focused on clean architecture, reliable delivery, and maintainable code."
    )

    section("Education")
    entry(
        "Bachelor of Science in Computer Science",
        "Air University, Islamabad",
        "Graduated",
        "Computer Science degree from Air University Islamabad - foundation in algorithms, "
        "software engineering, databases, and systems programming.",
    )

    section("Technical Skills")
    skills = [
        "Languages: Python, JavaScript, TypeScript, Go",
        "Frontend: React, HTML5, CSS3, responsive UI",
        "Backend: Node.js, Express, FastAPI, REST APIs",
        "Desktop: PyQt6, Windows applications",
        "Automation: Playwright, Selenium, PyAutoGUI, RPA workflows",
        "Data: MongoDB, SQLite, PostgreSQL, Redis",
        "DevOps: Docker, Git, GitHub Actions, CI/CD",
        "AI/ML: TensorFlow, Whisper, Groq LLM integration",
    ]
    for s in skills:
        reset_x()
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(0, 5, f"- {s}")

    section("Experience")
    entry(
        "Independent Full-Stack Developer",
        "Freelance & Remote",
        "Present",
        "Deliver web apps, Python desktop tools, and automation pipelines for clients worldwide. "
        "Maintain 40+ open source repositories. Stack: Python, React, Node.js, PyQt6, Playwright.",
    )

    section("Selected Projects")
    projects = [
        ("Indus Transport Auto Dialer", "PyQt6 desktop dialer - Google Voice, AMD, CRM, predictive pacing."),
        ("Bulk Email Verifier", "Self-hosted email verification with Go + Node.js, Docker, SMTP validation."),
        ("Fiverr Lead Extractor CRM", "Playwright scraper, MongoDB, BullMQ, Excel export, Electron desktop app."),
        ("CallAudit-X", "AI call auditing - transcription, scoring, analytics SaaS platform."),
        ("Playwright Website Scraper Pro", "Multi-page scraper with GUI, asset download, and screenshots."),
        ("Google Voice Dispatch Agent", "Selenium automation with Groq LLM scripts and TTS integration."),
    ]
    for name, desc in projects:
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(15, 23, 42)
        pdf.cell(0, 5, name, ln=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(0, 4.5, desc)
        pdf.ln(1)

    section("Services")
    body(
        "Web development (React, Node.js, SaaS)  |  Python & desktop apps (PyQt6, FastAPI)  |  "
        "Automation & scraping (Playwright, Selenium)  |  AI integration (Whisper, Groq, ML prototypes)"
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUT))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
