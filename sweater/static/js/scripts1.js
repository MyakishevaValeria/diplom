$('tr').each(function(){
  $(this).find('td').each(function(){
    if ($(this).html() == '10') {
    $(this).parent('tr').addClass('empty1');
      return false;
    }
    if ($(this).html() == '0.0') {
      $(this).parent('tr').addClass('empty1');
      return false;
    }
  });
});
