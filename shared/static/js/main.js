jQuery.extend({
    getValues: function(url) {
        var result = null;
        $.ajax({
            url: url,
            type: 'get',
            dataType: 'json',
            async: false,
            success: function(data) {
                result = data;
            }
        });
       return result;
    }
});


(function(document, $) {
    "use strict";

    var $document = $(document);

    var classname = {
        settings: null,


        bind: function () {
            var that = this;


            $("div").on('click', function(e){

            });

            $document.keypress(function(e) {
                if(e.which == 13) {
                }
            });
        },


        init: function () {
            this.settings = $("#settings").data("settings");
        },

        mustache: function(){
            var view = {
              title: "Joe",
              calc: function () {
                return 2 + 4;
              }
            };
            var output = Mustache.render("{{title}} spends {{calc}}", view);
            console.log(output);
        },
    }





    $document.ready(function () {
        
        classname.init();
        classname.bind()
        
    });

})(document, jQuery);
