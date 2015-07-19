var tabs_1 = "tab_exp";
var tabs_2 = "tab_codsub";

$(document).ready(function() {
    var date = new Date();
    var year = date.getFullYear();
    var month = date.getMonth();
    var yearMonth = year+"/0"+month;
    var textoFiltro = "";

    $('#endDate').attr("value", yearMonth);

    $('#search_by').change(function(){
        if ($('#search_by').val() == 1){
            textoFiltro = "Filtrar por código";
            $('#filtrar_por').text(textoFiltro);
            $('#txt_filtro_num').attr('type','text');
            $('#txt_filtro_text').attr('type','hidden');
            $('#txt_filtro_text').attr('value','');
        }else{
            textoFiltro = "Palabras clave a buscar en la descripción de la partida/subpartida";
            $('#filtrar_por').text(textoFiltro);
            $('#txt_filtro_num').attr('type','hidden');
            $('#txt_filtro_num').attr('value','');
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
        endDate: yearMonth,
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
        endDate: yearMonth,
    });


    $('#myTabs_1').on('shown.bs.tab', function(e){
        $('#tables').hide();
        $('#datos').show();

        $('#parametros').removeClass('collapse');
        $('#parametros').addClass('collapse in'); 
        $('#resultados').removeClass('collapse in');
        $('#resultados').addClass('collapse');  
    });


    $('#myTabs_2').on('shown.bs.tab', function(e){
        var activeTab =  $(e.target).attr('id');

        if(activeTab == "tab_codsub"){
            $('#search').show();
            $('#pais').show();
            $('#filtrar_por').text(textoFiltro);
            if ($('#search_by').val() == 1){
                textoFiltro = "Filtrar por código";
                $('#filtrar_por').text(textoFiltro);
                $('#txt_filtro_num').attr('type','text');
                $('#txt_filtro_text').attr('type','hidden');
                $('#txt_filtro_text').attr('value','');
            }else{
                textoFiltro = "Palabras clave a buscar en la descripción de la partida/subpartida";
                $('#filtrar_por').text(textoFiltro);
                $('#txt_filtro_num').attr('type','hidden');
                $('#txt_filtro_num').attr('value','');
                $('#txt_filtro_text').attr('value','');
                $('#txt_filtro_text').attr('type','text');
            }
        }

        if(activeTab == "tab_pais"){
            $('#search').hide();
            $('#pais').hide();
            $('#filtrar_por').text('Escriba el nombre del país');
            $('#txt_filtro_num').attr('type','hidden');
            $('#txt_filtro_num').attr('value','');
            $('#txt_filtro_text').attr('value','');
            $('#txt_filtro_text').attr('type','text');
        }

        $('#parametros').removeClass('collapse');
        $('#parametros').addClass('collapse in'); 
        $('#resultados').removeClass('collapse in');
        $('#resultados').addClass('collapse');  

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
        $('#resultados').removeClass('collapse in');
        $('#resultados').addClass('collapse');     
    });


    $('#btn_search').click(function(){
        var search_by;
        var standar;
        var period;
        var desde = $('#startDate').val().split("/");
        if(parseInt(desde[1]) < 10){
            desde_mes = "/0"+(parseInt(desde[1])-1).toString();
        }else{
            desde_mes = "/"+(parseInt(desde[1])-1).toString();
        }
        var txt_desde = desde[0]+desde_mes;
        var txt_hasta = $('#endDate').val();
        var txt_patron;
        var txt_agregacion;
        var bandera;

        $('#parametros').removeClass('collapse in');
        $('#parametros').addClass('collapse'); 
        $('#resultados').removeClass('collapse');
        $('#resultados').addClass('collapse in');  

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
            if(tabs_2 == "tab_codsub"){
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

            if(tabs_1 == "tab_exp"){
                tipo = 1;
            }else{
                tipo = 2;
            }

            if(tabs_2 == "tab_codsub"){
                option = 1;
            }else{
                option = 2;
            }

            $.getJSON('/comercio/', {'tipo': tipo, 'option': option, 'search_by': search_by, 'standar': standar, 'txt_desde': txt_desde,
                                     'txt_hasta': txt_hasta, 'period': period, 'txt_agregacion': txt_agregacion, 'txt_patron': txt_patron, 'checkbox_pais': checkbox_pais},
            function(data){
                table_A(data, standar);
                table_B(data, tabs_1, tabs_2, standar, checkbox_pais);
                
                $('#tables').show();
                $('#graph').show();

                if (option == 1 && checkbox_pais == 0 ){
                    grafico_1(data, standar);
                }

                if (option == 2 || (option == 1 && checkbox_pais == 1 ) ){
                    grafico_2(data, txt_desde, txt_hasta);
                }

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


    function table_B(data, tipo, option, standar, checkbox_pais){
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

        if( option == "tab_codsub" && checkbox_pais == 0){
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

        if( (option == "tab_codsub" && checkbox_pais == 1) || option == "tab_pais" ){
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


function OrdenarPorFOB(a, b){
    return b.fob - a.fob;
}


function grafico_1(data, standar){
    total_productos = data[0][0].length;
    total_datos = data[1][0].length;
    tipo = tabs_1;

    $('#graph').perfectScrollbar('destroy');
    $('#div_graph_comercio').perfectScrollbar('destroy');
    $('#div_graph_comercio').empty();
    $('#ul_graph_comercio').empty();

    var arrayCodigoFOB = new Array();

    for(var i=0; i < total_productos; i++){
        arrayCodigoFOB.push({codigo: data[0][0][i][0], nombre: data[0][0][i][1], fob: 0});
    }


    for (var j=0; j<arrayCodigoFOB.length; j++) {
        for(var k=0; k < total_datos; k++){
            if(data[1][0][k][1] == arrayCodigoFOB[j].codigo){
                arrayCodigoFOB[j].fob = arrayCodigoFOB[j].fob + data[1][0][k][3];
            }
        }
    }
    
    arraySortCodigoFOB = arrayCodigoFOB.sort(OrdenarPorFOB);

    arrayTopFOB = arraySortCodigoFOB.slice(0,5);

    if(total_datos > 0){
        fecha_inicial = data[1][0][0][0];
        fecha_final = data[1][0][total_datos-1][0];

        for(var i=0; i<arrayTopFOB.length; i++){
            productoFechas = [];
            productoFOBs = [];
            productoCIFs = [];

            for(var j=0; j < total_datos; j++){
                subpartida = data[1][0][j][1];
                fecha_sub = data[1][0][j][0];
                fob_sub = data[1][0][j][3];
                if(tipo == "tab_imp"){
                    cif_sub = data[1][0][j][4];
                }

                if(arrayTopFOB[i].codigo == subpartida){
                    productoFechas.push(fecha_sub);
                    productoFOBs.push(fob_sub);
                    if(tipo == "tab_imp"){
                        productoCIFs.push(cif_sub);
                    }
                }
            }

            if(tipo == "tab_exp"){
                num_ope = 1;
            }else{
                num_ope = 2;
            }

            link_ul = "producto"+(i+1);

            $("#ul_graph_comercio").append('<li><a href="#'+link_ul+'" role="tab" data-toggle="tab">' +arrayTopFOB[i].codigo+'</a></li>')
            $("#div_graph_comercio").append('<div class="tab-pane text-center" id="'+link_ul+'"></div>');

            for(var k=0; k<num_ope; k++)
            {
                if(k == 0){
                    div_name = "producto"+(i+1)+"_fob";
                }else{
                    div_name = "producto"+(i+1)+"_cif";
                }
                
                $('#'+link_ul).append('<div id="'+div_name+'" class="graph text-center" ></div>');

                if(num_ope == 1){
                    $("#guia-grafico").text(" (Se muestra los productos con mayor exportación de miles de dólares.)");
                    graph_title = "Exportación miles de dólares FOB de "  + arrayTopFOB[i].nombre; 
                }else{
                    $("#guia-grafico").text(" (Se muestra los productos con mayor importación de miles de dólares.)");
                    if(k == 0){
                        graph_title = "Importación miles de dólares FOB de "  + arrayTopFOB[i].nombre; 
                    }else{
                        graph_title = "Importación miles de dólares CIF de "  + arrayTopFOB[i].nombre;  
                    } 
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
        }

        $("#ul_graph_comercio li:first-child").addClass( "active" );
        $("#div_graph_comercio .tab-pane:first-child").addClass( "active" );
        $('#graph').perfectScrollbar();
        $('#div_graph_comercio').perfectScrollbar();
    }else{
        $("#div_graph_comercio").append('No se encontraron registros');
    }
}


function grafico_2(data, f_inicial, f_final){
    total_productos = data[0][0].length;
    total_datos = data[1][0].length;
    tipo = tabs_1;

    $('#graph').perfectScrollbar('destroy');
    $('#div_graph_comercio').perfectScrollbar('destroy');
    $('#div_graph_comercio').empty();
    $('#ul_graph_comercio').empty();

    if(tipo == "tab_exp"){
        ope = 1;
    }else{
        ope = 2;
    }

    console.log(data);

    // arraySortFOB = data[1][0].sort(ComparatorFOBPais);

    // var arraySortUniqueFOB = [];
    // $.each(arraySortFOB, function(i, el){
    //     if($.inArray(el[1], arraySortUniqueFOB) === -1) arraySortUniqueFOB.push(el[1]);
    // });

    // arrayTopFOB = arraySortUniqueFOB.slice(0,5);



    var paises = [];
    $.each(data[1][0], function(i, el){
        if($.inArray(el[1], paises) === -1) paises.push(el[1]);
    });

    var arrayPaisFOB = new Array();

    for(var i=0; i < paises.length; i++){
        arrayPaisFOB.push({pais: paises[i], fob: 0});
    }

    console.log(arrayPaisFOB);

    for (var j=0; j<arrayPaisFOB.length; j++) {
        for(var k=0; k < total_datos; k++){
            if(data[1][0][k][1] == arrayPaisFOB[j].pais){
                arrayPaisFOB[j].fob = arrayPaisFOB[j].fob + data[1][0][k][4];
            }
        }
    }
    
    arraySortPaisFOB = arrayPaisFOB.sort(OrdenarPorFOB);

    arrayTopFOB = arraySortPaisFOB.slice(0,5);

    console.log(arrayPaisFOB);
    console.log(arrayTopFOB);

    anio1 = parseInt(f_inicial.split("/")[0]);
    mes1 = parseInt(f_inicial.split("/")[1])+1;
    anio2 = parseInt(f_final.split("/")[0]);
    mes2 = parseInt(f_final.split("/")[1]);
    mes1_aux = mes1;

    graph_subtitle = "desde " + anio1+"/"+mes1 + " hasta " + f_final;

    for(var i = 0; i < arrayTopFOB.length; i++){
        
        fechas_grafico = [];
        FOBs_grafico = [];
        CIFs_grafico = [];
        nombre_pais = arrayTopFOB[i].pais.replace(/ /g,"_").replace(/\(/g, '_').replace(/\)/g, '');
        
        $("#ul_graph_comercio").append('<li><a href="#'+nombre_pais+'" role="tab" data-toggle="tab">' +arrayTopFOB[i].pais+'</a></li>')
        $("#div_graph_comercio").append('<div class="tab-pane text-center" id="'+nombre_pais+'"></div>');

        for(var op = 0; op < ope; op++){

            if(ope == 1){
                $("#guia-grafico").text(" (Se muestra los países con mayor exportación de miles de dólares.)");
                div_name = nombre_pais+"_fob";
                graph_title = "Exportación miles de dólares FOB a "  + arrayTopFOB[i].pais; 
            }else{
                $("#guia-grafico").text(" (Se muestra los países con mayor importación de miles de dólares.)");
                if(op == 0){
                    div_name = nombre_pais+"_fob";
                    graph_title = "Importación miles de dólares FOB desde "  + arrayTopFOB[i].pais; 
                }else{
                    div_name = nombre_pais+"_cif";
                    graph_title = "Importación miles de dólares CIF desde "  + arrayTopFOB[i].pais;  
                } 
            }
            
            $('#'+nombre_pais).append('<div id="'+div_name+'" class="graph text-center" ></div>');

            for(var j = anio1; j  <= anio2; j++){
            
                if(j == anio2){
                    mes2_aux = mes2;
                }else{
                    mes2_aux = 12;
                }

                for(var k = mes1_aux; k <= mes2_aux; k++){
                    if(k < 10){
                        fecha_aux = j +"-0"+ k;
                    }else{
                        fecha_aux = j +"-"+ k;
                    }
                    
                    suma_fob = 0.0;
                    suma_cif = 0.0;
                    for(var l=0; l<data[1][0].length; l++){
                        if(fecha_aux == data[1][0][l][0] && arrayTopFOB[i].pais == data[1][0][l][1]){
                            if(op == 0){
                                suma_fob = suma_fob + parseFloat(data[1][0][l][4]);
                            }else{
                                suma_cif = suma_cif + parseFloat(data[1][0][l][5]);
                            }
                        }
                    }
                    if(op == 0){
                        fechas_grafico.push(fecha_aux);
                        FOBs_grafico.push(Math.round (suma_fob*100) / 100);
                    }else{
                        fechas_grafico.push(fecha_aux);
                        CIFs_grafico.push(Math.round (suma_cif*100) / 100);
                    }
                }
                mes1_aux = 1;
            }
            mes1_aux = mes1;

            if (fechas_grafico.length  <= 12) 
            {
                graph_width = 900;
            }else{
                graph_width = fechas_grafico.length * 75;
            }

            graph_valuesX = fechas_grafico;
        
            if(op == 0){
                name_Yaxis = "FOB (Miles de Dólares)";
                graph_valuesY = FOBs_grafico;
            }else{
                name_Yaxis = "CIF (Miles de Dólares)";
                graph_valuesY = CIFs_grafico;
            }

            dibujar_grafico(div_name, graph_title, graph_subtitle, graph_width, graph_valuesX, name_Yaxis, graph_valuesY);
        }
    }

    $("#ul_graph_comercio li:first-child").addClass( "active" );
    $("#div_graph_comercio .tab-pane:first-child").addClass( "active" );
    $('#graph').perfectScrollbar();
    $('#div_graph_comercio').perfectScrollbar();
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