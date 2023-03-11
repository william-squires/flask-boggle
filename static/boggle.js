"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  let response = await axios.post("/api/new-game");
  gameId = response.data.gameId;
  let board = response.data.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {

  $table.empty();
  const $board = $("<tbody></tbody>");

  for (let row of board) {
    $board.append(makeBoardRow(row));
  }

  $table.append($board);
}

/** makes the html for a single board row */
function makeBoardRow(row) {

  const $row = $("<tr></tr>");
  for (let letter of row) {
    const $letter = $("<td></td>");
    $letter.text(letter);
    $row.append($letter);
  }
  return $row;
}

/** When the user submits a word, makes an API call checking
 * if the word is valid.
 * If so, add to list on screen
 * Otherwise, display a message in DOM
 */
async function handleSubmitWord(evt) {
  evt.preventDefault();
  const word = $wordInput.val().toUpperCase();
  const response = await submitWord(word);
  if (response === "ok") {
    displayValid(word);
  } else {
    displayInvalid(response, word);
  }
}

/** sends word to API to determine validity. 
 * Returns response from API */
async function submitWord(word) {
  const response = await axios.post("http://localhost:5000/api/score-word",
    { gameId, word });

  return response.data.result;
}

/** When an invalid word is input, displays a message explaining why */
function displayInvalid(msg, word) {
  const message = `${word} is ${msg}`;
  $message.text(message);
}

/** When a valid word is input, adds it to the list of input words */
function displayValid(word) {
  $playedWords.append(`<li>${word}</li>`);
}

$form.on("submit", handleSubmitWord);

start();