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
            else {
                //alert('No existen registros con el ID Único ' + idUnico);
                    $j.magnificPopup.open({
                        items: {
                            src:  '<div id="test-modal" class="alertaVENTANA" style="top:0px; left: 450px;">'
                                  + '<div class="textoALERTA">'
                                  + 'No existen registros con el ID Único: ' + idUnico
                                  + '</div>'
                                  + '<a class="popup-modal-dismiss" href="#"><div class="aceptarBTN" style="left:150px;"> </div></a>'
                                  + '</div>'
                        },
                        type: 'inline',
                        preloader: true,
                        modal: true
                    });

                    $j(document).on('click', '.popup-modal-dismiss', function (e) {
                        e.preventDefault();
                        $j.magnificPopup.close();
                    });
            }

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
                    // alert('Error ' + data.status);
                         $j.magnificPopup.open({
                        items: {
                            src:  '<div id="test-modal" class="alertaVENTANA" style="top:0px; left: 450px;">'
                                  + '<div class="textoALERTA">'
                                  + 'Error ' + data.status
                                  + '</div>'
                                  + '<a class="popup-modal-dismiss" href="#"><div class="aceptarBTN" style="left:150px;"> </div></a>'
                                  + '</div>'
                        },
                        type: 'inline',
                        preloader: true,
                        modal: true
                    });

                    $j(document).on('click', '.popup-modal-dismiss', function (e) {
                        e.preventDefault();
                        $j.magnificPopup.close();
                    });
                }
            });
        }




    $j(document).ready(function() {
         $j("input[type=text]").keyup(function () {
             $j(this).val($(this).val().toUpperCase());

         });

        $j("textarea").keyup(function () {
             $j(this).val($(this).val().toUpperCase());

         });

         $j(".guardarOBTN").on('click', function(){

             if ($j('#id_inversionTotal').val() == 0 || $j('#id_inversionTotal').val() == '' ){
                   $j.magnificPopup.open({
                        items: {
                            src:  '<div id="test-modal" class="alertaVENTANA" style="top:0px; left: 450px;">'
                                  + '<div class="textoALERTA">'
                                  + 'El monto de Inversión Total debe ser mayor a 0. Favor de verificar.'
                                  + '</div>'
                                  + '<a class="popup-modal-dismiss" href="#"><div class="aceptarBTN" style="left:150px;"> </div></a>'
                                  + '</div>'
                        },
                        type: 'inline',
                        preloader: true,
                        modal: true
                    });

                    $j(document).on('click', '.popup-modal-dismiss', function (e) {
                        e.preventDefault();
                        $j.magnificPopup.close();
                    });
             }
             else
             {
                 document.getElementById('obra_form').submit('_save');
             }
         });

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
                    //alert('Si el Status de Obra es PROYECTADA, el porcentaje de Avance debe ser igual a 0. Favor de verificar el Status.');
                      $j.magnificPopup.open({
                        items: {
                            src:  '<div id="test-modal" class="alertaVENTANA" style="top:0px; left: 450px;">'
                                  + '<div class="textoALERTA">'
                                  + 'Si el Status de Obra es PROYECTADA, el porcentaje de Avance debe ser igual a 0. Favor de verificar el Status.'
                                  + '</div>'
                                  + '<a class="popup-modal-dismiss" href="#"><div class="aceptarBTN" style="left:150px;"> </div></a>'
                                  + '</div>'
                        },
                        type: 'inline',
                        preloader: true,
                        modal: true
                    });

                    $j(document).on('click', '.popup-modal-dismiss', function (e) {
                        e.preventDefault();
                        $j.magnificPopup.close();
                    });

                    $j("#id_tipoObra").val('---------');
                }
                else if (statusO == "2" && (avanceO == 0 || avanceO == 100))
                {
                    //alert('Si el Status de Obra es en PROCESO, el porcentaje de Avance debe ser mayor a 0 y menor a 100. Favor de verificar el Status.');
                    $j.magnificPopup.open({
                        items: {
                            src:  '<div id="test-modal" class="alertaVENTANA" style="top:0px; left: 450px;">'
                                  + '<div class="textoALERTA">'
                                  + 'Si el Status de Obra es en PROCESO, el porcentaje de Avance debe ser mayor a 0 y menor a 100. Favor de verificar el Status.'
                                  + '</div>'
                                  + '<a class="popup-modal-dismiss" href="#"><div class="aceptarBTN" style="left:150px;"> </div></a>'
                                  + '</div>'
                        },
                        type: 'inline',
                        preloader: true,
                        modal: true
                    });

                    $j(document).on('click', '.popup-modal-dismiss', function (e) {
                        e.preventDefault();
                        $j.magnificPopup.close();
                    });

                    $j("#id_tipoObra").val('---------');
                }
                else if (statusO == "3" && avanceO <100)
                {
                    //alert('Si el Status de Obra es CONCLUIDA, el porcentaje de Avance debe ser igual a 100. Favor de verificar el Status.');
                    $j.magnificPopup.open({
                        items: {
                            src:  '<div id="test-modal" class="alertaVENTANA" style="top:0px; left: 450px;">'
                                  + '<div class="textoALERTA">'
                                  + 'Si el Status de Obra es CONCLUIDA, el porcentaje de Avance debe ser igual a 100. Favor de verificar el Status.'
                                  + '</div>'
                                  + '<a class="popup-modal-dismiss" href="#"><div class="aceptarBTN" style="left:150px;"> </div></a>'
                                  + '</div>'
                        },
                        type: 'inline',
                        preloader: true,
                        modal: true
                    });

                    $j(document).on('click', '.popup-modal-dismiss', function (e) {
                        e.preventDefault();
                        $j.magnificPopup.close();
                    });

                    $j("#id_tipoObra").val('---------');
                }

                if ($j('#id_fechaInicio').val() != '') {
                     var VSDate = new Date($dp('#id_fechaInicio').datepicker("getDate"));
                }
                else {
                    var VSDate = "";
                }
                if ($j('#id_fechaTermino').val() != '') {
                    var VEDate = new Date($dp('#id_fechaTermino').datepicker("getDate"));
                }
                else{
                    var VEDate ="";
                }
                var VToday = new Date();

                if(statusO == '1'){

                    if (VSDate !='' && VSDate < VToday){
                        $j('select#id_tipoObra').val('---------');
                                        $j.magnificPopup.open({
                                                items: {
                                                    src:  '<div id="test-modal" class="alertaVENTANA" style="top:0px; left: 450px;">'
                                                          + '<div class="textoALERTA">'
                                                          +  'El Status de la obra debe ser en PROCESO  y el Avance mayor a 0'
                                                          + '</div>'
                                                          + '<a class="popup-modal-dismiss" href="#"><div class="aceptarBTN" style="left:150px;"> </div></a>'
                                                          + '</div>'
                                                },
                                                type: 'inline',
                                                preloader: true,
                                                modal: true
                                            });

                                            $j(document).on('click', '.popup-modal-dismiss', function (e) {
                                                e.preventDefault();
                                                $j.magnificPopup.close();
                                            });
                    }
                    if (VSDate !='' && VEDate !='' && VSDate < VToday && VEDate > VToday){
                        $j('select#id_tipoObra').val('---------');
                                        $j.magnificPopup.open({
                                                items: {
                                                    src:  '<div id="test-modal" class="alertaVENTANA" style="top:0px; left: 450px;">'
                                                          + '<div class="textoALERTA">'
                                                          +  'El Status de la obra debe ser en PROCESO  y el Avance mayor a 0'
                                                          + '</div>'
                                                          + '<a class="popup-modal-dismiss" href="#"><div class="aceptarBTN" style="left:150px;"> </div></a>'
                                                          + '</div>'
                                                },
                                                type: 'inline',
                                                preloader: true,
                                                modal: true
                                            });

                                            $j(document).on('click', '.popup-modal-dismiss', function (e) {
                                                e.preventDefault();
                                                $j.magnificPopup.close();
                                            });
                    }
                    if (VSDate !="" && VEDate !="" && VSDate < VToday && VEDate < VToday) {
                        $j('select#id_tipoObra').val('---------');
                                        $j.magnificPopup.open({
                                                items: {
                                                    src:  '<div id="test-modal" class="alertaVENTANA" style="top:0px; left: 450px;">'
                                                          + '<div class="textoALERTA">'
                                                          +  'El Status de la obra debe ser en CONCLUIDA  y el Avance igual a 100'
                                                          + '</div>'
                                                          + '<a class="popup-modal-dismiss" href="#"><div class="aceptarBTN" style="left:150px;"> </div></a>'
                                                          + '</div>'
                                                },
                                                type: 'inline',
                                                preloader: true,
                                                modal: true
                                            });

                                            $j(document).on('click', '.popup-modal-dismiss', function (e) {
                                                e.preventDefault();
                                                $j.magnificPopup.close();
                                            });
                    }
                }
                if(statusO == '2') {
                    if (VSDate !="" && VSDate > VToday) {
                        $j('select#id_tipoObra').val('---------');
                        $j.magnificPopup.open({
                            items: {
                                src: '<div id="test-modal" class="alertaVENTANA" style="top:0px; left: 450px;">'
                                + '<div class="textoALERTA">'
                                + 'El Status de la obra debe ser PROYECTADA  y el Avance igual a 0'
                                + '</div>'
                                + '<a class="popup-modal-dismiss" href="#"><div class="aceptarBTN" style="left:150px;"> </div></a>'
                                + '</div>'
                            },
                            type: 'inline',
                            preloader: true,
                            modal: true
                        });

                        $j(document).on('click', '.popup-modal-dismiss', function (e) {
                            e.preventDefault();
                            $j.magnificPopup.close();
                        });
                    }


                    if (VEDate !="" && VEDate < VToday){
                        $j('select#id_tipoObra').val('---------');
                                        $j.magnificPopup.open({
                                                items: {
                                                    src:  '<div id="test-modal" class="alertaVENTANA" style="top:0px; left: 450px;">'
                                                          + '<div class="textoALERTA">'
                                                          +  'El Status de la obra debe ser CONCLUIDA  y el Avance igual a 100'
                                                          + '</div>'
                                                          + '<a class="popup-modal-dismiss" href="#"><div class="aceptarBTN" style="left:150px;"> </div></a>'
                                                          + '</div>'
                                                },
                                                type: 'inline',
                                                preloader: true,
                                                modal: true
                                            });

                                            $j(document).on('click', '.popup-modal-dismiss', function (e) {
                                                e.preventDefault();
                                                $j.magnificPopup.close();
                                            });
                    }
                }
                if(statusO == '3'){
                    if (VEDate !="" && VEDate > VToday){
                        $j('select#id_tipoObra').val('---------');
                                        $j.magnificPopup.open({
                                                items: {
                                                    src:  '<div id="test-modal" class="alertaVENTANA" style="top:0px; left: 450px;">'
                                                          + '<div class="textoALERTA">'
                                                          +  'El Status de la obra debe ser en PROCESO  y el Avance mayor a 0'
                                                          + '</div>'
                                                          + '<a class="popup-modal-dismiss" href="#"><div class="aceptarBTN" style="left:150px;"> </div></a>'
                                                          + '</div>'
                                                },
                                                type: 'inline',
                                                preloader: true,
                                                modal: true
                                            });

                                            $j(document).on('click', '.popup-modal-dismiss', function (e) {
                                                e.preventDefault();
                                                $j.magnificPopup.close();
                                            });
                    }
                }
         });

         $j('#id_porcentajeAvance').on('change',function (){
                var avanceO = $j(this).val();
                var statusO = $j('select#id_tipoObra').val();

                if (statusO == "1" && avanceO > 0) {
                    //alert('Si el Status de Obra es PROYECTADA, el porcentaje de Avance debe ser igual a 0. Favor de verificar el Status.');
                    $j.magnificPopup.open({
                        items: {
                            src:  '<div id="test-modal" class="alertaVENTANA" style="top:0px; left: 450px;">'
                                  + '<div class="textoALERTA">'
                                  + 'Si el Status de Obra es PROYECTADA, el porcentaje de Avance debe ser igual a 0. Favor de verificar el Status.'
                                  + '</div>'
                                  + '<a class="popup-modal-dismiss" href="#"><div class="aceptarBTN" style="left:150px;"> </div></a>'
                                  + '</div>'
                        },
                        type: 'inline',
                        preloader: true,
                        modal: true
                    });

                    $j(document).on('click', '.popup-modal-dismiss', function (e) {
                        e.preventDefault();
                        $j.magnificPopup.close();
                    });

                    $j("#id_porcentajeAvance").val('0');
                }
                else if (statusO == "2" && (avanceO == 0 || avanceO == 100))
                {
                    //alert('Si el Status de Obra es en PROCESO, el porcentaje de Avance debe ser mayor a 0 y menor a 100. Favor de verificar el Status.');
                    $j.magnificPopup.open({
                        items: {
                            src:  '<div id="test-modal" class="alertaVENTANA" style="top:0px; left: 450px;">'
                                  + '<div class="textoALERTA">'
                                  + 'Si el Status de Obra es en PROCESO, el porcentaje de Avance debe ser mayor a 0 y menor a 100. Favor de verificar el Status.'
                                  + '</div>'
                                  + '<a class="popup-modal-dismiss" href="#"><div class="aceptarBTN" style="left:150px;"> </div></a>'
                                  + '</div>'
                        },
                        type: 'inline',
                        preloader: true,
                        modal: true
                    });

                    $j(document).on('click', '.popup-modal-dismiss', function (e) {
                        e.preventDefault();
                        $j.magnificPopup.close();
                    });

                    $j("#id_porcentajeAvance").val('0');
                }
                else if (statusO == "3" && avanceO <100)
                {
                    //alert('Si el Status de Obra es CONCLUIDA, el porcentaje de Avance debe ser igual a 100. Favor de verificar el Status.');
                    $j.magnificPopup.open({
                        items: {
                            src:  '<div id="test-modal" class="alertaVENTANA" style="top:0px; left: 450px;">'
                                  + '<div class="textoALERTA">'
                                  + 'Si el Status de Obra es CONCLUIDA, el porcentaje de Avance debe ser igual a 100. Favor de verificar el Status.'
                                  + '</div>'
                                  + '<a class="popup-modal-dismiss" href="#"><div class="aceptarBTN" style="left:150px;"> </div></a>'
                                  + '</div>'
                        },
                        type: 'inline',
                        preloader: true,
                        modal: true
                    });

                    $j(document).on('click', '.popup-modal-dismiss', function (e) {
                        e.preventDefault();
                        $j.magnificPopup.close();
                    });

                    $j("#id_porcentajeAvance").val('100');
                }

         });

    });
