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

	$j('#ver_datos button').on('click', verDatos);
}




function verDatos() {
    var arrayDependencias = $j("#msDependencias").multiselect("getChecked").map(function(){
                                         return this.value;
                                    }).get();

    //alert(arrayDependencias);
    $j.ajax({
        url: '/obras/api/busqueda',
        type: 'get',
        data: {
            access_token: 'FvQONn8eLTV7sadyxv1tqLqmgLNT2Q',
            dependencia:arrayDependencias.toString()
        },
        success: function(data) {
            //$('#datos').html
            tablaI(data);
            tablaD(data);

            var mapOptions = {
                zoom: 5,
                center: new google.maps.LatLng(19.2941124,-99.6312135)
            }
            var map = new google.maps.Map(document.getElementById('map-canvas'),
                                        mapOptions)
            var lugares =  new Array();
            lugares=puntosMapa(data);
            setMarkers(map,lugares);


            google.maps.event.addDomListener(window, 'load', initialize);

        },
        error: function(data) {
            alert('error!!! ' + data.status);
        }
    });
    //$.get('http://127.0.0.1:8000/obras/consultar-

}

function puntosMapa(Datos) {
  var arregloSimple=new Array();
  var arregloDoble=new Array();
    var arregloObjeto = new Object();
    for(var i= 0;i<Datos.obras.length;i++){
        var arregloSimple=new Array();
        arregloSimple.push(Datos.obras[i].estado.nombreEstado);
        arregloSimple.push(Datos.obras[i].estado.latitud);
        arregloSimple.push(Datos.obras[i].estado.longitud);
        arregloSimple.push(i);
        arregloDoble.push(arregloSimple);
    }
    arregloObjeto = arregloDoble;
    return arregloObjeto;
}


function setMarkers(mapa, lugares) {
    alert(lugares);
  for (var i = 0; i < lugares.length; i++) {
    var puntos = lugares[i];
    var myLatLng = new google.maps.LatLng(puntos[1], puntos[2]);
    var marker = new google.maps.Marker({
        position: myLatLng,
        map: mapa,
        title: puntos[0],
        zIndex: puntos[3]
    });
  }
}



