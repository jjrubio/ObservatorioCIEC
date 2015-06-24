var tabs_1 = "tab_exp";
var tabs_2 = "tab_codsub";

$(document).ready(function() {
    var date = new Date();
    var year = date.getFullYear();
    var textoFiltro = "";

    $('#endDate').attr("value", year+"/01");

    $('#search_by').change(function(){
        if ($('#search_by').val() == 1){
            textoFiltro = "Filtrar por código";
            $('#filtrar_por').text(textoFiltro);
            $('#txt_filtro_num').attr('type','text');
            $('#txt_filtro_text').attr('type','hidden');
            $('#txt_filtro_text').attr('value',' ');
        }else{
            textoFiltro = "Palabras clave a buscar en la descripción de la partida/subpartida";
            $('#filtrar_por').text(textoFiltro);
            $('#txt_filtro_num').attr('type','hidden');
            $('#txt_filtro_num').attr('value',' ');
            $('#txt_filtro_text').attr('type','text');
        }
    });


    $.fn.datepicker.dates['es'] = {
        days: ["Domingo", "Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"],
        daysShort: ["Dom","Lun","Mar","Mié","Juv","Vie","Sáb","Dom"],
        daysMin: ["Do","Lu","Ma","Mi","Ju","Vi","Sá","Do"],
        months: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
        monthsShort: ['Ene','Feb','Mar','Abr', 'May','Jun','Jul','Ago','Sep', 'Oct','Nov','Dic'],
        today: "Hoy",
        clear: "Limpiar"
    };


    $('.datepickerStart').datepicker({
        language: "es",
        format: "yyyy/mm",
        viewMode:"months",
        minViewMode:"months",
        startDate: "1990/01",
    }).on('changeDate',function(ev){
        var d1 = $('#startDate').val();
        $('.datepickerEnd').datepicker('setStartDate',d1);
    });


    $('.datepickerEnd').datepicker({
        language: "es",
        format: "yyyy/mm",
        viewMode:"months",
        minViewMode:"months",
        startDate: "1990/01",
    });


    $('#myTabs_1').on('shown.bs.tab', function(e){
        $('#tables').hide();
        $('#datos').show();
    });


    $('#myTabs_2').on('shown.bs.tab', function(e){
        var activeTab =  $(e.target).attr('id');

        if(activeTab == "tab_codsub"){
            $('#search').show();
            $('#pais').show();
            $('#filtrar_por').text(textoFiltro);
        }

        if(activeTab == "tab_pais"){
            $('#search').hide();
            $('#pais').hide();
            $('#filtrar_por').text('Escriba el nombre del país');
        }

        $('#tables').hide();
        $('#graph').hide();
        $('#datos').show();
    });


    $('#myTabs_1 li a').click(function () {
        var id = $(this).attr('id');
        tabs_1 = id;
    });


    $('#myTabs_2 li a').click(function () {
        var id = $(this).attr('id');
        tabs_2 = id;
    });


    $('#a-parametros').click( function(){
        $('#parametros').removeClass('collapse');
        $('#parametros').addClass('collapse in'); 
        $('#parametros').removeClass('collapse in');
        $('#parametros').addClass('collapse');    
    });


    $('#btn_search').click(function(){
        var tipo = tabs_1;
        var option = tabs_2;
        var search_by;
        var standar;
        var period;
        var txt_desde = $('#startDate').val();
        var txt_hasta = $('#endDate').val();
        var txt_patron;
        var txt_agregacion;
        var bandera;

        $('#resultados').removeClass('collapse');
        $('#resultados').addClass('collapse in'); 
        $('#parametros').removeClass('collapse in');
        $('#parametros').addClass('collapse');    

        $("#loading").css("display","inline");
        $("#tables").hide();
        $('#graph').hide();

        if($("#checkbox").is(':checked')) {
            bandera = 1;
        } else {
            bandera = 0;
        }

        if(txt_agregacion < 0){
                //Mostrar mensaje de error
        }else{
            if(option == "tab_codsub"){
                search_by = $('#search_by option:selected').attr('value');
                standar = $('#standars option:selected').attr('value');
                period = $('#period option:selected').attr('value');
                checkbox_pais = bandera;
            }else{
                search_by = 0;
                standar = $('#standars option:selected').attr('value');
                period = $('#period option:selected').attr('value');
                checkbox_pais = 0;
            }

            if ($('#search_by').val() == 1){
                txt_patron = $('#txt_filtro_num').val();
            }else{
                txt_patron = $('#txt_filtro_text').val();
            }

            txt_agregacion = $('#txt_agregacion').val();

            $.getJSON('/comercio/', {'tipo': tipo, 'option': option, 'search_by': search_by, 'standar': standar, 'txt_desde': txt_desde,
                                     'txt_hasta': txt_hasta, 'period': period, 'txt_agregacion': txt_agregacion, 'txt_patron': txt_patron, 'checkbox_pais': checkbox_pais},
            function(data){
                table_A(data, standar);
                table_B(data, option, tipo, standar, checkbox_pais);
                
                $('#tables').show();
                $('#graph').show();

                grafico(data);
                $("#loading").css("display","none");
            });
        }
    });


    function table_A(data, standar){
        len = data[0][0].length;

        $('#pie_de_tabla_nom').empty();
        $('#pie_de_tabla_nom').text('Mostrando un total de '+ len +' filas.');

        $('#table_A').bootstrapTable('destroy');
        $('#code_A').empty();

        if (standar == 1){
            $('#code_A').text("Subpartida");
        }else{
            $('#code_A').text("Código");
        }

        var data_A = [];
        var valores = {}

        for(var i = 0; i <len; i++)
        {
            valores = {}
            valores["codigo"] = data[0][0][i][0];
            valores["descripcion"] = data[0][0][i][1];
            data_A.push(valores);
        }

        $('#table_A').bootstrapTable({ data: data_A });

        $("#btnExportNomen").click(function(e){
            var uri = $('#table_A').battatech_excelexport({
                containerid: "table_A"
                ,returnUri: true
                ,datatype: "table"
                ,worksheetName: "Observatorio-Comercio Exterior"
            });
            $(this).attr('download', 'detalle_de_nomenclatura.xls').attr('href', uri).attr('target', '_blank');
        });
    }


    function table_B(data, option, tipo, standar, checkbox_pais){
        len = data[1][0].length;

        $('#pie_de_tabla_ex_im').empty();
        $('#pie_de_tabla_ex_im').text('Mostrando un total de '+ len +' filas.');

        $('#tipoTrans').empty();
        $('#table_B').bootstrapTable('destroy');
        $('#table_B thead tr').empty();

        if (tipo == "tab_exp"){
            $('#tipoTrans').text('DATOS DE EXPORTACIONES');
        }else{
            $('#tipoTrans').text('DATOS DE IMPORTACIONES');
        }

        if (standar == 1){
            clase = 'Subpartida';
        }else{
            clase = 'Código';
        }

        if( checkbox_pais == 0 ){
            if (tipo == "tab_exp"){
                $('#table_B thead tr').append('<th id="fecha_B" data-field="fecha" data-align="center" data-sortable="true">Fecha</th>'+
                                             '<th id="code_B" data-field="codigo" data-align="center" data-sortable="true">'+clase+'</th>'+
                                             '<th id="peso_B" data-field="peso" data-align="center" data-sortable="true">Peso (Miles de Kilos)</th>'+
                                             '<th id="fob_B" data-field="fob" data-align="center" data-sortable="true">FOB (Miles de Dólares)</th>');
                var data_B = [];
                var valores = {}
                for(var i = 0; i <len; i++)
                {
                    valores = {}
                    valores["fecha"] = data[1][0][i][0];
                    valores["codigo"] = data[1][0][i][1];
                    valores["peso"] = data[1][0][i][2];
                    valores["fob"] = data[1][0][i][3];
                    data_B.push(valores);
                }
                trans = "exportaciones";
            }else{
                $('#table_B thead tr').append('<th id="fecha_B" data-field="fecha" data-align="center" data-sortable="true">Fecha</th>'+
                                             '<th id="code_B" data-field="codigo" data-align="center" data-sortable="true">'+clase+'</th>'+
                                             '<th id="peso_B" data-field="peso" data-align="center" data-sortable="true">Peso (Miles de Kilos)</th>'+
                                             '<th id="fob_B" data-field="fob" data-align="center" data-sortable="true">FOB (Miles de Dólares)</th>'+
                                             '<th id="cif_B" data-field="cif" data-align="center" data-sortable="true">CIF (Miles de Dólares)</th>');
                var data_B = [];
                var valores = {}
                for(var i = 0; i <len; i++)
                {
                        valores = {}
                        valores["fecha"] = data[1][0][i][0];
                        valores["codigo"] = data[1][0][i][1];
                        valores["peso"] = data[1][0][i][2];
                        valores["fob"] = data[1][0][i][3];
                        valores["cif"] = data[1][0][i][4];
                        data_B.push(valores);
                }
                trans = "importaciones";
            }
        }

        if( checkbox_pais == 1 || option == "tab_pais" ){
            if (tipo == "tab_exp"){
                $('#table_B thead tr').append('<th id="fecha_B" data-field="fecha" data-align="center" data-sortable="true">Fecha</th>'+
                                             '<th id="pais_B" data-field="pais" data-align="center" data-sortable="true">País</th>'+
                                             '<th id="code_B" data-field="codigo" data-align="center" data-sortable="true">'+clase+'</th>'+
                                             '<th id="peso_B" data-field="peso" data-align="center" data-sortable="true">Peso (Miles de Kilos)</th>'+
                                             '<th id="fob_B" data-field="fob" data-align="center" data-sortable="true">FOB (Miles de Dólares)</th>');
                var data_B = [];
                var valores = {}
                for(var i = 0; i <len; i++)
                {
                        valores = {}
                        valores["fecha"] = data[1][0][i][0];
                        valores["pais"] = data[1][0][i][1];
                        valores["codigo"] = data[1][0][i][2];
                        valores["peso"] = data[1][0][i][3];
                        valores["fob"] = data[1][0][i][4];
                        data_B.push(valores);
                }
                trans = "exportaciones";
            }else{
                $('#table_B thead tr').append('<th id="fecha_B" data-field="fecha" data-align="center" data-sortable="true">Fecha</th>'+
                                             '<th id="pais_B" data-field="pais" data-align="center" data-sortable="true">País</th>'+
                                             '<th id="code_B" data-field="codigo" data-align="center" data-sortable="true">'+clase+'</th>'+
                                             '<th id="peso_B" data-field="peso" data-align="center" data-sortable="true">Peso (Miles de Kilos)</th>'+
                                             '<th id="fob_B" data-field="fob" data-align="center" data-sortable="true">FOB (Miles de Dólares)</th>'+
                                             '<th id="cif_B" data-field="cif" data-align="center" data-sortable="true">CIF (Miles de Dólares)</th>');
                var data_B = [];
                var valores = {}
                for(var i = 0; i <len; i++)
                {
                        valores = {}
                        valores["fecha"] = data[1][0][i][0];
                        valores["pais"] = data[1][0][i][1];
                        valores["codigo"] = data[1][0][i][2];
                        valores["peso"] = data[1][0][i][3];
                        valores["fob"] = data[1][0][i][4];
                        valores["cif"] = data[1][0][i][5];
                        data_B.push(valores);
                }
                trans = "importaciones";
            }
        }

        $('#table_B').bootstrapTable({ data: data_B });

        $("#btnExportTrans").click(function(e){
            var uri = $('#table_B').battatech_excelexport({
                containerid: "table_B"
                ,returnUri: true
                ,datatype: "table"
                ,worksheetName: "Observatorio-Comerio Exterior"
            });
            $(this).attr('download', 'datos_de_'+trans+'.xls').attr('href', uri).attr('target', '_blank');
        });

        $('.fixed-table-toolbar:last #totales_trans').empty();

        if(tipo == "tab_exp"){
            $('.fixed-table-toolbar:last').append("<div id='totales_trans'><b>Peso total:</b> "+data[2][0].toFixed(2)+" miles de kilos <br>" +
                                                "<b>Total FOB:</b> "+data[2][1].toFixed(2)+" miles de dólares <br></div>");
            $('.fixed-table-toolbar:last #totales_trans').css("padding-top", "12px");
        }else{
            $('.fixed-table-toolbar:last').append("<div id='totales_trans'><b>Peso total:</b> "+data[2][0].toFixed(2)+" miles de kilos <br>" +
                                                "<div class='col-lg-4'><b>Total FOB:</b> "+data[2][1].toFixed(2)+" miles de dólares <br></div> " +
                                                "<div class='col-lg-4'><b>Total CIF:</b> "+data[2][2].toFixed(2)+" miles de dólares</div></div>");
            $('.fixed-table-toolbar:last #totales_trans').css("padding-top", "12px");
            $('.fixed-table-toolbar:last #totales_trans div').css("padding-left", "0px");
        }
    }
});


