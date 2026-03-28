import os
import re

cur_dir = os.path.dirname(__file__)
act_dir = os.path.join(cur_dir, 'activities')

for fn in os.listdir(act_dir):
    if not fn.endswith('.html'):
        continue
    filepath = os.path.join(act_dir, fn)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Strategy: Replace exact 'const TOTAL_ROUNDS = 10;' or similar.
    # But leave things like sorting-game.html which has `const TOTAL_ROUNDS = ROUND_TYPES.length;` alone for now.
    
    new_content = content.replace("const TOTAL_ROUNDS = 10;", "const TOTAL_ROUNDS = 5;")
    new_content = new_content.replace("let TOTAL_ROUNDS = 10;", "let TOTAL_ROUNDS = 5;")

    if '0/10' in new_content:
        new_content = new_content.replace('>0/10<', '>0/5<')
        
    if "updateProgress(round, 10)" in new_content:
        new_content = new_content.replace("updateProgress(round, 10)", "updateProgress(round, 5)")
        
    # Some specific score-displays
    if 'score-display">0/10<' in content:
        new_content = new_content.replace('score-display">0/10<', 'score-display">0/5<')

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {fn}")
    else:
        print(f"Skipped {fn} (no static TOTAL_ROUNDS=10 found)")

print("Done updating normal round limits.")
