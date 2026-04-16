import os
import re
import glob

CSS_ADDITIONS = """
/* --- PART 1: Projects Images --- */
.proj-img-wrap, .archive-icon.proj-img-wrap {
  overflow: hidden;
  border-radius: 8px; /* good default for rounded cards */
}
.detail-image-main {
  overflow: hidden;
}
.proj-img-wrap img,
.detail-image-main img {
  object-fit: cover;
  object-position: center;
  width: 100%;
}
.proj-img-wrap img {
  aspect-ratio: 16/9;
}
.detail-image-main img {
  border-radius: 8px; /* usually hero images look better rounded */
}

/* --- PART 2: Footer Icons & Tooltips --- */
.footer-social {
  display: flex;
  align-items: center;
  gap: 16px;
}
.footer-social > a {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
}
/* existing icons */
.footer-social > a > svg {
  transition: transform 0.2s ease, filter 0.2s ease;
}

/* new icons */
.g-icon, .in-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
}
.footer-social > a:hover .g-icon,
.footer-social > a:hover .in-icon {
  transform: scale(1.1);
}
.footer-social > a:hover .in-icon {
  filter: brightness(1.15);
}

/* Tooltips */
.footer-social > a::before {
  content: attr(data-tooltip);
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%) translateY(-8px);
  background: #1a1f3c;
  color: #fff;
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 12px;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s ease, transform 0.2s ease;
  z-index: 10;
}
.footer-social > a:hover::before {
  opacity: 1;
  transform: translateX(-50%) translateY(-4px);
}

/* --- PART 3: Intro Animation --- */
#intro-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: #f4f6f8;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: opacity 0.5s ease;
}

#intro-overlay.hidden {
  opacity: 0;
  pointer-events: none;
}

.intro-text-container {
  display: flex;
  overflow: hidden;
}

.intro-letter {
  font-family: 'Inter', sans-serif;
  font-size: 5rem;
  color: #1a1f3c;
  letter-spacing: 0.3em;
  font-weight: 700;
  opacity: 0;
  transform: translateY(40px);
  transition: opacity 0.4s ease, transform 0.4s ease;
}

.intro-letter.show {
  opacity: 1;
  transform: translateY(0);
}
"""

JS_ADDITIONS = """
document.addEventListener("DOMContentLoaded", function() {
    if (!sessionStorage.getItem("introPlayed")) {
        const overlay = document.createElement("div");
        overlay.id = "intro-overlay";
        
        const container = document.createElement("div");
        container.className = "intro-text-container";
        
        const name = "LUAN";
        name.split("").forEach((char) => {
            const span = document.createElement("span");
            span.className = "intro-letter";
            span.textContent = char;
            container.appendChild(span);
        });
        
        overlay.appendChild(container);
        document.body.appendChild(overlay);
        
        document.body.style.overflow = "hidden";
        
        const letters = container.querySelectorAll(".intro-letter");
        letters.forEach((letter, index) => {
            setTimeout(() => {
                letter.classList.add("show");
            }, 100 + (index * 150)); 
        });
        
        setTimeout(() => {
            overlay.classList.add("hidden");
            setTimeout(() => {
                overlay.remove();
                document.body.style.overflow = ""; 
            }, 500); 
        }, 1300);
        
        sessionStorage.setItem("introPlayed", "true");
    }
});
"""

NEW_GMAIL = '''<a href="mailto:luanlaguna7@gmail.com" aria-label="Email" data-tooltip="Gmail">
              <svg viewBox="0 0 40 40" class="social-icon g-icon">
                <rect width="40" height="40" rx="8" fill="#ffffff" />
                <path d="M7 12 L20 22 L33 12 V28 H7 Z" fill="#f4f6f8"/> 
                <path d="M7 12 L20 22 L20 26 L7 16 Z" fill="#ea4335"/>
                <path d="M7 12 H11 V28 H7 Z" fill="#ea4335"/>
                <path d="M33 12 L20 22 L20 26 L33 16 Z" fill="#4285f4"/>
                <path d="M29 12 H33 V28 H29 Z" fill="#4285f4"/>
              </svg>
            </a>'''

