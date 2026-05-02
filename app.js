"use strict";

const animals = [
  {
    id: "dog",
    name: "いぬ",
    homeId: "doghouse",
    image: "./assets/animals/dog.svg",
    prompt: "わんわんの おうち どこかな？",
    cry: "わんわん"
  },
  {
    id: "cat",
    name: "ねこ",
    homeId: "cushion",
    image: "./assets/animals/cat.svg",
    prompt: "ねこさん どこで やすむかな？",
    cry: "にゃーお"
  },
  {
    id: "bird",
    name: "とり",
    homeId: "tree",
    image: "./assets/animals/bird.svg",
    prompt: "とりさんの おうち どこかな？",
    cry: "ぴよぴよ"
  },
  {
    id: "fish",
    name: "さかな",
    homeId: "aquarium",
    image: "./assets/animals/fish.svg",
    prompt: "さかなさんは どこかな？",
    cry: "ぱくぱく"
  },
  {
    id: "rabbit",
    name: "うさぎ",
    homeId: "grass",
    image: "./assets/animals/rabbit.svg",
    prompt: "うさぎさん どこが すきかな？",
    cry: "ぴょんぴょん"
  },
  {
    id: "panda",
    name: "ぱんだ",
    homeId: "bamboo",
    image: "./assets/animals/panda.svg",
    prompt: "ぱんださんの おうち どこかな？",
    cry: "もぐもぐ"
  },
  {
    id: "pig",
    name: "ぶた",
    homeId: "pigpen",
    image: "./assets/animals/pig.svg",
    prompt: "ぶたさんの おうち どこかな？",
    cry: "ぶーぶー"
  },
  {
    id: "frog",
    name: "かえる",
    homeId: "lilypad",
    image: "./assets/animals/frog.svg",
    prompt: "かえるさん どこに いるかな？",
    cry: "けろけろ"
  },
  {
    id: "bear",
    name: "くま",
    homeId: "cave",
    image: "./assets/animals/bear.svg",
    prompt: "くまさんの おうち どこかな？",
    cry: "がおー"
  },
  {
    id: "mouse",
    name: "ねずみ",
    homeId: "hole",
    image: "./assets/animals/mouse.svg",
    prompt: "ねずみさん どこに かくれるかな？",
    cry: "ちゅうちゅう"
  }
];

const homes = [
  { id: "doghouse", name: "いぬごや", image: "./assets/homes/doghouse.svg" },
  { id: "cushion", name: "クッション", image: "./assets/homes/cushion.svg" },
  { id: "tree", name: "き", image: "./assets/homes/tree.svg" },
  { id: "aquarium", name: "すいそう", image: "./assets/homes/aquarium.svg" },
  { id: "grass", name: "くさむら", image: "./assets/homes/grass.svg" },
  { id: "bamboo", name: "たけ", image: "./assets/homes/bamboo.svg" },
  { id: "pigpen", name: "ぶたごや", image: "./assets/homes/pigpen.svg" },
  { id: "lilypad", name: "はす", image: "./assets/homes/lilypad.svg" },
  { id: "cave", name: "ほらあな", image: "./assets/homes/cave.svg" },
  { id: "hole", name: "あな", image: "./assets/homes/hole.svg" }
];

const ROUND_SIZE = 5;
const MUTE_STORAGE_KEY = "doubutsusanno-outi.muted";

const homesById = new Map(homes.map((home) => [home.id, home]));

const startScreen = document.querySelector("#startScreen");
const gameScreen = document.querySelector("#gameScreen");
const endScreen = document.querySelector("#endScreen");
const startButton = document.querySelector("#startButton");
const againButton = document.querySelector("#againButton");
const nextButton = document.querySelector("#nextButton");
const nextArea = document.querySelector("#nextArea");
const roundLabel = document.querySelector("#roundLabel");
const message = document.querySelector("#message");
const animalStage = document.querySelector("#animalStage");
const animalImage = document.querySelector("#animalImage");
const animalName = document.querySelector("#animalName");
const homesGrid = document.querySelector("#homesGrid");
const playField = document.querySelector(".play-field");
const installGuideButton = document.querySelector("#installGuideButton");
const installSheet = document.querySelector("#installSheet");
const installLead = document.querySelector("#installLead");
const installSteps = document.querySelector("#installSteps");
const pwaInstallButton = document.querySelector("#pwaInstallButton");
const closeInstallButton = document.querySelector("#closeInstallButton");
const muteButtons = document.querySelectorAll(".mute-toggle");

