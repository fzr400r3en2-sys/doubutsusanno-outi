"use strict";

const animals = [
  {
    id: "dog",
    name: "いぬ",
    homeId: "doghouse",
    image: "./assets/animals/dog.svg",
    prompt: "わんわんの おうち どこかな？"
  },
  {
    id: "cat",
    name: "ねこ",
    homeId: "cushion",
    image: "./assets/animals/cat.svg",
    prompt: "ねこさん どこで やすむかな？"
  },
  {
    id: "bird",
    name: "とり",
    homeId: "tree",
    image: "./assets/animals/bird.svg",
    prompt: "とりさんの おうち どこかな？"
  },
  {
    id: "fish",
    name: "さかな",
    homeId: "aquarium",
    image: "./assets/animals/fish.svg",
    prompt: "さかなさんは どこかな？"
  },
  {
    id: "rabbit",
    name: "うさぎ",
    homeId: "grass",
    image: "./assets/animals/rabbit.svg",
    prompt: "うさぎさん どこが すきかな？"
  }
];

const homes = [
  {
    id: "doghouse",
    name: "いぬごや",
    image: "./assets/homes/doghouse.svg"
  },
  {
    id: "cushion",
    name: "クッション",
    image: "./assets/homes/cushion.svg"
  },
  {
    id: "tree",
    name: "き",
    image: "./assets/homes/tree.svg"
  },
  {
    id: "aquarium",
    name: "すいそう",
    image: "./assets/homes/aquarium.svg"
  },
  {
    id: "grass",
    name: "くさむら",
    image: "./assets/homes/grass.svg"
  }
];

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
const installGuideButton = document.querySelector("#installGuideButton");
const installSheet = document.querySelector("#installSheet");
const installLead = document.querySelector("#installLead");
const installSteps = document.querySelector("#installSteps");
const pwaInstallButton = document.querySelector("#pwaInstallButton");
const closeInstallButton = document.querySelector("#closeInstallButton");

let animalOrder = [];
let currentIndex = 0;
let settled = false;
let nextTimer = 0;
let deferredInstallPrompt = null;

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
  animalOrder = shuffleItems(animals);
  currentIndex = 0;
  showScreen(gameScreen);
  renderRound();
}

function currentAnimal() {
  return animalOrder[currentIndex];
}

function renderRound() {
  const animal = currentAnimal();
  settled = false;
  window.clearTimeout(nextTimer);
  nextArea.hidden = true;

  animalStage.classList.remove("is-thinking", "is-going-home");
  animalStage.style.setProperty("--go-x", "0px");
  animalStage.style.setProperty("--go-y", "0px");

  roundLabel.textContent = `${currentIndex + 1}ひきめの どうぶつさん`;
  message.textContent = animal.prompt;
  animalImage.src = animal.image;
  animalImage.alt = animal.name;
  animalName.textContent = animal.name;

  homesGrid.replaceChildren();
  for (const home of homes) {
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
  animalStage.classList.remove("is-thinking");
  void animalStage.offsetWidth;
  animalStage.classList.add("is-thinking");

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
  message.textContent = "おうちに かえったね";

  const move = calculateMove(button);
  animalStage.style.setProperty("--go-x", `${move.x}px`);
  animalStage.style.setProperty("--go-y", `${move.y}px`);
  animalStage.classList.remove("is-thinking");
  animalStage.classList.add("is-going-home");

  window.setTimeout(() => {
    nextArea.hidden = false;
  }, 620);

  nextTimer = window.setTimeout(() => {
    goNext();
  }, 2100);
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
  window.clearTimeout(nextTimer);
  if (!settled) {
    return;
  }

  currentIndex += 1;
  if (currentIndex >= animalOrder.length) {
    showScreen(endScreen);
    return;
  }

  renderRound();
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

showScreen(startScreen);
registerServiceWorker();

const installKindFromUrl = requestedInstallKind();
if (installKindFromUrl) {
  window.setTimeout(() => openInstallGuide(installKindFromUrl), 450);
}
