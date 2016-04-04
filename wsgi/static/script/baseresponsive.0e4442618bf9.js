$("img").addClass("img-responsive img-thumbnail");
var w = $(window);
var r = function(){$("body").css("padding-top", $(".navbar-fixed-top").height()+20); $("body").css("padding-bottom", (w.height()*0.1) );}
w.resize(r);
w.load(r);
