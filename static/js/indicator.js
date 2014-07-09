$(document).ready( function() {
    initialize();
});

function getMenu(cat, subcat, ind){
    // $.get('/detalle-indicador/'+cat+'/'+subcat+'/'+ind+'/', function(data) {
        // $('#category').empty();
        $('#subcategory').empty();
        $('#indicator').empty();

        history.pushState(null, "", "/calculo-indicador/"+cat+"/"+subcat+"/"+ind+"/");

        // $.each(data, function(key, value) {
        //     $.each(data[key], function(key2, value2) {
        //         if(key==0){
        //             $('#subcategory').append($("<option></option>").attr("value",key2).text(value2.name));
        //             $('#subcategory option[value='+key2+']').attr("data-icon","fa "+value2.icon);
        //         }
        //         if(key==1){
        //             $('#indicator').append($("<option></option>").attr("value",key2).text(value2.name));
        //             $('#indicator option[value='+key2+']').attr("data-icon","fa "+value2.icon);
        //         }
        //     });
        // });

        $('#category option[value='+2+']').attr("selected","selected");
        $('#subcategory option[value='+subcat+']').attr("selected","selected");
        $('#indicator option[value='+ind+']').attr("selected","selected");

        location.reload();
        // $('.panel-body b:first'). text(data[2][0].name.toUpperCase());
        // $('.panel-body p span'). text(data[2][0].definition);
        // $('.panel-body img').attr("src",MEDIA_URL+data[2][0].formula);
        // $('.panel-footer .pull-right span'). text(data[2][0].unit);

        // $('.selectpicker').selectpicker('refresh');


    // });
}


$('#category').change( function() {
      getMenu($(this).val(), 1, 1);
       // history.pushState(null, "", "/calculo-indicador/"+$(this).val()+"/"+1+"/"+1+"/");
       // location.reload();
    // }
    // history.replaceState(null, null, "/calculo-indicador/"+$(this).val()+"/"+1+"/"+1+"/");
});

$('#subcategory').change( function() {
    // getMenu($("#category").val(), $(this).val(), 0);
});

$('#indicator').change( function() {
    // getMenu($("#category").val(), $("#subcategory").val(), $(this).val());
});

function initialize(){
    // getMenu($("#category").val(), 0, 0);

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


var d = new Date();
//Valores por defecto para Periodo Inicial y Periodo Final
$('#method').change(function(){
  $('#yearStart').empty();
  $('#trimStart').empty();
  $('#yearEnd').empty();
  $('#trimEnd').empty();
  if(this.value == 1){
    modificarPeriodo($('#yearStart'), 2003, 2007);
    modificarPeriodo($('#yearEnd'), 2003, 2007);
    modificarPeriodo($('#trimStart'), 4, 4);
    modificarPeriodo($('#trimEnd'), 1, 1);
    $('#yearEnd option[value='+2007+']').attr("selected","selected");
  }else{
    modificarPeriodo($('#yearStart'), 2007, d.getFullYear());
    modificarPeriodo($('#yearEnd'), 2007, d.getFullYear());
    modificarPeriodo($('#trimStart'), 2, 4);
    modificarPeriodo($('#trimEnd'), 1, Math.round((d.getMonth()+1)/3));
    $('#yearEnd option[value='+d.getFullYear()+']').attr("selected","selected");
    $('#trimEnd option:last').attr("selected","selected");
  }
  $('.selectpicker').selectpicker('refresh');
});

//Cambio en el año del periodo inicial
$('#yearStart').change(function(){
  $('#trimStart').empty();
  $('#yearEnd').empty();
  $('#trimEnd').empty();
  if($('#method').val() == 1){
    if($('#yearStart').val() == 2003){
      modificarPeriodo('#trimStart', 4, 4);
    }else if($('#yearStart').val() == 2007){
      modificarPeriodo('#trimStart', 1, 1);
    }else{
      modificarPeriodo('#trimStart', 1, 4);
    }
    modificarPeriodo($('#yearEnd'), $('#yearStart').val(), 2007);
    modificarPeriodo($('#trimEnd'), 1, 1);
    $('#yearEnd option[value='+2007+']').attr("selected","selected");
  }else{
    if($('#yearStart').val() == 2007){
      modificarPeriodo('#trimStart', 2, 4);
    }else if($('#yearStart').val() == d.getFullYear()){
      modificarPeriodo('#trimStart', 1, Math.round((d.getMonth()+1)/3));
    }else{
      modificarPeriodo('#trimStart', 1, 4);
    }
    modificarPeriodo($('#yearEnd'), $('#yearStart').val(), d.getFullYear());
    modificarPeriodo($('#trimEnd'), 1, Math.round((d.getMonth()+1)/3));
    $('#trimEnd option[value='+Math.round((d.getMonth()+1)/3)+']').attr("selected","selected");
    $('#yearEnd option[value='+d.getFullYear()+']').attr("selected","selected");
  }
  if(this.value == $('#yearEnd').val()){
    $('#trimEnd').empty();
    modificarPeriodo($('#trimEnd'), $('#trimStart').val(), $('#trimStart option:last').val());
  }
  $('.selectpicker').selectpicker('refresh');
});

//Cambio en el trimestre del periodo Inicial
$('#trimStart').change(function(){
  if($('#yearStart').val() == $('#yearEnd').val()){
    $('#trimEnd').empty();
    modificarPeriodo($('#trimEnd'), $('#trimStart').val(), $('#trimStart option:last').val());
    $('.selectpicker').selectpicker('refresh');
  }
});

//Cambio en el año del periodo Final
$('#yearEnd').change(function(){
  $('#trimEnd').empty();
  if($('#method').val() == 1){
    if($('#yearEnd').val() == 2003){
      modificarPeriodo('#trimEnd', 4, 4);
    }else if($('#yearEnd').val() == 2007){
      modificarPeriodo('#trimEnd', 1, 1);
    }else{
      modificarPeriodo('#trimEnd', 1, 4);
    }
  }else{
    if($('#yearEnd').val() == 2007){
      modificarPeriodo('#trimEnd', 2, 4);
    }else if($('#yearEnd').val() == d.getFullYear()){
      modificarPeriodo('#trimEnd', 1, Math.round((d.getMonth()+1)/3));
    }else{
      modificarPeriodo('#trimEnd', 1, 4);
    }
  }
  if(this.value == $('#yearStart').val()){
    $('#trimEnd').empty();
    modificarPeriodo($('#trimEnd'), $('#trimStart').val(), 4);
  }
  $('.selectpicker').selectpicker('refresh');
});

function modificarPeriodo(variable, start, end){
  for( var i = start; i <= end; i++ ){
    $(variable).append($("<option></option>").attr("value",i).text(i));
  }
}


var selected = new Array();
$('input:checkbox').each(function(){
    if($(this).is(':checked')){
        selected.push($(this).attr('id'));
    }
});

$.getJSON('/valid_desa/', {'id_desagregacions[]': selected},
function(data){
    console.log(data);
});
//console.log(selected);

