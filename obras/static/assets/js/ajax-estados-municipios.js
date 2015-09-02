/**
 * Created by mng687 on 9/1/15.
 */
var $j = jQuery.noConflict();

$j(document).on('ready', function() {
    if ($('#id_municipio').find('option:selected').val() == "") {
        clearMunicipios();
    }
    else {
        var municipioId = $('#id_municipio').find('option:selected').val()

        $j.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if(settings.type == "POST")
                    xhr.setRequestHeader("X-CSRFToken", $j('[name="csrfmiddlewaretoken"]').val());
                if(settings.type == "GET")
                    xhr.setRequestHeader("X-CSRFToken", $j('[name="csrfmiddlewaretoken"]').val());
            }
        });

        $.get('/obras/register-by-token', function(ans) {
            var ajaxData = { access_token: ans.access_token, estados: estadoId };

            $j.ajax({
                url: '/obras/api/municipios_por_estado',
                type: 'get',
                data: ajaxData,
                success: function(ans) {
                    alert("Sí lo estoy haciendo chucha " + municipioId);
                    populateMunicpiosSelect(ans);
                    $('#id_municipio').select(municipioId);
                }
            });
        });
    }
    $('#id_estado').on('change', function() {
        var option = $(this).find('option:selected');

        if (option != null) {
            var estadoId = option.val();
            if (estadoId == "")
                clearMunicipios();
            else
                getMunicipiosForEstado(parseInt(estadoId));
        }
    });
});

function getMunicipiosForEstado(estadoId) {
    $j.ajaxSetup(
        {
            beforeSend: function(xhr, settings) {
                if(settings.type == "POST")
                    xhr.setRequestHeader("X-CSRFToken", $j('[name="csrfmiddlewaretoken"]').val());
                if(settings.type == "GET")
                    xhr.setRequestHeader("X-CSRFToken", $j('[name="csrfmiddlewaretoken"]').val());
            }
        }
    );

    $.get('/obras/register-by-token', function(ans) {
        var ajaxData = { access_token: ans.access_token, estados: estadoId };

        $j.ajax({
            url: '/obras/api/municipios_por_estado',
            type: 'get',
            data: ajaxData,
            success: function(ans) {
                populateMunicpiosSelect(ans);
            }
        });
    });
}

function populateMunicpiosSelect(municipios) {
    clearMunicipios();
    for (var i = 0; i < municipios.length; i++) {
        $j('#id_municipio').append(
            '<option value="'+municipios[i].id+'">' +
            municipios[i].nombreMunicipio +
            '</option>'
        );
    }
}

function clearMunicipios() {
    $j('#id_municipio')
        .empty()
        .append('<option value>---------</option>');
}