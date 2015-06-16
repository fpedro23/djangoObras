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

	$j('#ver_datos #button').on('click', verDatos);
    $j('#ver_tabla_estado #estado').on('click', mostrarTablas);
    $j('#ver_tabla_dependencia #dependencia').on('click', mostrarTablas)
    $j('#ver_grafica #grafica').on('click', graficas)
    $j('#ver_grafica_estado #estado').on('click', graficas);
    $j('#ver_grafica_dependencia #dependencia').on('click', graficas);
    $j('#ver_grafica_tipos #tipoGrafica').on('change', graficas);
    $j('#ver_grafica_datos #datosGrafica').on('change', graficas);
    $j('#go_Graficas #goGraficas').on('click', enviaFiltrosGrafica);
    $j('#art_limpiar #limpiar').on('click', limpia);

    $j('#regresaGraficas #regresarBTN').on('click', regresa);


}

function limpia(){
   $j("#forma").reset();
}

jQuery.fn.reset = function () {
  $j(this).each (function() { this.reset(); });
}

function enviaFiltrosGrafica() {
    var arrayTipoInversion = $l("#msTipoInversion").multiselect("getChecked").map(function(){return this.value;}).get();
    var arrayEstatusObra = $l("#msEstatusObra").multiselect("getChecked").map(function(){return this.value;}).get();
    var arrayDependencias = $l("#msDependencias").multiselect("getChecked").map(function(){return this.value;}).get();
    var arrayEstados = $l("#msEstados").multiselect("getChecked").map(function(){return this.value;}).get();
    var arrayClasificacion = $l("#msClasificacion").multiselect("getChecked").map(function(){return this.value;}).get();
    var arrayImpacto = $l("#msImpacto").multiselect("getChecked").map(function(){return this.value;}).get();
    var arrayInaugurador = $l("#msInaugurador").multiselect("getChecked").map(function(){return this.value;}).get();
    var fechaInicio1 = $l("#fechaInicial1").val();
    var fechaInicio2 = $l("#fechaInicial2").val();
    var fechaFin1 = $l("#fechaFinal1").val();
    var fechaFin2 = $l("#fechaFinal2").val();
    var inversionInicial = $l("#inversionInicial").val();
    var inversionFinal = $l("#inversionFinal").val();


    var ajax_data = {
      "access_token"  : $j('[name="csrfmiddlewaretoken"]').val()  //'3JrrYpjjShuhPp81AsvTPW1VVJS3RG'
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


    $j.ajax({
        url: '/obras/graficas',
        type: 'get',
        data: ajax_data,
        success: function(data) {
            alert(data);
            $j('#pagina').html(data);

        },
        error: function(data) {
            alert('error!!! ' + data.status);
        }
    });
}


function verDatos() {
    var arrayTipoInversion = $l("#msTipoInversion").multiselect("getChecked").map(function(){return this.value;}).get();
    var arrayEstatusObra = $l("#msEstatusObra").multiselect("getChecked").map(function(){return this.value;}).get();
    var arrayInstanciaEjecutora = $l("#msInstanciaEjecutora").multiselect("getChecked").map(function(){return this.value;}).get();
    var arrayDependencias = $l("#msDependencias").multiselect("getChecked").map(function(){return this.value;}).get();
    var arrayEstados = $l("#msEstados").multiselect("getChecked").map(function(){return this.value;}).get();
    var arrayClasificacion = $l("#msClasificacion").multiselect("getChecked").map(function(){return this.value;}).get();
    var arrayImpacto = $l("#msImpacto").multiselect("getChecked").map(function(){return this.value;}).get();
    var arrayInaugurador = $l("#msInaugurador").multiselect("getChecked").map(function(){return this.value;}).get();
    var fechaInicio1 = $l("#fechaInicial1").val();
    var fechaInicio2 = $l("#fechaInicial2").val();
    var fechaFin1 = $l("#fechaFinal1").val();
    var fechaFin2 = $l("#fechaFinal2").val();
    var inversionInicial = $l("#inversionInicial").val();
    var inversionFinal = $l("#inversionFinal").val();


    var ajax_data = {
      "access_token"  : newToken
    };

    if(arrayDependencias.toString()!=""){ajax_data.dependencia=arrayDependencias.toString();}
    if(arrayEstatusObra.toString()!=""){ajax_data.tipoDeObra=arrayEstatusObra.toString();}
    if(arrayInstanciaEjecutora.toString()!=""){ajax_data.instanciaEjecutora=arrayInstanciaEjecutora.toString();}
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

function regresa(){
    $pp('#pagina').show();
    $pp('#div-grafica').removeClass("mfp-show");
    $pp('#div-grafica').addClass("mfp-hide");
}


function mostrarTablas() {

            tablaD(datosJson);
}

function graficas(){
    var tipoReporte = $j('input:radio[name=graficaTipo]:checked').val();
    var tipoGrafica = $j("#tipoGrafica").val();
    var datosGrafica = $j("#datosGrafica").val();
    var titulo="";
    var categorias = new Array();
    var datas = new Array();
    var montos = new Array();

    $pp('#pagina').hide();
    $pp('#div-grafica').addClass("mfp-show");

    if (tipoReporte=="Dependencia") {
        for (var i = 0; i < datosJson.reporte_dependencia.length; i++) {
            categorias.push(datosJson.reporte_dependencia[i].dependencia.nombreDependencia);
            datas.push(datosJson.reporte_dependencia[i].numero_obras);
            montos.push(datosJson.reporte_dependencia[i].sumatotal);
            titulo="Número de obras por Dependencia";
        }
    }else{
        for (var i = 0; i < datosJson.reporte_estado.length; i++) {
            categorias.push(datosJson.reporte_estado[i].estado.nombreEstado);
            datas.push(datosJson.reporte_estado[i].numeroObras);
            montos.push(datosJson.reporte_estado[i].sumatotal);
            titulo="Número de obras por Estado";
        }
    }

    Highcharts.setOptions({
        lang: {
                downloadJPEG: "Descargar imágen JPEG",
                downloadPDF: "Descargar documento PDF",
                downloadPNG: "Descargar imágen PNG",
                downloadSVG: "Descargar vector de imágen SVG",
                loading: "Cargando...",
                printChart: "Imprimir Gráfica",
                resetZoom: "Quitar zoom",
                resetZoomTitle: "Quitar el nivel de zoom ",
                numericSymbols: [' mil', ' millones']
            }
    });


    switch (tipoGrafica) {
        case "Columna3D":
            if(datosGrafica=="Numero"){
                columnaGrafica(categorias,datas,titulo,"Número de obras");
            }else{
                columnaGrafica(categorias,montos,titulo,"Monto Total");
            }
            break;
        case "Columna2D":
            if(datosGrafica=="Numero"){
                columna2DGrafica(categorias,datas,titulo,"Número de obras");
            }else{
                columna2DGrafica(categorias,montos,titulo,"Monto Total");
            }

            break;
        case "Pastel":
            if(datosGrafica=="Numero") {
                pieGrafica(arregloDataGrafica(datosJson, tipoReporte,datosGrafica), titulo, 0,"Número de obras");
            }else{
                pieGrafica(arregloDataGrafica(datosJson, tipoReporte,datosGrafica), titulo, 0,"Monto Total");
            }
            break;
        case "Dona":
            if(datosGrafica=="Numero") {
                pieGrafica(arregloDataGrafica(datosJson, tipoReporte,datosGrafica), titulo, 100,"Número de obras");
            }else{
                pieGrafica(arregloDataGrafica(datosJson, tipoReporte,datosGrafica), titulo, 100,"Monto Total");
            }
            break;
        case "Barra":
            if(datosGrafica=="Numero"){
                barraGrafica(categorias,datas,titulo,"Número de obras","Mil"," Mil");
            }else{
                barraGrafica(categorias,montos,titulo,"Monto Total","Millones"," MDP");
            }
            break;
        case "Lineal":

            break;
    }


    $j.tablaGrafica(datosJson);
}


function arregloDataGrafica(Datos,tipoReporte,datosGrafica) {
    var arregloSimple=new Array();
    var arregloDoble=new Array();
    var arregloObjeto = new Object();

    if (tipoReporte=="Dependencia") {
        for(var i= 0;i<Datos.reporte_dependencia.length;i++){
            var arregloSimple=new Array();
            arregloSimple.push(Datos.reporte_dependencia[i].dependencia.nombreDependencia);
            if(datosGrafica=="Numero") {
                arregloSimple.push(Datos.reporte_dependencia[i].numero_obras);
            }else{
                arregloSimple.push(Datos.reporte_dependencia[i].sumatotal);
            }
            arregloDoble.push(arregloSimple);
        }
    }else{
        for (var i = 0; i < datosJson.reporte_estado.length; i++) {
            var arregloSimple=new Array();
            arregloSimple.push(Datos.reporte_estado[i].estado.nombreEstado);
            if(datosGrafica=="Numero") {
                arregloSimple.push(Datos.reporte_estado[i].numeroObras);
            }else{
                arregloSimple.push(Datos.reporte_estado[i].sumatotal);
            }
            arregloDoble.push(arregloSimple);
        }
    }
    arregloObjeto = arregloDoble;
    return arregloObjeto;
}

function columnaGrafica(categorias,datas,titulo,nombreData){


    $pp('#containerGrafica').highcharts({
        chart: {
            renderTo: 'container',
            type: 'column',
            margin: 120,
            marginLeft: 50,
            marginRight: 50,
            marginTop: 50,
            zoomType: 'x',
            panning: true,
            panKey: 'shift',
            options3d: {
                enabled: true,
                alpha: 10,
                beta: 10,
                depth: 70
            }
        },
        credits: {
            enabled: false
        },
        title: {
            text: titulo
        },

        subtitle: {
            text: ''
        },
        plotOptions: {
            column: {
                depth: 25
            },
            series: {
                pointWidth: 15
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
            name: nombreData,
            data: datas
        }]
    });
}


function pieGrafica(datas,titulo,dona,nombreData) {

    $pp('#containerGrafica').highcharts({
        chart: {
            type: 'pie',
            zoomType: 'x',
            panning: true,
            panKey: 'shift',
            options3d: {
                enabled: true,
                alpha: 45,
                beta: 0
            }
        },
        title: {
            text: titulo
        },
        credits: {
            enabled: false
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {
            pie: {
                innerSize: dona,
                allowPointSelect: true,
                cursor: 'pointer',
                depth: 35,
                dataLabels: {
                    enabled: true,
                    format: '{point.name}'
                }
            }
        },
        series: [{
            type: 'pie',
            name: nombreData,
            data: datas
        }]
    });
}

function barraGrafica(categorias,datas,titulo,nombreData,unidades,sufijo){
    Highcharts.setOptions({
        lang: {
                numericSymbols: [unidades]
            }
    });
    $pp('#containerGrafica').highcharts({
        chart: {
            type: 'bar',
            zoomType: 'x',
            panning: true,
            panKey: 'shift'
        },
        title: {
            text: titulo
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            categories: categorias,
            title: {
                text: null
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: '',
                align: 'high'
            },
            labels: {
                overflow: 'justify'
            }
        },
        tooltip: {
            valueSuffix: sufijo
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true
                }
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: -40,
            y: 100,
            floating: true,
            borderWidth: 1,
            backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
            shadow: true
        },
        credits: {
            enabled: false
        },
        series: [{
            name: nombreData,
            data: datas
        }]
    });
}

function columna2DGrafica(categorias,datas,titulo,nombreData){
    $pp('#containerGrafica').highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: titulo
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            categories: categorias,
            crosshair: true
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Rainfall (mm)'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f} mm</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: nombreData,
            data: datas

        }]
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
    for(var i= 0;i<Datos.reporte_estado.length;i++){
        var arregloSimple=new Array();
        arregloSimple.push(Datos.reporte_estado[i].estado.nombreEstado + ", número de obras: " + Datos.reporte_estado[i].numeroObras);
        arregloSimple.push(Datos.reporte_estado[i].estado.latitud);
        arregloSimple.push(Datos.reporte_estado[i].estado.longitud);
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
    var sHtmlExporta="";
    var sHtmlShorter="";
    var sHtmlistado="";

    sHtmlExporta= '<div class="row titulo">'
                    + '<div class="col-md-6">'
                    +     'Resultados'
                   + ' </div>'
               + '</div>'
                +'<table cellspacing="1" id="tablaExporta2">';
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
                +'<td>' + Datos.obras[i].identificador +'</td>'
                +'<td>' + Datos.obras[i].denominacion +'</td>'
                +'<td>' + Datos.obras[i].estado.nombreEstado +'</td>'
                +'</tr>'

        sHtmlistado +='<tr>'
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


     $j('#tabla-exporta2').hide();
    $j('#datos').html(sHtmlShorter + sHtml);
    $j('#tabla-exporta2').html(sHtmlExporta + sHtml);

}


// llena la tabla del lado derecho
function tablaD(Datos){
    var tipoReporte = $j('input:radio[name=tipoReporte]:checked').val();
    var dependenciasChecked="";
    var estadosChecked="";
    var sHtmlExporta="";
    var sHtmlShorter="";

    sHtmlExporta= '<div class="row titulo">'
                    + '<div class="col-md-6">'
                    +     'Reporte'
                   + ' </div>'
               + '</div>'
                +'<table cellspacing="1" id="tablaExporta">';
    sHtmlShorter ='<table cellspacing="1" class="tablesorter" id="tablaDerecha">';
    //alert($j('input:radio[name=tipoReporte]:checked').val());

    var sHtml='<thead>'
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
                        //+'<div class="first principioFLECHA" id="firstD" style="height:11px"></div>'
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
                +'$ts(function() {'
                +'    $ts("#tablaDerecha").tablesorter({'
                +'    theme: "blue",'
                +'    showProcessing: true,'
                +'    headerTemplate : "{content} {icon}",'
                +'    widgets: [ "uitheme", "zebra", "pager", "scroller" ],'
                +'    widgetOptions : {'
                +'        scroller_height : 140,'
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

    $j('#tabla-exporta').hide();
    $j('#datostablaDerecha').html(sHtmlShorter + sHtml);
    $j('#tabla-exporta').html(sHtmlExporta + sHtml);

}

// llena la tabla del lado derecho

$j.tablaGrafica = function(Datos){
    var tipoReporte = $j('input:radio[name=graficaTipo]:checked').val();
    var dependenciasChecked="";
    var estadosChecked="";


    //alert($j('input:radio[name=tipoReporte]:checked').val());
    var sHtml= '<div class="row titulo">'
                    + '<div class="col-md-6">'
                    +     'Reporte'
                   + ' </div>'
               + '</div>'
                    +'<table cellspacing="1"  class="tablesorter" id="tablaGrafica">'
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

                +'<script id="js" type="text/javascript">'
                +'$ts(function() {'
                +'    $ts("#tablaGrafica").tablesorter({'
                +'    theme: "blue",'
                +'    showProcessing: true,'
                +'    headerTemplate : "{content} {icon}",'
                +'    widgets: [ "uitheme", "zebra", "pager","scroller" ],'
                +'    widgetOptions : {'
                +'        scroller_height : 90,'
                +'        scroller_upAfterSort: true,'
                +'        scroller_jumpToHeader: true,'
                +'        scroller_barWidth : null,'
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