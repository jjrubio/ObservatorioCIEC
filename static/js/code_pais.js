$(document).ready( function () {
    $('#tabla_codigo_paises').bdt();
});

$('#codigo_pais').click(function(){
    $('#div_tabla').show();
});

$('#btn-delete').click(function(){
    $('#msg_1').empty();
    $('#msg_2').empty();
    var txt_choice = $('#id_choices').val();
    var txt_code = $('#code').val();
    var spin = "<b><i class=\'fa fa-spinner fa-spin fa-3x\'></i></b>";                
    $('#msg_2').append("Eliminando los datos."+spin);
    $(this).attr('disabled','disabled');
    $.getJSON('/eliminar_comercio/', {'txt_choice':txt_choice, 'txt_code': txt_code},
    function(data){
        if (data == 0){
            $('#msg_2').empty();
            $('#msg_1').append('* Error, campo vacío.');
        }else if(data == 1){
            $('#msg_2').empty();
            $('#msg_1').append('* Error, solo números.');
        }else if(data == 2){
            $('#msg_2').empty();
            $('#msg_1').append('* Error, no existe ese código de país en la tabla seleccionada.');
        }else{
            $('#msg_2').empty();
            $('#msg_2').append('* Se eliminaron los datos correctamente.');
        }
        $('#btn-delete').removeAttr("disabled");
    });
});
                                                                                                                                                                            
$('#button_send').click(function(){
    $("#loading").show();
});
$('#formulario').one('submit', function() {
    $(this).find('input[type="submit"]').attr('disabled','disabled');
});