let roundAnimals = [];
let roundHomes = [];
let currentIndex = 0;
let settled = false;
let deferredInstallPrompt = null;
let muted = readMuted();
let audioContext = null;

const installGuides = {
  iphone: {
    lead: "Safariで開いて、ホーム画面にアイコンを置けます。",
    steps: [
      "Safariの共有ボタンをタップします。",
      "ホーム画面に追加を選びます。",
      "追加をタップします。"
    ]
  },
  android: {
    lead: "Chromeで開いて、ホーム画面にアイコンを置けます。",
    steps: [
      "画面の案内または右上のメニューを開きます。",
      "アプリをインストール、またはホーム画面に追加を選びます。",
      "追加をタップします。"
    ]
  },
  other: {
    lead: "スマートフォンやタブレットのブラウザからホーム画面に追加できます。",
    steps: [
      "ブラウザのメニューを開きます。",
      "ホーム画面に追加、またはインストールを選びます。",
      "追加をタップします。"
    ]
  },
  standalone: {
    lead: "ホーム画面から起動中です。",
    steps: [
      "このまま遊べます。"
    ]
  }
};

function shuffleItems(items) {
  const copied = [...items];
  for (let i = copied.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [copied[i], copied[j]] = [copied[j], copied[i]];
  }
  return copied;
}

function showScreen(screen) {
  for (const target of [startScreen, gameScreen, endScreen]) {
    target.hidden = target !== screen;
    target.classList.toggle("is-active", target === screen);
  }
}

function startGame() {
  roundAnimals = shuffleItems(animals).slice(0, ROUND_SIZE);
  roundHomes = shuffleItems(roundAnimals.map((animal) => homesById.get(animal.homeId)));
  currentIndex = 0;
  showScreen(gameScreen);
  renderRound();
}

function currentAnimal() {
  return roundAnimals[currentIndex];
}

function renderRound() {
  const animal = currentAnimal();
  settled = false;
  nextArea.hidden = true;
  clearCelebrations();

  animalStage.classList.remove("is-thinking", "is-going-home");
  animalStage.style.setProperty("--go-x", "0px");
  animalStage.style.setProperty("--go-y", "0px");

  roundLabel.textContent = `${currentIndex + 1}ひきめの どうぶつさん`;
  message.classList.remove("is-correct");
  message.textContent = animal.prompt;
  animalImage.src = animal.image;
  animalImage.alt = animal.name;
  animalName.textContent = animal.name;

  homesGrid.replaceChildren();
  for (const home of roundHomes) {
    const button = document.createElement("button");
    button.className = "home-card";
    button.type = "button";
    button.dataset.homeId = home.id;
    button.setAttribute("aria-label", `${home.name}をえらぶ`);

    const img = document.createElement("img");
    img.src = home.image;
    img.alt = "";
    img.draggable = false;

    const label = document.createElement("span");
    label.textContent = home.name;

    button.append(img, label);
    button.addEventListener("click", () => chooseHome(home, button));
    homesGrid.append(button);
  }
}

function chooseHome(home, button) {
  if (settled) {
    return;
  }

  clearHomeStates();
  button.classList.add("is-selected");

  const animal = currentAnimal();
  if (home.id === animal.homeId) {
    sendAnimalHome(button);
    return;
  }

  message.textContent = "こっちかな？";
  message.classList.remove("is-correct");
  animalStage.classList.remove("is-thinking");
  void animalStage.offsetWidth;
  animalStage.classList.add("is-thinking");
  playMissTone();
  vibrate(15);

  const guide = homesGrid.querySelector(`[data-home-id="${animal.homeId}"]`);
  if (guide) {
    guide.classList.add("is-guide");
  }
}

function clearHomeStates() {
  for (const card of homesGrid.querySelectorAll(".home-card")) {
    card.classList.remove("is-selected", "is-guide", "is-happy");
  }
}

