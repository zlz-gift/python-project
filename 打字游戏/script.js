// ---- Quotes Database ----
const quotesByDifficulty = {
  easy: [
    'The game is afoot.',
    'Come, Watson, come!',
    'There is nothing more to be said.',
    'You know my methods, Watson.',
    'Elementary, my dear Watson.',
    'I have already solved the case.',
    'The evidence is quite clear.',
    'Action is the real measure of intelligence.',
    'A trusty comrade is always of use.',
    'There is nothing so important as trifles.',
  ],
  medium: [
    'When you have eliminated the impossible, whatever remains, however improbable, must be the truth.',
    'There is nothing more deceptive than an obvious fact.',
    'I ought to know by this time that when a fact appears to be opposed to a long train of deductions it invariably proves to be capable of bearing some other interpretation.',
    'I never make exceptions. An exception disproves the rule.',
    'What one man can invent another can discover.',
    'Nothing clears up a case so much as stating it to another person.',
    'Education never ends, Watson. It is a series of lessons, with the greatest for the last.',
  ],
  hard: [
    'I have seen too much not to know that the impression of a woman may be more valuable than the conclusion of an analytical reasoner.',
    'It is a capital mistake to theorize before one has data. Insensibly one begins to twist facts to suit theories, instead of theories to suit facts.',
    'My name is Sherlock Holmes. It is my business to know what other people do not know.',
    'The world is full of obvious things which nobody by any chance ever observes.',
    'Life is infinitely stranger than anything which the mind of man could invent. We would not dare to conceive the things which are really mere commonplaces of existence.',
    'From a drop of water a logician could infer the possibility of an Atlantic or a Niagara without having seen or heard of one or the other.',
  ],
};

// ---- DOM Elements ----
const quoteElement = document.getElementById('quote');
const messageElement = document.getElementById('message');
const typedValueElement = document.getElementById('typed-value');
const wpmElement = document.getElementById('wpm');
const timerElement = document.getElementById('timer');
const accuracyElement = document.getElementById('accuracy');
const bestScoreElement = document.getElementById('best-score');
const progressBar = document.getElementById('progress-bar');
const startButton = document.getElementById('start');
const restartButton = document.getElementById('restart');
const diffButtons = document.querySelectorAll('.diff-btn');

// ---- Game State ----
let words = [];
let wordIndex = 0;
let startTime = 0;
let gameActive = false;
let timerInterval = null;
let totalKeystrokes = 0;
let correctKeystrokes = 0;
let lastTypedValue = '';
let currentDifficulty = 'easy';

// ---- localStorage Helpers ----
const STORAGE_KEY = 'typingGameBestScores';

function getBestScores() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
  } catch {
    return {};
  }
}

function saveBestScore(difficulty, wpm, accuracy, time) {
  const scores = getBestScores();
  const prev = scores[difficulty];
  const entry = { wpm: round1(wpm), accuracy: round1(accuracy), time: round2(time) };
  if (!prev || wpm > prev.wpm) {
    scores[difficulty] = entry;
    localStorage.setItem(STORAGE_KEY, JSON.stringify(scores));
    return true;
  }
  return false;
}

function displayBestScore(difficulty) {
  const scores = getBestScores();
  const best = scores[difficulty];
  if (best) {
    const label = getDifficultyLabel(difficulty);
    bestScoreElement.textContent = `最佳成绩 (${label}): ${best.wpm} WPM | 准确率 ${best.accuracy}% | ${best.time}s`;
  } else {
    bestScoreElement.textContent = '';
  }
}

function getDifficultyLabel(d) {
  return { easy: '简单', medium: '中等', hard: '困难' }[d] || d;
}

// ---- Utility ----
function round1(n) { return Math.round(n * 10) / 10; }
function round2(n) { return Math.round(n * 100) / 100; }

function calcWPM(wordCount, elapsedSeconds) {
  if (elapsedSeconds <= 0) return 0;
  return wordCount / (elapsedSeconds / 60);
}

// ---- Core Game Functions ----
function startGame() {
  const quotes = quotesByDifficulty[currentDifficulty];
  const quote = quotes[Math.floor(Math.random() * quotes.length)];
  words = quote.split(' ');
  wordIndex = 0;
  totalKeystrokes = 0;
  correctKeystrokes = 0;
  lastTypedValue = '';

  // Render quote with word spans
  quoteElement.innerHTML = words.map(w => `<span class="word">${w}</span>`).join(' ');
  const spans = quoteElement.querySelectorAll('span.word');
  if (spans.length) spans[0].classList.add('highlight');

  // Reset UI
  messageElement.innerText = '';
  typedValueElement.value = '';
  typedValueElement.disabled = false;
  typedValueElement.classList.remove('error');
  typedValueElement.focus();
  timerElement.textContent = '0.0s';
  wpmElement.textContent = 'WPM: 0';
  accuracyElement.textContent = '准确率: --';
  progressBar.style.width = '0%';
  displayBestScore(currentDifficulty);

  // Button visibility
  startButton.classList.add('hidden');
  restartButton.classList.remove('hidden');

  // Start timer
  startTime = Date.now();
  gameActive = true;
  if (timerInterval) clearInterval(timerInterval);
  timerInterval = setInterval(updateTimer, 100);
}

