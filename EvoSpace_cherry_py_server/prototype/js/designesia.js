// ===============================
// designesia 2011  //
// ===============================

$(document).ready(function() {
  $(".hide_content").hide();
  $(".min").hide();

  $(".plus").click(function()
  {
	$(this).slideToggle(100);
	$(".min").show();
    $(this).next(".hide_content").slideToggle(200);
    $(this).next(".min").slideToggle(200);

});
  
  $(".min").click(function()
  {
	$(this).parent().prev(".plus").slideToggle(200);
    $(this).parent().slideToggle(200);
	$(this).fadeOut(10);
  });

  
});


// ===============================
// fading object //
// ===============================


$(document).ready(function(){

$('.pic_hover').hover(
    function() {
        $(this).find('.rollover').stop().fadeTo(150, 1);
    },
	
    function() {
		$(this).find('.rollover').stop().fadeTo(150, 0);
    }	
)

});


$(document).ready(function(){
	$("#wrapper").fadeIn(700);
	$(".hide_content .inner").css("-webkit-border-radius", "20px");
	$(".hide_content .inner").css("-moz-border-radius", "20px");
	$(".contact_form_holder").css("-moz-border-radius", "10px");

	$("#social-icons img").stop().animate({"opacity": ".25"}, "50");
	
	$("#social-icons img").hover(
	function() {
	$(this).stop().animate({"opacity": "1"}, "50");
	},
	function() {
	$(this).stop().animate({"opacity": ".25"}, "50");
	
});
 
});

// set all images opacity

$(document).ready(function(){
$('.pf_gallery li').hover(function() {
	$('.pf_gallery li').not($(this)).stop().animate({opacity: .3}, 100);
	
}, function() {
    $('.pf_gallery li').stop().animate({opacity: 1});}, 100);


});
