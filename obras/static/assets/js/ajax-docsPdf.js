/**
 * Created by usuario on 30/04/2015.
 */
/**
 * Created by db2 on 7/04/15.
 */
var $j = jQuery.noConflict();

$j(document).on('ready', main_consulta);

function main_consulta() {
    $j.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if(settings.type == "POST"){
				xhr.setRequestHeader("X-CSRFToken", $j('[name="csrfmiddlewaretoken"]').val());
			}
            if(settings.type == "GET"){
				xhr.setRequestHeader("X-CSRFToken", $j('[name="csrfmiddlewaretoken"]').val());
			}
		}
	});

    $j('#crearObra').on('click', crear_obra)
    $j('#modificarObra').on('click', modificar_obra)
    $j('#agregarClasificacion').on('click', agregar_clasificacion)
    $j('#buscarClasificacion').on('click', buscar_clasificacion)


}

function crear_obra(){
    verDocPdf('ManualAltaObra','Crear una Obra');
}
function modificar_obra(){
    //verVideo('modificacionObra.mp4','Modificar una Obra');
}
function agregar_clasificacion(){
    //verVideo('agregarClasificacion.mp4','Agregar una Clasificación');
}
function buscar_clasificacion(){
    //verVideo('buscarClasificacion.mp4','Buscar una Clasificación');
}
function verDocPdf(nombreVideo,titulo){


    $('#titulo').html(titulo);
    //$j('#descripcion').html(descripcion);
    $('#vistaPdf').html('<embed src="media/videos/Python_Web_Development_with_Django.pdf" width="720" height="375">');


}