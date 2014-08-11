
function getMenu(cat, subcat, ind){
        var url = location.href;
        var arrayURL = location.href.split('/');

        if(arrayURL[3] == 'calculo-indicador'){
          history.pushState(null, "", "/calculo-indicador/"+cat+"/"+subcat+"/"+ind+"/");
        }else{
          history.pushState(null, "", "/definicion-indicador/"+cat+"/"+subcat+"/"+ind+"/");
        }
        window.location.reload();
}

$(window).bind("popstate", function(e) {
        window.location.reload();
});

$('#linkToCalc').click(function(){
      history.pushState(null, "", "/calculo-indicador/"+$("#category").val()+"/"+$("#subcategory").val()+"/"+$("#indicator").val()+"/");
      window.location.reload();
});

$('#category').change( function() {
      getMenu($(this).val(), 1, 1);
});

$('#subcategory').change( function() {
    getMenu($("#category").val(), $(this).val(), 1);
});

$('#indicator').change( function() {
    getMenu($("#category").val(), $("#subcategory").val(), $(this).val());
});

$('#a-parametros').click(function(){
  $('#desagregaciones').removeClass( "in" );
  $('#resultados').removeClass( "in" );
});

$('#a-desagregaciones').click(function(){
  $('#parametros').removeClass( "in" );
  $('#resultados').removeClass( "in" );
});

$('#a-resultados').click(function(){
  $('#desagregaciones').removeClass( "in" );
  $('#parametros').removeClass( "in" );
});

$('.btn-next').click( function(){
    $('#parametros').removeClass( "in" );
    var id_indicator = $('#indicator option:selected').attr('id');
    indicador_desagregacion_filtro(id_indicator);
});

$('.btn-back').click( function(){
    $('#desagregaciones').removeClass( "in" );
});

