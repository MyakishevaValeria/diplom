$('tr').each(function(){
  $(this).find('td').each(function(){
    if ($(this).html() == '10.0') {
      $(this).parent('tr').addClass('empty');
      return false;
    }
    if ($(this).html() == '0.0') {
      $(this).parent('tr').addClass('empty1');
      return false;
    }
    if ($(this).html() == '6.5') {
      $(this).parent('tr').addClass('empty2');
      return false;
    }
  });
});