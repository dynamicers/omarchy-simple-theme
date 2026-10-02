#!/usr/bin/env python3
"""Render an illustrative theme preview from the real palette (not a screenshot)."""
from pathlib import Path
import base64
import html
import subprocess
import tomllib

root = Path(__file__).resolve().parents[1]
c = tomllib.loads((root / 'colors.toml').read_text())
parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">']

def rect(x, y, w, h, color, stroke=None, radius=0):
    extra = f' stroke="{stroke}" stroke-width="2"' if stroke else ''
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{color}"{extra}/>')

def text(x, y, value, color=None, size=21, family='JetBrains Mono,monospace'):
    parts.append(f'<text x="{x}" y="{y}" fill="{color or c["foreground"]}" font-family="{family}" font-size="{size}">{html.escape(value)}</text>')

wallpaper = base64.b64encode((root / 'backgrounds/01-minimal.png').read_bytes()).decode()
parts.append(f'<image href="data:image/png;base64,{wallpaper}" width="1920" height="1080" preserveAspectRatio="xMidYMid slice"/>')
rect(0, 0, 1920, 42, c['dark_background'])
text(32, 28, 'simple  /  omarchy', size=18)
text(894, 28, '01  02  03', c['light_foreground'], 17)
text(1570, 28, 'quiet by design', c['light_foreground'], 17)

# Editor: the sidebar and main surface use different theme tokens.
rect(86, 176, 1058, 624, c['background'], c['hyprland_active_border'])
rect(88, 178, 1054, 46, c['dark_background'])
text(113, 208, 'simple.py', c['bright_foreground'], 18)
text(986, 208, 'EDITOR', c['dark_foreground'], 15)
rect(88, 224, 218, 540, c['dark_background'])
text(111, 267, 'EXPLORER', c['light_foreground'], 16)
text(111, 316, 'simple/', size=19)
text(131, 355, 'backgrounds', c['light_foreground'], 17)
rect(98, 373, 194, 35, c['selection'])
text(131, 397, 'colors.toml', c['bright_foreground'], 17)
text(131, 437, 'README.md', c['light_foreground'], 17)
text(131, 477, 'simple.py', c['light_foreground'], 17)
lines = [
    [('comment', '# A calmer space to think.')],
    [('magenta', 'from '), ('foreground', 'pathlib '), ('magenta', 'import '), ('yellow', 'Path')],
    [],
    [('magenta', 'class '), ('yellow', 'Simple'), ('foreground', ':')],
    [('foreground', '    background = '), ('green', '"#181b1a"')],
    [('foreground', '    sidebar    = '), ('green', '"#141716"')],
    [('foreground', '    accent     = '), ('green', '"#7d9fb5"')],
    [],
    [('magenta', '    def '), ('blue', 'apply'), ('foreground', '(self):')],
    [('foreground', '        palette = '), ('yellow', 'Path'), ('foreground', '('), ('green', '"colors.toml"'), ('foreground', ')')],
    [('magenta', '        return '), ('foreground', 'palette.read_text()')],
    [],
    [('comment', '# Muted color. Clear focus. No distraction.')],
]
for i, tokens in enumerate(lines):
    y = 267 + i * 35
    text(326, y, str(i + 1), c['dark_foreground'], 18)
    x = 378
    for key, value in tokens:
        text(x, y, value, c['dark_foreground'] if key == 'comment' else c[key], 21)
        x += len(value) * 12.65
rect(88, 764, 1054, 34, c['dark_background'])
text(111, 787, 'NORMAL', c['green'], 16)
text(850, 787, 'Python   UTF-8   13:1', c['light_foreground'], 16)

# Terminal demo contains only synthetic content.
rect(1172, 176, 664, 422, c['background'], c['hyprland_inactive_border'])
rect(1174, 178, 660, 46, c['dark_background'])
text(1198, 208, 'foot', c['light_foreground'], 18)
text(1198, 266, '> simple', c['blue'], 23)
text(1198, 311, 'simple', c['bright_foreground'], 34)
text(1198, 351, 'A quiet theme for Omarchy.', size=20)
text(1198, 401, 'surfaces  charcoal / green-gray', c['light_foreground'], 19)
text(1198, 438, 'palette   muted One Dark', c['light_foreground'], 19)
text(1198, 475, 'focus     slate blue-gray', c['light_foreground'], 19)
for i, key in enumerate(['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'magenta']):
    rect(1200 + i * 79, 517, 62, 18, c[key], radius=3)
text(1198, 571, '> _', c['green'], 22)

rect(1172, 622, 664, 178, c['lighter_background'], '#434a48')
text(1198, 662, 'Less noise. More room.', c['bright_foreground'], 24)
text(1198, 704, 'Soft accents, layered dark surfaces', c['light_foreground'], 19)
text(1198, 738, 'and a subtle, recognizable focus border.', c['light_foreground'], 19)
text(92, 920, 'simple', c['bright_foreground'], 58, 'sans-serif')
text(94, 964, 'Muted One Dark · green-gray surfaces · four wallpapers', c['light_foreground'], 22, 'sans-serif')
text(94, 1023, 'Illustrative palette preview — not a desktop screenshot', c['light_foreground'], 15, 'sans-serif')
parts.append('</svg>')
svg = root / 'docs/preview.svg'
svg.write_text('\n'.join(parts))
subprocess.run(['rsvg-convert', str(svg), '-o', str(root / 'preview.png')], check=True)
print(root / 'preview.png')
