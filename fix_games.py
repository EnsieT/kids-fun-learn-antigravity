import os
import re

cur_dir = os.path.dirname(__file__)
act_dir = os.path.join(cur_dir, 'activities')

# 1. Fix silly-story.html
silly_path = os.path.join(act_dir, 'silly-story.html')
with open(silly_path, 'r', encoding='utf-8') as f:
    silly = f.read()
silly = silly.replace("banks[who]", "banks['who']")
with open(silly_path, 'w', encoding='utf-8') as f:
    f.write(silly)
print("Fixed silly-story.html")

# 2. Fix train-track.html
train_path = os.path.join(act_dir, 'train-track.html')
with open(train_path, 'r', encoding='utf-8') as f:
    train = f.read()

# ADD CSS for selected
css_addition = """    .draggable-piece:active { cursor: grabbing; }

    .draggable-piece.selected {
      border: 3px solid #FFEB3B;
      border-radius: 8px;
      transform: scale(1.1);
    }"""
train = train.replace("    .draggable-piece:active { cursor: grabbing; }", css_addition)

# JS replacement for logic
js_logic = """
let correctlyPlaced = 0;
let selectedPiece = null;

function initGame() {
  round = 0; mistakes = 0; selectedPiece = null;
  hideFeedback();
  document.getElementById('completion-screen').style.display = 'none';
  loadRound();
}"""
train = train.replace("""let correctlyPlaced = 0;

function initGame() {""", js_logic)


# Event binding replacement
events_old = """    // Drop logic
    cell.addEventListener('dragover', e => { e.preventDefault(); cell.classList.add('drag-over'); });
    cell.addEventListener('dragleave', e => { cell.classList.remove('drag-over'); });
    cell.addEventListener('drop', handleDrop);
  });
  
  // Prepare toolbox pieces
  let piecesToRender = currentLevel.holes.map(h => h.split(',')[2]).concat(currentLevel.fakes);
  piecesToRender = shuffle(piecesToRender);
  
  piecesToRender.forEach((p, idx) => {
    const div = document.createElement('div');
    div.className = `draggable-piece track-${p}`;
    div.draggable = true;
    div.dataset.type = p;
    div.id = `piece-${idx}`;
    div.addEventListener('dragstart', handleDragStart);
    tb.appendChild(div);
  });
}

function handleDragStart(e) {
  e.dataTransfer.setData('text/plain', e.target.id);
  playSound('pop');
}

function handleDrop(e) {
  e.preventDefault();
  const cell = e.currentTarget;
  cell.classList.remove('drag-over');
  
  const pieceId = e.dataTransfer.getData('text/plain');
  const piece = document.getElementById(pieceId);
  if(!piece) return;"""

events_new = """    // Drop logic
    cell.addEventListener('click', () => handleSlotClick(cell));
  });
  
  // Prepare toolbox pieces
  let piecesToRender = currentLevel.holes.map(h => h.split(',')[2]).concat(currentLevel.fakes);
  piecesToRender = shuffle(piecesToRender);
  
  piecesToRender.forEach((p, idx) => {
    const div = document.createElement('div');
    div.className = `draggable-piece track-${p}`;
    div.dataset.type = p;
    div.id = `piece-${idx}`;
    div.addEventListener('click', () => handlePieceClick(div));
    tb.appendChild(div);
  });
}

function handlePieceClick(piece) {
  if (selectedPiece) selectedPiece.classList.remove('selected');
  selectedPiece = piece;
  piece.classList.add('selected');
  playSound('pop');
}

function handleSlotClick(cell) {
  if (!selectedPiece) return;
  if (!cell.classList.contains('dropzone')) return;
  
  const piece = selectedPiece;"""

train = train.replace(events_old, events_new)

with open(train_path, 'w', encoding='utf-8') as f:
    f.write(train)
print("Fixed train-track.html")

