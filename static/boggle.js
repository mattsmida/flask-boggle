"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  const response = await fetch(`/api/new-game`, {
    method: "POST",
  });
  const gameData = await response.json();

  gameId = gameData.gameId;
  let board = gameData.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  $table.empty();
  // loop over board and create the DOM tr/td structure
  for (let row of board) {
    let $newTr = $('<tr>');
    for (let letter of row) {
      // let $newTd = $('td');
      // $table.append($newTd.html(letter));
      $newTr.append(`<td>${letter}</td>`);
      // Append to new tr here.
    }
    // Append the new tr to the table here.
    $table.append($newTr);
  }


}


start();