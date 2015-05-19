/**
 * Created by usuario on 30/04/2015.
 */
/**
 * Created by db2 on 7/04/15.
 */
var $j = jQuery.noConflict();
$j(document).on('ready', main_consulta);

var datosJson;

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
    $j('#ver_tabla_estado #estado').on('click', mostrarTablas);
    $j('#ver_tabla_dependencia #dependencia').on('click', mostrarTablas)
    $j('#ver_grafica button').on('click', graficas)
    $j('#ver_grafica_estado #estado').on('click', graficas);
    $j('#ver_grafica_dependencia #dependencia').on('click', graficas);
}




function verDatos() {
    var arrayTipoInversion = $j("#msTipoInversion").multiselect("getChecked").map(function(){return this.value;}).get();
    var arrayEstatusObra = $j("#msEstatusObra").multiselect("getChecked").map(function(){return this.value;}).get();
    var arrayDependencias = $j("#msDependencias").multiselect("getChecked").map(function(){return this.value;}).get();
    var arrayEstados = $j("#msEstados").multiselect("getChecked").map(function(){return this.value;}).get();
    var arrayClasificacion = $j("#msClasificacion").multiselect("getChecked").map(function(){return this.value;}).get();
    var arrayImpacto = $j("#msImpacto").multiselect("getChecked").map(function(){return this.value;}).get();
    var arrayInaugurador = $j("#msInaugurador").multiselect("getChecked").map(function(){return this.value;}).get();
    var fechaInicio1 = $j("#fechaInicial1").val();
    var fechaInicio2 = $j("#fechaInicial2").val();
    var fechaFin1 = $j("#fechaFinal1").val();
    var fechaFin2 = $j("#fechaFinal2").val();
    var inversionInicial = $j("#inversionInicial").val();
    var inversionFinal = $j("#inversionFinal").val();


    var ajax_data = {
      "access_token"  : 'egE2YWdVkqGyB3yOf7TFZbiyCKlzHb'
    };

    if(arrayDependencias.toString()!=""){ajax_data.dependencia=arrayDependencias.toString();}
    if(arrayEstatusObra.toString()!=""){ajax_data.tipoDeObra=arrayEstatusObra.toString();}
    if(arrayEstados.toString()!=""){ajax_data.estado=arrayEstados.toString();}
    if(arrayClasificacion.toString()!=""){ajax_data.clasificacion=arrayClasificacion.toString();}
    if(arrayTipoInversion.toString()!=""){ajax_data.tipoDeInversion=arrayTipoInversion.toString();}
    if(arrayInaugurador.toString()!=""){ajax_data.inaugurador=arrayInaugurador.toString();}
    if(arrayImpacto.toString()!=""){ajax_data.impacto=arrayImpacto.toString();}
    if(fechaInicio1!=""){ajax_data.fechaInicio=$j.date(fechaInicio1);}
    if(fechaInicio2!=""){ajax_data.fechaInicioSegunda=$j.date(fechaInicio2);}
    if(fechaFin1!=""){ajax_data.fechaFin=$j.date(fechaFin1);}
    if(fechaFin2!=""){ajax_data.fechaFinSegunda=$j.date(fechaFin2);}
    if(inversionInicial!=""){ajax_data.inversionMinima=inversionInicial;}
    if(inversionFinal!=""){ajax_data.inversionMaxima=inversionFinal;}
    if($j('#inauguradas').is(':checked')){ajax_data.inaugurada = $j('#inauguradas').is(':checked');}

    $j("#ajaxProgress").show();
    $j.ajax({
        url: '/obras/api/busqueda',
        type: 'get',
        data: ajax_data,
        success: function(data) {
            //$j('#datos').html
            tablaI(data);
            tablaD(data);
            datosJson=data;
            // MAPA
            var mapOptions = {
                zoom: 4,
                center: new google.maps.LatLng(22.6526121, -100.1780452),
                mapTypeId: google.maps.MapTypeId.SATELLITE
            }
            var map = new google.maps.Map(document.getElementById('map-canvas'),
                                        mapOptions)
            var lugares =  new Array();
            lugares=puntosMapa(data);
            setMarkers(map,lugares);
            google.maps.event.addDomListener(window, 'load', initialize);
            // mapa
            // graficas

            $j("#ajaxProgress").hide();
        },
        error: function(data) {
            alert('error!!! ' + data.status);
            $j("#ajaxProgress").hide();
        }
    });
}



function mostrarTablas() {

            tablaD(datosJson);
}

function graficas(){

    columnaGrafica();
    $j.tablaGrafica(datosJson);
}

