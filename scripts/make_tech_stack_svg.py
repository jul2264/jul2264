from pathlib import Path

def make_tech_stack_svg(output_path="tech-stack.svg"):
    svg_width = 860
    svg_height = 315

    rows = [
        # Row 1: Core Languages
        [
            {"name": "Python", "color": "#3776AB", "icon": "python"},
            {"name": "JavaScript", "color": "#F7DF1E", "icon": "javascript"},
            {"name": "TypeScript", "color": "#3178C6", "icon": "typescript"},
            {"name": "Java", "color": "#ED8B00", "icon": "java"},
            {"name": "C++", "color": "#00599C", "icon": "cpp"},
            {"name": "Go", "color": "#00ADD8", "icon": "go"},
        ],
        # Row 2: Frontend & Node
        [
            {"name": "HTML", "color": "#E34F26", "icon": "html"},
            {"name": "CSS", "color": "#1572B6", "icon": "css"},
            {"name": "React", "color": "#61DAFB", "icon": "react"},
            {"name": "Node.js", "color": "#5FA04E", "icon": "nodejs"},
        ],
        # Row 3: Backend & ML
        [
            {"name": "Django", "color": "#44B78B", "icon": "django"},
            {"name": "TensorFlow", "color": "#FF6F00", "icon": "tensorflow"},
            {"name": "Meilisearch", "color": "#FF5C00", "icon": "meilisearch"},
        ],
        # Row 4: Databases
        [
            {"name": "PostgreSQL", "color": "#4169E1", "icon": "postgres"},
            {"name": "MySQL", "color": "#4479A1", "icon": "mysql"},
            {"name": "Redis", "color": "#DC382D", "icon": "redis"},
        ],
        # Row 5: Tools & Environment
        [
            {"name": "Docker", "color": "#2496ED", "icon": "docker"},
            {"name": "Linux", "color": "#FCC624", "icon": "linux"},
            {"name": "Git", "color": "#F05032", "icon": "git"},
            {"name": "VS Code", "color": "#007ACC", "icon": "vscode"},
        ]
    ]

    def get_icon_svg(icon_type, color):
        if icon_type == "python":
            return f'<path d="M8 1C4 1 4 3 4 4V6H8V7H3C1 7 1 10 1 12C1 14 3 15 5 15H6V13C6 11 8 11 10 11H13V9C13 7 13 7 11 7H10V5C10 3 10 1 8 1Z" fill="{color}"/><circle cx="6" cy="3" r="0.8" fill="#fff"/>'
        elif icon_type == "javascript":
            return f'<rect x="1" y="1" width="14" height="14" rx="2" fill="{color}"/><text x="8" y="12" font-family="ui-monospace, monospace" font-size="9" font-weight="bold" fill="#000" text-anchor="middle">JS</text>'
        elif icon_type == "typescript":
            return f'<rect x="1" y="1" width="14" height="14" rx="2" fill="{color}"/><text x="8" y="12" font-family="ui-monospace, monospace" font-size="9" font-weight="bold" fill="#fff" text-anchor="middle">TS</text>'
        elif icon_type == "java":
            return f'<path d="M5 12C5 12 7 13 9 13C11 13 13 12 13 12 M4 14C4 14 7 15 9 15C11 15 14 14 14 14 M7 2C7 2 5 4 7 6C9 8 9 9 7 11 M10 2C10 2 8 4 10 6C12 8 12 9 10 11" fill="none" stroke="{color}" stroke-width="1.3"/>'
        elif icon_type == "cpp":
            return f'<rect x="1" y="1" width="14" height="14" rx="2" fill="{color}"/><text x="8" y="11.5" font-family="ui-monospace, monospace" font-size="8" font-weight="bold" fill="#fff" text-anchor="middle">C++</text>'
        elif icon_type == "go":
            return f'<path d="M0 6 C2 2 6 2 8 6 C6 10 2 10 0 6 M10 6 C12 2 16 2 18 6 C16 10 12 10 10 6" fill="none" stroke="{color}" stroke-width="2"/>'
        elif icon_type == "html":
            return f'<polygon points="2,1 14,1 12,14 8,15 4,14" fill="none" stroke="{color}" stroke-width="1.5"/><text x="8" y="10.5" font-family="ui-monospace, monospace" font-size="7" font-weight="bold" fill="{color}" text-anchor="middle">H5</text>'
        elif icon_type == "css":
            return f'<polygon points="2,1 14,1 12,14 8,15 4,14" fill="none" stroke="{color}" stroke-width="1.5"/><text x="8" y="10.5" font-family="ui-monospace, monospace" font-size="7" font-weight="bold" fill="{color}" text-anchor="middle">C3</text>'
        elif icon_type == "nodejs":
            return f'<polygon points="8,1 15,5 15,13 8,17 1,13 1,5" fill="none" stroke="{color}" stroke-width="1.8"/>'
        elif icon_type == "react":
            return f'<ellipse cx="8" cy="8" rx="7" ry="3" fill="none" stroke="{color}" stroke-width="1.5"/><ellipse cx="8" cy="8" rx="7" ry="3" fill="none" stroke="{color}" stroke-width="1.5" transform="rotate(60 8 8)"/><ellipse cx="8" cy="8" rx="7" ry="3" fill="none" stroke="{color}" stroke-width="1.5" transform="rotate(120 8 8)"/><circle cx="8" cy="8" r="1.5" fill="{color}"/>'
        elif icon_type == "django":
            return f'<rect x="1" y="1" width="14" height="14" rx="2" fill="{color}"/><text x="8" y="12" font-family="ui-monospace, monospace" font-size="9" font-weight="bold" fill="#fff" text-anchor="middle">dj</text>'
        elif icon_type == "tensorflow":
            return f'<path d="M8 1L14 4.5V11.5L11 10V6.5L8 4.8L5 6.5V13.5L8 15.2L11 13.5V11.5L8 13.2L3 10.3V4.5L8 1Z" fill="{color}"/>'
        elif icon_type == "postgres":
            return f'<circle cx="8" cy="8" r="7" fill="none" stroke="{color}" stroke-width="1.5"/><path d="M5 8C5 6 11 6 11 8C11 11 5 11 5 13" fill="none" stroke="{color}" stroke-width="1.5"/>'
        elif icon_type == "mysql":
            return f'<path d="M3 13C3 7 7 3 13 3M6 13C6 9 9 6 13 6" fill="none" stroke="{color}" stroke-width="1.8"/><circle cx="13" cy="13" r="1.5" fill="{color}"/>'
        elif icon_type == "redis":
            return f'<path d="M1 4L8 1L15 4L8 7Z M1 8L8 11L15 8 M1 12L8 15L15 12" fill="none" stroke="{color}" stroke-width="1.5"/>'
        elif icon_type == "meilisearch":
            return f'<path d="M2 14L8 2L14 14" fill="none" stroke="{color}" stroke-width="2"/><line x1="4" y1="10" x2="12" y2="10" stroke="{color}" stroke-width="1.5"/>'
        elif icon_type == "docker":
            return f'<rect x="1" y="7" width="3" height="3" fill="{color}"/><rect x="5" y="7" width="3" height="3" fill="{color}"/><rect x="9" y="7" width="3" height="3" fill="{color}"/><rect x="5" y="3" width="3" height="3" fill="{color}"/><path d="M1 11C1 14 4 15 8 15C13 15 15 12 16 10H0Z" fill="{color}"/>'
        elif icon_type == "linux":
            return f'<path d="M8 2C6 2 5 4 5 7C5 10 4 12 3 13H13C12 12 11 10 11 7C11 4 10 2 8 2Z" fill="{color}"/>'
        elif icon_type == "git":
            return f'<path d="M15 8L8 15L1 8L8 1Z" fill="none" stroke="{color}" stroke-width="1.8"/><circle cx="8" cy="5" r="1.5" fill="{color}"/><circle cx="8" cy="11" r="1.5" fill="{color}"/><circle cx="11" cy="8" r="1.5" fill="{color}"/>'
        elif icon_type == "vscode":
            return f'<path d="M12 1L4 7L1 5L4 11L12 15L15 13V3Z" fill="none" stroke="{color}" stroke-width="1.5"/>'
        else:
            return f'<circle cx="8" cy="8" r="5" fill="{color}"/>'

    y_start = 74
    row_step = 44
    margin_left = 30

    pills_xml = []

    for r_idx, row in enumerate(rows):
        y = y_start + r_idx * row_step
        current_x = margin_left

        for item in row:
            name = item["name"]
            color = item["color"]
            icon_type = item["icon"]

            text_len = len(name)
            pill_width = max(72, text_len * 10 + 44)

            icon_svg = get_icon_svg(icon_type, color)

            pill = (
                f'<g transform="translate({current_x}, {y})">'
                f'<rect x="0" y="0" width="{pill_width}" height="32" rx="6" ry="6" fill="#161b22" stroke="#30363d" stroke-width="1"/>'
                f'<g transform="translate(10, 8)">{icon_svg}</g>'
                f'<text x="34" y="20.5" class="badge-text" fill="#c9d1d9">{name}</text>'
                f'</g>'
            )
            pills_xml.append(pill)
            current_x += pill_width + 12

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
  <style>
    .bg {{ fill: #0d1117; rx: 10px; ry: 10px; stroke: #30363d; stroke-width: 1px; }}
    .header-bar {{ fill: #161b22; rx: 10px; ry: 10px; }}
    .term-title {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; font-size: 13px; fill: #8b949e; font-weight: 600; }}
    .term-prompt {{ fill: #58a6ff; }}
    .section-title {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; font-size: 14.5px; font-weight: 600; fill: #e6edf3; }}
    
    .badge-text {{
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
      font-size: 12.5px;
      font-weight: 600;
    }}
  </style>

  <!-- Frame -->
  <rect x="0" y="0" width="{svg_width}" height="{svg_height}" class="bg" />
  
  <!-- Header Bar -->
  <path d="M 0 10 A 10 10 0 0 1 10 0 L {svg_width - 10} 0 A 10 10 0 0 1 {svg_width} 10 L {svg_width} 32 L 0 32 Z" fill="#161b22" />
  <circle cx="20" cy="18" r="5" fill="#ff5f56" />
  <circle cx="36" cy="18" r="5" fill="#ffbd2e" />
  <circle cx="52" cy="18" r="5" fill="#27c93f" />
  <text x="75" y="22" class="term-title"><tspan class="term-prompt">jul2264@github ~ $</tspan> cat tech_stack.md</text>

  <!-- Section Title -->
  <text x="30" y="58" class="section-title">🛠️ I code using</text>

  <!-- Badge Pills -->
  <g>
    {"".join(pills_xml)}
  </g>
</svg>
"""

    out_path = Path(output_path)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Generated tech stack SVG at {out_path} ({len(svg_content)} bytes)")

if __name__ == "__main__":
    make_tech_stack_svg()
