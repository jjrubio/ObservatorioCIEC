$(document).ready( function() {
    initialize();
});

function getMenu(cat, subcat, ind){
    $.get('/detalle-indicador/'+cat+'/'+subcat+'/'+ind+'/', function(data) {

        $('#subcategory').empty();
        $('#indicator').empty();

        $.each(data, function(key, value) {
            $.each(data[key], function(key2, value2) {
                if(key==0){
                    $('#subcategory').append($("<option></option>").attr("value",key2).text(value2.name));
                    $('#subcategory option[value='+key2+']').attr("data-icon","fa "+value2.icon);
                }
                if(key==1){
                    $('#indicator').append($("<option></option>").attr("value",key2).text(value2.name));
                    $('#indicator option[value='+key2+']').attr("data-icon","fa "+value2.icon);
                }
            });
        });

        $('#subcategory option[value='+subcat+']').attr("selected","selected");
        $('#indicator option[value='+ind+']').attr("selected","selected");


        $('.panel-body b:first'). text(data[2][0].name.toUpperCase());
        $('.panel-body p span'). text(data[2][0].definition);
        $('.panel-body img').attr("src",MEDIA_URL+data[2][0].formula);
        $('.panel-footer .pull-right span'). text(data[2][0].unit);

        $('.selectpicker').selectpicker('refresh');
    });
}

$('#category').change( function() {
        getMenu($(this).val(), 0, 0);
});

$('#subcategory').change( function() {
        getMenu($("#category").val(), $(this).val(), 0);
});

$('#indicator').change( function() {
        getMenu($("#category").val(), $("#subcategory").val(), $(this).val());
});

function initialize(){
        getMenu($("#category").val(), 0, 0);
}

$('.btn-next').click( function(){
    $('#parametros').removeClass( "in" );
});

$('.btn-back').click( function(){
    $('#desagregaciones').removeClass( "in" );
});

$('.btn-calc').click( function(){
    $('#desagregaciones').removeClass( "in" );
});