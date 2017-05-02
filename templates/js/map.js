
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
