$('tr').each(function(){
  $(this).find('td').each(function(){
    if ($(this).html() == 'допущен') {
      $(this).parent('tr').addClass('empty');
      return false;
    }
    if ($(this).html() == "не допущен") {
      $(this).parent('tr').addClass('empty1');
      return false;
    }
  });
});

jQuery( function($) {
$('tbody tr[data-href]').addClass('clickable').click( function() {
window.location = $(this).attr('data-href');
});
});