NEW_LINKEDIN = '''<a href="https://www.linkedin.com/in/luan-laguna-390032174/" target="_blank" rel="noopener" aria-label="LinkedIn" data-tooltip="LinkedIn">
              <svg viewBox="0 0 40 40" class="social-icon in-icon">
                <rect width="40" height="40" rx="8" fill="#0A66C2" />
                <path d="M12.5 14.5c1.8 0 2.9-1.2 2.9-2.7 0-1.5-1.1-2.7-2.8-2.7s-2.9 1.2-2.9 2.7c0 1.5 1.1 2.7 2.8 2.7zm-2.2 4.1h4.5v14.1h-4.5V18.6zm13.1-4.7c-2.4 0-3.5 1.3-4.1 2.3v-2h-4.5c.1 1.3 0 14.1 0 14.1h4.5v-7.9c0-4.2 2.2-5 3.5-5 1.4 0 2.6 1 2.6 4.3v8.6h4.5v-9c0-4.8-2.6-7.4-6.5-7.4z" fill="#FFF"/>
              </svg>
            </a>'''

files = glob.glob('*.html') + glob.glob('projects/*.html')

email_pat = re.compile(r'<a href="mailto:[^"]+"[^>]*aria-label="Email"[^>]*>.*?</a>', re.IGNORECASE | re.DOTALL)
linkedin_pat = re.compile(r'<a href="https://www\.linkedin\.com/[^"]+"[^>]*aria-label="LinkedIn"[^>]*>.*?</a>', re.IGNORECASE | re.DOTALL)

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Apply footer
    content = email_pat.sub(NEW_GMAIL, content)
    content = linkedin_pat.sub(NEW_LINKEDIN, content)
    
    gh_match = re.search(r'(<a href="https://github\.com/[^"]+"[^>]*aria-label="GitHub")([^>]*>)', content)
    if gh_match and 'data-tooltip' not in gh_match.group(0):
        content = content.replace(gh_match.group(0), gh_match.group(1) + ' data-tooltip="GitHub"' + gh_match.group(2))

    if fpath == 'projects.html':
        content = content.replace(
            '<div class="proj-img-placeholder">OpsQuery &mdash; screenshot coming soon</div>',
            '<img src="assets/projects/opsquery-hero.jpg.jpg" alt="OpsQuery project" />'
        )
        brm_regex = r'<div class="archive-icon" aria-hidden="true">\s*<!-- Settings / operations icon -->\s*<svg viewBox="0 0 24 24">.*?</svg>\s*</div>'
        brm_repl = '<div class="archive-icon proj-img-wrap" aria-hidden="true" style="padding: 0; background: none; border-radius: 8px; width: 100%; height: auto;"><img src="assets/projects/brmachine-dashboard.jpg" alt="BRMachine Dashboard" style="display:block;"/></div>'
        content = re.sub(brm_regex, brm_repl, content, flags=re.DOTALL)
        
    elif fpath == 'projects\\\\opsquery.html' or fpath == 'projects/opsquery.html':
        content = content.replace(
            '<div class="detail-image-placeholder">OpsQuery &mdash; screenshot coming soon</div>',
            '<img src="../assets/projects/opsquery-hero.jpg.jpg" alt="OpsQuery project" />'
        )
    elif fpath == 'projects\\\\restaurant-platform.html' or fpath == 'projects/restaurant-platform.html':
        content = content.replace(
            '<img src="../assets/projects/ordering-platform.jpg"',
            '<img src="../assets/projects/restaurant-hero.jpg.jpg"'
        )

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)

with open('style.css', 'a', encoding='utf-8') as f:
    f.write('\\n' + CSS_ADDITIONS + '\\n')

with open('js/animations.js', 'a', encoding='utf-8') as f:
    f.write('\\n' + JS_ADDITIONS + '\\n')

print("Done")
