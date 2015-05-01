/**
 * Created by usuario on 30/04/2015.
 */
/**
 * Created by db2 on 7/04/15.
 */
$(document).on('ready', main_consulta);

function main_consulta() {
    $.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if(settings.type == "POST"){
				xhr.setRequestHeader("X-CSRFToken", $('[name="csrfmiddlewaretoken"]').val());
			}
            if(settings.type == "GET"){
				xhr.setRequestHeader("X-CSRFToken", $('[name="csrfmiddlewaretoken"]').val());
			}
		}
	});

	$('#ver_datos button').on('click', verDatos);
}




function verDatos() {
    var arrayDependencias = $("#msDependencias").multiselect("getChecked").map(function(){
                                         return this.value;
                                    }).get();

    alert(arrayDependencias);
    //for ( in dependencias.value) {
    //       alert(dep);
    //}


    $.get('http://127.0.0.1:8000/obras/consultar-obras');
}
