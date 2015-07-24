var $j = jQuery.noConflict();
$j(document).on('ready', main_consulta);

var datosJson;
var newToken

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

	$j('#buscarICO').on('click', verDatos);
    $j('#id_dependencia').on('change', setImage);
    $j('#imprimirBTN').on('click', imprimeFicha);
    //valida_token();
    $.get("/obras/register-by-token", function(respu) {
        newToken=respu.access_token;
        setImage();
    });

}

function imprimeFicha(){
    if ($j('#idobraUNICO').val() != null && $j('#idobraUNICO').val() !="")
    {
        location.href="/obras/ficha?identificador_unico="+ $j.trim($j('#idobraUNICO').val().toString());
    };

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
            if (data.id!=null){location.href='/admin/obras/obra/'+data.id+'/?m=1';
            }
            else { alert('No existen registros con el ID Único ' + idUnico);}

        },
        error: function(data) {
            alert('error!! ' + data.status);
        }
    });
}

function setImage(){
            var idDep = $j("#id_dependencia").val();
            var sHtml="";

            var ajax_data = {"access_token"  : newToken};

            if(idDep.toString()!=""){ajax_data.id=idDep.toString();}


            $j.ajax({
                url: '/obras/api/dependencia_imagen',
                type: 'get',
                data: ajax_data,
                success: function(data) {
                    sHtml= '<img src="' + data[0].dependencia.imagenDependencia.toString() +'" >'
                    $j('#logoDEP').html(sHtml);

                },
                error: function(data) {
                    alert('Error ' + data.status);
                }
            });
        }




    $j(document).ready(function() {
         $j("input[name=inaugurada]").click(function () {
            var inauguradaOPC  = $j('input:radio[name=inaugurada]:checked').val();
             if (inauguradaOPC != "True") {
                 $j("#id_inaugurador").val('---------');
                 $j("#id_inaugurador").prop('disabled','disabled');
             }
             else{
                  $j("#id_inaugurador").removeAttr("disabled");
             }


         });


         $j('select#id_tipoObra').on('change',function () {
                var statusO = $j(this).val();
                var avanceO = $j("#id_porcentajeAvance").val();

                if (statusO == "1" && avanceO > 0) {
                    alert('Si el Status de Obra es PROYECTADA, el porcentaje de Avance debe ser igual a 0. Favor de verificar el Status.');
                    $j("#id_tipoObra").val('---------');
                }
                else if (statusO == "2" && (avanceO == 0 || avanceO == 100))
                {
                    alert('Si el Status de Obra es en PROCESO, el porcentaje de Avance debe ser mayor a 0 y menor a 100. Favor de verificar el Status.');
                    $j("#id_tipoObra").val('---------');
                }
                else if (statusO == "3" && avanceO <100)
                {
                    alert('Si el Status de Obra es CONCLUIDA, el porcentaje de Avance debe ser igual a 100. Favor de verificar el Status.');
                    $j("#id_tipoObra").val('---------');
                }

         });

         $j('#id_porcentajeAvance').on('change',function (){
                var avanceO = $j(this).val();
                var statusO = $j('select#id_tipoObra').val();

                if (statusO == "1" && avanceO > 0) {
                    alert('Si el Status de Obra es PROYECTADA, el porcentaje de Avance debe ser igual a 0. Favor de verificar el Status.');
                    $j("#id_porcentajeAvance").val('0');
                }
                else if (statusO == "2" && (avanceO == 0 || avanceO == 100))
                {
                    alert('Si el Status de Obra es en PROCESO, el porcentaje de Avance debe ser mayor a 0 y menor a 100. Favor de verificar el Status.');
                    $j("#id_porcentajeAvance").val('0');
                }
                else if (statusO == "3" && avanceO <100)
                {
                    alert('Si el Status de Obra es CONCLUIDA, el porcentaje de Avance debe ser igual a 100. Favor de verificar el Status.');
                    $j("#id_porcentajeAvance").val('100');
                }

         });

        $j('#id_fechaInicio').on('changeDate',function(){
            var vFecIni = this.val();
            alert("entra");
            if ($j('#id_fechaTermino').val() != "")
            {
                var iniDate = new Date(vFecIni),
                endDate = new Date($j('#id_fechaTermino').val());
                if(iniDate > endDate) {
                    alert("error");
                }
            }
        });

        $j('#id_fechaTermino').on('change',function(){
            var vFecFin = this.val();
        });



    });
