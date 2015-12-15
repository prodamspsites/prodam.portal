(function($) {
  $(document).ready(function() {

    if ($('body').hasClass('section-cidadao') || $('body').hasClass('section-empresa') || $('body').hasClass('section-turista')) {
      console.log('teste');
    }


    $(document).on('click', '.ploneCalendar td a', function(e) {
      e.preventDefault()
      year = $('#calendar-previous').data('year');
      month = parseInt($('#calendar-previous').data('month')) +1;
      day = $(this).text();
      date = month + '/' + day + '/' + year;
      var form = $('<form action="' + portal_url + '/agenda/agenda-prefeito" method="post">' +
                   '<input type="text" name="date" value="' + date + '" />' +
                   '</form>');
      $('body').append(form);
      console.log(date)
      form.submit();
      return false
    });

    $(document).on('click', '#servicos-externos a', function(e) {
      e.preventDefault();
      thisClass = $(this).parent().parent().attr('class').split(' ')[0]
      url = portal_url + '/@@sp-agora';
      $.post( url, { id: thisClass })
        .done(function( data ) {
          html = '<div id="' + thisClass + '" class="dash">' + data + '</div>'
          $(html).insertAfter("#servicos-externos");
        });
      return false
    });

    $(document).on('click', '.dash .fechar-dash', function(e) {
      $('.dash').remove();
    })

    if ($('body').hasClass('site-Prefeitura')) {
      // calendarUrl = portal_url + '/agenda/';

      // function getCalendar(calendarUrl) {
      //     $.ajax({url: calendarUrl, success: function(calendar) {

      //     calendar = $(calendar).find('dl.portletCalendar');
      //     $(calendar).find('*').each(function() {$(this).removeClass()});
      //     $(calendar).find('#calendar-previous').removeAttr('id').addClass('prev-month');
      //     $(calendar).find('#calendar-next').removeAttr('id').addClass('next-month');

      //     year = $(calendar).find('.prev-month').data('year');
      //     month = parseInt($(calendar).find('.prev-month').data('month')) +1;
      //     prevMonth = 0;
      //     nextMonth = 0;


      //     function getPrevMonth() {
      //       prevMonth = month -1;
      //       url = portal_url + '/agenda/?month=' + prevMonth + '&year=' + year;
      //       _prevDays = $(calendar).find('tbody tr:first td:empty');
      //       $.ajax({url: url, success: function(result){
      //         prevDays = $(result).find('tbody tr:last td:not(:empty)');
      //       }}).done(function() {
      //         $(_prevDays).each(function(i) {
      //           $(this).html($(prevDays[i]).html())
      //         })
      //         $('#agendaPrefeito').html(calendar);
      //       });
      //     };

      //     function getNextMonth() {
      //       nextMonth = month +1;
      //       url = portal_url + '/agenda/?month=' + nextMonth + '&year=' + year;
      //       _nextDays = $(calendar).find('tbody tr:last td:empty');

      //       $.ajax({url: url, success: function(result){
      //         nextDays = $(result).find('tbody tr:first td:not(:empty)');
      //         _nextDays.length > 0 ? tr = 'tr:nth-child(2)' : tr = 'tr:first';
      //         getNextWeek = $(result).find('tbody '+ tr);
      //       }}).done(function() {
      //         $(_nextDays).each(function(i) {
      //           $(this).html($(nextDays[i]).html());
      //         })
      //         $('tbody', calendar).append(getNextWeek);
      //       });
      //     };

      //     getNextMonth();
      //     getPrevMonth();

      //     function changeMonth(value) {
      //       month = month + value;
      //     }

      //   }})
      // }

      // $(document).on('click', 'a.prev-month, a.next-month', function(e) {
      //   e.preventDefault()
      //   thisMonth = $(this).data('month');
      //   thisYear = $(this).data('year');
      //   url = portal_url + '/agenda/' + '?month:int='+thisMonth+'&year:int='+thisYear;
      //   getCalendar(url);

      //   return false
      // });

      // getCalendar(calendarUrl);


      $(document).on('click', '.ploneCalendar td a', function(e) {
        e.preventDefault()
        year = $('#calendar-previous').data('year');
        month = parseInt($('#calendar-previous').data('month')) +1;
        day = $(this).text();
        date = month + '/' + day + '/' + year;
        var form = $('<form action="' + portal_url + '/agenda/agenda-prefeito" method="post">' +
                     '<input type="text" name="date" value="' + date + '" />' +
                     '</form>');
        $('body').append(form);
        console.log(date)
        form.submit();
        return false
      });

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
