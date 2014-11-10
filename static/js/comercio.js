$(document).ready(function() {

    var date = new Date();
    var year = date.getFullYear();
    $('#endDate').attr("value", year+"/01");

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
    });

    $('.datepickerEnd').datepicker({
        language: "es",
        format: "yyyy/mm",
        viewMode:"months",
        minViewMode:"months",
        startDate: "1990/01",
    });

    // $('.datepicker').datepicker().on(picker_event, function(e){
    //     console.log('as');
    // });

    // $( "#endDate" ).focus(function() {
    //   console.log('as');
    //   fecha = '2011'+'/01';
    //   // fecha = $('#startDate').attr("value");
    //   console.log(fecha);
    //   $('.datepickerEnd').datepicker('setStartDate', fecha);
    // });



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

            txt_patron = $('#txt_patron').val();
            txt_agregacion = $('#txt_agregacion').val();


            $.getJSON('/comercio/', {'tipo': tipo, 'option': option, 'search_by': search_by, 'standar': standar, 'txt_desde': txt_desde,
                                                 'txt_hasta': txt_hasta, 'period': period, 'txt_agregacion': txt_agregacion, 'txt_patron': txt_patron, 'checkbox_pais': checkbox_pais},
            function(data){
                console.log(data);
                console.log(data[1][0][0][0]);
                console.log(data[1][0][0][2]);

                table_A(data);
                table_B(data);
                $('#scroll_table').show();
            });
            //Verificacion de parametros enviados al servidor
            // console.log("TAB_PESTAÑA: "+tab_selected+";"+"OPTION_CODE_PAIS: "+options+";"+"SEARCH_BY: "+search_by+";"+"ESTANDAR: "+standars+";"+"PERIODO: "+"DESDE: "+txt_desde+";"+"HASTA: "+txt_hasta+";"+period+";"+"AGREGACION_VALOR:"+txt_agregacion+";"+"SEPARAR_PAIS: "+checkbox_select);
        }
    });

    function table_A(data){
        len = data[0][0].length;
        
        for(i=0;i<len;i++){
            var datos = '<tr>'+'<td>'+data[0][0][i][0]+'</td>'+'<td>'+data[0][0][i][1]+'</td>'+'</tr>';
            $('#datos_tabla_A').append(datos);
        }
    }

    function table_B(data){
        console.log(data[1]);
        len = data[1][0].length;
        console.log(len);
    }


});