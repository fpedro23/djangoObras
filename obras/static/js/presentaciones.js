/**
 * Created by db2 on 7/04/15.
 */
$(document).on('ready', main_presentaciones);

function main_presentaciones() {
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if(settings.type == "POST"){
				xhr.setRequestHeader("X-CSRFToken", $('[name="csrfmiddlewaretoken"]').val());
			}
		}
	});

	$('#balancegeneral button').on('click', balance_general);
    $('#hiperinfogeneral button').on('click', hiper_info_general);
    $('#hiperinauguradas button').on('click', hiper_inauguradas);
    $('#hiperporsector button').on('click', hiper_por_sector);
    $('#hiperporentidad button').on('click', hiper_por_entidad);

    $('#balancegeneralppt').on('click', balance_general);

}

function balance_general() {
		$.post('balance-general-ppt');
}
function hiper_info_general() {
		$.post('hiper-info-general-ppt');
}
function hiper_inauguradas() {
		$.post('hiper-inauguradas-ppt');
}
function hiper_por_sector() {
		$.post('hiper-por-sector-ppt');
}
function hiper_por_entidad() {
		$.post('hiper-por-entidad-ppt');
}