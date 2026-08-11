from pathlib import Path

def make_contact_svg(output_path="contact.svg"):
    svg_width = 860
    svg_height = 210

    contacts = [
        {
            "label": "Email",
            "value": "juliansteve.anban@gmail.com",
            "color": "#FF5252",
            "icon_type": "email"
        },
        {
            "label": "LinkedIn",
            "value": "linkedin.com/in/juliansteve",
            "color": "#0077B5",
            "icon_type": "linkedin"
        },
        {
            "label": "Portfolio",
            "value": "julian-steve-anban-portfolio.vercel.app",
            "color": "#00E5FF",
            "icon_type": "portfolio"
        }
    ]

    def get_icon_svg(icon_type, color):
        if icon_type == "email":
            return f'<path d="M2 4L8 9.5L14 4 M2 4H14V13H2Z" fill="none" stroke="{color}" stroke-width="1.6"/>'
        elif icon_type == "linkedin":
            return f'<rect x="1" y="1" width="14" height="14" rx="2" fill="{color}"/><text x="8" y="11.5" font-family="ui-monospace, monospace" font-size="9" font-weight="bold" fill="#fff" text-anchor="middle">in</text>'
        elif icon_type == "portfolio":
            return f'<circle cx="8" cy="8" r="6" fill="none" stroke="{color}" stroke-width="1.5"/><path d="M2 8H14 M8 2C10 4 10 12 8 14 M8 2C6 4 6 12 8 14" fill="none" stroke="{color}" stroke-width="1.3"/>'
        else:
            return f'<circle cx="8" cy="8" r="5" fill="{color}"/>'

    y_start = 74
    row_step = 42

    rows_xml = []
    for idx, c in enumerate(contacts):
        y = y_start + idx * row_step
        label = c["label"]
        val = c["value"]
        color = c["color"]
        icon_svg = get_icon_svg(c["icon_type"], color)

        val_len = len(val)
        pill_width = max(420, val_len * 10 + 135)

        row_xml = (
            f'<g transform="translate(30, {y})">'
            f'<rect x="0" y="0" width="{pill_width}" height="32" rx="6" ry="6" fill="#161b22" stroke="#30363d" stroke-width="1"/>'
            f'<g transform="translate(12, 8)">{icon_svg}</g>'
            f'<text x="36" y="20.5" class="label-text" fill="{color}">{label.ljust(9)}:</text>'
            f'<text x="135" y="20.5" class="val-text" fill="#c9d1d9">{val}</text>'
            f'</g>'
        )
        rows_xml.append(row_xml)

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
  <style>
    .bg {{ fill: #0d1117; rx: 10px; ry: 10px; stroke: #30363d; stroke-width: 1px; }}
    .header-bar {{ fill: #161b22; rx: 10px; ry: 10px; }}
    .term-title {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; font-size: 13px; fill: #8b949e; font-weight: 600; }}
    .term-prompt {{ fill: #58a6ff; }}
    .section-title {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; font-size: 14.5px; font-weight: 600; fill: #e6edf3; }}
    
    .label-text {{
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
      font-size: 12.5px;
      font-weight: 700;
    }}

    .val-text {{
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
      font-size: 12.5px;
      font-weight: 500;
    }}
  </style>

  <!-- Frame -->
  <rect x="0" y="0" width="{svg_width}" height="{svg_height}" class="bg" />
  
  <!-- Header Bar -->
  <path d="M 0 10 A 10 10 0 0 1 10 0 L {svg_width - 10} 0 A 10 10 0 0 1 {svg_width} 10 L {svg_width} 32 L 0 32 Z" fill="#161b22" />
  <circle cx="20" cy="18" r="5" fill="#ff5f56" />
  <circle cx="36" cy="18" r="5" fill="#ffbd2e" />
  <circle cx="52" cy="18" r="5" fill="#27c93f" />
  <text x="75" y="22" class="term-title"><tspan class="term-prompt">jul2264@github ~ $</tspan> cat contact_info.md</text>

  <!-- Section Title -->
  <text x="30" y="58" class="section-title">📬 Connect &amp; Portfolio</text>

  <!-- Contact Rows -->
  <g>
    {"".join(rows_xml)}
  </g>
</svg>
"""

    out_path = Path(output_path)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Generated contact card SVG at {out_path} ({len(svg_content)} bytes)")

if __name__ == "__main__":
    make_contact_svg()
