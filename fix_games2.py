import os
import re
import urllib.parse

cur_dir = os.path.dirname(__file__)
act_dir = os.path.join(cur_dir, 'activities')

# 1. Provide empty fallback for playSound in silly-story
silly_path = os.path.join(act_dir, 'silly-story.html')
with open(silly_path, 'r', encoding='utf-8') as f:
    silly = f.read()

if "window.playSound" not in silly:
    silly = silly.replace("<script>", "<script>\nwindow.playSound = function() {};")
    with open(silly_path, 'w', encoding='utf-8') as f:
        f.write(silly)

# 2. Fix playSound and SVGs in train-track
train_path = os.path.join(act_dir, 'train-track.html')
with open(train_path, 'r', encoding='utf-8') as f:
    train = f.read()

if "window.playSound" not in train:
    train = train.replace("<script>", "<script>\nwindow.playSound = function() {};")

# Fully encode SVG data URIs so they actually render in all browsers
svgs = {
    "track-h": "<svg viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'><rect x='0' y='30' width='80' height='20' fill='#9E9E9E'/><rect x='10' y='20' width='10' height='40' fill='#5D4037'/><rect x='35' y='20' width='10' height='40' fill='#5D4037'/><rect x='60' y='20' width='10' height='40' fill='#5D4037'/></svg>",
    "track-v": "<svg viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'><rect x='30' y='0' width='20' height='80' fill='#9E9E9E'/><rect x='20' y='10' width='40' height='10' fill='#5D4037'/><rect x='20' y='35' width='40' height='10' fill='#5D4037'/><rect x='20' y='60' width='40' height='10' fill='#5D4037'/></svg>",
    "track-br": "<svg viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'><path d='M 40 80 Q 40 40 80 40 L 80 60 Q 60 60 60 80 Z' fill='#9E9E9E'/><path d='M 50 80 L 70 80' stroke='#5D4037' stroke-width='10'/><path d='M 80 50 L 80 70' stroke='#5D4037' stroke-width='10'/></svg>",
    "track-bl": "<svg viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'><path d='M 40 80 Q 40 40 0 40 L 0 60 Q 20 60 20 80 Z' fill='#9E9E9E'/></svg>",
    "track-tr": "<svg viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'><path d='M 40 0 Q 40 40 80 40 L 80 20 Q 60 20 60 0 Z' fill='#9E9E9E'/></svg>",
    "track-tl": "<svg viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'><path d='M 40 0 Q 40 40 0 40 L 0 20 Q 20 20 20 0 Z' fill='#9E9E9E'/></svg>"
}

css_lines = []
for k, v in svgs.items():
    encoded = urllib.parse.quote(v)
    css_lines.append(f"    .{k} {{ background-image: url('data:image/svg+xml;utf8,{encoded}'); }}")

new_css = "\n".join(css_lines)

# Regex to completely replace the track SVG CSS blocks to ensure rendering
train = re.sub(r'    \.track-h \{.*?    \.track-tl \{[^\}]*\}', new_css, train, flags=re.DOTALL)

with open(train_path, 'w', encoding='utf-8') as f:
    f.write(train)

print("Fixed train SVGs and playSound fallback")
