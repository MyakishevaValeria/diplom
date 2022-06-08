$('tr').each(function(){
  $(this).find('td').each(function(){
    if ($(this).html() == '35') {
      $(this).parent('tr').addClass('empty');
      return false;
    }
    if ($(this).html() == '32') {
      $(this).parent('tr').addClass('empty1');
      return false;
    }
    if ($(this).html() == "допущен") {
      $(this).parent('tr').addClass('empty2');
      return false;
    }
  });
});

jQuery( function($) {
$('tbody tr[data-href]').addClass('clickable').click( function() {
window.location = $(this).attr('data-href');
});
});