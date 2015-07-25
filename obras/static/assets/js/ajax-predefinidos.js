/**
 * Created by usuario on 30/04/2015.
 */
/**
 * Created by db2 on 7/04/15.
 */
var $j = jQuery.noConflict();

$j(document).on('ready', main_consulta);

var datosJson
var newToken

var descripcionIniciadas = "Obras proyectadas cuya fecha de inicio ya venció, es decir; obras proyectadas que a la fecha actual ya deberían estar en proceso";
var descripcionVencidas = "Obras en proceso cuya fecha de término ya venció, es decir; obras en proceso que a la fecha actual ya deberían estar concluidas";
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
			}
            if(settings.type == "GET"){
				xhr.setRequestHeader("X-CSRFToken", $j('[name="csrfmiddlewaretoken"]').val());
			}
		}
	});

    valida_token();
    //volverHistorico();
    //$j('#obrasPorAutorizar').on('click', verDatos('obras_por_autorizar'))
    //$j('#obrasIniciadas').on('click', verDatos('obras_iniciadas'))
    //$j('#obrasVencidas').on('click', verDatos('obras_vencidas'))
    //$j('#obrasPorDependencia').on('click', verDatos('obras_por_dependencia'))
    $j('#obrasPorAutorizar').on('click', verDatos)
    $j('#obrasIniciadas').on('click', obrasIniciadas)
    $j('#obrasVencidas').on('click', obrasVencidas)
    $j('#obrasPorDependencia').on('click', obrasPorDependencia)


}


function verDatos() {
    $j('#load3').removeClass("mfp-hide");
    $j('#load3').addClass("mfp-show");
    var ajax_data = {
      "access_token"  : newToken
    };
    $j.ajax({
        url: '/obras/api/obras_por_autorizar',
        type: 'get',
        data: ajax_data,
        success: function(data) {
            $j('#historico').val("SI");
            tablaI(data,'Obras por Autorizar');
            datosJson=data;
            $j('#load3').addClass("mfp-hide");
        },
        error: function(data) {
            $j('#load3').addClass("mfp-hide");
            alert('error!!! ' + data.status);
        }
    });
}


function obrasIniciadas() {
    $j('#load1').removeClass("mfp-hide");
    $j('#load1').addClass("mfp-show");

    var ajax_data = {
      "access_token"  : newToken
    };
    $j.ajax({
        url: '/obras/api/obras_iniciadas',
        type: 'get',
        data: ajax_data,
        success: function(data) {
            $j('#historico').val("SI");
            tablaI(data,'Obras Iniciadas',descripcionIniciadas);
            datosJson=data;
            $j('#load1').addClass("mfp-hide");
        },
        error: function(data) {
            $j('#load1').addClass("mfp-hide");
            alert('error!!! ' + data.status);
        }
    });

}

function obrasVencidas() {
    $j('#load2').removeClass("mfp-hide");
    $j('#load2').addClass("mfp-show");
    var ajax_data = {
      "access_token"  : newToken
    };
    //alert(descripcionVencidas);
    $j.ajax({
        url: '/obras/api/obras_vencidas',
        type: 'get',
        data: ajax_data,
        success: function(data) {
            $j('#historico').val("SI");

            tablaI(data,'Obras Vencidas',descripcionVencidas);
            datosJson=data;
            $j('#load2').addClass("mfp-hide");
        },
        error: function(data) {
            alert('error!!! ' + data.status);
            $j('#load2').addClass("mfp-hide");
        }
    });

}

function obrasPorDependencia() {
    $j('#load3').removeClass("mfp-hide");
    $j('#load3').addClass("mfp-show");
    var ajax_data = {
      "access_token"  : newToken
    };
    $j.ajax({
        url: '/obras/api/obras_por_dependencia',
        type: 'get',
        data: ajax_data,
        success: function(data) {
            $j('#historico').val("SI");
            tablaI(data,'Obras por Dependencia','');
            datosJson=data;
            $j('#load3').addClass("mfp-hide");
        },
        error: function(data) {
            $j('#load3').addClass("mfp-hide");
            alert('error!!! ' + data.status);

        }
    });

}

