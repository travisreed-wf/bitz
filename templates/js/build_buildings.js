var table = $('table').DataTable({
  "paging": false,
  "info": false
});

var build = function(btn){
  btn = $(btn);
  var data = {
    'building': btn.data('building'),
    'count': btn.data('count')
  };
  $.ajax({
      url: '/build/buildings/',
      method: 'POST',
      data: JSON.stringify(data),
      contentType: 'application/json',
      success: function(resp) {
        console.log('attempting update');
        update_resources($.parseJSON(resp));
      },
      error: function(resp) {
        window.alert(resp.responseText || 'Unknown Error');
      }
    });
};
