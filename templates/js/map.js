
var tile_data = [];

var build = function(btn){
  btn = $(btn);
  var modal = $('#buildModal');
  var location = $("#location-table").data('location-id');
  var tilePosition = $('#tileID').data('tile-position');
  var building = modal.find('input:checked')[0].name;
  $.ajax({
      url: '/build/' + location + "/" + tilePosition + "/" + building + '/',
      method: 'PUT',
      success: function(resp) {
        modal.modal('hide');
      }
    });
};

$('#buildModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget);
  var modal = $(this);
  var html = '';
  var tilePosition = button.data('tile-position');
  var building;
  var availableBuildings = button.data('available-buildings').split(',');
  for (var i = 0; i < availableBuildings.length; i++){
    building = availableBuildings[i];
    html += '<span id="' + tileID + '"data-tile-position="' + tilePosition + '"></span><div class="radio"><label><input type="radio" name="' + building + '">' + building + '</label></div>'
  }
  modal.find('.modal-body').html(html);
});


var tileActionClick = function(btn){
  btn = $(btn);
  var location = $("#location-table").data('location-id');
  var actionName = btn.data('action');
  var tilePosition = btn.data('tile-position');
  var tile = tile_data[tilePosition];
  var action;
  if (tile){
    action = tile[actionName];
    if (action) {
      update_resources(action);
    }
  }
  else {
    tile = [];
    tile_data[tilePosition] = tile;

  }
  if (tile[actionName]){
    tile[actionName]['outstandingClicks'] += 1;
    outstandingClicks = tile[actionName]['outstandingClicks'];
  }
  else{
    outstandingClicks = 1
  }
  if (!tile[actionName] || outstandingClicks >= 10){
    $.ajax({
      url: '/map/' + location + "/" + tilePosition + "/" + actionName + "/?clicks=" + outstandingClicks,
      method: 'PUT',
      success: function(resp) {
        if (!action){
          resp = $.parseJSON(resp);
          tile[actionName] = resp;
          update_resources(resp);
        }
        tile[actionName]['outstandingClicks'] = 0;

      }
    });

  }
};

var update_resources = function(data){
  var resourceName;
  for (resourceName in data['gained_resources']){
    span = $('#resource-' + resourceName);
    currentCount = parseInt(span.text());
    currentCount += data['gained_resources'][resourceName];
    span.text(currentCount);
  }
  for (resourceName in data['used_resources']){
    var span = $('#resource-' + resourceName);
    currentCount = parseInt(span.text());
    currentCount -= data['used_resources'][resourceName];
    span.text(currentCount);
  }
};

window.onbeforeunload = function() {
  var location = $("#location-table").data('location-id');
  var tilePosition;
  for (tilePosition in tile_data){
    var tile = tile_data[tilePosition];
    for (var actionName in tile){
      var action = tile[actionName];
      outstandingClicks = action['outstandingClicks'];
       $.ajax({
        url: '/map/' + location + "/" + tilePosition + "/" + actionName + "/?clicks=" + outstandingClicks,
        method: 'PUT'
      });
    }
  }
};
