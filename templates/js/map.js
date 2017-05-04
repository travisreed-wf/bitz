
var tile_data = [];

var build = function(){
  var tileID = $('#buildTileID').data('tile-id');
  var s = $('#building-select');
  var building = s.val();
  $.ajax({
      url: '/build/' + tileID + "/" + building + '/',
      method: 'PUT',
      success: function() {
        window.location.reload();
      }
    });
};

$('#buildModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget);
  var select = $('#building-select');
  var building;
  var availableBuildings = button.data('available-buildings').split(',');
  for (var i = 0; i < availableBuildings.length; i++){
    building = availableBuildings[i];
    select.append('<option value="' + building + '">' + building + '</option>');
  }
  var modal = $(this);
  var tileID = button.data('tile-id');
  var html = '<span id="buildTileID" data-tile-id="' + tileID + '">Assigning a building to this tile will reduce the costs of constructing that building</span>';
  modal.find('.modal-body').append(html);
  select.select2();
});


$('#exploreModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget);
  var modal = $(this);
  modal.find('button').show();
  var html = '';
  var tileCoord = button.data('tile-str-coord');
  var tileCost = parseInt(button.data('tile-cost'));
  tileCost = numberWithCommas(tileCost);
  var tileDistance = button.data('tile-distance');
  var tileID = button.data('tile-id');
    html += (
    '<span id="tileSpan" data-tile-id="' + tileID + '">' +
    'Are you sure that you want to explore the tile at ' + tileCoord + '?' +
    '<br>Because it is ' + tileDistance + ' tiles from the middle, it will cost ' +
    '<img src="/static/img/resources/Food.png" style="width:30px;height:30px; padding-bottom: 5px"> <span>x ' + tileCost + '</span> ' +
    'to explore.</span>');

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
        var imagePath = '/static/img/tiles/' + tileName+ '.png';
        var html = (
          '<div class="row">' +
            '<div class="col-md-2">' +
              '<img width="100%" src="' + imagePath + '">' +
            '</div>' +
            '<div class="col-md-5">' +
              'Congratulations! You have discovered ' + tileName + '.' +
            '</div>' +
          '</div>'
        );
        modal.find('.modal-body').html(html);
        var td = $('#td-' + tileID);
        td.css('background-image', 'url(' + imagePath + ')');
        td.find('button').hide();
        update_resources(data);
      },
      error: function(resp) {
        window.alert(resp.responseText || 'Unknown Error');
      }
    });
};

$(document).ready(function() {
  var td;
  $('td').find('img').each(function(){
    var currentWidth = $(this).width();
    $(this).attr('width', currentWidth * .9);
    $(this).attr('height', currentWidth * .9);
    td = $(this).closest('td');
    td.attr('height', currentWidth / .9);
    td.attr('width', currentWidth / .9);
  })
});