function tablaI(Datos){
    var sHtml='<table cellspacing="1" class="tablesorter" id="tablaIzquierda">'
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

    for(var i= 0;i<Datos.obras.length;i++){
        sHtml +='<tr>'
                +'<td>' + i +'</td>'
                +'<td>' + Datos.obras[i].denominacion +'</td>'
                +'<td>' + Datos.obras[i].estado.nombreEstado +'</td>'
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
                +'$(function() {'
                +'    $("#tablaIzquierda").tablesorter({'
                +'    theme: "blue",'
                +'    showProcessing: true,'
                +'    headerTemplate : "{content} {icon}",'
                +'    widgets: [ "uitheme", "zebra", "pager", "scroller" ],'
                +'    widgetOptions : {'
                +'        scroller_height : 300,'
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




    $j('#datos').html(sHtml);
}


// llena la tabla del lado derecho
function tablaD(Datos){
    var tipoReporte = $j('input:radio[name=tipoReporte]:checked').val();

    //alert($j('input:radio[name=tipoReporte]:checked').val());
    var sHtml='<table cellspacing="1" class="tablesorter" id="tablaDerecha">'
                    +'<thead>'
                        +'<tr>'
                            +'<th>Tipo Inversi&oacute;n</th>'
                            +'<th>No. de Obras</th>'
                            +'<th>Monto</th>'
                        +'</tr>'
                    +'</thead>'
                    +'<tfoot>'
                        +'<tr>'
                            +'<th>Tipo Inversi&oacute;n</th>'
                            +'<th>No. de Obras</th>'
                            +'<th>Monto</th>'
                        +'</tr>'

                        +'<tr><td class="pager" id="pagerD" colspan="3">'
                        +'<img src="../../static/assets/tablesorter/addons/pager/icons/first.png" class="first" id="firstD"/>'
                        +'<img src="../../static/assets/tablesorter/addons/pager/icons/prev.png" class="prev" id="prevD"/>'
                        +'<span class="pagedisplay" id="displayPage"></span>'
                        +'<img src="../../static/assets/tablesorter/addons/pager/icons/next.png" class="next" id="nextD"/>'
                        +'<img src="../../static/assets/tablesorter/addons/pager/icons/last.png" class="last" id="lastD"/>'
                        +'<select class="pagesize" id="pagesizeD">'
                        +'<option selected="selected"  value="10">10</option>'
                        +'    <option value="20">20</option>'
                        +'    <option value="30">30</option>'
                        +'    <option  value="40">40</option>'
                        +'</select></td></tr>'

                    +'</tfoot>'
                    +'<tbody>';

    if (tipoReporte=="Dependencia") {
        for (var i = 0; i < Datos.reporte_dependencia.length; i++) {
            sHtml += '<tr>'
            + '<td>' + Datos.reporte_dependencia[i].dependencia.nombreDependencia + '</td>'
            + '<td>' + Datos.reporte_dependencia[i].numero_obras + '</td>'
            + '<td>' + Datos.reporte_dependencia[i].sumatotal + '</td>'
            + '</tr>'
        }
    }

    if (tipoReporte=="Estado") {
        for (var i = 0; i < Datos.reporte_estado.length; i++) {
            sHtml += '<tr>'
            + '<td>' + Datos.reporte_estado[i].estado.nombreEstado + '</td>'
            + '<td>' + Datos.reporte_estado[i].numeroObras + '</td>'
            + '<td>' + Datos.reporte_estado[i].sumatotal + '</td>'
            + '</tr>'
        }
    }

        sHtml +='</tbody>'
                +'</table>'

                +'<fieldset>'
                +'   <div class="row"><div class="col-xs-8">'
                +'       Dependencia'
                +'       </div>'
                +'       <div class="col-xs-4">'
                +'            <input type="radio" name="tipoReporte" value="Dependencia" onclick="verDatos()"/>'
                +'       </div>'
                +'   </div>'
                +'   <div class="row"><div class="col-xs-8">'
                +'       Estado'
                +'       </div>'
                +'       <div class="col-xs-4">'
                +'            <input type="radio" name="tipoReporte" value="Estado" onclick="verDatos()"/>'
                +'       </div>'
                +'   </div>'
                +'   <div class="row"><div class="col-xs-8">'
                +'       RCI'
                +'       </div>'
                +'       <div class="col-xs-4">'
                +'            <input type="radio" name="tipoReporte" value="RCI" onclick="verDatos()"/>'
                +'       </div>'
                +'   </div>'
                +'</fieldset>'



               /*+'<link class="ui-theme" rel="stylesheet" href="../../static/assets/tablesorter/css/jquery-ui.min.css">'
                +'<link class="theme blue" rel="stylesheet" href="../../static/assets/tablesorter/themes/blue/theme.blue.css">'
                +'<script type="text/javascript" src="../../static/assets/tablesorter/jquery.tablesorter.js"></script>'
                +'<script src="../../static/assets/tablesorter/jquery.tablesorter.widgets.js"></script>'
                +'<script type="text/javascript" src="../../static/assets/tablesorter/widget-pager.js"></script>'
                +'<script src="../../static/assets/tablesorter/widget-scroller.js"></script>' */

                +'<script id="js" type="text/javascript">'
                +'$(function() {'
                +'    $("#tablaDerecha").tablesorter({'
                +'    theme: "blue",'
                +'    showProcessing: true,'
                +'    headerTemplate : "{content} {icon}",'
                +'    widgets: [ "uitheme", "zebra", "pager", "scroller" ],'
                +'    widgetOptions : {'
                +'        scroller_height : 200,'
                +'        scroller_upAfterSort: true,'
                +'        scroller_jumpToHeader: true,'
                +'        scroller_barWidth : null,'
                +'          pager_selectors: {'
                +'                container   : "#pagerD",'
                +'                first       : "#firstD",'
                +'                prev        : "#prevD",'
                +'                next        : "#nextD",'
                +'                last        : "#lastD",'
                +'                gotoPage    : "#gotoPageD",'
                +'                pageDisplay : "#displayPage",'
                +'                pageSize    : "#pagesizeD"'
                +'        }'
                +'    }'
                +'});'
                +'});'
                +'</script>';




    $j('#datostablaDerecha').html(sHtml);
}