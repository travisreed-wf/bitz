
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


$('#exploreModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget);
  var modal = $(this);
  var html = '';
  var tileCoord = button.data('tile-str-coord');
  var tileID = button.data('tile-id');
    html += '<span id="tileSpan" data-tile-id="' + tileID + '">Are you sure that you want to build explore the tile at ' + tileCoord + '?</span>';

  modal.find('.modal-body').html(html);
});

var explore = function(btn){
  btn = $(btn);
  btn.toggle();
  var modal = $('#exploreModal');
  var tileID = $('#tileSpan').data('tile-id');
  $.ajax({
      url: '/explore/' + tileID + '/',
      method: 'POST',
      success: function(resp) {
        var data = $.parseJSON(resp);
        var tileName = data['tile_name'];
        var imagePath = '/static/img/tiles/' + tileName+ '.png'
        var html = (
          '<div class="row">' +
            '<div class="col-md-2">' +
              '<img width="100%" src="' + imagePath + '"></img>' +
            '</div>' +
            '<div class="col-md-5">' +
              'Congratulations! You have discovered ' + tileName + '.' +
            '</div>' +
          '</div>'
        );
        modal.find('.modal-body').html(html);
        var td = $('#td-' + tileID);
        td.attr('background', imagePath);
        td.find('button').hide();
      }
    });
};
