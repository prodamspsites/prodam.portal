(function($) {
   $(document).ready(function() {
     $("#clickVideo a").bind("click", function () {
        event.preventDefault();
        var thisItem = $(this);
        var thisTitle = $(thisItem).attr('title');
        var thisLink = $(thisItem).attr('rel');
        var video = '<object width="290" height="203"><param name="movie" value="'+thisLink+'"><param name="allowScriptAccess" value="always"><embed src="'+thisLink+'" type="application/x-shockwave-flash" allowscriptaccess="always" width="290" height="203"></object>';
        $('.destaque').html(video);
        $('#tituloVideo').text(thisTitle)
     })
     $("#tab-cid").bind("click", function(){
        event.preventDefault();
        $(".secoesServicos").hide();
        $("#home-secoes-cidadao").show();
     })
     $("#tab-emp").bind("click", function(){
        event.preventDefault();
        $(".secoesServicos").hide();
        $("#home-secoes-empresa").show();
     })
     $("#tab-tur").bind("click", function(){
        event.preventDefault();
        $(".secoesServicos").hide();
        $("#home-secoes-turista").show();
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