$('tr').each(function(){
  $(this).find('td').each(function(){
    if ($(this).html() == 'Испрсавен') {
    $(this).parent('tr').addClass('empty');
      return false;
    }
    if ($(this).html() == 'Неиспсравен') {
      $(this).parent('tr').addClass('empty1');
      return false;
    }
    if ($(this).html() == '7132') {
      $(this).parent('tr').addClass('empty1');
      return false;
    }
  });
});


