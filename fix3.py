import os
import re
import base64

cur_dir = os.path.dirname(__file__)
act_dir = os.path.join(cur_dir, 'activities')

# 1. Fix silly-story.html undefined variables
silly_path = os.path.join(act_dir, 'silly-story.html')
with open(silly_path, 'r', encoding='utf-8') as f:
    silly = f.read()

silly = silly.replace("item[currentLang]", "item[getCurrentLanguage()]")
silly = silly.replace("banks.who[currentStory.who][currentLang]", "banks.who[currentStory.who][getCurrentLanguage()]")
silly = silly.replace("banks.action[currentStory.action][currentLang]", "banks.action[currentStory.action][getCurrentLanguage()]")
silly = silly.replace("banks.where[currentStory.where][currentLang]", "banks.where[currentStory.where][getCurrentLanguage()]")

with open(silly_path, 'w', encoding='utf-8') as f:
    f.write(silly)
print("Fixed silly-story.html language variable")


# 2. Base64 encode train SVGs to completely bypass DOM/browser URL parsing issues
train_path = os.path.join(act_dir, 'train-track.html')
with open(train_path, 'r', encoding='utf-8') as f:
    train = f.read()

# Original SVGs
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
    b64 = base64.b64encode(v.encode('utf-8')).decode('utf-8')
    # Using strict base64 rules
    css_lines.append(f"    .{k} {{ background-image: url('data:image/svg+xml;base64,{b64}'); }}")

new_css = "\\n".join(css_lines)

# Replace the previous URL-encoded block
train = re.sub(r'    \.track-h \{ background-image: url\(\'data:image/svg\+xml;utf8.*?    \.track-tl \{[^\}]+; \}', new_css, train, flags=re.DOTALL)

with open(train_path, 'w', encoding='utf-8') as f:
    f.write(train)

print("Fixed train SVGs to Base64")
