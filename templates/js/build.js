
var build_data = [];

var build = function(btn){
  btn = $(btn);
  var toolName = btn.data('tool');
  var data = build_data[toolName];
  if (data){
    update_resources(data);
  }
  else {
    data = [];
    build_data[toolName] = data;

  }
  if (typeof(data['outstandingClicks']) !== "undefined"){
    data['outstandingClicks'] += 1;
    outstandingClicks = data['outstandingClicks'];
  }
  else{
    outstandingClicks = 1
  }

  if (typeof(data['outstandingClicks']) === 'undefined' || outstandingClicks >= 10){
    $.ajax({
      url: '/build/tools/' + toolName + "/?clicks=" + outstandingClicks,
      method: 'PUT',
      success: function(resp) {
        if (!data['gained_resources']){
          resp = $.parseJSON(resp);
          data = resp;
          update_resources(resp);
        }
       data['outstandingClicks'] = 0;
      }
    });

  }
};

var update_resources = function(data){
  for (var resourceName in data['gained_resources']){
    var span = $('#resource-' + resourceName);
    currentCount = parseInt(span.text());
    currentCount += data['gained_resources'][resourceName];
    span.text(currentCount);
  }
  for (var resourceName in data['used_resources']){
    var span = $('#resource-' + resourceName);
    currentCount = parseInt(span.text());
    currentCount -= data['used_resources'][resourceName];
    span.text(currentCount);
  }
};

window.onbeforeunload = function() {
  for (var toolName in build_data){
    var data = build_data[toolName];
    outstandingClicks = data['outstandingClicks'];
     $.ajax({
      url: '/build/tools/' + toolName + "/?clicks=" + outstandingClicks,
      method: 'PUT'
    });

  }
};
