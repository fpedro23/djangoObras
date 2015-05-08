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
            access_token: 'TtXhoxrKoy2zh8BjzMRPaXtm2S4Quq',
            dependencia:arrayDependencias.toString()
        },
        success: function(data) {
            //$('#datos').html
            tabla(data);

        },
        error: function(data) {
            alert('error!!! ' + data.status);
        }
    });
    //$.get('http://127.0.0.1:8000/obras/consultar-obras');
}

function tabla(Datos){
    var sHtml='<table cellspacing="1" class="tablesorter" id="tablaIzquierda">'
                    +'<thead>'
                        +'<tr>'
                            +'<th>ID</th>'
                            +'<th>DENOMINACI&Oacute;N</th>'
                            +'<th>ESTADO</th>'
                        +'</tr>'
                    +'</thead>'
                    +'<tfoot>'
                        +'<tr>'
                            +'<th>ID</th>'
                            +'<th>DENOMINACI&Oacute;N</th>'
                            +'<th>ESTADO</th>'
                        +'</tr>'

                        +'<tr><td class="pager" id="pagerI" colspan="3">'
                        +'<img src="../../static/assets/tablesorter/addons/pager/icons/first.png" class="first" id="firstI"/>'
                        +'<img src="../../static/assets/tablesorter/addons/pager/icons/prev.png" class="prev" id="prevI"/>'
                        +'<input type="text" class="pagedisplay" id="pagedisplayI"/>'
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
                +'                container   : "#pagerI",       // target the pager markup'
                +'                first       : "#firstI",       // go to first page arrow'
                +'                prev        : "#prevI",        // previous page arrow'
                +'                next        : "#nextI",        // next page arrow'
                +'                last        : "#lastI",        // go to last page arrow'
                +'                gotoPage    : "#gotoPageI",    // go to page selector - select dropdown that sets the current page'
                +'                pageDisplay : "#pagedisplayI", // location of where the "output" is displayed'
                +'                pageSize    : "#pagesizeI"     // page size selector - select dropdown that sets the "size" option'
                +'        }'
                +'    }'
                +'});'
                +'});'
                +'</script>';




    $j('#datos').html(sHtml);
}