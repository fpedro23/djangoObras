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
    verDatos();

}




function verDatos() {


    $.get("/obras/register-by-token", function(respu) {
        var ajax_data = {
            "access_token": respu.access_token
        };

        $j.ajax({
            url: '/obras/api/inicio',
            type: 'get',
            data: ajax_data,
            success: function (data) {
                datosJson = data;

                graficas();
                datosConcluidas();
                // MAPA
                var mapOptions = {
                zoom: 4,
                center: new google.maps.LatLng(22.6526121, -100.1780452),
                mapTypeId: google.maps.MapTypeId.SATELLITE
                }
                var map = new google.maps.Map(document.getElementById('mapa'),
                                            mapOptions)
                var lugares =  new Array();
                lugares=puntosMapaTotales(data);
                setMarkers(map,lugares);
                google.maps.event.addDomListener(window, 'load', initialize);
                // mapa

            },
            error: function (data) {
                alert('error!!! ' + data.status);
            }
        });
    });
}



function datosConcluidas() {

    $j('#info2012').html(formato_numero(datosJson.reporte2012.obras_concluidas.total, 0, '.', ','));
    $j('#info2013').html(formato_numero(datosJson.reporte2013.obras_concluidas.total, 0, '.', ','));
    $j('#info2014').html(formato_numero(datosJson.reporte2014.obras_concluidas.total, 0, '.', ','));
    $j('#info2015').html(formato_numero(datosJson.reporte2015.obras_concluidas.total, 0, '.', ','));

}

function graficas(){

    titulo="Total de obras";


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



    pieGrafica(arregloDataGrafica(datosJson), titulo, 0,"Número de obras");

}


function arregloDataGrafica(Datos) {
    var arregloSimple=new Array();
    var arregloDoble=new Array();
    var arregloObjeto = new Object();



            var arregloSimple=new Array();
            arregloSimple.push("Obras Concluidas");
            arregloSimple.push(Datos.reporte_total.obras_concluidas.total);
            arregloSimple.push(Datos.reporte_total.obras_concluidas.inversion_total);

            arregloDoble.push(arregloSimple);
            var arregloSimple2=new Array();
            arregloSimple2.push("Obras en Proceso");
            arregloSimple2.push(Datos.reporte_total.obras_proceso.total);
            arregloSimple2.push(Datos.reporte_total.obras_proceso.inversion_total);
            arregloDoble.push(arregloSimple2);
            var arregloSimple3=new Array();
            arregloSimple3.push("Obras Proyectadas");
            arregloSimple3.push(Datos.reporte_total.obras_proyectadas.total);
            arregloSimple3.push(Datos.reporte_total.obras_proyectadas.inversion_total)
            arregloDoble.push(arregloSimple3);


    arregloObjeto = arregloDoble;
    return arregloObjeto;
}


