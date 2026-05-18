const quotes = [
    'When you have eliminated the impossible, whatever remains, however improbable, must be the truth.',
    'There is nothing more deceptive than an obvious fact.',
    'I ought to know by this time that when a fact appears to be opposed to a long train of deductions it invariably proves to be capable of bearing some other interpretation.',
    'I never make exceptions. An exception disproves the rule.',
    'What one man can invent another can discover.',
    'Nothing clears up a case so much as stating it to another person.',
    'Education never ends, Watson. It is a series of lessons, with the greatest for the last.',
];
let words = [];
let wordIndex = 0;
let startTime = Date.now();
const quoteElement = document.getElementById('quote');
const messageElement = document.getElementById('message');
const typedValueElement = document.getElementById('typed-value');
const wpmElement = document.getElementById('wpm');



document.getElementById('start').addEventListener('click', () => {
  const quoteIndex = Math.floor(Math.random() * quotes.length);
  const quote = quotes[quoteIndex];
  words = quote.split(' ');
  wordIndex = 0;
  const spanWords = words.map(function(word) { return `<span class="word">${word}</span>`});
  quoteElement.innerHTML = spanWords.join(' ');
  const spans = quoteElement.querySelectorAll('span.word');
  if (spans.length) spans[0].classList.add('highlight');
  messageElement.innerText = '';
  typedValueElement.value = '';
  typedValueElement.focus();
  startTime = new Date().getTime();
  // reset wpm display
  if (wpmElement) wpmElement.innerText = '';
});

typedValueElement.addEventListener('input', () => {
  if (!words.length) return;
  const currentWord = words[wordIndex];
  const typedValue = typedValueElement.value;
  const spans = Array.from(quoteElement.querySelectorAll('span.word'));

  // 完成整句
  if (typedValue === currentWord && wordIndex === words.length - 1) {
    const elapsedTimeMs = new Date().getTime() - startTime;
    const elapsedSeconds = elapsedTimeMs / 1000;
    const wpm = calcWPM(words.length, elapsedSeconds);
    const message = `CONGRATULATIONS! You finished in ${elapsedSeconds.toFixed(2)} seconds.`;
    messageElement.innerText = message;
    if (wpmElement) wpmElement.innerText = `WPM: ${wpm.toFixed(1)}`;
    // remove highlight from last
    if (spans[wordIndex]) spans[wordIndex].classList.remove('highlight');
    return;
  }

  // 用户敲空格且单词正确：切换到下一个词
  if (typedValue.endsWith(' ') && typedValue.trim() === currentWord) {
    typedValueElement.value = '';
    spans.forEach(s => s.classList.remove('highlight'));
    wordIndex++;
    if (wordIndex < spans.length) {
      spans[wordIndex].classList.add('highlight');
    }
    return;
  }

  // 如果输入为当前单词的前缀，视为正确进度
  if (currentWord.startsWith(typedValue)) {
    typedValueElement.classList.remove('error');
  } else {
    typedValueElement.classList.add('error');
  }
  // 更新实时 WPM（基于已完成单词数 + 当前输入的字符进度）
  if (wpmElement) {
    const elapsedSeconds = (new Date().getTime() - startTime) / 1000;
    // 已完成的单词数
    const completedWords = wordIndex + (typedValue.trim().length > 0 && currentWord.startsWith(typedValue) ? typedValue.trim().split(" ").length - 0 : 0);
    const wpmNow = calcWPM(completedWords, Math.max(elapsedSeconds, 0.1));
    wpmElement.innerText = `WPM: ${wpmNow.toFixed(1)}`;
  }
});

function calcWPM(wordCount, elapsedSeconds){
  if (elapsedSeconds <= 0) return 0;
  // 传统 WPM 使用每分钟单词数：wordCount / minutes
  const minutes = elapsedSeconds / 60;
  return wordCount / minutes;
}