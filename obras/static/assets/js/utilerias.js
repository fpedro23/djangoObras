/**
 * 
 */

    

var num = 50; //number of pixels before modifying styles
var $nums=jQuery.noConflict();
$nums(window).bind('scroll', function () {
    if ($nums(window).scrollTop() > 50) {
        $nums('.busca').addClass('fixed');
    } else {
        $nums('.busca').removeClass('fixed');
    }
});


$nums(document).ready(function() {
    
    $nums('#inversionInicial').numeric({ decimalPlaces: 2 });
    $nums('#inversionFinal').numeric({ decimalPlaces: 2 });
 
    
    
    
    $nums(".numeric").numeric();
	$nums(".integer").numeric(false, function() { alert("Integers only"); this.value = ""; this.focus(); });
	$nums(".positive").numeric({ negative: false }, function() { alert("No negative values"); this.value = ""; this.focus(); });
	$nums(".positive-integer").numeric({ decimal: false, negative: false }, function() { alert("Positive integers only"); this.value = ""; this.focus(); });
    
	$nums("#remove").click(
		function(e)
		{
			e.preventDefault();
			$nums(".numeric,.integer,.positive,.positive-integer,.decimal-2-places").removeNumeric();
		}
	);
    
    
});