jQuery.fn.ForceNumericOnly =
function()
{
    return this.each(function()
    {
        $(this).keydown(function(e)
        {
            var key = e.charCode || e.keyCode || 0;
            // allow backspace, tab, delete, enter, arrows, numbers and keypad numbers ONLY
            // home, end, period, and numpad decimal
            return (
                key == 8 ||
                key == 9 ||
                key == 13 ||
                (key >= 48 && key <= 57));
        });
    });
};


$("#txt_filtro_num").ForceNumericOnly();


jQuery.fn.ForceTextOnly =
function()
{
    return this.each(function()
    {
        $(this).keydown(function(e)
        {
            var key = e.charCode || e.keyCode || 0;
            // allow backspace, tab, delete, enter, arrows, numbers and keypad numbers ONLY
            // home, end, period, and numpad decimal
            return (
                key == 8 ||
                key == 9 ||
                key == 13 ||
                (key >= 65 && key <= 90));
        });
    });
};


$("#txt_filtro_text").ForceTextOnly();


function grafico(data){
    total_productos = data[0][0].length;
    total_datos = data[1][0].length;
    tipo = tabs_1;

    $('#graph').perfectScrollbar('destroy');
    $('#div_graph_comercio').perfectScrollbar('destroy');
    $('#div_graph_comercio').empty();
    $('#ul_graph_comercio').empty();

    if(total_datos > 0){
        fecha_inicial = data[1][0][0][0];
        fecha_final = data[1][0][total_datos-1][0];

        num_productos = 0;
        num_productos_con_datos = 0;

        do{
            for(var i=0; i < total_productos; i++)
            {
                producto = data[0][0][i][0];
                productoFechas = [];
                productoFOBs = [];
                if(tipo == "tab_imp"){
                    productoCIFs = [];
                }

                for(var j=0; j < total_datos; j++){
                    subpartida = data[1][0][j][1];
                    fecha_sub = data[1][0][j][0];
                    fob_sub = data[1][0][j][3];
                    if(tipo == "tab_imp"){
                        cif_sub = data[1][0][j][4];
                    }

                    if(producto == (subpartida.substring(0, subpartida.length - 2)))
                    {
                        productoFechas.push(fecha_sub);
                        productoFOBs.push(fob_sub);
                        if(tipo == "tab_imp"){
                            productoCIFs.push(cif_sub);
                        }
                    }
                }

                if(productoFechas.length > 0)
                {
                    num_productos_con_datos++;

                    if(tipo == "tab_exp"){
                        num_ope = 1;
                    }else{
                        num_ope = 2;
                    }

                    link_ul = "producto"+(num_productos_con_datos);

                    $("#ul_graph_comercio").append('<li><a href="#'+link_ul+'" role="tab" data-toggle="tab"> Producto #' +num_productos_con_datos+'</a></li>')
                    $("#div_graph_comercio").append('<div class="tab-pane text-center" id="'+link_ul+'"></div>');

                    for(var k=0; k<num_ope; k++)
                    {
                        if(k == 0){
                            div_name = "producto"+(num_productos_con_datos)+"_fob";
                        }else{
                            div_name = "producto"+(num_productos_con_datos)+"_cif";
                        }
                        
                        $('#'+link_ul).append('<div id="'+div_name+'" class="graph text-center" ></div>');

                        if(num_ope == 1){
                            graph_title = "Exportación de "  + data[0][0][i][1];  
                        }else{
                            graph_title = "Importación de "  + data[0][0][i][1];  
                        }
                        
                        graph_subtitle = "desde " + fecha_inicial + " hasta " + fecha_final;

                        if (productoFechas.length  <= 12) 
                        {
                            graph_width = 900;
                        }else{
                            graph_width = productoFechas.length * 75;
                        }

                        graph_valuesX = productoFechas;
                        
                        if(k == 0){
                            name_Yaxis = "FOB (Miles de Dólares)";
                            graph_valuesY = productoFOBs;
                        }else{
                            name_Yaxis = "CIF (Miles de Dólares)";
                            graph_valuesY = productoCIFs;
                        }

                        dibujar_grafico(div_name, graph_title, graph_subtitle, graph_width, graph_valuesX, name_Yaxis, graph_valuesY);
                    }
                    
                    if (num_productos_con_datos == 8){
                        break;
                    }
                }
            }

            $("#ul_graph_comercio li:first-child").addClass( "active" );
            $("#div_graph_comercio .tab-pane:first-child").addClass( "active" );
            $('#graph').perfectScrollbar();
            $('#div_graph_comercio').perfectScrollbar();

        }while(false);
    }else{
        $("#div_graph_comercio").append('No se encontraron registros');
    }
}


function dibujar_grafico(div, title, subtitle, width, valuesX, name_Yaxis, valuesY){
    var options = {
        chart: {
            renderTo: div,
            type: 'spline',
            width: width,
            animation: false,
        },
        title: {
            text: title,
            x: -20
        },
        subtitle: {
            text: subtitle,
            x: -20
        },
        xAxis: {
            categories: valuesX,
            title: {
                enabled: true,
                text: 'Fecha',
            },
        },
        yAxis: {
            title: {
                enabled: true,
                text: name_Yaxis,
            },
            min: 0,
            lineWidth: 1,
            tickInterval: 1,

        },
        legend: {
            enabled: false
        },
        tooltip: {
            animation: false,
            enabled: false
        },
        plotOptions: {
            series: {
                shadow: false,
                animation: false,
                marker: {
                        enabled: false
                },
            },
        },
        series: [{
            name: "Producción",
            data: valuesY,
            dataLabels: {
                enabled: true,
                color: 'black',
                y: -20
            },
            color: '#6AA4D9',
        },],
    };

    var chart = new Highcharts.Chart(options);
}