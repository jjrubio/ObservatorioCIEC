var last_year;
var last_trim;
var excel_filename_download;

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

$('#accordion').on('show.bs.collapse', function () {
    $('#accordion .in').collapse('hide');
});

$('.btn-next, #a-desagregaciones').click( function(){
    $('#desagregaciones').collapse('show');
    var id_indicator = $('#indicator option:selected').attr('id');
    indicador_desagregacion_filtro(id_indicator);
});
//
$('.btn-back, #a-parametros').click( function(){
    $('#parametros').collapse('show');
});

$('.btn-calc, #a-resultados').click( function(){
    $('#resultado').collapse('show');
    $('#loading-result').show();
    $('#content-result').hide();
    $('#content-not-result').hide();
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
        if(data.length>0){
          table(data);
          graphs(data);
          $('#content-result').show();
        }else{
          $('#content-not-result').show();
        }
        $('#loading-result').hide();

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
  var uri = $('#Exporta_a_Excel').btechco_excelexport({
    containerid: "Exporta_a_Excel"
    ,returnUri: true
    ,datatype: $datatype.Table
  });
  $(this).attr('download', excel_filename_download+'.xls').attr('href', uri).attr('target', '_blank');
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

    $('#scroll_table').perfectScrollbar('destroy');
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
                }else{
                    $('#periodo tr:last-child td:last-child').after('<td>'+data[i][3][j][k].toFixed(6)+'</td>');
                }
            }
        }
    }
    $('#scroll_table').perfectScrollbar();
}

