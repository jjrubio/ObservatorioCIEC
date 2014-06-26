$(document).ready( function() {
    var limit = 2;
    var count = 0;
    
    filter();

    function loadCheckbox(){
        $.getJSON('/list/',
        function(data){
            $('#ckb').children().remove();
            $.each(data, function(index, item){
                var tmpHTML = "<div class=\'checkbox\'><label><input type=\'checkbox\' id="+item.pk+">"+item.fields.name+"</label></div>";
                $('#ckb').append(tmpHTML);
            });
            filter();
        });
    }

    function filter(){
        $(":checkbox").click(function(){
            var id_1 = $(this).attr('id');
            var isChecked_1 = $(this).attr('checked');
            $.getJSON('/list_denied/', {'id_desagregacion': id_1},
            function(data){
                $('#ckb').children().remove();
                $.each(data, function(index, item){
                    if(id_1 == item.pk){
                        var tmpHTML = "<div class=\'checkbox\'><label><input type=\'checkbox\' checked id="+item.pk+">"+item.fields.name+"</label></div>";
                        $('#ckb').append(tmpHTML);
                    }else{
                        var tmpHTML = "<div class=\'checkbox\'><label><input type=\'checkbox\' id="+item.pk+">"+item.fields.name+"</label></div>";
                        $('#ckb').append(tmpHTML);
                    }
                });
                //count ++;
                console.log("Id del primer checkbox: ", id_1);
                validCheckbox(id_1);
            });
        });
    }

    function validCheckbox(id_1){
        $('input:checkbox').change(function(){
            var Validos = [];
            $('input:checkbox').each(function(){
                if($(this).is(':checked')){
                    var id_dentro = $(this).attr('id');
                    console.log("Clic DENTRO: ", id_dentro);
                    count++;
                    console.log("valor del count es: ", count);
                    Validos.push($(this).attr('id'));
                }else{
                    var id_afuera = $(this).attr('id');
                    console.log("Clic afuera: ", id_afuera);
                }
            });
            console.log("Validos: ", Validos);
            if(count>limit){
                console.log("Stop");
                $(this).prop('checked', false);
                alert("Ha escogido mas de dos desagregaciones.");
            }else{
                console.log("Continue");
                count = 0;
            }
        });
    }
});