function sendAnimalHome(button) {
  settled = true;
  button.classList.add("is-happy");
  message.classList.remove("is-correct");
  void message.offsetWidth;
  message.textContent = "ぴったり！おうちだね";
  message.classList.add("is-correct");

  spawnCelebration(button);

  const move = calculateMove(button);
  animalStage.style.setProperty("--go-x", `${move.x}px`);
  animalStage.style.setProperty("--go-y", `${move.y}px`);
  animalStage.classList.remove("is-thinking");
  animalStage.classList.add("is-going-home");

  playSuccessChord();
  vibrate([28, 40, 28]);
  speakCry(currentAnimal().cry);

  window.setTimeout(() => {
    nextArea.hidden = false;
    nextButton.focus({ preventScroll: true });
  }, 620);
}

function spawnCelebration(button) {
  if (!playField) {
    return;
  }
  clearCelebrations();
  const buttonRect = button.getBoundingClientRect();
  const fieldRect = playField.getBoundingClientRect();
  const cele = document.createElement("div");
  cele.className = "home-celebrate";
  cele.setAttribute("aria-hidden", "true");
  cele.style.left = `${buttonRect.left - fieldRect.left}px`;
  cele.style.top = `${buttonRect.top - fieldRect.top}px`;
  cele.style.width = `${buttonRect.width}px`;
  cele.style.height = `${buttonRect.height}px`;
  playField.append(cele);
}

function clearCelebrations() {
  if (!playField) {
    return;
  }
  for (const node of playField.querySelectorAll(".home-celebrate")) {
    node.remove();
  }
}

function calculateMove(button) {
  const animalRect = animalImage.getBoundingClientRect();
  const homeImage = button.querySelector("img");
  const targetRect = (homeImage || button).getBoundingClientRect();

  const animalCenterX = animalRect.left + animalRect.width / 2;
  const animalCenterY = animalRect.top + animalRect.height / 2;
  const targetCenterX = targetRect.left + targetRect.width / 2;
  const targetCenterY = targetRect.top + targetRect.height / 2;

  return {
    x: Math.round(targetCenterX - animalCenterX),
    y: Math.round(targetCenterY - animalCenterY)
  };
}

function goNext() {
  if (!settled) {
    return;
  }

  currentIndex += 1;
  if (currentIndex >= roundAnimals.length) {
    showScreen(endScreen);
    return;
  }

  renderRound();
}

function readMuted() {
  try {
    return window.localStorage.getItem(MUTE_STORAGE_KEY) === "1";
  } catch (error) {
    return false;
  }
}

function writeMuted(value) {
  try {
    window.localStorage.setItem(MUTE_STORAGE_KEY, value ? "1" : "0");
  } catch (error) {
    /* ignore */
  }
}

function applyMutedState() {
  for (const button of muteButtons) {
    button.setAttribute("aria-pressed", muted ? "true" : "false");
    button.dataset.muted = muted ? "1" : "0";
    button.textContent = muted ? "おとオフ" : "おとオン";
  }
  if (muted && window.speechSynthesis) {
    window.speechSynthesis.cancel();
  }
}

function toggleMute() {
  muted = !muted;
  writeMuted(muted);
  applyMutedState();
  if (!muted) {
    playPing();
  }
}

function ensureAudio() {
  if (muted) {
    return null;
  }
  if (!audioContext) {
    const Ctor = window.AudioContext || window.webkitAudioContext;
    if (!Ctor) {
      return null;
    }
    try {
      audioContext = new Ctor();
    } catch (error) {
      return null;
    }
  }
  if (audioContext.state === "suspended") {
    audioContext.resume().catch(() => {});
  }
  return audioContext;
}

function playTone(frequency, startOffset, duration, gain = 0.18) {
  const ctx = ensureAudio();
  if (!ctx) {
    return;
  }
  const start = ctx.currentTime + startOffset;
  const osc = ctx.createOscillator();
  const env = ctx.createGain();
  osc.type = "sine";
  osc.frequency.value = frequency;
  env.gain.setValueAtTime(0, start);
  env.gain.linearRampToValueAtTime(gain, start + 0.02);
  env.gain.exponentialRampToValueAtTime(0.0001, start + duration);
  osc.connect(env).connect(ctx.destination);
  osc.start(start);
  osc.stop(start + duration + 0.05);
}

