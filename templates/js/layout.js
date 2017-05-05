function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

$.fn.animateHighlight = function(highlightColor, duration) {
    var highlightBg = highlightColor || "#FFFF9C";
    var animateMs = duration || 1500;
    var originalBg = this.css("backgroundColor");
    this.stop().css("background-color", highlightBg)
        .animate({backgroundColor: originalBg}, animateMs);
};


function update_resources(data){
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
}

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip({container: 'body'});

    $('#notifications-button').click(function() {
      var notificationIDs = [];
      $('li.notification').each(function(){
        notificationIDs.push($(this).data('id'))
      });
      console.log(notificationIDs);
      $.ajax({
        url: '/notifications/mark_as_read/',
        data: JSON.stringify(notificationIDs),
        contentType: 'application/json',
        method: 'PUT',
        success: function() {
          $('.notification-icon').removeClass('notification-icon');
        }
      });
    });

    if ($('.notification-icon').first().data('count') == '0'){
      $('.notification-icon').removeClass('notification-icon');
    }
});