function pieGrafica(datas,titulo,dona,nombreData) {

    var myComments=["First input","second comment","another comment","last comment"]
    $j('#containerGrafica').highcharts({
        chart: {
            type: 'pie',
            zoomType: 'x',
            panning: true,
            panKey: 'shift',
            options3d: {
                enabled: true,
                alpha: 45,
                beta: 0
            },
            style: {
                 color: '#FFFFFF',
                 fontFamily: 'soberana_sanslight',
                 fontSize: '15px'
            }
        },
        title: {
            style: {
                 color: '#FFFFFF',
                 fontFamily: 'soberana_sanslight'
            },
            text: titulo
        },
        credits: {
            enabled: false
        },
        tooltip: {
            style: { fontFamily: 'soberana_sanslight', fontSize: '15px' },
            pointFormat: 'Número de obras: <b>{point.y}</b><br>Porcentaje del Total: <b>{point.percentage:.2f}%</b>'

            //    var comment = myComments[serieI];


        },
        plotOptions: {
            pie: {
                style: { fontFamily: 'soberana_sanslight',color: 'white' ,fontSize: '12px' },
                innerSize: dona,
                allowPointSelect: true,
                cursor: 'pointer',
                depth: 35,
                dataLabels: {
                    enabled: true,
                    style: { fontFamily: 'soberana_sanslight',color: 'white' ,fontSize: '12px' },
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
    for(var i= 0;i<Datos.reporte2015.obras_concluidas.obras.length;i++){
        var arregloSimple=new Array();
        arregloSimple.push(Datos.reporte2015.obras_concluidas.obras[i].estado + ", obras Concluidas : " + Datos.reporte2015.obras_concluidas.obras[i].numero_obras);
        arregloSimple.push(Datos.reporte2015.obras_concluidas.obras[i].latitud);
        arregloSimple.push(Datos.reporte2015.obras_concluidas.obras[i].longitud);
        arregloSimple.push(i);
        arregloDoble.push(arregloSimple);
    }

    for(var j= 0;j<Datos.reporte2015.obras_proceso.obras.length;j++){
        var arregloSimple=new Array();
        arregloSimple.push(Datos.reporte2015.obras_proceso.obras[j].estado + ", obras en Proceso  : " + Datos.reporte2015.obras_proceso.obras[j].numero_obras);
        arregloSimple.push(Datos.reporte2015.obras_proceso.obras[j].latitud);
        arregloSimple.push(Datos.reporte2015.obras_proceso.obras[j].longitud);
        arregloSimple.push(j+i);
        arregloDoble.push(arregloSimple);
    }
    for(var k= 0;k<Datos.reporte2015.obras_proyectadas.obras.length;k++){
        var arregloSimple=new Array();
        arregloSimple.push(Datos.reporte2015.obras_proyectadas.obras[k].estado + ", obras Proyectadas : " + Datos.reporte2015.obras_proyectadas.obras[k].numero_obras);
        arregloSimple.push(Datos.reporte2015.obras_proyectadas.obras[k].latitud);
        arregloSimple.push(Datos.reporte2015.obras_proyectadas.obras[k].longitud);
        arregloSimple.push(k+j);
        arregloDoble.push(arregloSimple);
    }

    arregloObjeto = arregloDoble;
    return arregloObjeto;
}

function puntosMapaTotales(Datos) {
  var arregloSimple=new Array();
  var arregloDoble=new Array();
    var arregloObjeto = new Object();
    for(var i= 0;i<Datos.reporte_mapa.obras_mapa.obras.length;i++){
        var arregloSimple=new Array();
        arregloSimple.push(Datos.reporte_mapa.obras_mapa.obras[i].estado + ", " + Datos.reporte_mapa.obras_mapa.obras[i].numero_obras + " Obras, " + formato_numero(Datos.reporte_mapa.obras_mapa.obras[i].totalinvertido,2,'.',',') + " MDP.");
        arregloSimple.push(Datos.reporte_mapa.obras_mapa.obras[i].latitud);
        arregloSimple.push(Datos.reporte_mapa.obras_mapa.obras[i].longitud);
        arregloSimple.push(i);
        arregloDoble.push(arregloSimple);
    }
    arregloObjeto = arregloDoble;
    return arregloObjeto;
}


function setMarkers(mapa, lugares) {


  var image = {
    url: '../../static/assets/js/pines/pin.png',
    size: new google.maps.Size(20, 32),
    origin: new google.maps.Point(0,0),
    anchor: new google.maps.Point(0,32)};

  for (var i = 0; i < lugares.length; i++) {
    var puntos = lugares[i];
    var myLatLng = new google.maps.LatLng(puntos[1], puntos[2]);
    var marker = new google.maps.Marker({
        position: myLatLng,
        map: mapa,
        icon: '../../static/assets/js/pines/pin4.png',
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


function formato_numero(numero, decimales, separador_decimal, separador_miles){
    numero=parseFloat(numero);
    if(isNaN(numero)){
        return "";
    }

    if(decimales!==undefined){
        // Redondeamos
        numero=numero.toFixed(decimales);
    }

    // Convertimos el punto en separador_decimal
    numero=numero.toString().replace(".", separador_decimal!==undefined ? separador_decimal : ",");

    if(separador_miles){
        // Añadimos los separadores de miles
        var miles=new RegExp("(-?[0-9]+)([0-9]{3})");
        while(miles.test(numero)) {
            numero=numero.replace(miles, "$1" + separador_miles + "$2");
        }
    }

    return numero;
}