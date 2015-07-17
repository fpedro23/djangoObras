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

    $j('#obrasPorAutorizar').on('click', verDatos)


}


function verDatos() {

    var ajax_data = {
      "access_token"  : newToken
    };

    $j("#ajaxProgress").show();
    $j.ajax({
        url: '/obras/api/obras_por_autorizar',
        type: 'get',
        data: ajax_data,
        success: function(data) {
            tablaI(data);
            datosJson=data;
        },
        error: function(data) {
            alert('error!!! ' + data.status);
        }
    });
}

function tablaI(Datos){
    var sHtmlExporta="";
    var sHtmlShorter="";
    var sHtmlistado="";

    sHtmlExporta= '<table id="tablaExporta2" class="table table-striped">'
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
                +'<tbody>';
    sHtmlShorter ='<table cellspacing="1" class="tablesorter" id="tablaIzquierda">';
    sHtmlistado ='<table cellspacing="1" id="tablaListado">';
    var sHtml='<thead>'
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
    sHtmlistado = sHtml;
    for(var i= 0;i<Datos.obras.length;i++){
        sHtml +='<tr>'
                +'<td><a href="/admin/obras/obra/' + Datos.obras[i].id + '/?m=1">' + Datos.obras[i].identificador_unico +'</a></td>'
                +'<td>' + Datos.obras[i].denominacion +'</td>'
                +'<td>' + Datos.obras[i].estado__nombreEstado +'</td>'
                +'</tr>'

        sHtmlistado +='<tr>'
                +'<td>' + Datos.obras[i].identificador_unico +'</td>'
                +'<td>' + Datos.obras[i].denominacion +'</td>'
                +'<td>' + Datos.obras[i].estado__nombreEstado +'</td>'
                +'</tr>'
        sHtmlExporta += '<tr>'
                +'<td>' + Datos.obras[i].identificador_unico +'</td>'
                +'<td>' + Datos.obras[i].denominacion +'</td>'
                +'<td>' + Datos.obras[i].estado__nombreEstado +'</td>'
                +'</tr>'
    }

        sHtml +='</tbody>'
                +'</table>'

               /*+'<link class="ui-theme" rel="stylesheet" href="../../static/assets/tablesorter/css/jquery-ui.min.css">'
                +'<link class="theme blue" rel="stylesheet" href="../../static/assets/tablesorter/themes/blue/theme.blue.css">'
                +'<script type="text/javascript" src="../../static/assets/tablesorter/jquery.tablesorter.js"></script>'
                +'<script src="../../static/assets/tablesorter/jquery.tablesorter.widgets.js"></script>'
                +'<script type="text/javascript" src="../../static/assets/tablesorter/widget-pager.js"></script>'
                +'<script src="../../static/assets/tablesorter/widget-scroller.js"></script>' */

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
                +'</script>';

    sHtmlExporta +='</tbody>'
                +'</table>';
     $j('#tabla-exporta2').hide();
    $j('#datos').html(sHtmlShorter + sHtml);
    $j('#tabla-exporta2').html(sHtmlExporta);

}

