import sys
from pathlib import Path
from PIL import Image

RAMP = " .`:-=+*cs#%@"  # Bright (0=space) -> Dark (@)

def make_ascii_svg(image_path="source-prepped.png", output_path="jul-ascii.svg", cols=85):
    img_path = Path(image_path)
    if not img_path.exists():
        img_path = Path("source-photo.jpg")
        if not img_path.exists():
            print(f"Error: Neither {image_path} nor source-photo.jpg found.")
            return

    img = Image.open(img_path).convert("L")
    w, h = img.size
    
    # Monospace font aspect ratio correction (~0.52 height/width ratio)
    aspect_ratio = h / w
    rows = int(cols * aspect_ratio * 0.52)
    
    img_resized = img.resize((cols, rows), Image.Resampling.LANCZOS)
    
    ascii_rows = []
    for r in range(rows):
        row_chars = []
        for c in range(cols):
            val = img_resized.getpixel((c, r))
            # Map 255 (white) to 0 (space), 0 (black) to dark glyph
            idx = int((255 - val) / 255 * (len(RAMP) - 1))
            char = RAMP[idx]
            # Replace special XML characters
            if char == "&": char = "&amp;"
            elif char == "<": char = "&lt;"
            elif char == ">": char = "&gt;"
            elif char == '"': char = "&quot;"
            row_chars.append(char)
        ascii_rows.append("".join(row_chars))

    # SVG styling & dimensions
    svg_width = 370
    font_size = 6.6
    line_height = 8.0
    
    margin_top = 45
    margin_left = 16
    
    svg_height = int(margin_top + rows * line_height + 20)

    # Build SVG clip-paths and text rows
    clip_defs = []
    text_elements = []
    
    total_rows = len(ascii_rows)
    row_duration = 0.05
    
    for idx, row_text in enumerate(ascii_rows):
        y_pos = margin_top + idx * line_height
        clip_id = f"row-clip-{idx}"
        delay = round(idx * row_duration, 3)
        
        # Clip rect definition that wipes horizontally
        clip_defs.append(
            f'<clipPath id="{clip_id}">'
            f'<rect x="0" y="{y_pos - line_height}" width="{svg_width}" height="{line_height + 4}">'
            f'<animate attributeName="width" from="0" to="{svg_width}" dur="0.12s" begin="{delay}s" fill="freeze" />'
            f'</rect></clipPath>'
        )
        
        # Text row element using clip-path
        text_elements.append(
            f'<text x="{margin_left}" y="{y_pos}" clip-path="url(#{clip_id})" xml:space="preserve">{row_text}</text>'
        )

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
  <style>
    .bg {{ fill: #0d1117; rx: 10px; ry: 10px; stroke: #30363d; stroke-width: 1px; }}
    .header-bar {{ fill: #161b22; rx: 10px; ry: 10px; }}
    .term-title {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; font-size: 12px; fill: #8b949e; font-weight: 600; }}
    .term-prompt {{ fill: #58a6ff; }}
    
    text {{
      font-family: "SF Mono", Consolas, "Courier New", monospace;
      font-size: {font_size}px;
      fill: #8b949e;
      white-space: pre;
      letter-spacing: 0px;
    }}
  </style>

  <defs>
    {"".join(clip_defs)}
  </defs>

  <!-- Window Frame -->
  <rect x="0" y="0" width="{svg_width}" height="{svg_height}" class="bg" />
  
  <!-- Header Bar -->
  <path d="M 0 10 A 10 10 0 0 1 10 0 L {svg_width - 10} 0 A 10 10 0 0 1 {svg_width} 10 L {svg_width} 32 L 0 32 Z" fill="#161b22" />
  <circle cx="16" cy="16" r="4.5" fill="#ff5f56" />
  <circle cx="30" cy="16" r="4.5" fill="#ffbd2e" />
  <circle cx="44" cy="16" r="4.5" fill="#27c93f" />
  <text x="62" y="20" class="term-title"><tspan class="term-prompt">jul2264@github ~ $</tspan> cat avatar.txt</text>

  <!-- ASCII Character Grid -->
  <g>
    {"".join(text_elements)}
  </g>
</svg>
"""

    out_path = Path(output_path)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Generated ASCII portrait SVG at {out_path} ({len(svg_content)} bytes)")

if __name__ == "__main__":
    make_ascii_svg()
