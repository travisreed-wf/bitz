var count = $( "div:contains('Wins')" ).find('.value').first().text();

$.ajax({
    url: 'https://bitz-game-staging.appspot.com/extension/clash_wins?count=' + count,
    type: 'POST'
});

$.ajax({
    url: 'https://bitz-game.appspot.com/extension/clash_wins?count=' + count,
    type: 'POST'
});
