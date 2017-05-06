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

$(document).ready(function(){
  window.setInterval(updateProgressBars, 1000);

  function updateProgressBars(){
    var secondsSinceLast;
    var progress;
    var totalExp;
    var intSecondsSinceLast;
    var roundedSecondsSinceLast;
    $('.tick-progress').each(function(){
      secondsSinceLast = $(this).data('seconds_since_last_tick');
      intSecondsSinceLast = parseInt(secondsSinceLast);
      intSecondsSinceLast += 1;
      $(this).data('seconds_since_last_tick', intSecondsSinceLast.toString());
      totalExp = $(this).data('seconds_between_ticks');
      progress = (100 * (parseInt(secondsSinceLast) + 1)) / parseInt(totalExp);
      progress = progress % 100;
      progress = progress.toString();
      roundedSecondsSinceLast = intSecondsSinceLast % totalExp;
      if (roundedSecondsSinceLast == 0){
        handleFullProgressBar($(this));
      }
      $(this).css('width', progress + "%");
      $(this).text( roundedSecondsSinceLast.toString() + '/' + totalExp);

    });
  }

  function handleFullProgressBar(bar){
    var production = bar.data('production_per_tick');
    var data = {'gained_resources': JSON.parse(production), 'used_resources': {}};
    console.log(data);
    update_resources(data)
  }

});
