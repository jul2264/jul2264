import json
from pathlib import Path
from datetime import datetime

PALETTE = [
    "#161b22",  # 0: None
    "#0e4429",  # 1: Low
    "#006d32",  # 2: Med-Low
    "#26a641",  # 3: Med-High
    "#39d353",  # 4: High
    "#69f0a0"   # 5: Neon Top
]

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAY_NAMES = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

def render_heatmap_svg():
    json_path = Path("data/contributions.json")
    if not json_path.exists():
        print("data/contributions.json not found, skipping heatmap render.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    days = data.get("days", [])
    total_contribs = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)
    username = data.get("username", "jul2264")

    # Group days into weeks (each week has 7 days starting Sunday)
    weeks = []
    current_week = []
    
    for day in days:
        dt = datetime.strptime(day["date"], "%Y-%m-%d")
        wday = (dt.weekday() + 1) % 7  # 0=Sunday, 1=Monday...
        
        if wday == 0 and current_week:
            weeks.append(current_week)
            current_week = []
        
        current_week.append({
            "date": day["date"],
            "count": day["count"],
            "level": min(day["level"], 5),
            "wday": wday,
            "dt": dt
        })
        
    if current_week:
        weeks.append(current_week)

    weeks = weeks[-53:]

    month_labels = []
    last_month = -1
    for w_idx, week in enumerate(weeks):
        if week:
            m = week[0]["dt"].month
            if m != last_month:
                month_labels.append((w_idx, MONTH_NAMES[m - 1]))
                last_month = m

    svg_width = 860
    svg_height = 230
    
    grid_x_start = 55
    grid_y_start = 75
    box_size = 11
    box_gap = 3
    step = box_size + box_gap

    rects_xml = []
    for col_idx, week in enumerate(weeks):
        for day in week:
            row_idx = day["wday"]
            x = grid_x_start + col_idx * step
            y = grid_y_start + row_idx * step
            color = PALETTE[day["level"]]
            
            delay = round((col_idx + row_idx) * 0.02, 3)
            smil_anim = f'<animate attributeName="opacity" values="0;1" keyTimes="0;1" dur="0.3s" begin="{delay}s" fill="freeze"/>'
            
            rect_str = (
                f'<rect class="day-box" x="{x}" y="{y}" width="{box_size}" height="{box_size}" rx="2.5" ry="2.5" '
                f'fill="{color}">'
                f'{smil_anim}'
                f'<title>{day["count"]} contributions on {day["date"]}</title></rect>'
            )
            rects_xml.append(rect_str)

    months_xml = []
    for w_idx, name in month_labels:
        mx = grid_x_start + w_idx * step
        months_xml.append(f'<text x="{mx}" y="{grid_y_start - 8}" class="label">{name}</text>')

    day_labels_xml = []
    for r_idx, name in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        dy = grid_y_start + r_idx * step + 9
        day_labels_xml.append(f'<text x="25" y="{dy}" class="label">{name}</text>')

    legend_x = svg_width - 150
    legend_y = svg_height - 22
    legend_boxes = []
    for i, pcol in enumerate(PALETTE):
        lx = legend_x + 32 + i * 14
        legend_boxes.append(f'<rect x="{lx}" y="{legend_y - 9}" width="10" height="10" rx="2" fill="{pcol}"/>')

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
  <style>
    .bg {{ fill: #0d1117; rx: 10px; ry: 10px; stroke: #30363d; stroke-width: 1px; }}
    .header-bar {{ fill: #161b22; rx: 10px; ry: 10px; }}
    .term-title {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 13px; fill: #8b949e; font-weight: 600; }}
    .term-prompt {{ fill: #58a6ff; }}
    .label {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 10px; fill: #7d8590; }}
    .stats-text {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 11px; fill: #c9d1d9; }}
    .highlight-val {{ fill: #39d353; font-weight: bold; }}
  </style>

  <!-- Card Frame -->
  <rect x="0" y="0" width="{svg_width}" height="{svg_height}" class="bg" />
  
  <!-- Terminal Header Bar -->
  <path d="M 0 10 A 10 10 0 0 1 10 0 L {svg_width - 10} 0 A 10 10 0 0 1 {svg_width} 10 L {svg_width} 36 L 0 36 Z" fill="#161b22" />
  <circle cx="20" cy="18" r="5" fill="#ff5f56" />
  <circle cx="36" cy="18" r="5" fill="#ffbd2e" />
  <circle cx="52" cy="18" r="5" fill="#27c93f" />
  <text x="75" y="22" class="term-title"><tspan class="term-prompt">{username}@github ~ $</tspan> ./contributions.sh</text>

  <!-- Month & Day Labels -->
  {"".join(months_xml)}
  {"".join(day_labels_xml)}

  <!-- Grid Cells -->
  <g>
    {"".join(rects_xml)}
  </g>

  <!-- Footer Stats -->
  <text x="25" y="{svg_height - 18}" class="stats-text">
    <tspan class="highlight-val">{total_contribs:,}</tspan> contributions in the last year
    │ Streak: <tspan class="highlight-val">{current_streak}d</tspan> (best: <tspan class="highlight-val">{longest_streak}d</tspan>)
  </text>

  <!-- Legend -->
  <g class="label">
    <text x="{legend_x}" y="{legend_y}">Less</text>
    {"".join(legend_boxes)}
    <text x="{legend_x + 108}" y="{legend_y}">More</text>
  </g>
</svg>
"""

    out_path = Path("contrib-heatmap.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Generated heatmap SVG at {out_path} ({len(svg_content)} bytes)")

if __name__ == "__main__":
    render_heatmap_svg()