function tablaI(Datos,titulo,descripcion){
    var sHtmlExporta="";
    var sHtmlShorter="";
    var sHtmlistado="";


    var sHtml = '<table id="tablaIzquierda" class="table table-striped">'
                +' <colgroup>'
                +' <col width="30%">'
                +' <col width="40%">'
                +' <col width="30%">'
                +' </colgroup> '
                +'<thead>'
                        +'<tr>'
                            +'<th>Id</th>'
                            +'<th>Denominaci&oacute;n</th>'
                            +'<th>Estado</th>'
                        +'</tr>'
                +'</thead>'
                +'<tfoot>'
                        +'<tr>'
                            +'<th>Id</th>'
                            +'<th>Denominaci&oacute;n</th>'
                            +'<th>Estado</th>'
                        +'</tr>'

                        +'<tr><td class="pager" id="pagerI" colspan="3">'
                        +'<img src="../../static/assets/tablesorter/addons/pager/icons/first.png" class="first" id="firstI"/>'
                        +'<img src="../../static/assets/tablesorter/addons/pager/icons/prev.png" class="prev" id="prevI"/>'
                        +'<span class="pagedisplay" id="pagedisplayI"></span>'
                        +'<img src="../../static/assets/tablesorter/addons/pager/icons/next.png" class="next" id="nextI"/>'
                        +'<img src="../../static/assets/tablesorter/addons/pager/icons/last.png" class="last" id="lastI"/>'
                        +'<select class="pagesize" id="pagesizeI">'
                        +'<option selected="selected"  value="10">10</option>'
                        +'    <option value="20">20</option>'
                        +'    <option value="30">30</option>'
                        +'    <option  value="40">40</option>'
                        +'</select></td></tr>'

                    +'</tfoot>'
                    +'<tbody>';
    for(var i= 0;i<Datos.length;i++){
        sHtml +='<tr>'
                +'<td><a href="/admin/obras/obra/' + Datos[i].id + '/?m=1">' + Datos[i].identificador_unico +'</a></td>'
                +'<td>' + Datos[i].denominacion +'</td>'
                +'<td>' + Datos[i].estado__nombreEstado +'</td>'
                +'</tr>'
    }

        sHtml +='</tbody>'
                +'</table>'
                +'<script id="js" type="text/javascript">'
                +'$ts(function() {'
                +'    $ts("#tablaIzquierda").tablesorter({'
                +'    theme: "blue",'
                +'    showProcessing: true,'
                +'    headerTemplate : "{content} {icon}",'
                +'    widgets: [ "uitheme", "zebra", "pager", "scroller" ],'
                +'    widgetOptions : {'
                +'        scroller_height : 190,'
                +'        scroller_upAfterSort: true,'
                +'        scroller_jumpToHeader: true,'
                +'        scroller_barWidth : null,'
                +'          pager_selectors: {'
                +'                container   : "#pagerI",'
                +'                first       : "#firstI",'
                +'                prev        : "#prevI",'
                +'                next        : "#nextI",'
                +'                last        : "#lastI",'
                +'                gotoPage    : "#gotoPageI",'
                +'                pageDisplay : "#pagedisplayI",'
                +'                pageSize    : "#pagesizeI"'
                +'        }'
                +'    }'
                +'});'
                +'});'
                +'</script>'
                +'</tbody>'
                +'</table>';
    $j('#titulo').html(titulo);
    $j('#descripcion').html(descripcion);
    $j('#tabla').html(sHtml);


}

function volverHistorico() {
    //var variable = (opener) ? opener.location.href : 'No disponible' ;
    //document.write(variable);
    var sHistorico = $j('#historico').val();
    if (sHistorico.toString() =="SI") {
        $.get("/obras/register-by-token", function (respu) {
           newToken = respu.access_token;
           verDatos()
        });
    }
}