function columnaGrafica(){
    var tipoReporte = $j('input:radio[name=graficaTipo]:checked').val();
    var categorias = new Array();
    var datas = new Array();
    var montos = new Array();
    if (tipoReporte=="Dependencia") {
        for (var i = 0; i < datosJson.reporte_dependencia.length; i++) {
            categorias.push(datosJson.reporte_dependencia[i].dependencia.nombreDependencia);
            datas.push(datosJson.reporte_dependencia[i].numero_obras);
            montos.push(datosJson.reporte_dependencia[i].sumatotal);
        }
    }else{
        for (var i = 0; i < datosJson.reporte_estado.length; i++) {
            categorias.push(datosJson.reporte_estado[i].estado.nombreEstado);
            datas.push(datosJson.reporte_estado[i].numeroObras);
            montos.push(datosJson.reporte_estado[i].sumatotal);
        }
    }

    $pp('#containerGrafica').highcharts({
        chart: {
            type: 'column',
            margin: 110,
            marginLeft: 50,
            marginRight: 50,
            marginTop: 50,
            options3d: {
                enabled: true,
                alpha: 10,
                beta: 25,
                depth: 70
            }
        },
        credits: {
            enabled: false
        },
        title: {
            text: 'Número de obras por Dependencia'
        },

        subtitle: {
            text: ''
        },
        plotOptions: {
            column: {
                depth: 25
            },
            series: {
                pointWidth: 30
            }
        },
        xAxis: {
            categories: categorias
        },
        yAxis: {
            title: {
                text: null
            }
        },
        series: [{
            name: 'Número de obras',
            data: datas
        },{
            name: 'Monto Total',
            data: montos}]
    });
}


$j.date = function(dateObject) {
    var d = new Date(dateObject);
    var day = d.getDate();
    var month = d.getMonth() + 1;
    var year = d.getFullYear();
    if (day < 10) {
        day = "0" + day;
    }
    if (month < 10) {
        month = "0" + month;
    }
    var date = year + "-" + month + "-" + day;

    return date;
};

function puntosMapa(Datos) {
  var arregloSimple=new Array();
  var arregloDoble=new Array();
    var arregloObjeto = new Object();
    for(var i= 0;i<Datos.obras.length;i++){
        var arregloSimple=new Array();
        arregloSimple.push(Datos.obras[i].estado.nombreEstado + ", " + Datos.obras[i].dependencia.nombreDependencia);
        arregloSimple.push(Datos.obras[i].estado.latitud);
        arregloSimple.push(Datos.obras[i].estado.longitud);
        arregloSimple.push(i);
        arregloDoble.push(arregloSimple);
    }
    arregloObjeto = arregloDoble;
    return arregloObjeto;
}


function setMarkers(mapa, lugares) {
  var infowindow = new google.maps.InfoWindow();
  for (var i = 0; i < lugares.length; i++) {
    var puntos = lugares[i];
    var myLatLng = new google.maps.LatLng(puntos[1], puntos[2]);
    var marker = new google.maps.Marker({
        position: myLatLng,
        map: mapa,
        title: puntos[0],
        zIndex: puntos[3]
    });

      google.maps.event.addListener(marker, 'click', (function(marker, puntos) {
        return function() {
          infowindow.setContent(puntos[0]);
          infowindow.open(mapa, marker);
        }
      })(marker, puntos));
  }
}



function tablaI(Datos){
    var sHtml='<h4>RESULTADOS</h4><table cellspacing="1" class="tablesorter" id="tablaIzquierda">'
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
                +'<td>' + Datos.obras[i].identificador +'</td>'
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
                +'        scroller_height : 250,'
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
    var dependenciasChecked="";
    var estadosChecked="";

    //alert($j('input:radio[name=tipoReporte]:checked').val());
    var sHtml='<h4>REPORTES</h4><table cellspacing="1" class="tablesorter" id="tablaDerecha">'
                    +'<thead>'
                        +'<tr>'
                            +'<th>Tipo Inversi&oacute;n</th>'
                            +'<th>No. de Obras</th>'
                            +'<th>Monto</th>'
                        +'</tr>'
                    +'</thead>'
                    +'<tfoot>'
                        +'<tr>'
                            +'<th>TOTALES</th>'
                            +'<th>'+ Datos.reporte_general[0].obras_totales +'</th>'
                            +'<th>'+ Datos.reporte_general[0].total_invertido +'</th>'
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
        dependenciasChecked="checked";
        for (var i = 0; i < Datos.reporte_dependencia.length; i++) {
            sHtml += '<tr>'
            + '<td>' + Datos.reporte_dependencia[i].dependencia.nombreDependencia + '</td>'
            + '<td>' + Datos.reporte_dependencia[i].numero_obras + '</td>'
            + '<td>' + Datos.reporte_dependencia[i].sumatotal + '</td>'
            + '</tr>'
        }
    }

    if (tipoReporte=="Estado") {
        estadosChecked="checked";
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

                //+'<fieldset>'
                //+'   <div class="row"><div class="col-xs-8">'
                //+'       Dependencia'
                //+'       </div>'
                //+'       <div class="col-xs-4">'
                //+'            <input type="radio" name="tipoReporte" value="Dependencia" ' + dependenciasChecked +'/>'   //onclick="verDatos()"
                //+'       </div>'
                //+'   </div>'
                //+'   <div class="row"><div class="col-xs-8">'
                //+'       Estado'
                //+'       </div>'
                //+'       <div class="col-xs-4">'
                //+'            <article id="ver_tablas">'
                //+'            <input type="radio" name="tipoReporte" value="Estado" ' + estadosChecked +'/>'
                //+'       </article>'
                //+'            <input type="radio" name="tipoReporte" value="Estado" ' + estadosChecked +'/>'
                //+'       </div>'
                //+'   </div>'
                //+'   <div class="row"><div class="col-xs-8">'
                //+'       RCI'
                //+'       </div>'
                //+'       <div class="col-xs-4">'
                //+'            <input type="radio" name="tipoReporte" value="RCI" "/>'
               // +'       </div>'
               // +'   </div>'
               // +'</fieldset>'



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
                +'        scroller_height : 150,'
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
    $j('#tablaGrafica').html(sHtml);
}