$('.btn-calc').click( function(){
    $('#desagregaciones').removeClass( "in" );
    $('.fa-spinner').show();
    $('#text-spinner').show();
    $('.graph').hide();
    var selected = new Array();
    $('input:checkbox').each(function(){
        if($(this).is(':checked')){
            selected.push($(this).attr('id'));
        }
    });

    var indicator = $('#indicator option:selected').attr('id');
    var represent = $('#represent').val();
    var method = $('#method').val();
    var yearStart = $('#yearStart').val();
    var trimStart = $('#trimStart').val();
    var yearEnd = $('#yearEnd').val();
    var trimEnd = $('#trimEnd').val();

    $.getJSON('/result/', {'indicator': indicator, 'represent': represent, 'method': method, 'yearStart': yearStart,
                                      'trimStart': trimStart, 'yearEnd': yearEnd, 'trimEnd': trimEnd, 'disintegrations[]': selected},
    function(data){
        console.log(data);
        $('.fa-spinner').hide();
        $('#text-spinner').hide();
        $('.graph').show();
        table(trimStart,trimEnd,yearStart,yearEnd,data);
        graphs();
        $('#btnExport').show();
        $('#scroll').show();
    });
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

$('#meaning-parameters').hide();

$('#info-represent').hover(function(){
    $('#meaning-parameters').show();
    $('#meaning-parameters .panel-body').empty();
    $('#meaning-parameters .panel-heading h3').empty();
    $('#meaning-parameters .panel-heading h3').text('Representatividad');
    $('#meaning-parameters .panel-body').html('<b>Nacional.-</b> Se define como el área total comprendida\
                                                                            por las zonas urbanas y zonas rurales. <br><br>\
                                                                            <b>Urbano.-</b> Se define como zona urbana como "ciudad" a\
                                                                            aquellos asentamientos de 2.000 o más habitantes. <br><br>\
                                                                            <b>Rural.-</b> Se define como zona "rural" o "campo" a las\
                                                                            zonas que se encuentren en las periferias de las ciudades\
                                                                            que tengan menos de 2.000 habitantes.');
}, function(){
    $('#meaning-parameters').hide();
})

$('#info-method').hover(function(){
    $('#meaning-parameters').show();
    $('#meaning-parameters .panel-body').empty();
    $('#meaning-parameters .panel-heading h3').empty();
    $('#meaning-parameters .panel-heading h3').text('Metodología');
    $('#meaning-parameters .panel-body').html('<b>2003-4 a 2007-1.-</b> Antes de esta fecha solo la población\
                                                                            urbana era analizada. A partir de esta fecha la definición de lo que\
                                                                            constituye un centro urbano fue cambiada también. <br><br>\
                                                                            <b>2007-2 a la actualidad.-</b> Se definen modificaciones en las\
                                                                            definiciones y clasificaciones utilizadas para el mercado laboral. Estas\
                                                                            son: definición de área urbana y rural, periodicidad de la encuesta,\
                                                                            PEA según mercado laboral, el periodo de referencia para la búsqueda\
                                                                            de empleo y el desempleo. ');
}, function(){
    $('#meaning-parameters').hide();
})

$("#btnExport").click(function(e){
    window.open('data:application/vnd.ms-excel,'+encodeURIComponent($('#dvData').html()));
    e.preventDefault();
});

function table(trim_1,trim_2,yearStart,yearEnd,data){
  $.getJSON('/table/', {'trim_1': trim_1, 'trim_2': trim_2, 'yearStart': yearStart, 'yearEnd': yearEnd},
    function(data){
      console.log(data);
      for(var i=0;i<data.length;i++){
        var tr_periodos = '<tr><td>'+data[i]+'</td></tr>';
        $('#periodo').append(tr_periodos);
      }
        /*$.each(data, function(index,value){
          console.log(value);
          var tr_periodos = '<tr></td>'+value+'</td></tr>';
          /*var th_one = '<th colspan="3">'+value.fields.name+'</th>';
          var th_two = '<th>'+'val1'+'</th>'+'<th>'+'val2'+'</th>'+'<th>'+'val3'+'</th>';
          var td = '<td>'+'3'+'</td>'+'<td>'+'4'+'</td>'+'<td>'+'5'+'</td>';
          $('#titulo').append(th_one);
          $('#titulo_secundario').append(th_two);
          $('#data').append(td);
          //$('#periodo').append(tr_periodos);
        });*/
    });
}

function graphs(){
  //console.log("Dentro de la funcion graph:"+data);
  var options = {
    chart : {
      renderTo: 'container',
      type : 'column'
    },
    title: {
      text: 'Titulo del grafico',
      x: -20
    },
    subtitle: {
      text: 'Subtitulo del grafico',
      x: -20
    },
    xAxis: {
      categories: []
    },
    yAxis:{
      title: 'Axisa Y'
    },
    series: [{}]
  };

  $.getJSON('/grafico/',
    function(data){
      console.log(data);
      options.series[0].name = 'Name';
      options.series[0].data = data;
      options.series[0].dashStyle = 'dash';
      options.xAxis.categories[0] = 'valueOne';
      var chart = new Highcharts.Chart(options);
  });  
}

function indicador_desagregacion_filtro(id_indicador){
  console.log(id_indicador);
  $.getJSON('/indicadorFiltro/', {'id_indicator': id_indicador},
    function(data){
        $('#ckb').children().remove();
          $.each(data, function(index, item){
            var tmpHTML = "<div class=\'checkbox\'><label><input type=\'checkbox\' id="+item.pk+">"+item.fields.name+"</label></div>";
            $('#ckb').append(tmpHTML);
          });
          init();
    });
}

//Validaciones entre desagregaciones
function init(){
  $(":checkbox").click(function(){
    var validos_selec = [];

    $('input:checkbox').each(function(){
      if($(this).is(':checked')){
        validos_selec.push($(this).attr('id'));
      }
    });

    if(validos_selec.length == 0){
      var id_indicator = $('#indicator option:selected').attr('id');
      indicador_desagregacion_filtro(id_indicator);
    }
    else if(validos_selec.length == 1){
      filter(validos_selec[0]);
    }
    else if(validos_selec.length > 2){
      $(this).prop('checked',false);
    }
  });
}

function filter(id_1){
  $.getJSON('/list_denied/', {'id_desagregacion': id_1},function(data){
      $('#ckb').children().remove();
      $.each(data, function(index, item){
          if(id_1 == item.pk){
              var tmpHTML = "<div class=\'checkbox\'><label><input type=\'checkbox\' checked id="+item.pk+">"+item.fields.name+"</label></div>";
              $('#ckb').append(tmpHTML);
          }else{
              var tmpHTML = "<div class=\'checkbox\'><label><input type=\'checkbox\' id="+item.pk+">"+item.fields.name+"</label></div>";
              $('#ckb').append(tmpHTML);
          }
          init();
      });
  });
}