function graphs(data){
  var tam_data = data.length;
  var tam_periodos = tam_data - 8;
  var titulo = data[tam_data - 8];
  var anios_titulo = data[tam_data - 7];
  var unidad = data[tam_data - 6];
  var valor_dim_1 = data[tam_data - 5][0];
  var valor_dim_2 = data[tam_data - 5][1];
  var name_desagre_1 = data[tam_data - 4];
  var name_desagre_2 = data[tam_data - 3];
  var type_desagre_1 =data[tam_data - 2];
  var type_desagre_2 =data[tam_data - 1];
  var number_tabs, type_desagre, fexp, totalFexp, name_desagre;
  var graph_render, graph_title, graph_subtitle, graph_valuesX, text_valuesY, space_valuesY, graph_title, graph_width;
  var name_ind_serie, data_ind_serie;
  var name_indPlus_serie, data_indPlus_serie;
  var name_indMinus_serie, data_indMinus_serie;

  $('#scroll_table').perfectScrollbar('destroy');
  $('#div_desagregaciones').perfectScrollbar('destroy');
  $("#ul_desagregaciones").empty();
  $('#div_desagregaciones').empty()

  if(valor_dim_2 == 0){
      $("#ul_desagregaciones").append('<li><a href="#'+name_desagre_1.replace(/ /g,"_")+'" role="tab" data-toggle="tab">'+name_desagre_1+'</a></li>')
      $("#div_desagregaciones").append('<div class="tab-pane" id="'+name_desagre_1.replace(/ /g,"_")+'"></div>');4
      number_tabs = 1;
      type_desagre = type_desagre_1;
      if(valor_dim_1 == 0){
        graph_title = titulo.split("Sin")[0];
      }else{
        graph_title = titulo.split("por")[0];
      }
      type = [name_desagre_1]
  }else{
      if(valor_dim_1 > valor_dim_2){
          type_desagre_1 =data[tam_data - 1];
          type_desagre_2 =data[tam_data - 2];
      }

      for(i=0; i<type_desagre_1.length; i++){
          $("#ul_desagregaciones").append('<li><a href="#'+type_desagre_1[i].replace(/ /g,"_")+'" role="tab" data-toggle="tab">'+type_desagre_1[i]+'</a></li>')
          $("#div_desagregaciones").append('<div class="tab-pane" id="'+type_desagre_1[i].replace(/ /g,"_")+'"></div>');
          $("#"+type_desagre_1[i].replace(/ /g,"_")).append('<b>'+name_desagre_1+': '+type_desagre_1[i]+' según '+name_desagre_2+'</b>');
      }

      number_tabs = type_desagre_1.length;
      type_desagre = type_desagre_2;
      graph_title = titulo.split("por")[0];
      type = type_desagre_1;
  }

  $("#ul_desagregaciones li:first-child").addClass( "active" );
  $("#div_desagregaciones .tab-pane:first-child").addClass( "active" );
  $('#scroll_table').perfectScrollbar();
  $('#div_desagregaciones').perfectScrollbar();

  for(i=0; i<number_tabs; i++){
    for(j=0; j<type_desagre.length; j++){

      name_ind_serie = 'Indicador';
      data_ind_serie = [];
      totalFexp = 0;
      for(k=0; k<tam_periodos; k++){
        fexp = data[k][2][j+(i*type_desagre.length)];
        if(fexp != 0){
          data_ind_serie.push(parseFloat(data[k][3][j+(i*type_desagre.length)][0].toFixed(4)));
        }
        totalFexp = totalFexp + fexp;
      }

      //Validar que se grafica
      if(totalFexp != 0){

        var typeID = "#"+type[i].replace(/ /g,"_")
        $(typeID).append('<div id="'+type_desagre[j].replace(/ /g,"_")+'_'+(i+1)+'" class="graph text-center" ></div>');

        graph_render = type_desagre[j].replace(/ /g,"_")+'_'+(i+1);
        if(number_tabs > 1){
          graph_subtitle = type[i]+' - '+type_desagre[j];
        }else{
          graph_subtitle = type_desagre[j];
        }


        graph_valuesX = [];
        for(k=0; k<tam_periodos; k++){
          graph_valuesX.push(data[k][0]+' - '+data[k][1]);
        }

        name_indMinus_serie = 'Negativo';
        data_indMinus_serie = [];
        for(k=0; k<tam_periodos; k++){
          fexp = data[k][2][j+(i*type_desagre.length)];
          if(fexp != 0){
            data_indMinus_serie.push(parseFloat(data[k][3][j+(i*type_desagre.length)][2].toFixed(4)));
          }
        }

        name_indPlus_serie = 'Positivo';
        data_indPlus_serie = [];
        for(k=0; k<tam_periodos; k++){
          fexp = data[k][2][j+(i*type_desagre.length)];
          if(fexp != 0){
            data_indPlus_serie.push(parseFloat(data[k][3][j+(i*type_desagre.length)][3].toFixed(4)));
          }
        }

        if(valor_dim_2 == 0){
          name_desagre = name_desagre_1;
        }else{
          name_desagre = name_desagre_1+'_'+name_desagre_2;
        }

        if(data[0][0] == data[tam_periodos-1][0]){
          excel_filename_download = titulo.split(" por ")[0].replace(/ /g,"_")+'-'+titulo.split(" nivel ")[1].replace(/ /g,"_")+'-'+name_desagre.replace(/ /g,"_")+'-'+data[0][0];
          img_filename_download = type[i].replace(/ /g,"_").replace(/,/g,"")+'-'+type_desagre[j].replace(/ /g,"-").replace(/,/g,"")+'-'+data[0][0];
        }else{
          excel_filename_download = titulo.split(" por ")[0].replace(/ /g,"_")+'-'+titulo.split(" nivel ")[1].replace(/ /g,"_")+'-'+name_desagre.replace(/ /g,"_")+'-'+data[0][0]+'_'+data[tam_periodos-1][0];
          img_filename_download = type[i].replace(/ /g,"_").replace(/,/g,"")+'-'+type_desagre[j].replace(/ /g,"-").replace(/,/g,"")+'-'+data[0][0]+'_'+data[tam_periodos-1][0];
        }


         if(tam_periodos <= 12){
          graph_width = 800;
          $(".graph").css("margin-left","8%");
        }else{
          graph_width = tam_periodos*75;
          $(".graph").css("margin-left","0px");
        }

        if(unidad == 'Porcentaje'){
          space_valuesY = 0.1;
          text_valuesY = 'Porcentaje';
        }else if(unidad == 'Años'){
          space_valuesY = 2;
          text_valuesY = 'Promedio de años';
        }else if(unidad == 'Dólares'){
          space_valuesY = 50;
          text_valuesY = 'Dólares';
        }else if(unidad == 'Personas'){
          space_valuesY = 1;
          text_valuesY = 'Número de personas';
        }

        var options = {
          chart: {
              renderTo: graph_render,
              type: 'spline',
              width: graph_width,
          },
          title: {
              text: graph_title,
              x: -20
          },
          subtitle: {
              text: graph_subtitle,
              x: -20
          },
          xAxis: {
            categories: graph_valuesX,
            title: {
                enabled: true,
                text: 'Años',
            },
          },
          yAxis: {
              labels: {
                  formatter: function () {
                    if(unidad == 'Porcentaje'){
                      return Highcharts.numberFormat(this.value*100, 2, ',') + '%';
                    }else if(unidad == 'Años'){
                      return (Highcharts.numberFormat(this.value*1, 0, ','));
                    }else if(unidad == 'Dólares'){
                      return ('$ '+Highcharts.numberFormat(this.value*1, 0, ','));
                    }else if(unidad == 'Personas'){
                      return (Highcharts.numberFormat(this.value*1, 0, ','));
                    }
                  },
              },
              title: {
                  enabled: true,
                  text: text_valuesY,
              },
              min: 0,
              lineWidth: 1,
              tickInterval: space_valuesY,

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
              name: name_ind_serie,
              data: data_ind_serie,
              dataLabels: {
                  enabled: true,
                  color: 'black',
                  formatter: function () {
                    if(unidad == 'Porcentaje'){
                      return Highcharts.numberFormat(this.y*100, 2, ',') + '%';
                    }else if(unidad == 'Años'){
                      return (Highcharts.numberFormat(this.y*1, 2, ','));
                    }else if(unidad == 'Dólares'){
                      return ('$ '+Highcharts.numberFormat(this.y*1, 2, ','));
                    }else if(unidad == 'Personas'){
                      return (Highcharts.numberFormat(this.y*1, 2, ','));
                    }
                  },
                  y: -20
              },
              color: '#6AA4D9',
          }, {
              name: name_indPlus_serie,
              data: data_indPlus_serie,
              dashStyle: 'Dash',
              color: '#6AA4D9',
          },{
              name: name_indMinus_serie,
              data: data_indMinus_serie,
              dashStyle: 'Dash',
              color: '#6AA4D9',
          },],
          exporting: {
              filename: img_filename_download,
          }
        };

        var chart = new Highcharts.Chart(options);
      }
    }
  }
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
