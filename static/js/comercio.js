$(document).ready(function() {

    var tabs = 1;

    $('#options').change(function(){
        var id = $(this).val();
        if(id == 1){
            $('#search_by_label').show();
            $('#search_by').show();
            $('#pais').show();
        }else{
            $('#search_by_label').hide();
            $('#search_by').hide();
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
        var options = $('#options option:selected').attr('value');
        var search_by;
        var standars;
        var period;
        var txt_desde = $('#txt_desde').val();
        var txt_hasta = $('#txt_hasta').val();
        var txt_patron;
        var txt_agregacion;
        var tab_selected = tabs;
        var bandera;
        
        if($("#checkbox").is(':checked')) {  
            bandera = 1;
        } else {  
            bandera = 0;
        }

        if(options == "1"){
            search_by = $('#search_by option:selected').attr('value');
            standars = $('#standars option:selected').attr('value');
            period = $('#period option:selected').attr('value');
            txt_patron = $('#txt_patron').val();
            txt_agregacion = $('#txt_agregacion').val();
            checkbox_select = bandera;
        }else{
            search_by = 0;
            standars = $('#standars option:selected').attr('value');
            period = $('#period option:selected').attr('value');
            txt_patron = $('#txt_patron').val();
            txt_agregacion = $('#txt_agregacion').val();
            checkbox_select = 0;
        }
        //Verificacion de parametros enviados al servdor
        console.log("TAB_PESTAÑA: "+tab_selected+";"+"OPTION_CODE_PAIS: "+options+";"+"SEARCH_BY: "+search_by+";"+"ESTANDAR: "+standars+";"+"PERIODO: "+"DESDE: "+txt_desde+";"+"HASTA: "+txt_hasta+";"+period+";"+"SEPARAR_PAIS: "+checkbox_select);

    });
});