/**
 * Created by db2 on 14/06/15.
 */
var $i = jQuery.noConflict();
//$i(document).on('ready', valida_token);

function valida_token(){
var ajax_datatoken = {
      "access_token"  : 'O9BfPpYQuu6a5ar4rGTd2dRdaYimVa'
    };


    $i.ajax({
        url: '/obras/register-by-token',
        type: 'get',
        data: ajax_datatoken,
        success: function(data) {
            //newToken = data.access_token;
            alert("entra");
            $i.cookie('token', data.access_token, { expires: 1, domain: 'http://localhost:8000/obras' });
            alert($.cookie('token'));
        },
        error: function(data) {
            alert('error!!! ' + data.status);
        }
    });
}

valida_token();