function finishGame() {
  gameActive = false;
  clearInterval(timerInterval);
  typedValueElement.disabled = true;

  const elapsedSeconds = (Date.now() - startTime) / 1000;
  const wpm = calcWPM(words.length, elapsedSeconds);
  const accuracy = totalKeystrokes > 0
    ? (correctKeystrokes / totalKeystrokes) * 100
    : 100;

  messageElement.innerHTML =
    `完成! 时间: <strong>${round2(elapsedSeconds)}s</strong> | ` +
    `WPM: <strong>${round1(wpm)}</strong> | ` +
    `准确率: <strong>${round1(accuracy)}%</strong>`;

  const isNewBest = saveBestScore(currentDifficulty, wpm, accuracy, elapsedSeconds);
  if (isNewBest) {
    messageElement.innerHTML += ' -- 新纪录!';
  }
  displayBestScore(currentDifficulty);

  // Final stats
  timerElement.textContent = `${round1(elapsedSeconds)}s`;
  wpmElement.textContent = `WPM: ${round1(wpm)}`;
  accuracyElement.textContent = `准确率: ${round1(accuracy)}%`;
  progressBar.style.width = '100%';

  // Remove word highlight
  quoteElement.querySelectorAll('span.word').forEach(s => s.classList.remove('highlight'));
}

function cancelGame() {
  gameActive = false;
  clearInterval(timerInterval);
  typedValueElement.disabled = true;
  typedValueElement.value = '';
  messageElement.innerText = '游戏已取消。';
  startButton.classList.remove('hidden');
  restartButton.classList.add('hidden');
  quoteElement.querySelectorAll('span.word').forEach(s => s.classList.remove('highlight'));
  progressBar.style.width = '0%';
  timerElement.textContent = '0.0s';
  wpmElement.textContent = 'WPM: 0';
  accuracyElement.textContent = '准确率: --';
}

// ---- Timer & Display Updates ----
function updateTimer() {
  if (!gameActive) return;
  const elapsed = (Date.now() - startTime) / 1000;
  timerElement.textContent = `${elapsed.toFixed(1)}s`;
  updateWPM();
}

function updateWPM() {
  if (!gameActive || wordIndex === 0) return;
  const elapsed = (Date.now() - startTime) / 1000;
  if (elapsed < 0.1) return;
  wpmElement.textContent = `WPM: ${round1(calcWPM(wordIndex, elapsed))}`;
}

function updateProgress() {
  if (words.length === 0) return;
  progressBar.style.width = `${(wordIndex / words.length) * 100}%`;
}

function updateAccuracyDisplay() {
  if (totalKeystrokes === 0) {
    accuracyElement.textContent = '准确率: --';
    return;
  }
  const acc = (correctKeystrokes / totalKeystrokes) * 100;
  accuracyElement.textContent = `准确率: ${round1(acc)}%`;
}

// ---- Difficulty Selection ----
function setDifficulty(difficulty) {
  if (!quotesByDifficulty[difficulty]) return;
  currentDifficulty = difficulty;
  diffButtons.forEach(b => b.classList.toggle('active', b.dataset.difficulty === difficulty));
  displayBestScore(difficulty);

  if (gameActive) {
    cancelGame();
    messageElement.innerText = '难度已更改，点击 Start 开始新游戏。';
  }
}

// ---- Event: Start / Restart ----
startButton.addEventListener('click', startGame);
restartButton.addEventListener('click', startGame);

// ---- Event: Difficulty Buttons ----
diffButtons.forEach(btn => {
  btn.addEventListener('click', () => setDifficulty(btn.dataset.difficulty));
});

// ---- Event: Typing Input ----
typedValueElement.addEventListener('input', () => {
  if (!gameActive) return;

  const currentWord = words[wordIndex];
  const typedValue = typedValueElement.value;

  // Track keystroke accuracy (only character additions, not deletions)
  if (typedValue.length > lastTypedValue.length) {
    const added = typedValue.slice(lastTypedValue.length);
    const nonSpaceCount = [...added].filter(c => c !== ' ').length;
    if (nonSpaceCount > 0) {
      totalKeystrokes += nonSpaceCount;
      const trimmed = typedValue.trim();
      if (trimmed === '' || currentWord.startsWith(trimmed)) {
        correctKeystrokes += nonSpaceCount;
      }
      updateAccuracyDisplay();
    }
  }
  lastTypedValue = typedValue;

  const spans = Array.from(quoteElement.querySelectorAll('span.word'));

  // Space triggers word advance when the typed word matches
  if (typedValue.endsWith(' ') && typedValue.trim() === currentWord) {
    typedValueElement.value = '';
    lastTypedValue = '';
    spans.forEach(s => s.classList.remove('highlight'));
    wordIndex++;
    updateProgress();

    if (wordIndex >= words.length) {
      finishGame();
      return;
    }
    spans[wordIndex].classList.add('highlight');
    updateWPM();
    return;
  }

  // Final word completed without trailing space
  if (typedValue === currentWord && wordIndex === words.length - 1) {
    updateProgress();
    finishGame();
    return;
  }

  // Visual feedback: correct prefix vs error
  if (currentWord.startsWith(typedValue)) {
    typedValueElement.classList.remove('error');
  } else {
    typedValueElement.classList.add('error');
  }

  updateWPM();
});

// ---- Keyboard Shortcuts ----
document.addEventListener('keydown', (e) => {
  // Enter to start/restart (only when input is not focused)
  if (e.key === 'Enter' && !gameActive && document.activeElement !== typedValueElement) {
    e.preventDefault();
    startGame();
  }
  // Esc to cancel active game
  if (e.key === 'Escape' && gameActive) {
    e.preventDefault();
    cancelGame();
  }
});

// ---- Init ----
displayBestScore(currentDifficulty);
