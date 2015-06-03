$(document).ready( function() {
    var test = 0;
    var formato_categorias = ['2003','2004','2005'];
    var formato_series = [{name: 'Indicador 1',data: [49.9, 71.5, 106.4]},
                                {name: 'Indicador 2',data: [43.9, 31.5, 60.4]},
                                {name: 'Indicador 3',data: [29.9, 17.5, 16.4]}];
    
    $.getJSON('/test/', {'test': test},
        function(data){
            $('#container').highcharts({
            chart: {
                type: 'column'
            },
            title: {
                text: 'Titulo de Gráfico'
            },
            subtitle: {
                text: 'Subtitulo'
            },
            xAxis:{
                categories:data
            },
            series: formato_series,
            yAxis: {
                min: 0,
                title: {
                    text: 'Título Axis Y'
                }
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            }
        });
    });
});