function playSuccessChord() {
  playTone(523.25, 0, 0.32);
  playTone(659.25, 0.09, 0.32);
  playTone(783.99, 0.18, 0.42, 0.2);
}

function playMissTone() {
  playTone(392, 0, 0.18, 0.12);
  playTone(330, 0.08, 0.22, 0.1);
}

function playPing() {
  playTone(880, 0, 0.18, 0.14);
}

function speakCry(text) {
  if (muted || !text) {
    return;
  }
  const synth = window.speechSynthesis;
  if (!synth || typeof window.SpeechSynthesisUtterance !== "function") {
    return;
  }
  try {
    synth.cancel();
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = "ja-JP";
    utter.rate = 1.0;
    utter.pitch = 1.25;
    utter.volume = 0.9;
    synth.speak(utter);
  } catch (error) {
    /* ignore */
  }
}

function vibrate(pattern) {
  if (muted) {
    return;
  }
  if (typeof navigator.vibrate === "function") {
    try {
      navigator.vibrate(pattern);
    } catch (error) {
      /* ignore */
    }
  }
}

function isStandaloneMode() {
  return window.matchMedia("(display-mode: standalone)").matches || window.navigator.standalone === true;
}

function detectDeviceKind() {
  const userAgent = window.navigator.userAgent || "";
  const platform = window.navigator.platform || "";
  const isIPadOS = platform === "MacIntel" && window.navigator.maxTouchPoints > 1;

  if (/iPhone|iPad|iPod/.test(userAgent) || isIPadOS) {
    return "iphone";
  }

  if (/Android/.test(userAgent)) {
    return "android";
  }

  return "other";
}

function requestedInstallKind() {
  const params = new URLSearchParams(window.location.search);
  const target = params.get("install");
  if (target === "iphone" || target === "android") {
    return target;
  }
  return "";
}

function renderInstallGuide(kind) {
  const guideKind = isStandaloneMode() ? "standalone" : kind;
  const guide = installGuides[guideKind] || installGuides.other;

  installLead.textContent = guide.lead;
  installSteps.replaceChildren();

  for (const step of guide.steps) {
    const item = document.createElement("li");
    item.textContent = step;
    installSteps.append(item);
  }

  pwaInstallButton.hidden = !deferredInstallPrompt || guideKind === "iphone" || guideKind === "standalone";
}

function openInstallGuide(kind = detectDeviceKind()) {
  renderInstallGuide(kind);
  installSheet.hidden = false;
  closeInstallButton.focus({ preventScroll: true });
}

function closeInstallGuide() {
  installSheet.hidden = true;
  installGuideButton.focus({ preventScroll: true });
}

function registerServiceWorker() {
  if (!("serviceWorker" in navigator)) {
    return;
  }

  window.addEventListener("load", () => {
    navigator.serviceWorker.register("./sw.js").catch(() => {});
  });
}

startButton.addEventListener("click", startGame);
againButton.addEventListener("click", startGame);
nextButton.addEventListener("click", goNext);
installGuideButton.addEventListener("click", () => openInstallGuide());
closeInstallButton.addEventListener("click", closeInstallGuide);
pwaInstallButton.addEventListener("click", async () => {
  if (!deferredInstallPrompt) {
    return;
  }

  deferredInstallPrompt.prompt();
  await deferredInstallPrompt.userChoice;
  deferredInstallPrompt = null;
  renderInstallGuide(detectDeviceKind());
});

for (const button of muteButtons) {
  button.addEventListener("click", toggleMute);
}

installSheet.addEventListener("click", (event) => {
  if (event.target === installSheet) {
    closeInstallGuide();
  }
});

window.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !installSheet.hidden) {
    closeInstallGuide();
  }
});

window.addEventListener("beforeinstallprompt", (event) => {
  event.preventDefault();
  deferredInstallPrompt = event;
  if (!installSheet.hidden) {
    renderInstallGuide(detectDeviceKind());
  }
});

window.addEventListener("appinstalled", () => {
  deferredInstallPrompt = null;
  if (!installSheet.hidden) {
    renderInstallGuide("standalone");
  }
});

applyMutedState();
showScreen(startScreen);
registerServiceWorker();

const installKindFromUrl = requestedInstallKind();
if (installKindFromUrl) {
  window.setTimeout(() => openInstallGuide(installKindFromUrl), 450);
}
