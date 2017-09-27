$(".geocomplete").geocomplete();
// Trigger geocoding request.
$("button.find").click(function(){
    $("input").trigger("geocode");
});