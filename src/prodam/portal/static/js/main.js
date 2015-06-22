(function($) {
   $(document).ready(function() {
     $(".noticias_actions a").bind("click", function () {
        event.preventDefault();
        var size = parseInt($('.contentBody').css("font-size"));
        if ($(this).hasClass("aumentar_fonte")) {
          size = size + 6;
        } else {
          size = size - 6;
          if (size <= 10) {
            size = 10;
          }
        }
        $('.contentBody').css({"font-size": size, "line-height": "100%"});
      });
   })
})(jQuery);