var table = $('table').DataTable({
  "paging": false,
  "info": false
});

$.fn.animateHighlight = function(highlightColor, duration) {
    var highlightBg = highlightColor || "#FFFF9C";
    var animateMs = duration || 1500;
    var originalBg = this.css("backgroundColor");
    this.stop().css("background-color", highlightBg)
        .animate({backgroundColor: originalBg}, animateMs);
};

var update_resources = function(data){
  var resourceName;
  var td;
  for (resourceName in data['gained_resources']){
    span = $('#resource-' + resourceName);
    currentCount = parseInt(span.text());
    currentCount += data['gained_resources'][resourceName];
    span.text(currentCount);
    td = span.closest('td');
    if (td.length > 0){
      td.animateHighlight("#5cb85c", 2000);
    }
    else {
      span.parent().closest('span').animateHighlight("#5cb85c", 2000);
    }
  }
  for (resourceName in data['used_resources']){
    var span = $('#resource-' + resourceName);
    currentCount = parseInt(span.text());
    currentCount -= data['used_resources'][resourceName];
    span.text(currentCount);
    td = span.closest('td');
    if (td.length > 0){
      console.log('attempting to remove td');
      td.animateHighlight('#d9534f', 2000);
    }
    else {
      span.parent().closest('span').animateHighlight('#d9534f', 2000);
    }
  }
};


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
