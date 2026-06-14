"""Add screenshot sections to GitHub repo READMEs from captured portfolio assets."""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

OWNER = "mafzalkalwardev"
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets" / "projects"
DATA_JS = ROOT / "js" / "projects-data.js"

SKIP_PUSH = {
    "mafzalkalwardev",
    "professional-portfolio",
    "mafzalkalwardev.github.io",
    "odysseus",
    "quickdraw-test",
}


def load_projects() -> list[dict]:
    text = DATA_JS.read_text(encoding="utf-8")
    m = re.search(r"window\.PORTFOLIO_PROJECTS\s*=\s*(\[.*?\]);", text, re.S)
    return json.loads(m.group(1)) if m else []


def patch_readme(readme: str, repo: str, has_video: bool) -> str:
    section = "## Screenshots\n\n"
    section += f"![{repo} dashboard](docs/screenshots/app.png)\n\n"
    if has_video:
        section += f"[Demo video](docs/screenshots/demo.webm)\n\n"

    if "## Screenshots" in readme:
        readme = re.sub(
            r"## Screenshots\b.*?(?=\n## |\Z)",
            section.rstrip() + "\n",
            readme,
            count=1,
            flags=re.S,
        )
    elif "## Screenshot" in readme:
        readme = re.sub(
            r"## Screenshot\b.*?(?=\n## |\Z)",
            section.rstrip() + "\n",
            readme,
            count=1,
            flags=re.S,
        )
    else:
        anchor = "## Features"
        if anchor in readme:
            readme = readme.replace(anchor, section + anchor, 1)
        elif "## Quick Start" in readme:
            readme = readme.replace("## Quick Start", section + "## Quick Start", 1)
        else:
            readme = readme.rstrip() + "\n\n" + section

    readme = re.sub(
        r"!\[[^\]]*\]\(docs/screenshots/placeholder\.svg\)\s*\n\*Add real captures.*?\*\s*\n?",
        "",
        readme,
        flags=re.S,
    )
    return readme


def update_repo(project: dict, dry_run: bool = False) -> bool:
    repo = project["repo"]
    slug = project["slug"]
    png = ASSETS / f"{slug}.png"
    if not png.exists():
        return False

    video = ROOT / "assets" / "videos" / f"{slug}.webm"
    has_video = video.exists()

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / repo
        subprocess.run(
            ["gh", "repo", "clone", f"{OWNER}/{repo}", str(path), "--", "--depth", "1"],
            check=True,
            capture_output=True,
        )
        shots = path / "docs" / "screenshots"
        shots.mkdir(parents=True, exist_ok=True)
        shutil.copy(png, shots / "app.png")
        if has_video:
            shutil.copy(video, shots / "demo.webm")

        readme_path = path / "README.md"
        if not readme_path.exists():
            return False
        readme = readme_path.read_text(encoding="utf-8")
        readme_path.write_text(patch_readme(readme, repo, has_video), encoding="utf-8")

        if dry_run:
            print(f"  would update {repo}")
            return True

        subprocess.run(["git", "-C", str(path), "add", "docs/screenshots", "README.md"], check=True)
        status = subprocess.run(
            ["git", "-C", str(path), "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True,
        )
        if not status.stdout.strip():
            return False
        subprocess.run(
            ["git", "-C", str(path), "commit", "-m", "docs: add real project screenshots and demo media"],
            check=True,
        )
        subprocess.run(["git", "-C", str(path), "push", "origin", "HEAD"], check=True)
        print(f"  pushed {repo}")
        return True


def main() -> None:
    projects = load_projects()
    updated = 0
    for p in projects:
        if p["repo"] in SKIP_PUSH:
            continue
        try:
            if update_repo(p):
                updated += 1
        except subprocess.CalledProcessError as exc:
            print(f"  failed {p['repo']}: {exc}")
    print(f"Updated {updated} repo READMEs.")


if __name__ == "__main__":
    main()
