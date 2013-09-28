(function(document, $, Mustache) {
    "use strict";

    var $document = $(document);
   
    var ajax = {

        settings: null,

        getCookie: function(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            else
            {
                cookieValue = undefined;
            }
            return cookieValue;
        }, 

        setCookie: function(c_name,value,exdays) {
            var exdate=new Date();
            exdate.setDate(exdate.getDate() + exdays);
            var c_value=escape(value) + ((exdays===null) ? "" : "; expires="+exdate.toUTCString());
            document.cookie=c_name + "=" + c_value;
        },

        csrfSafeMethod: function(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        },

        request: function(url,type,data) {
            //check if csfr token is required
            if(!this.csrfSafeMethod(type))
            {
                var csrftoken = this.csrftoken;
            }
            var result = null;

            $.ajax({
                crossDomain: false, // obviates need for sameOrigin test
                url: url,
                type: type,
                data: JSON.stringify(data),
                dataType: "json",
                async: false,
                 statusCode: {
                    401: function() {
                        this.login();
                    },

                },
                beforeSend: function(xhr) {
                    //set csrf token
                    if (csrftoken) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }

                    if (xhr && xhr.overrideMimeType) {
                      xhr.overrideMimeType("application/j-son;charset=UTF-8");
                    }

                },
                success: function(result_) {
                    result = {"content": result_,
                              "ok": true
                            };

                            
                },
                error: function(xhr){
                    result = {"content": JSON.parse(xhr.responseText),
                              "ok": false,
                    };
                }
            });
            return result;
        },


        init: function(){
            this.csrftoken = this.getCookie('csrftoken');
        }
    }; 



    var mustache = {
        settings: null,
        templates: {},
        modal: null,

        init: function (file, modal_placeholder, modal_template) {
            var that = this;
            this.settings = {"modal_template": modal_template};
            this.modal = $(modal_placeholder);
            $.ajaxSetup({async:false});
            $.get(file, function(template) {

                $(template).filter(".template").each(function( index, tpl ) {
                    //console.log($(tpl).data("name"));
                    that.templates[$(tpl).data("name")] = '{{=<% %>=}} \n'+$(tpl).html();
                });
            });
            $.ajaxSetup({async:true});
            
        },

        render: function(tpl_name, data){

            if(tpl_name in this.templates)
            {

                if( data === undefined ){
                    data = {};
                }

                return Mustache.render(this.templates[tpl_name], this.standartFunctions(data));
            }
            else
            {
                return false;
            }
        },

        standartFunctions : function(vars){
            vars.csrftoken = ajax.csrftoken;
            return vars;
        },


        displayModal: function(modal_name, vars)
        {
            var template = this.render(modal_name, vars);
            this.modal.html(template);
            this.modal.modal('show');
            this.bind();
        },

        hideModal: function()
        {
            this.modal.modal('hide');
        },

        times: function(n){
            var c = 0;
            var temp = [];
            while( n > c)
            {
                temp.push(n);
                c++;
            }
            return temp;
        },

        login: function(){
            this.displayModal("login", {});
        },

        bind: function(){
            var that = this;
            $("a[data-action=login]").on("click",function(){
                that.displayModal("login", {});
            });

            $("a[data-action=signup]").on("click",function(){
                that.displayModal("signup", {});
            });

            $("a[data-action=forget-password]").on("click",function(){
                that.displayModal("forget-password", {});
            });
        }

    };


    var page_form = {


        settings: null,
        templates: {},
        $div: null,
        modal: null,
        data: {
            "items": [],
            "name": null,
            "tags": []
        },

        init: function (id) {
            this.$div =  $(id);
            
        },

        add_point: function(){

            var data = {};
            data.title = $("[data-field=item-title]").val();
            $("[data-field=item-title]").val('');
            data.text = $("[data-field=item-text]").val();
            $("[data-field=item-text]").val('');

            this.data.items.push(data);
            this.render(data);

        },

        render: function(obj){
            this.$div.append(mustache.render("form-argument", obj));
        },

        save: function(){

            this.data.tags = $("[data-field=item-tags]").val().split(", ");
            this.data.name = $("[data-field=item-name]").val();
            var resp = ajax.request("/pages/create/ajax", "POST", this.data);
            window.location = "/pages/"+resp.content.slug;
            console.log(this.data);


        },

        bind: function(){
            var that = this;
            $("a[data-action=add-point]").on("click",function(){
               console.log("add-point");
               that.add_point();
            });

            $("a[data-action=save-page]").on("click",function(){
               console.log("save-page");
               that.save();
               return false;
            });

        }

    }

    

    $document.ready(function () {

        ajax.init();

        mustache.init("/js_templates.mustache", 
                      "#Modal", 
                      "modal");
        mustache.bind();
        page_form.init("#arguments");
        page_form.bind();

    });

    

})(document, jQuery, Mustache);