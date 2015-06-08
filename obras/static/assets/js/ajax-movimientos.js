var $j = jQuery.noConflict();
$j(document).on('ready', main_consulta);

var datosJson;

function main_consulta() {
    $j.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if(settings.type == "POST"){
				xhr.setRequestHeader("X-CSRFToken", $j('[name="csrfmiddlewaretoken"]').val());
               // alert($j('[name="csrfmiddlewaretoken"]').val());
			}
            if(settings.type == "GET"){
				xhr.setRequestHeader("X-CSRFToken", $j('[name="csrfmiddlewaretoken"]').val());
               //  alert($j('[name="csrfmiddlewaretoken"]').val());
			}
		}
	});

	$j('#buscarICO').on('click', verDatos);

}




function verDatos() {
    var idUnico = $j("#idobra").val();



    var ajax_data = {
      "access_token"  : 'ibpbhu2gOyZXMpCWzUvOITDJZ9XSso'
    };

    if(idUnico.toString()!=""){ajax_data.identificador_unico=idUnico.toString();}



    $j.ajax({
        url: '/obras/api/id_unico',
        type: 'get',
        data: ajax_data,
        success: function(data) {
            //$j('#datos').html
           //alert('success!!! ' + data.id);
            if (data.id!=null){location.href='/admin/obras/obra/'+data.id+'/?m=1';}
            else { alert('No existen registros con elID Único ' + idUnico);}

        },
        error: function(data) {
            alert('error!!! ' + data.status);
        }
    });
}


