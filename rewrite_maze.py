import os
import re

cur_dir = os.path.dirname(__file__)
act_dir = os.path.join(cur_dir, 'activities')
maze_path = os.path.join(act_dir, 'maze.html')

with open(maze_path, 'r', encoding='utf-8') as f:
    maze = f.read()

# 1. Remove the Difficulty Buttons UI
maze = re.sub(r'<div id="difficulty-btns">.*?</div>', '', maze, flags=re.DOTALL)

# 1.5 Remove the Next Level button from completion screen
maze = re.sub(r'<button class="play-again-btn" id="next-lvl-btn".*?</button>', '', maze, flags=re.DOTALL)

# 2. Modify the JS to use a bank of 20 randomized seeds and a 5-round limit
js_logic_replacement = """/* ── Config & Bank ── */
const TOTAL_ROUNDS = 5;
let round = 0;
let totalMistakes = 0;

// Bank of 20 distinct mazes spanning multiple sizes and shapes
const MAZE_BANK = [
  { size: 5, cs: 64, seed: 10 }, { size: 5, cs: 64, seed: 42 },
  { size: 5, cs: 64, seed: 88 }, { size: 5, cs: 64, seed: 150 },
  { size: 6, cs: 56, seed: 23 }, { size: 6, cs: 56, seed: 111 },
  { size: 6, cs: 56, seed: 210 }, { size: 6, cs: 56, seed: 333 },
  { size: 6, cs: 56, seed: 444 }, { size: 6, cs: 56, seed: 555 },
  { size: 7, cs: 46, seed: 137 }, { size: 7, cs: 46, seed: 250 },
  { size: 7, cs: 46, seed: 388 }, { size: 7, cs: 46, seed: 501 },
  { size: 7, cs: 46, seed: 700 }, { size: 8, cs: 40, seed: 11 },
  { size: 8, cs: 40, seed: 99 }, { size: 8, cs: 40, seed: 400 },
  { size: 9, cs: 36, seed: 777 }, { size: 9, cs: 36, seed: 999 }
];

let roundBank = []; // The 5 selected challenges

const WALL_CLR  = '#5C3D11';
const WALL_W    = '4px';
const OPEN_CLR  = 'rgba(180,150,100,0.15)';
const OPEN_W    = '1px';

let mazeWalls = null, currentPos = {r:0,c:0};
let visitedSet = new Set(), wrongMoves = 0, stepCount = 0, gameWon = false;

const MAZE_THEMES = [
  {p_en:'Help the cow reach the grass!', p_hi:'गाय को घास तक पहुंचाओ!', p_gu:'ગાયને ઘાસ સુધી પહોંચાડો!', hero:'🐄', goal:'🌾'},
  {p_en:'Help the bunny reach the carrot!', p_hi:'खरगोश को गाजर तक पहुंचाओ!', p_gu:'સસલાને ગાજર સુધી પહોંચાડો!', hero:'🐇', goal:'🥕'},
  {p_en:'Help the monkey reach the banana!', p_hi:'बंदर को केले तक पहुंचाओ!', p_gu:'વાંદરાને કેળા સુધી પહોંચાડો!', hero:'🐒', goal:'🍌'},
  {p_en:'Help the bee reach the flower!', p_hi:'मधुमक्खी को फूल तक पहुंचाओ!', p_gu:'મધમાખીને ફૂલ સુધી પહોંચાડો!', hero:'🌸', goal:'🍯'},
  {p_en:'Help the squirrel reach the nut!', p_hi:'गिलहरी को अखरोट तक पहुंचाओ!', p_gu:'ખિસકોલીને અખરોટ સુધી પહોંચાડો!', hero:'🐿️', goal:'🥜'},
  {p_en:'Help the fish reach the coral!', p_hi:'मछली को मूंगे तक पहुंचाओ!', p_gu:'માછલીને પરવાળા સુધી પહોંચાડો!', hero:'🐠', goal:'🪸'},
  {p_en:'Help the astronaut reach the planet!', p_hi:'अंतरिक्ष यात्री को ग्रह तक पहुंचाओ!', p_gu:'અંતરિક્ષયાત્રીને ગ્રહ સુધી પહોંચાડો!', hero:'👨‍🚀', goal:'🪐'},
  {p_en:'Help the car reach the house!', p_hi:'कार को घर तक पहुंचाओ!', p_gu:'કારને ઘર સુધી પહોંચાડો!', hero:'🚗', goal:'🏠'}
];
let currentTheme = MAZE_THEMES[0];

function onLanguageChange() {
  updatePromptText();
}

function updatePromptText() {
  const p = {en:currentTheme.p_en, hi:currentTheme.p_hi, gu:currentTheme.p_gu};
  document.getElementById('prompt-text').textContent = t(p);
}

function initGame() {
  round = 0; totalMistakes = 0;
  roundBank = shuffle(MAZE_BANK).slice(0, TOTAL_ROUNDS);
  hideFeedback();
  document.getElementById('completion-screen').classList.remove('show');
  const gameArea = document.getElementById('game-area');
  if(gameArea) {
    gameArea.classList.remove('hidden');
    gameArea.style.filter = 'none';
  }
  loadRound();
}

function loadRound() {
  updateProgress(round, TOTAL_ROUNDS);
  if (round >= TOTAL_ROUNDS) { endGame(); return; }
  
  gameWon=false; wrongMoves=0; stepCount=0;
  currentPos={r:0,c:0}; visitedSet=new Set(['0,0']);
  
  currentTheme = pickRandom(MAZE_THEMES, 1)[0];
  
  const conf = roundBank[round];
  mazeWalls = generateMaze(conf.size, conf.seed + Math.floor(Math.random() * 100)); // Dynamic variation
  
  updateStats(); 
  renderMaze(); 
  updatePromptText();
  setTimeout(()=>speak({en:currentTheme.p_en, hi:currentTheme.p_hi, gu:currentTheme.p_gu}), 300);
}

function updateStats() {
  document.getElementById('wrong-count').textContent = `❌ ${wrongMoves}`;
  document.getElementById('steps-count').textContent = `👣 ${stepCount}`;
}

function renderMaze() {
  const conf = roundBank[round];
  const {size, cs} = conf;
  const grid = document.getElementById('maze-grid');
  grid.style.gridTemplateColumns = `repeat(${size},${cs}px)`;
  grid.innerHTML = '';

  for (let r=0; r<size; r++) {
    for (let c=0; c<size; c++) {
      const cell = document.createElement('div');
      cell.className = 'maze-cell';
      cell.style.width  = cs+'px';
      cell.style.height = cs+'px';
      cell.style.fontSize = Math.floor(cs*.62)+'px';
      cell.dataset.r = r; cell.dataset.c = c;

      const w = mazeWalls[r][c];
      cell.style.borderTop    = w.N ? `${WALL_W} solid ${WALL_CLR}` : `${OPEN_W} solid ${OPEN_CLR}`;
      cell.style.borderLeft   = w.W ? `${WALL_W} solid ${WALL_CLR}` : `${OPEN_W} solid ${OPEN_CLR}`;
      cell.style.borderRight  = (c===size-1) ? `${WALL_W} solid ${WALL_CLR}` : `${OPEN_W} solid ${OPEN_CLR}`;
      cell.style.borderBottom = (r===size-1) ? `${WALL_W} solid ${WALL_CLR}` : `${OPEN_W} solid ${OPEN_CLR}`;

      const isCurrent = r===currentPos.r && c===currentPos.c;
      const isEnd     = r===size-1 && c===size-1;
      if (visitedSet.has(`${r},${c}`) && !isCurrent) cell.classList.add('visited');
      if (isCurrent)  cell.classList.add('current');
      if (isEnd)      cell.classList.add('end-cell');

      if (isCurrent) { const sp=document.createElement('span'); sp.textContent=currentTheme.hero; cell.appendChild(sp); }
      else if (isEnd) { const sp=document.createElement('span'); sp.textContent=currentTheme.goal; cell.appendChild(sp); }

      cell.addEventListener('pointerdown', onCellPointer);
      grid.appendChild(cell);
    }
  }
}

function onCellPointer(e) {
  e.preventDefault();
  if (gameWon) return;
  handleMove(parseInt(e.currentTarget.dataset.r), parseInt(e.currentTarget.dataset.c));
}

function handleMove(r, c) {
  const {r:cr, c:cc} = currentPos;
  const dr=r-cr, dc=c-cc;
  if (Math.abs(dr)+Math.abs(dc)!==1) return;

  const dir = dr===-1?'N': dr===1?'S': dc===-1?'W':'E';

  if (mazeWalls[cr][cc][dir]) {
    wrongMoves++; updateStats();
    speak({en:"That's a wall!",hi:'यह दीवार है!',gu:'આ દીવાલ છે!'});
    const size = roundBank[round].size;
    const idx = cr*size+cc;
    const cells = document.querySelectorAll('.maze-cell');
    if (cells[idx]) {
      cells[idx].classList.remove('shake');
      void cells[idx].offsetWidth;
      cells[idx].classList.add('shake');
      setTimeout(()=> {if(cells[idx]) cells[idx].classList.remove('shake');}, 350);
    }
    return;
  }

  visitedSet.add(`${r},${c}`);
  currentPos={r,c}; stepCount++; updateStats(); renderMaze();

  const size = roundBank[round].size;
  if (r===size-1 && c===size-1) {
    gameWon=true;
    totalMistakes += wrongMoves;
    speak({en:'You made it! Great job!', hi:'वाह! बहुत अच्छा!', gu:'વાહ! બહુ સારું!'});
    launchConfetti();
    setTimeout(() => {
        round++;
        loadRound();
    }, 1500);
  }
}

function endGame() {
  showCompletion('maze', totalMistakes, TOTAL_ROUNDS);
}

document.addEventListener('DOMContentLoaded', () => { initLanguageSelector(); initGame(); });
"""

# Inject using regex up until the end 
maze = re.sub(r'/\* ── Config ── \*/.*?document.addEventListener', js_logic_replacement + '\n// document.addEventListener', maze, flags=re.DOTALL)

with open(maze_path, 'w', encoding='utf-8') as f:
    f.write(maze)

print("maze updated successfully")
