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

    alert(arrayDependencias);
    $j.ajax({
        url: '/obras/api/busqueda',
        type: 'get',
        data: {
            access_token: '7IfNOl1kJ6n73vt0Kx44scoIdlQFhZ',
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
    var sHtml='<table cellspacing="1" class="tablesorter">'
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

                        +'<tr><td class="pager" id="pager" colspan="3">'
                        +'<img src="../../static/assets/tablesorter/addons/pager/icons/first.png" class="first"/>'
                        +'<img src="../../static/assets/tablesorter/addons/pager/icons/prev.png" class="prev"/>'
                        +'<input type="text" class="pagedisplay"/>'
                        +'<img src="../../static/assets/tablesorter/addons/pager/icons/next.png" class="next"/>'
                        +'<img src="../../static/assets/tablesorter/addons/pager/icons/last.png" class="last"/>'
                        +'<select class="pagesize">'
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
                //+'<script src="../../static/assets/tablesorter/jquery.tablesorter.widgets.js"></script>'
                //+'<script src="../../static/assets/tablesorter/widget-scroller.js"></script>'
                +'<script type="text/javascript">'
                //+'$S=jQuery.noConflict();'
                +'$(function() {'
                +'    $("table")'
                +'        .tablesorter({theme: "blue",showProcessing: true,headerTemplate : "{content} {icon}", widgets: ["uitheme","pager","zebra", "scroller"],'
                +'          widgetOptions : {'
                +'          scroller_height : 300,'
                +'          scroller_upAfterSort: true,'
                +'          scroller_jumpToHeader: true,'
                +'          scroller_barWidth : null}'
                +'        })'
                //+'        .tablesorterPager({container: $("#pager")});'
                +'});'
                +'</script>';




    $j('#datos').html(sHtml);
}