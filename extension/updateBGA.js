$(document).ready(function(){
  console.log("Travis was here");
  setTimeout(checkForGameData, 10000);
});
function checkForGameData() {
  var gameDivs = $('.palmares_game');
  var gameStatsText = '';
  var data = {};
  var index;
  gameDivs.each(function () {
    var gameName = $(this).find('.game_name').text();
    gameStatsText = $(this).find('.palmares_details').text();
    index = gameStatsText.search('victories');
    if (index > 4) {
      var winCount = gameStatsText.substring(index - 4, index - 1);
      winCount = winCount.trim();
      winCount = parseInt(winCount);
    }
    data[gameName] = winCount;

  });
  console.log(data);
  if (Object.keys(data).length > 0){
    $.ajax({
        url: 'https://bitz-game-staging.appspot.com/extension/bga_wins/',
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json'
    });

    $.ajax({
      url: 'https://bitz-game.appspot.com/extension/bga_wins/',
      type: 'POST',
      data: JSON.stringify(data),
      contentType: 'application/json'
    });
  }

}

