$(document).ready(function() {

    var date = new Date();
    var year = date.getFullYear();
    $('#endDate').attr("value", year+"/01");

    $('#search_by').change(function(){
        if ($('#search_by').val() == 1){
            $('#filtrar_por').text('Filtrar por código');
            $('#txt_filtro_num').attr('type','text');
            $('#txt_filtro_text').attr('type','hidden');
            $('#txt_filtro_text').attr('value',' ');
        }else{
            $('#filtrar_por').text('Filtrar por palabra clave');
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
        console.log(d1);
        $('.datepickerEnd').datepicker('setStartDate',d1);
    });

    $('.datepickerEnd').datepicker({
        language: "es",
        format: "yyyy/mm",
        viewMode:"months",
        minViewMode:"months",
        startDate: "1990/01",
    });

    var tabs = 1;

    $('#options').change(function(){
        var id = $(this).val();
        if(id == 1){
            $('#search').show();
            $('#pais').show();
        }else{
            $('#search').hide();
            $('#pais').hide();
        }
    });

    $('#myTabs li').click(function () {
        var id = $(this).attr('id');
        tabs = id;
        /*$('#options').prop('selectedIndex',0);
        $('#search_by').prop('selectedIndex',0);
        $('#standars').prop('selectedIndex',0);
        $('#period').prop('selectedIndex',0);*/
    });

    //Evento boton
    $('#btn_search').click(function(){
        var option = $('#options option:selected').attr('value');
        var search_by;
        var standar;
        var period;
        var txt_desde = $('#startDate').val();
        var txt_hasta = $('#endDate').val();
        var txt_patron;
        var txt_agregacion;
        var tipo = tabs;
        var bandera;

        if($("#checkbox").is(':checked')) {
            bandera = 1;
        } else {
            bandera = 0;
        }

        if(txt_agregacion < 0){
            //Mostrar mensaje de error
        }else{
            if(option == "1"){
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
                console.log(data);
                $('#tables').show();
                table_A(data, standar);
                table_B(data, option, tipo, standar, checkbox_pais);
            });
        }
    });

    function table_A(data, standar){
        len = data[0][0].length;
        console.log(len);

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
    }


    function table_B(data, option, tipo, standar, checkbox_pais){
        len = data[1][0].length;
        console.log(len);

        $('#tipoTrans').empty();
        $('#table_B').bootstrapTable('destroy');
        $('#table_B thead tr').empty();

        if (tipo == 1){
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
            if (tipo == 1){
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
            }
        }

        if( checkbox_pais == 1 || option == 2 ){
            if (tipo == 1){
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
            }
        }

        $('#table_B').bootstrapTable({ data: data_B });
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
