var $j = jQuery.noConflict();
$j(document).on('ready', main_consulta);

var datosJson;
var newToken;

function valida_token(){
var ajax_datatoken = {
      "access_token"  : 'O9BfPpYQuu6a5ar4rGTd2dRdaYimVa'
    };


    $j.ajax({
        url: '/obras/register-by-token',
        type: 'get',
        data: ajax_datatoken,
        success: function(data) {
            newToken = data.access_token;
            //alert(data.access_token);
        },
        error: function(data) {
            alert('error!!! ' + data.status);
        }
    });
}

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
    valida_token();
	$j('#buscarICO').on('click', verDatos);

}




function verDatos() {
    var idUnico = $j("#idobra").val();



    var ajax_data = {
      "access_token"  : newToken
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


