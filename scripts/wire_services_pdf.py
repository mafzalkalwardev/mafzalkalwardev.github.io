from pathlib import Path

PDF = "assets/Muhammad-Afzal-Kalwar-Services.pdf"
BTN = (
    f'<a href="{PDF}" class="btn btn-cv btn-lg" '
    'download="Muhammad-Afzal-Kalwar-Services.pdf">Download services PDF</a>'
)

idx = Path("index.html")
t = idx.read_text(encoding="utf-8")
if "Muhammad-Afzal-Kalwar-Services.pdf" not in t:
    if '<a href="contact.html" class="btn btn-cv btn-lg">Contact form</a>' in t:
        t = t.replace(
            '<a href="contact.html" class="btn btn-cv btn-lg">Contact form</a>',
            '<a href="contact.html" class="btn btn-cv btn-lg">Contact form</a>\n            ' + BTN,
            1,
        )
    t = t.replace(
        '<a href="assets/Muhammad-Afzal-Kalwar-CV.pdf" download="Muhammad-Afzal-Kalwar-CV.pdf">Download CV</a>',
        '<a href="assets/Muhammad-Afzal-Kalwar-CV.pdf" download="Muhammad-Afzal-Kalwar-CV.pdf">Download CV</a>\n'
        '      <a href="assets/Muhammad-Afzal-Kalwar-Services.pdf" download="Muhammad-Afzal-Kalwar-Services.pdf">Services PDF</a>',
        1,
    )
    idx.write_text(t, encoding="utf-8", newline="\n")
    print("index updated")
else:
    print("index already linked")

cpath = Path("contact.html")
c = cpath.read_text(encoding="utf-8")
if "Muhammad-Afzal-Kalwar-Services.pdf" not in c:
    needle = "Available for new projects</strong>"
    if needle in c:
        c = c.replace(
            needle,
            needle
            + '<p style="margin-top:0.5rem"><a href="assets/Muhammad-Afzal-Kalwar-Services.pdf" download>'
            "Download services one-pager (PDF)</a></p>",
            1,
        )
        cpath.write_text(c, encoding="utf-8", newline="\n")
        print("contact updated")
    else:
        print("contact: banner not found")
else:
    print("contact already linked")

rpath = Path("README.md")
r = rpath.read_text(encoding="utf-8")
if "Muhammad-Afzal-Kalwar-Services.pdf" not in r:
    r = (
        r.rstrip()
        + """

## Services one-pager

Shareable PDF for LinkedIn / WhatsApp:

- [Download Muhammad-Afzal-Kalwar-Services.pdf](assets/Muhammad-Afzal-Kalwar-Services.pdf)
- Live hire page: https://mafzalkalwardev.github.io/#hire-me
"""
    )
    rpath.write_text(r + "\n", encoding="utf-8", newline="\n")
    print("readme updated")
else:
    print("readme already linked")
