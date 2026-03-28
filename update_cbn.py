import os
import re

cur_dir = os.path.dirname(__file__)
act_dir = os.path.join(cur_dir, 'activities')

scene_val = """const SCENES = [
  // 1: Sunny Farmville
  {
    name: 'Farm 🚜', colors: [1,2,3,4,5,6],
    regions: [
      {id:'sky', num:2, label:'Sky', path:'<rect id="sky" x="0" y="0" width="400" height="200" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'sun', num:4, label:'Sun', path:'<circle id="sun" cx="330" cy="70" r="45" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'cloud1', num:6, label:'Cloud1', path:'<ellipse id="cloud1" cx="100" cy="60" rx="40" ry="20" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'cloud2', num:6, label:'Cloud2', path:'<ellipse id="cloud2" cx="220" cy="90" rx="50" ry="25" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'grass', num:3, label:'Grass', path:'<rect id="grass" x="0" y="200" width="400" height="200" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'house_w', num:1, label:'Wall', path:'<rect id="house_w" x="50" y="160" width="120" height="100" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'house_r', num:5, label:'Roof', path:'<polygon id="house_r" points="110,90 30,160 190,160" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'house_d', num:6, label:'Door', path:'<rect id="house_d" x="90" y="200" width="40" height="60" rx="4" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'tractor_b', num:1, label:'Tractor', path:'<rect id="tractor_b" x="220" y="240" width="100" height="50" rx="8" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'tractor_c', num:5, label:'Cab', path:'<rect id="tractor_c" x="270" y="190" width="50" height="50" rx="4" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'wheel_b', num:6, label:'Wheel1', path:'<circle id="wheel_b" cx="300" cy="290" r="25" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'wheel_s', num:6, label:'Wheel2', path:'<circle id="wheel_s" cx="240" cy="300" r="15" class="cbn-region" fill="#E0E0E0"/>'}
    ]
  },
  // 2: Under the Sea
  {
    name: 'Ocean 🐠', colors: [2,3,4,5,7,1],
    regions: [
      {id:'water', num:2, label:'Water', path:'<rect id="water" x="0" y="0" width="400" height="320" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'sand', num:4, label:'Sand', path:'<ellipse id="sand" cx="200" cy="360" rx="250" ry="60" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'sub_b', num:4, label:'Sub Base', path:'<ellipse id="sub_b" cx="200" cy="180" rx="80" ry="40" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'sub_t', num:5, label:'Sub Top', path:'<rect id="sub_t" x="170" y="120" width="40" height="40" rx="5" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'sub_w1', num:2, label:'Win1', path:'<circle id="sub_w1" cx="160" cy="180" r="15" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'sub_w2', num:2, label:'Win2', path:'<circle id="sub_w2" cx="200" cy="180" r="15" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'sub_w3', num:2, label:'Win3', path:'<circle id="sub_w3" cx="240" cy="180" r="15" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'fish1', num:5, label:'Fish1', path:'<ellipse id="fish1" cx="80" cy="100" rx="25" ry="15" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'fish1t', num:1, label:'Tail1', path:'<polygon id="fish1t" points="55,100 35,85 35,115" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'fish2', num:7, label:'Fish2', path:'<ellipse id="fish2" cx="320" cy="240" rx="20" ry="12" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'weed1', num:3, label:'Weed', path:'<path id="weed1" d="M 60 400 Q 70 300 50 250 Q 30 200 60 150" class="cbn-region" fill="none" stroke="#E0E0E0" stroke-width="12"/>'},
      {id:'weed2', num:3, label:'Weed', path:'<path id="weed2" d="M 350 400 Q 330 300 350 250 Q 360 200 330 160" class="cbn-region" fill="none" stroke="#E0E0E0" stroke-width="12"/>'}
    ]
  },
  // 3: Space Adventure
  {
    name: 'Space 🚀', colors: [6,2,4,1,3,7],
    regions: [
      {id:'space', num:6, label:'Space Base', path:'<rect id="space" x="0" y="0" width="400" height="400" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'planet1', num:4, label:'Planet1', path:'<circle id="planet1" cx="80" cy="90" r="50" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'ring1', num:3, label:'Ring', path:'<ellipse id="ring1" cx="80" cy="90" rx="80" ry="15" class="cbn-region" fill="#E0E0E0" transform="rotate(20 80 90)"/>'},
      {id:'moon', num:2, label:'Moon', path:'<circle id="moon" cx="300" cy="300" r="70" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'crater1', num:6, label:'Crater1', path:'<circle id="crater1" cx="280" cy="280" r="15" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'crater2', num:6, label:'Crater2', path:'<circle id="crater2" cx="330" cy="320" r="10" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'rocket_b', num:1, label:'Rocket Base', path:'<polygon id="rocket_b" points="200,100 170,220 230,220" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'rocket_w', num:2, label:'Window', path:'<circle id="rocket_w" cx="200" cy="160" r="12" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'rocket_f1', num:7, label:'Fin1', path:'<polygon id="rocket_f1" points="170,220 150,250 180,220" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'rocket_f2', num:7, label:'Fin2', path:'<polygon id="rocket_f2" points="230,220 250,250 220,220" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'flame', num:4, label:'Flame', path:'<polygon id="flame" points="180,220 220,220 200,280" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'star1', num:4, label:'Star', path:'<circle id="star1" cx="350" cy="50" r="6" class="cbn-region" fill="#E0E0E0"/>'},
      {id:'star2', num:4, label:'Star', path:'<circle id="star2" cx="50" cy="300" r="5" class="cbn-region" fill="#E0E0E0"/>'}
    ]
  }
];"""

cbn_path = os.path.join(act_dir, 'color-by-number.html')
with open(cbn_path, 'r', encoding='utf-8') as f:
    cbn_content = f.read()

# Replace SCENES block
cbn_content = re.sub(r'const SCENES = \[.*?\];', scene_val, cbn_content, flags=re.DOTALL)

# Also update the scene buttons in DOM
new_buttons = """<button class="scene-btn active" onclick="loadScene(0,this)">🚜 Farm</button>
    <button class="scene-btn" onclick="loadScene(1,this)">🐠 Ocean</button>
    <button class="scene-btn" onclick="loadScene(2,this)">🚀 Space</button>"""
cbn_content = re.sub(r'<button class="scene-btn active" onclick="loadScene\(0,this\)">.*?</button>.*?<button class="scene-btn" onclick="loadScene\(3,this\)">.*?</button>', new_buttons, cbn_content, flags=re.DOTALL)

with open(cbn_path, 'w', encoding='utf-8') as f:
    f.write(cbn_content)
    
print("Updated color-by-number.")
