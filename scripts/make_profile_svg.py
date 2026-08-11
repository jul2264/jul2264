from pathlib import Path

def make_profile_svg(output_path="profile.svg"):
    svg_width = 860
    svg_height = 185

    name = "Julian Steve"
    role = "Intern @ YugaYatra | 3rd Yr CS Student @ SRM University"
    
    bio_lines = [
        "Full-Stack Developer & Software Engineering Intern building scalable web apps,",
        "distributed systems, and intelligent search backends. Passionate about DSA",
        "fundamentals, modern web architectures, and high-performance software."
    ]

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
  <style>
    .bg {{ fill: #0d1117; rx: 10px; ry: 10px; stroke: #30363d; stroke-width: 1px; }}
    .header-bar {{ fill: #161b22; rx: 10px; ry: 10px; }}
    .term-title {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; font-size: 13px; fill: #8b949e; font-weight: 600; }}
    .term-prompt {{ fill: #58a6ff; }}
    
    .name-text {{
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
      font-size: 19px;
      font-weight: 700;
      fill: #58a6ff;
    }}

    .role-text {{
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
      font-size: 13px;
      font-weight: 600;
      fill: #79c0ff;
    }}

    .bio-text {{
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
      font-size: 12.5px;
      fill: #c9d1d9;
    }}
  </style>

  <!-- Frame -->
  <rect x="0" y="0" width="{svg_width}" height="{svg_height}" class="bg" />
  
  <!-- Header Bar -->
  <path d="M 0 10 A 10 10 0 0 1 10 0 L {svg_width - 10} 0 A 10 10 0 0 1 {svg_width} 10 L {svg_width} 32 L 0 32 Z" fill="#161b22" />
  <circle cx="20" cy="18" r="5" fill="#ff5f56" />
  <circle cx="36" cy="18" r="5" fill="#ffbd2e" />
  <circle cx="52" cy="18" r="5" fill="#27c93f" />
  <text x="75" y="22" class="term-title"><tspan class="term-prompt">jul2264@github ~ $</tspan> whoami</text>

  <!-- Content -->
  <g>
    <!-- Name -->
    <text x="30" y="64" class="name-text">👋 Hi, I'm {name}</text>
    
    <!-- Subtitle / Role -->
    <text x="30" y="88" class="role-text">{role}</text>
    
    <!-- Separator -->
    <line x1="30" y1="102" x2="{svg_width - 30}" y2="102" stroke="#30363d" stroke-width="1" stroke-dasharray="4 4" />

    <!-- Bio Paragraph -->
    <text x="30" y="124" class="bio-text">{bio_lines[0]}</text>
    <text x="30" y="142" class="bio-text">{bio_lines[1]}</text>
    <text x="30" y="160" class="bio-text">{bio_lines[2]}</text>
  </g>
</svg>
"""

    out_path = Path(output_path)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Generated profile SVG at {out_path} ({len(svg_content)} bytes)")

if __name__ == "__main__":
    make_profile_svg()