// llena la tabla del lado derecho

$j.tablaGrafica = function(Datos){
    var tipoReporte = $j('input:radio[name=graficaTipo]:checked').val();
    var dependenciasChecked="";
    var estadosChecked="";


    //alert($j('input:radio[name=tipoReporte]:checked').val());
    var sHtml= '<h4>REPORTES</h4> <table cellspacing="1"  class="tablesorter" id="tablaGrafica">'
                    +'<thead>'
                        +'<tr>'
                            +'<th>Tipo Inversi&oacute;n</th>'
                            +'<th>No. de Obras</th>'
                            +'<th>Monto</th>'
                        +'</tr>'
                    +'</thead>'
                    +'<tfoot>'
                        +'<tr>'
                            +'<th>TOTALES</th>'
                            +'<th>'+ Datos.reporte_general[0].obras_totales +'</th>'
                            +'<th>'+ Datos.reporte_general[0].total_invertido +'</th>'
                        +'</tr>'

                        +'<tr><td class="pager" id="pagerG" colspan="3">'
                        +'<img src="../../static/assets/tablesorter/addons/pager/icons/first.png" class="first" id="firstG"/>'
                        +'<img src="../../static/assets/tablesorter/addons/pager/icons/prev.png" class="prev" id="prevG"/>'
                        +'<span class="pagedisplay" id="displayPageG"></span>'
                        +'<img src="../../static/assets/tablesorter/addons/pager/icons/next.png" class="next" id="nextG"/>'
                        +'<img src="../../static/assets/tablesorter/addons/pager/icons/last.png" class="last" id="lastG"/>'
                        +'<select class="pagesize" id="pagesizeG">'
                        +'<option selected="selected"  value="10">10</option>'
                        +'    <option value="20">20</option>'
                        +'    <option value="30">30</option>'
                        +'    <option  value="40">40</option>'
                        +'</select></td></tr>'

                    +'</tfoot>'
                    +'<tbody>';

    if (tipoReporte=="Dependencia") {
        dependenciasChecked="checked";
        for (var i = 0; i < Datos.reporte_dependencia.length; i++) {
            sHtml += '<tr>'
            + '<td>' + Datos.reporte_dependencia[i].dependencia.nombreDependencia + '</td>'
            + '<td>' + Datos.reporte_dependencia[i].numero_obras + '</td>'
            + '<td>' + Datos.reporte_dependencia[i].sumatotal + '</td>'
            + '</tr>'
        }
    }

    if (tipoReporte=="Estado") {
        estadosChecked="checked";
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
                +'<script src="http://mottie.github.io/tablesorter/docs/js/jquery-latest.min.js"></script>'
                +'<link class="ui-theme" rel="stylesheet" href="../../static/assets/tablesorter/css/jquery-ui.min.css">'
                +'<link class="theme blue" rel="stylesheet" href="../../static/assets/tablesorter/themes/blue/theme.blue.css">'
                +'<script type="text/javascript" src="../../static/assets/tablesorter/jquery.tablesorter.js"></script>'
                +'<script src="../../static/assets/tablesorter/jquery.tablesorter.widgets.js"></script>'
                +'<script type="text/javascript" src="../../static/assets/tablesorter/widget-pager.js"></script>'
                +'<script src="../../static/assets/tablesorter/widget-scroller.js"></script>'
                +'<script id="js" type="text/javascript">'
                +'$(function() {'
                +'    $("#tablaGrafica").tablesorter({'
                +'    theme: "blue",'
                +'    showProcessing: true,'
                +'    headerTemplate : "{content} {icon}",'
                +'    widgets: [ "uitheme", "zebra", "pager"],'
                +'    widgetOptions : {'
                //+'        scroller_height : 150,'
                //+'        scroller_upAfterSort: true,'
                //+'        scroller_jumpToHeader: true,'
                //+'        scroller_barWidth : null,'
                +'          pager_selectors: {'
                +'                container   : "#pagerG",'
                +'                first       : "#firstG",'
                +'                prev        : "#prevG",'
                +'                next        : "#nextG",'
                +'                last        : "#lastG",'
                +'                gotoPage    : "#gotoPageG",'
                +'                pageDisplay : "#displayPageG",'
                +'                pageSize    : "#pagesizeG"'
                +'        }'
                +'    }'
                +'});'
                +'});'
                +'</script>';

        $j('#divTablaGrafica').html($j(sHtml));

}