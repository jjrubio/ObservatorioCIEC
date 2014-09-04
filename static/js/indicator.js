var last_year;
var last_trim;

$(document).ready(function() {
    $.getJSON('/last-full-year/',function(data){
        last_year = data[0];
        last_trim = data[1];
    });
});

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
    $('#parametros').removeClass( "in" );
    $('#desagregaciones').removeClass( "in" );
    $('#loading-result').show();
    $('#content-result').hide();
    var selected = [];
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
        table(data);
        graphs(data);
        $('#loading-result').hide();
        $('#content-result').show();
    });
});

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
    modificarPeriodo($('#yearStart'), 2007, last_year);
    modificarPeriodo($('#yearEnd'), 2007, last_year);
    modificarPeriodo($('#trimStart'), 2, 4);
    modificarPeriodo($('#trimEnd'), 1, last_trim);
    $('#yearEnd option[value='+last_year+']').attr("selected","selected");
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
    }else if($('#yearStart').val() == last_year){
      modificarPeriodo('#trimStart', 1, last_trim);
    }else{
      modificarPeriodo('#trimStart', 1, 4);
    }
    modificarPeriodo($('#yearEnd'), $('#yearStart').val(), last_year);
    modificarPeriodo($('#trimEnd'), 1, last_trim);
    $('#trimEnd option[value='+last_trim+']').attr("selected","selected");
    $('#yearEnd option[value='+last_year+']').attr("selected","selected");
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
    }else if($('#yearEnd').val() == last_year){
      modificarPeriodo('#trimEnd', 1, last_trim);
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

function table(data){
    var tam_data = data.length;
    var tam_periodos = tam_data - 8;
    var titulo = data[tam_data - 8];
    var anios_titulo = data[tam_data - 7];
    var valor_dim_1 = data[tam_data -5][0];
    var valor_dim_2 = data[tam_data -5][1];
    var nombres_desagre = [];

    $('.title').text(titulo);
    $('.years-title').text(anios_titulo);

    if(valor_dim_2 == 0){
        for(i=0 ; i<(data[tam_data-2].length); i++){
            nombres_desagre.push(data[tam_data-2][i]);
        }
    }else{
        for(i=0 ; i<(data[tam_data-2].length); i++){
            for(j=0 ; j<(data[tam_data-1].length); j++){
                nombres_desagre.push(data[tam_data-2][i]+' - '+data[tam_data-1][j]);
            }
        }
    }


    $('#titulo').empty()
    $('#titulo_secundario').empty()
    $('#periodo').empty()

    $('#titulo').append('<th></th>');
    $('#titulo_secundario').append('<th class="text-center">Periodo</th>');

    for(i=0; i<nombres_desagre.length; i++){
        var th_one = '<th colspan="3" class="text-center">'+nombres_desagre[i]+'</th>';
        var th_two = '<th class="text-center">'+'N'+'</th>'+'<th class="text-center">'+'Indic.'+'</th>'+'<th class="text-center">'+'Std.'+'</th>';
        $('#titulo').append(th_one);
        $('#titulo_secundario').append(th_two);
    }

    for(i=0; i<tam_periodos; i++){
        data_x_periodo = '<tr><td nowrap>'+data[i][0]+' - '+data[i][1]+'</td></tr>'
        $('#periodo').append(data_x_periodo);
        for(j=0; j<data[i][2].length; j++){
            if(data[i][2][j] == 0){
                $('#periodo tr:last-child td:last-child').after('<td>   </td>');
            }else{
                $('#periodo tr:last-child td:last-child').after('<td>'+data[i][2][j]+'</td>');
            }
            for(k=0; k<2; k++){
                if(data[i][2][j] == 0){
                    $('#periodo tr:last-child td:last-child').after('<td>   </td>');
                }else if(data[i][3][j][k] == null){
                    $('#periodo tr:last-child td:last-child').after('<td>'+0+'</td>');
                }else{
                    $('#periodo tr:last-child td:last-child').after('<td>'+data[i][3][j][k].toFixed(6)+'</td>');
                }
            }
        }
    }
}

function graphs(data){
    var tam_data = data.length;
    var tam_periodos = tam_data - 8;
    var titulo = data[tam_data - 8];
    var anios_titulo = data[tam_data - 7];
    var valor_dim_1 = data[tam_data - 5][0];
    var valor_dim_2 = data[tam_data - 5][1];
    var name_desagre_1 = data[tam_data - 4];
    var name_desagre_2 = data[tam_data - 3];
    var type_desagre_1;
    var type_desagre_2;
    var nombres_desagre = [];

    $("#ul_desagregaciones").empty();
    if(valor_dim_2 == 0){
        $("#ul_desagregaciones").append('<li><a href="#'+name_desagre_1+'" role="tab" data-toggle="tab">'+name_desagre_1+'</a></li>')
        $("#div_desagregaciones").append('<div class="tab-pane active" id="'+name_desagre_1+'"></div>');
    }else{
        if(valor_dim_1 <= valor_dim_2){
            type_desagre_1 =data[tam_data - 2];
            type_desagre_2 =data[tam_data - 1];
        }else{
            type_desagre_1 =data[tam_data - 1];
            type_desagre_2 =data[tam_data - 2];
        }

        for(i=0; i<type_desagre_1.length; i++){
            $("#ul_desagregaciones").append('<li><a href="#'+type_desagre_1[i]+'" role="tab" data-toggle="tab">'+type_desagre_1[i]+'</a></li>')
            $("#div_desagregaciones").append('<div class="tab-pane active" id="'+type_desagre_1[i]+'"></div>');
        }
    }
    $("#ul_desagregaciones li:first-child").addClass( "active" );



  // var tam_total,i,index=0,j,cst,count=0,dim_1,dim_2,representatividad;
  // var valores = [];
  // var anio_trim = [];
  // var to_graph = [];
  // var name_desagre = [];
  // tam_total = data.length;
  // tam_for = tam_total - 3;

  // console.log(data);

  // for(i=0;i<tam_for;i++){
  //   anio_trim.push(data[i][0]+'-'+data[i][1]);
  //   console.log(data[i]);
  //   for(j=0;j<data[i][2].length;j++){
  //     valores[index] = [data[i][2][j][0], (data[i][2][j][0] + data[i][2][j][1]), (data[i][2][j][0] - data[i][2][j][1])];
  //     index++;
  //   }
  // }
  // cst = data[0][2].length;
  // for(i=0;i<valores.length;i++){
  //   if(count<cst){
  //     if(to_graph[count] == null){
  //       to_graph[count] = valores[i];
  //     }else{
  //       to_graph[count] = to_graph[count].concat(valores[i]);
  //     }
  //     count++;
  //   }else{
  //     count=0;
  //     to_graph[count] = to_graph[count].concat(valores[i]);
  //     count++;
  //   }
  // }
  // representatividad = data[tam_for];
  // dim_1 = data[tam_for+1][0];
  // dim_2 = data[tam_for+1][1];
  // for(i=(tam_for+2);i<tam_total;i++){
  //   for(j=0;j<(data[i].length);j++){
  //     name_desagre.push(data[i][j]);
  //   }
  // }
  // // console.log(to_graph);
  var options = {
    chart: {
            renderTo: 'container',
            type: 'spline',
        },
        title: {
            // text: 'Tasa de poblacion en edad de trabajar',
            text: 'Hombre',
            x: -20 //center
        },
        // subtitle: {
        //     text: 'Hombre',
        //     x: -20
        // },
        xAxis: {
            categories: ['2003', '2004', '2005', '2006', '2007'],
            title: {
                enabled: true,
                text: 'Años',
            },
        },
        yAxis: {
            title: {
                text: 'Porcentaje (%)'
            },
            labels: {
                formatter: function () {
                    return (this.value*100) + '%';
                }
            },
        },
        legend: {
            enabled: false
        },
        tooltip: {
            enabled: false
        },
        plotOptions: {
            series: {
                marker: {
                    enabled: false
                },
            },
        },
        series: [{
            name: 'Indicador',
            data: [0.70, 0.69, 0.95, 1.4512, 1.82],
            dataLabels: {
                enabled: true,
                formatter: function () {
                    return Highcharts.numberFormat(this.y*100, 2, ',') + '%';
                },
                color: '#5b9bd5',
                y: -15
            },
            color: '#6AA4D9',
        }, {
            name: 'Positivo',
            data: [0.75, 0.74, 1.00, 1.50, 1.87],
            dashStyle: 'Dot',
            color: '#6AA4D9',
        },{
            name: 'Negativo',
            data: [0.65, 0.64, 0.90, 1.40, 1.77],
            dashStyle: 'Dot',
            color: '#6AA4D9',
        },],
        exporting: {
            filename: 'custom-file-name'
        }
  };


  // options.series[0].data = [5, 12];
  // options.series[0].dashStyle = 'dash';
  // options.xAxis.categories[0] = 'valueOne';
  var chart = new Highcharts.Chart(options);

  // chart.series[0].addPoint(50);
}

function indicador_desagregacion_filtro(id_indicador){
  $.getJSON('/indicadorFiltro/', {'id_indicator': id_indicador},
    function(data){
        $('#ckb').children().remove();
          $.each(data, function(index, item){
            var tmpHTML = "<div class=\'checkbox\'><label><input type=\'checkbox\' id="+item.pk+">"+item.fields.name+"</label></div>";
            $('#ckb').append(tmpHTML);
          });
          init(data);
    });
}

//Validaciones entre desagregaciones
function init(data){
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
      filter(validos_selec[0],data);

    }
    else if(validos_selec.length > 2){
      $(this).prop('checked',false);
    }
  });
}

function filter(id_1,data_filter){
  var des_filter = [];
  $.each(data_filter, function(i,v){
    des_filter.push(v.pk);
  });

  $.getJSON('/list_denied/', {'id_desagregacion': id_1, 'data_filters[]' : des_filter},function(data){
      $('#ckb').children().remove();
      $.each(data, function(index, item){
          if(id_1 == item.pk){
              var tmpHTML = "<div class=\'checkbox\'><label><input type=\'checkbox\' checked id="+item.pk+">"+item.fields.name+"</label></div>";
              $('#ckb').append(tmpHTML);
          }else{
              var tmpHTML = "<div class=\'checkbox\'><label><input type=\'checkbox\' id="+item.pk+">"+item.fields.name+"</label></div>";
              $('#ckb').append(tmpHTML);
          }
          init(data_filter);
      });
  });
}
