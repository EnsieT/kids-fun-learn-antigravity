import os
import re

activities_dir = r'c:\Users\user\Desktop\KidsEdu - Antigravity\kids-fun-learn\activities'

def update_activity_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(filepath)
    activity_name = filename.replace('.html', '').replace('-', ' ').title()

    # 1. Update Title and Add Description
    title_pattern = r'<title>.*?</title>'
    new_title = f'<title>{activity_name} 🎮 Kids Fun Learn</title>\n<meta name="description" content="Play {activity_name} and learn with Fun! Kids Fun Learn educational portal."/>'
    if re.search(title_pattern, content):
        content = re.sub(title_pattern, new_title, content)

    # 2. Add ARIA labels to standard elements
    # Home button
    content = content.replace('onclick="goHome()"', 'onclick="goHome()" aria-label="Go Home"')
    
    # 3. Decorative Emojis
    emoji_pattern = r'<span class="card-emoji">(.*?)</span>'
    content = re.sub(emoji_pattern, r'<span class="card-emoji" aria-hidden="true">\1</span>', content)
    
    # 4. Canvas
    content = content.replace('<canvas id="confetti-canvas"></canvas>', '<canvas id="confetti-canvas" aria-hidden="true"></canvas>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for filename in os.listdir(activities_dir):
    if filename.endswith('.html'):
        update_activity_file(os.path.join(activities_dir, filename))

print(f"Updated {len([f for f in os.listdir(activities_dir) if f.endswith('.html')])} activity files.")
