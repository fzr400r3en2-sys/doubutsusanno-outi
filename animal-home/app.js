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

let animalOrder = [];
let currentIndex = 0;
let settled = false;
let nextTimer = 0;

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

startButton.addEventListener("click", startGame);
againButton.addEventListener("click", startGame);
nextButton.addEventListener("click", goNext);

showScreen(startScreen);
