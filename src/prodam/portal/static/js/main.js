(function($) {
  $(document).ready(function() {
    if ($('body').hasClass('section-agenda')) {
      year = $('#calendar-previous').data('year');
      month = parseInt($('#calendar-previous').data('month')) +1;
      prevMonth = 0;
      nextMonth = 0;

      function getPrevMonth() {
        prevMonth = month -1;
        url = window.location.href + '?month=' + prevMonth + '&year=' + year;
        _prevDays = $('.ploneCalendar tbody tr:first td:empty');
        $.ajax({url: url, success: function(result){
          prevDays = $(result).find('.ploneCalendar tbody tr:last td:not(:empty)');
        }}).done(function() {
          $(_prevDays).each(function(i) {
            $(this).html($(prevDays[i]).html())
          })
        });
      };

      function getNextMonth() {
        nextMonth = month +1;
        url = window.location.href + '?month=' + nextMonth + '&year=' + year;
        _nextDays = $('.ploneCalendar tbody tr:last td:empty')

        $.ajax({url: url, success: function(result){
          nextDays = $(result).find('.ploneCalendar tbody tr:first td:not(:empty)');
          _nextDays ? tr = 'tr:first' : tr = 'tr:nth-child(2)';
          getNextWeek = $(result).find('.ploneCalendar tbody '+ tr);
        }}).done(function() {
          $(_nextDays).each(function(i) {
            $(this).html($(nextDays[i]).html());
          })
          $('.ploneCalendar tbody').append(getNextWeek);
        });
      };

      getNextMonth();
      getPrevMonth();
      $('.portletCalendar').show();

      function changeMonth(value) {
        month = month + value;
      }
    }

    $('select.lista-institucionais').change(function(){
      var url = $(this).val();
      window.location = url;
    });
    $("#clickVideo a").bind("click", function () {
      event.preventDefault();
      var thisItem = $(this);
      var thisTitle = $(thisItem).attr('title');
      var thisLink = $(thisItem).attr('rel');
      var video = '<object width="290" height="203"><param name="movie" value="'+thisLink+'"><param name="allowScriptAccess" value="always"><embed src="'+thisLink+'" type="application/x-shockwave-flash" allowscriptaccess="always" width="290" height="203"></object>';
      $('.destaque').html(video);
      $('#tituloVideo').text(thisTitle);
    })
    $("#tab-cid a").bind("click", function(){
      $(".secao-pai a").removeClass("menuAtivo");
      $("#tab-cid a").addClass("menuAtivo");
      $(".secoesServicos").hide();
      $("#home-secoes-cidadao").show();
      return false;
    })
    $("#tab-emp a").bind("click", function(){
      $(".secao-pai a").removeClass("menuAtivo");
      $("#tab-emp a").addClass("menuAtivo");
      $(".secoesServicos").hide();
      $("#home-secoes-empresa").show();
      return false;
    })
    $("#tab-tur a").bind("click", function(){
      $(".secao-pai a").removeClass("menuAtivo");
      $("#tab-tur a").addClass("menuAtivo");
      $(".secoesServicos").hide();
      $("#home-secoes-turista").show();
      return false;
    })
    $(".noticias_actions a").bind("click", function () {
      event.preventDefault();
      var size = parseInt($('.contentBody').css("font-size"));
      if ($(this).hasClass("aumentar_fonte")) {
        if(size < 24 ) {
          size = size + 2;
        }
      } else {
        if(size > 12 ) {
          size = size - 2;
        }
      }
      $('.contentBody').css("font-size", size);
    });
  })
})(jQuery);
