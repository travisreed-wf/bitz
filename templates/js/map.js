
var tileActionClick = function(btn){
  btn = $(btn);
  var location = $("#location-table").data('location-id');
  var actionName = btn.data('action');
  var tilePosition = btn.data('tile-position');
  $.ajax({
    url: '/map/' + location + "/" + tilePosition + "/" + actionName + "/",
    method: 'PUT',
    success: function(resp) {
      console.log(resp);
    }
  });
};
