
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
  modal.find('button').show();
  var html = '';
  var tileCoord = button.data('tile-str-coord');
  var tileCost = button.data('tile-cost');
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
        td.attr('background', imagePath);
        td.find('button').hide();
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
