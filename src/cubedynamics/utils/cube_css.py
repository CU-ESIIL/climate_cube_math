"""Helpers for emitting lightweight CSS cube HTML scaffolding."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

DEFAULT_FACES = {
    "front": "none",
    "back": "none",
    "right": "none",
    "left": "none",
    "top": "none",
    "bottom": "none",
}


def _face_style(face_uri: str) -> str:
    base_style = "background: rgba(255, 255, 255, 0.05);"
    if face_uri.lower() == "none":
        return base_style
    return "background-image: url('{0}'); background-size: cover; background-position: center;".format(
        face_uri
    )


def write_css_cube_static(
    *, out_html: str = "cube_da.html", size_px: int = 260, faces: Dict[str, str] | None = None
) -> Path:
    """Write a standalone HTML page with a simple CSS-based cube skeleton."""

    face_map = {**DEFAULT_FACES, **(faces or {})}
    size = int(size_px)
    half = size / 2

    html = f"""
<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <title>Cube Viewer</title>
  <style>
    :root {{
      --cube-size: {size}px;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 0;
      width: 100%;
      height: 100%;
      background: #0b0e16;
      color: #f7f7f7;
      font-family: system-ui, -apple-system, sans-serif;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }}
    #scene {{
      width: 900px;
      height: 900px;
      position: relative;
      perspective: 1400px;
    }}
    #cube-container {{
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
    }}
    #cube {{
      position: relative;
      width: var(--cube-size);
      height: var(--cube-size);
      transform-style: preserve-3d;
      transform: translateZ(-{half}px) rotateX(-28deg) rotateY(28deg);
      transition: transform 0.3s ease;
    }}
    #cube:hover {{
      transform: translateZ(-{half}px) rotateX(-18deg) rotateY(38deg);
    }}
    .face {{
      position: absolute;
      width: var(--cube-size);
      height: var(--cube-size);
      backface-visibility: hidden;
      border: 1px solid rgba(255, 255, 255, 0.12);
      box-shadow: inset 0 0 20px rgba(0,0,0,0.25);
      background-color: rgba(255,255,255,0.02);
    }}
    #front {{ transform: rotateY(0deg) translateZ({half}px); { _face_style(face_map['front']) } }}
    #back {{ transform: rotateY(180deg) translateZ({half}px); { _face_style(face_map['back']) } }}
    #right {{ transform: rotateY(90deg) translateZ({half}px); { _face_style(face_map['right']) } }}
    #left {{ transform: rotateY(-90deg) translateZ({half}px); { _face_style(face_map['left']) } }}
    #top {{ transform: rotateX(90deg) translateZ({half}px); { _face_style(face_map['top']) } }}
    #bottom {{ transform: rotateX(-90deg) translateZ({half}px); { _face_style(face_map['bottom']) } }}
    #colorbar-container {{
      position: absolute;
      bottom: 40px;
      left: 50%;
      transform: translateX(-50%);
      width: 60%;
      max-width: 420px;
      color: #e0e0e0;
      font-size: 12px;
      text-align: center;
    }}
    #colorbar {{
      width: 100%;
      height: 14px;
      border-radius: 4px;
      background: linear-gradient(90deg, #440154, #3b528b, #21908c, #5dc863, #fde725);
      border: 1px solid rgba(255,255,255,0.15);
      box-shadow: 0 2px 12px rgba(0,0,0,0.45);
    }}
    #colorbar-labels {{
      display: flex;
      justify-content: space-between;
      margin-top: 6px;
      opacity: 0.9;
    }}
  </style>
</head>
<body>
  <div id=\"scene\">
    <div id=\"cube-container\">
      <div id=\"cube\">
        <div class=\"face\" id=\"front\"></div>
        <div class=\"face\" id=\"back\"></div>
        <div class=\"face\" id=\"right\"></div>
        <div class=\"face\" id=\"left\"></div>
        <div class=\"face\" id=\"top\"></div>
        <div class=\"face\" id=\"bottom\"></div>
      </div>
    </div>
    <div id=\"colorbar-container\">
      <div id=\"colorbar\"></div>
      <div id=\"colorbar-labels\">
        <span id=\"cube-cb-min\"></span>
        <span id=\"cube-cb-max\"></span>
      </div>
    </div>
  </div>
  <script>
    (function() {{
      var minEl = document.getElementById('cube-cb-min');
      var maxEl = document.getElementById('cube-cb-max');
      var body = document.body;
      if (body && minEl && maxEl) {{
        minEl.textContent = body.dataset.cbMin || '';
        maxEl.textContent = body.dataset.cbMax || '';
      }}
    }})();
  </script>
</body>
</html>
"""

    out_path = Path(out_html)
    out_path.write_text(html, encoding="utf-8")
    return out_path


__all__ = ["write_css_cube_static", "DEFAULT_FACES"]
