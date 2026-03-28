"""Update SEO meta descriptions and add OG tags to all activity HTML files."""
import os
import re

ACTIVITIES_DIR = os.path.join(os.path.dirname(__file__), 'activities')

# Better descriptions per activity
DESCRIPTIONS = {
    'balloon-pop': 'Pop colorful balloons by tapping the right answers! A fun reaction game for kids aged 4-6 on Kids Fun Learn.',
    'block-builder': 'Build colorful block patterns by placing shapes on a grid. A creative puzzle game for children aged 4-6.',
    'catch-it': 'Catch falling objects by tapping them before they disappear! A fast and fun reflex game for kids aged 4-6.',
    'color-by-number': 'Learn colors and numbers together by painting beautiful pictures. A creative activity for children aged 4-6.',
    'concept-match': 'Match related concepts together to build thinking skills. An educational matching game for kids aged 4-6.',
    'counting': 'Learn to count objects from 1 to 9 with fun emojis and voice support. An interactive counting game for ages 4-6.',
    'drawing': 'Express your creativity with a free drawing canvas! Pick colors, brushes, and stamps in this art activity for kids.',
    'identify-animals': 'Identify different animals by their emoji pictures. A fun wildlife recognition game for children aged 4-6.',
    'identify-fruits': 'Learn to recognize fruits and vegetables by their pictures. A healthy eating awareness game for kids aged 4-6.',
    'jigsaw': 'Solve colorful jigsaw puzzles by dragging pieces into place. A brain-training puzzle game for children aged 4-6.',
    'letter-sounds': 'Learn the sounds that letters make with interactive phonics activities. Perfect for early readers aged 4-6.',
    'match-columns': 'Draw lines to match items from two columns. A visual connection game that builds logical thinking for ages 4-6.',
    'math': 'Practice simple addition and subtraction with fun emoji visuals. An interactive math game for children aged 5-6.',
    'maze': 'Navigate through exciting mazes from start to finish! A problem-solving adventure game for kids aged 4-6.',
    'memory-game': 'Flip cards to find matching pairs and train your memory. A classic memory challenge for children aged 4-6.',
    'music': 'Create your own music by playing virtual instruments! A creative sound exploration activity for kids aged 4-6.',
    'number-line': 'Jump along the number line to reach the target number. A visual math activity for children aged 5-6.',
    'odd-one-out': 'Find the item that does not belong in each group. A critical thinking game for children aged 5-6.',
    'pattern': 'Complete the pattern by choosing the right emoji. A sequence recognition game for kids aged 5-6.',
    'pattern-complete': 'Figure out what comes next in the pattern sequence. An advanced pattern recognition game for ages 5-6.',
    'rhyming-sort': 'Sort words by their rhyming sounds into the right groups. A phonics and reading activity for kids aged 4-6.',
    'shadow-match': 'Match objects to their shadows! A visual perception game that builds observation skills for ages 4-6.',
    'shape-matching': 'Match shapes by dragging them to their correct partners. A geometry recognition game for children aged 5-6.',
    'sorting-game': 'Sort items into the correct baskets by category. A classification game that builds logical thinking for ages 5-6.',
    'sound-bingo': 'Listen to sounds and mark the matching pictures on your bingo card. An auditory learning game for kids aged 4-6.',
    'tower-build': 'Stack blocks to build the tallest tower you can! A physics and balance game for children aged 4-6.',
    'tracing': 'Trace letters and shapes with your finger or mouse. A handwriting practice activity for kids aged 4-6.',
    'whats-missing': 'Study a scene, then figure out what disappeared! A memory and observation game for children aged 4-6.',
}

# Friendly display names 
DISPLAY_NAMES = {
    'balloon-pop': 'Balloon Pop',
    'block-builder': 'Block Builder',
    'catch-it': 'Catch It',
    'color-by-number': 'Color by Number',
    'concept-match': 'Concept Match',
    'counting': 'Counting Game',
    'drawing': 'Free Drawing',
    'identify-animals': 'Animal Fun',
    'identify-fruits': 'Fruits & Veggies',
    'jigsaw': 'Jigsaw Puzzle',
    'letter-sounds': 'Letter Sounds',
    'match-columns': 'Match Columns',
    'math': 'Simple Math',
    'maze': 'Maze Adventure',
    'memory-game': 'Memory Game',
    'music': 'Music Maker',
    'number-line': 'Number Line Jump',
    'odd-one-out': 'Odd One Out',
    'pattern': 'Pattern Game',
    'pattern-complete': 'What Comes Next?',
    'rhyming-sort': 'Rhyming Sort',
    'shadow-match': 'Shadow Match',
    'shape-matching': 'Shape Matching',
    'sorting-game': 'Sort into Baskets',
    'sound-bingo': 'Sound Bingo',
    'tower-build': 'Tower Build',
    'tracing': 'Tracing Fun',
    'whats-missing': "What's Missing?",
}

def update_activity_file(filepath, activity_key):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    desc = DESCRIPTIONS.get(activity_key, '')
    name = DISPLAY_NAMES.get(activity_key, activity_key.replace('-', ' ').title())
    
    if not desc:
        print(f"  SKIP {activity_key}: no description defined")
        return False
    
    # 1. Update meta description to be more specific
    old_desc_pattern = r'<meta name="description" content="[^"]*"/>'
    new_desc = f'<meta name="description" content="{desc}"/>'
    content = re.sub(old_desc_pattern, new_desc, content)
    
    # 2. Add OG tags if not present
    if 'og:title' not in content:
        og_tags = f'\n<meta property="og:title" content="{name} 🎮 Kids Fun Learn"/>\n<meta property="og:description" content="{desc}"/>\n<meta property="og:type" content="website"/>'
        # Insert after meta description
        content = content.replace(new_desc, new_desc + og_tags)
    
    # 3. Add theme-color if not present 
    if 'theme-color' not in content:
        content = content.replace('</head>', '<meta name="theme-color" content="#FFD700"/>\n</head>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  UPDATED {activity_key}")
    return True

def main():
    count = 0
    for filename in sorted(os.listdir(ACTIVITIES_DIR)):
        if not filename.endswith('.html'):
            continue
        activity_key = filename.replace('.html', '')
        filepath = os.path.join(ACTIVITIES_DIR, filename)
        if update_activity_file(filepath, activity_key):
            count += 1
    print(f"\nDone! Updated {count} activity files.")

if __name__ == '__main__':
    main()
