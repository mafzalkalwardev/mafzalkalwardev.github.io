window.TECH_STACK = [
  { name: "Python", slug: "python", color: "#3776AB" },
  { name: "JavaScript", slug: "javascript", color: "#F7DF1E" },
  { name: "TypeScript", slug: "typescript", color: "#3178C6" },
  { name: "Go", slug: "go", color: "#00ADD8" },
  { name: "C#", slug: "csharp", color: "#512BD4" },
  { name: "HTML5", slug: "html5", color: "#E34F26" },
  { name: "CSS3", slug: "css3", color: "#1572B6" },
  { name: "React", slug: "react", color: "#61DAFB" },
  { name: "Next.js", slug: "nextjs", color: "#000000", si: "nextdotjs" },
  { name: "Node.js", slug: "nodejs", color: "#339933" },
  { name: "Express", slug: "express", color: "#808080", si: "express" },
  { name: "FastAPI", slug: "fastapi", color: "#009688", si: "fastapi" },
  { name: "Flask", slug: "flask", color: "#000000", si: "flask" },
  { name: "Django", slug: "django", color: "#092E20", si: "django" },
  { name: "PyQt6", slug: "qt", color: "#41CD52", si: "qt" },
  { name: "Electron", slug: "electron", color: "#47848F", si: "electron" },
  { name: ".NET", slug: "dot-net", color: "#512BD4", si: "dotnet" },
  { name: "Tailwind", slug: "tailwindcss", color: "#06B6D4", si: "tailwindcss" },
  { name: "Bootstrap", slug: "bootstrap", color: "#7952B3", si: "bootstrap" },
  { name: "Playwright", slug: "playwright", color: "#2EAD33", si: "playwright" },
  { name: "Selenium", slug: "selenium", color: "#43B02A" },
  { name: "Docker", slug: "docker", color: "#2496ED" },
  { name: "Kubernetes", slug: "kubernetes", color: "#326CE5", si: "kubernetes" },
  { name: "MongoDB", slug: "mongodb", color: "#47A248" },
  { name: "PostgreSQL", slug: "postgresql", color: "#4169E1" },
  { name: "SQLite", slug: "sqlite", color: "#003B57", si: "sqlite" },
  { name: "Redis", slug: "redis", color: "#DC382D" },
  { name: "Prisma", slug: "prisma", color: "#2D3748", si: "prisma" },
  { name: "Firebase", slug: "firebase", color: "#FFCA28", si: "firebase" },
  { name: "AWS", slug: "amazonwebservices", color: "#FF9900", si: "amazonwebservices" },
  { name: "Azure", slug: "azure", color: "#0078D4", si: "microsoftazure" },
  { name: "Vercel", slug: "vercel", color: "#000000", si: "vercel" },
  { name: "Nginx", slug: "nginx", color: "#009639", si: "nginx" },
  { name: "Jenkins", slug: "jenkins", color: "#D24939", si: "jenkins" },
  { name: "Git", slug: "git", color: "#F05032" },
  { name: "GitHub", slug: "github", color: "#181717" },
  { name: "GitLab", slug: "gitlab", color: "#FC6D26", si: "gitlab" },
  { name: "Linux", slug: "linux", color: "#FCC624" },
  { name: "TensorFlow", slug: "tensorflow", color: "#FF6F00" },
  { name: "PyTorch", slug: "pytorch", color: "#EE4C2C", si: "pytorch" },
  { name: "Pandas", slug: "pandas", color: "#150458", si: "pandas" },
  { name: "NumPy", slug: "numpy", color: "#013243", si: "numpy" },
  { name: "Jupyter", slug: "jupyter", color: "#F37626", si: "jupyter" },
  { name: "OpenAI", slug: "openai", color: "#412991", si: "openai" },
  { name: "Groq", slug: "groq", color: "#F55036", si: "groq" },
  { name: "Stripe", slug: "stripe", color: "#635BFF", si: "stripe" },
  { name: "Vite", slug: "vite", color: "#646CFF", si: "vite" },
  { name: "npm", slug: "npm", color: "#CB3837", si: "npm" },
  { name: "GraphQL", slug: "graphql", color: "#E10098", si: "graphql" },
  { name: "Blazor", slug: "blazor", color: "#512BD4", si: "blazor" },
];

window.CV_PATH = "assets/Muhammad-Afzal-Kalwar-CV.pdf";

function techIconUrl(item) {
  if (item.si) {
    return `https://cdn.simpleicons.org/${item.si}/${item.color.replace("#", "")}`;
  }
  return `https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/${item.slug}/${item.slug}-original.svg`;
}

function renderTechIcon(item) {
  const url = techIconUrl(item);
  return `
    <div class="tech-icon-item" title="${item.name}">
      <div class="tech-icon-wrap">
        <img src="${url}" alt="${item.name}" width="32" height="32" loading="lazy" />
      </div>
      <span class="tech-icon-label">${item.name}</span>
    </div>`;
}

function renderTechIconGrid(containerId) {
  const el = document.getElementById(containerId);
  if (!el || !window.TECH_STACK) return;
  el.classList.add('stagger-grid');
  el.innerHTML = window.TECH_STACK.map(renderTechIcon).join("");
  if (window.initReveal) window.initReveal([el]);
  if (window.initTechIconHover) window.initTechIconHover(el);
}

window.renderTechIconGrid = renderTechIconGrid;

document.addEventListener('DOMContentLoaded', () => {
  renderTechIconGrid('techIconGrid');
  renderTechIconGrid('techIconGridHome');
});
