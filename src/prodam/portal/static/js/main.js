(function($) {
   $(document).ready(function() {
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