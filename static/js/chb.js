$(document).ready( function() {
    init();

    function init(){
        $(":checkbox").click(function(){
            var validos_selec = [];

            $('input:checkbox').each(function(){
                if($(this).is(':checked')){
                    validos_selec.push($(this).attr('id'));
                }
            });

            if(validos_selec.length == 0){
                loadCheckbox();
            }
            else if(validos_selec.length == 1){
                filter(validos_selec[0]);
            }
            else if(validos_selec.length > 2){
                $(this).prop('checked',false);
            }
        });
    }

    
    function loadCheckbox(){
        $.getJSON('/list/',function(data){
            $('#ckb').children().remove();
            $.each(data, function(index, item){
                var tmpHTML = "<div class=\'checkbox\'><label><input type=\'checkbox\' id="+item.pk+">"+item.fields.name+"</label></div>";
                $('#ckb').append(tmpHTML);
            });
            filter(0);
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
});