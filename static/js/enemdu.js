var msg_1 = "* Error, solo números.";
var msg_2 = "* Error, verifique que los campos no esten vacíos.";
var msg_3 = "* Error, solo años desde 2003 hasta actualidad.";
var msg_4 = "* Error, solo números entre 1 al 4";
var msg_5 = "* Se eliminaron los dato exitosamente.";
var msg_6 = "* Error, los datos que desea eliminar no existen.";
var msg_7 = "* Error, año inicial tiene que ser menor al año final.";
var msg_8 = "* Error, trimestre inicial tiene que ser menor al trimestre final.";

$('#btn-delete').click(function(){
	$('#msg_1').empty();
    $('#msg_2').empty();
    $('#msg_3').empty();
    var txt_anio = $('#anio').val();
    var txt_trimestre = $('#tri').val();
    var choice = $('#id_choices').val();
    var spin = "<b><i class=\'fa fa-spinner fa-spin fa-3x\'></i></b>";

    $('#msg_3').append("Eliminando los datos, por favor espere."+spin);
    
	$.getJSON('/eliminar_datos/', {'choice':choice, 'txt_anio': txt_anio, 'txt_trimestre': txt_trimestre},
    function(data){
    	if (data == 1){
            $('#msg_3').empty();
            $('#msg_3').append(msg_5);
        }else if(data == 2){
            $('#msg_3').empty();
            $('#msg_2').append(msg_4);
        }else if(data == 0){
            $('#msg_3').empty();
            $('#msg_1').append(msg_3);
        }else if(data == 3){
            $('#msg_3').empty();
            $('#msg_3').append(msg_6);
        }else if(data == 4){
            $('#msg_3').empty();
            $('#msg_3').append(msg_2);
        }else{
            $('#msg_3').empty();
            $('#msg_3').append(msg_1);
        }
    });

});

$('#btn-delete-range').click(function(){
    $('#msg_4').empty();
    $('#msg_5').empty();
    $('#msg_6').empty();
    $('#msg_7').empty();
    $('#msg_8').empty();
    var txt_anio_1 = $('#anio_1').val();
    var txt_anio_2 = $('#anio_2').val();
    var txt_trimestre_1 = $('#tri_1').val();
    var txt_trimestre_2 = $('#tri_2').val();
    var choice = $('#id_choices').val();
    var spin = "<b><i class=\'fa fa-spinner fa-spin fa-3x\'></i></b>";

    $('#msg_8').append("Eliminando los datos, por favor espere."+spin);

    $.getJSON('/eliminar_datos_rango/', {'choice':choice, 'txt_anio_1': txt_anio_1, 'txt_anio_2': txt_anio_2, 'txt_trimestre_1': txt_trimestre_1, 'txt_trimestre_2': txt_trimestre_2},
    function(data){
        if (data == 0){
            $('#msg_8').empty();
            $('#msg_8').append(msg_5);
        }else if(data == 1){
            $('#msg_8').empty();
            $('#msg_4').append(msg_3);
        }else if(data == 2){
            $('#msg_8').empty();
            $('#msg_5').append(msg_3);
        }else if(data == 3){
            $('#msg_8').empty();
            $('#msg_8').append(msg_7);
        }else if(data == 4){
            $('#msg_8').empty();
            $('#msg_8').append(msg_2);
        }else if(data == 5){
            $('#msg_8').empty();
            $('#msg_8').append(msg_1);
        }else{
            $('#msg_8').empty();
            $('#msg_8').append(msg_6);
        }
    });
});

$('#btn-delete-year-range').click(function(){
    $('#msg_9').empty();
    $('#msg_10').empty();
    $('#msg_11').empty();
    $('#msg_12').empty();
    var txt_year = $('#year').val();
    var txt_tri_1 = $('#trimestre_1').val();
    var txt_tri_2 = $('#trimestre_2').val();
    var choice = $('#id_choices').val();
    var spin = "<b><i class=\'fa fa-spinner fa-spin fa-3x\'></i></b>";

    $('#msg_12').append("Eliminando los datos, por favor espere."+spin);

    $.getJSON('/eliminar_anio_rango_trim/', {'choice':choice, 'txt_year': txt_year, 'txt_tri_1': txt_tri_1, 'txt_tri_2': txt_tri_2},
    function(data){
        if (data == 4){
            $('#msg_12').empty();
            $('#msg_12').append(msg_2);
        }else if(data == 5){
            $('#msg_12').empty();
            $('#msg_12').append(msg_1);
        }else if(data == 3){
            $('#msg_12').empty();
            $('#msg_9').append(msg_3);
        }else if(data == 2){
            $('#msg_12').empty();
            $('#msg_10').append(msg_4);
        }else if(data == 1){
            $('#msg_12').empty();
            $('#msg_11').append(msg_4);
        }else if(data == 6){
            $('#msg_12').empty();
            $('#msg_12').append(msg_8);
        }else if(data == 0){
            $('#msg_12').empty();
            $('#msg_12').append(msg_5);
        }else{
            $('#msg_12').empty();
            $('#msg_12').append(msg_6);
        }
    });
});