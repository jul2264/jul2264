import os
from pathlib import Path

def make_info_card(output_path="info-card.svg"):
    svg_width = 490
    svg_height = 430
    
    is_static = os.environ.get("STATIC", "0") == "1"

    lines = [
        {"key": "User", "val": "juliansteve (Julian Steve)", "key_color": "#58a6ff"},
        {"type": "sep"},
        {"key": "OS", "val": "SRMIST Sophomore (Computer Science)", "key_color": "#79c0ff"},
        {"key": "Focus", "val": "DSA Fundamentals & System Design", "key_color": "#d2a8ff"},
        {"key": "Languages", "val": "Python, C++, Go, Java, JS, HTML/CSS", "key_color": "#7ee787"},
        {"key": "Stack", "val": "FastAPI, React, Docker, Linux, Postgres, Redis", "key_color": "#ffa657"},
        {"key": "Security", "val": "Wireshark, Nmap, Burp Suite, Radare2, SQLMap", "key_color": "#ff7b72"},
        {"key": "Socials", "val": "LinkedIn: juliansteve | Email: juliansteve.anban", "key_color": "#a5d6ff"},
        {"type": "sep"},
    ]

    palette_colors = ["#ff5f56", "#ffbd2e", "#27c93f", "#58a6ff", "#bc8cff", "#39d353", "#ffa657", "#c9d1d9"]

    y_start = 55
    line_step = 32

    rows_xml = []
    anim_delay = 0.08

    for idx, line in enumerate(lines):
        y = y_start + idx * line_step
        delay = round(anim_delay, 2)

        if line.get("type") == "sep":
            inner = f'<line x1="30" y1="{y - 8}" x2="{svg_width - 30}" y2="{y - 8}" stroke="#30363d" stroke-width="1" stroke-dasharray="4 4" />'
        else:
            key = line["key"]
            val = line["val"]
            kc = line["key_color"]
            inner = (
                f'<text x="30" y="{y}" class="key-text" fill="{kc}">{key.ljust(11)}:</text>'
                f'<text x="145" y="{y}" class="val-text">{val}</text>'
            )

        if not is_static:
            smil = (
                f'<animate attributeName="opacity" values="0;1" keyTimes="0;1" dur="0.35s" begin="{delay}s" fill="freeze" />'
                f'<animateTransform attributeName="transform" type="translate" values="-10,0;0,0" keyTimes="0;1" dur="0.35s" begin="{delay}s" fill="freeze" />'
            )
            rows_xml.append(f'<g>{smil}{inner}</g>')
        else:
            rows_xml.append(f'<g>{inner}</g>')

        anim_delay += 0.05

    palette_y = y_start + len(lines) * line_step + 10
    palette_xml = []
    for i, pcol in enumerate(palette_colors):
        px = 30 + i * 22
        palette_xml.append(f'<circle cx="{px + 6}" cy="{palette_y}" r="7" fill="{pcol}" />')

    if not is_static:
        delay = round(anim_delay, 2)
        smil = (
            f'<animate attributeName="opacity" values="0;1" keyTimes="0;1" dur="0.35s" begin="{delay}s" fill="freeze" />'
            f'<animateTransform attributeName="transform" type="translate" values="-10,0;0,0" keyTimes="0;1" dur="0.35s" begin="{delay}s" fill="freeze" />'
        )
        palette_group = f'<g>{smil}{"".join(palette_xml)}</g>'
    else:
        palette_group = f'<g>{"".join(palette_xml)}</g>'

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
  <style>
    .bg {{ fill: #0d1117; rx: 10px; ry: 10px; stroke: #30363d; stroke-width: 1px; }}
    .header-bar {{ fill: #161b22; rx: 10px; ry: 10px; }}
    .term-title {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 12px; fill: #8b949e; font-weight: 600; }}
    .term-prompt {{ fill: #58a6ff; }}
    
    .key-text {{
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 12.5px;
      font-weight: bold;
    }}
    
    .val-text {{
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 12.5px;
      fill: #c9d1d9;
    }}
  </style>

  <!-- Frame -->
  <rect x="0" y="0" width="{svg_width}" height="{svg_height}" class="bg" />
  
  <!-- Header Bar -->
  <path d="M 0 10 A 10 10 0 0 1 10 0 L {svg_width - 10} 0 A 10 10 0 0 1 {svg_width} 10 L {svg_width} 32 L 0 32 Z" fill="#161b22" />
  <circle cx="16" cy="16" r="4.5" fill="#ff5f56" />
  <circle cx="30" cy="16" r="4.5" fill="#ffbd2e" />
  <circle cx="44" cy="16" r="4.5" fill="#27c93f" />
  <text x="62" y="20" class="term-title"><tspan class="term-prompt">jul2264@github ~ $</tspan> neofetch</text>

  <!-- Content Rows -->
  <g>
    {"".join(rows_xml)}
    {palette_group}
  </g>
</svg>
"""

    out_path = Path(output_path)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Generated info card SVG at {out_path} ({len(svg_content)} bytes)")

if __name__ == "__main__":
    make_info_card()
