var table = $('table').DataTable({
  "paging": false,
  "info": false
});

var research = function(btn){
  btn = $(btn);
  var data = {
    'technology': btn.data('technology')
  };
  $.ajax({
      url: '/technologies/',
      method: 'POST',
      data: JSON.stringify(data),
      contentType: 'application/json',
      success: function(resp) {
        update_resources($.parseJSON(resp));
        window.location.reload();
      },
      error: function(resp) {
        window.alert(resp.responseText || 'Unknown Error');
      }
    });
};
