/**
 * 
 */

    

var num = 50; //number of pixels before modifying styles

$(window).bind('scroll', function () {
    if ($(window).scrollTop() > 50) {
        $('.busca').addClass('fixed');
    } else {
        $('.busca').removeClass('fixed');
    }
});


$(document).ready(function() {
    
    $('#inversionInicial').numeric({ decimalPlaces: 2 });
 
    
    
    
    $(".numeric").numeric();
	$(".integer").numeric(false, function() { alert("Integers only"); this.value = ""; this.focus(); });
	$(".positive").numeric({ negative: false }, function() { alert("No negative values"); this.value = ""; this.focus(); });
	$(".positive-integer").numeric({ decimal: false, negative: false }, function() { alert("Positive integers only"); this.value = ""; this.focus(); });
    
	$("#remove").click(
		function(e)
		{
			e.preventDefault();
			$(".numeric,.integer,.positive,.positive-integer,.decimal-2-places").removeNumeric();
		}
	);
    
    
});