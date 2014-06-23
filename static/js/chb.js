$(document).ready( function() {
    var limit = 2;
    var count = 0;
    
    filter();

    function loadCheckbox(){
        var id_3 = 0;
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
                //console.log(data);
                $('#ckb').children().remove();
                $.each(data, function(index, item){
                    if(id_1 == item.pk){
                        var tmpHTML = "<div class=\'checkbox\'><label><input type=\'checkbox\' checked id="+item.pk+">"+item.fields.name+"</label></div>";
                        $('#ckb').append(tmpHTML);
                        //console.log(item.pk);
                    }else{
                        var tmpHTML = "<div class=\'checkbox\'><label><input type=\'checkbox\' id="+item.pk+">"+item.fields.name+"</label></div>";
                        $('#ckb').append(tmpHTML);
                        //console.log(item.pk);
                    }
                });
                count ++;
                console.log("Id del primer checkbox: ", id_1);
                validCheckbox(id_1);
            });
        });
    }

    function validCheckbox(id_1){
        $(":checkbox").click(function(){
            var id_2 = $(this).attr('id');
            var isChecked_2 = $(this).attr('checked');
            if(id_2 == id_1){
                count--;
                loadCheckbox();
            }
            else{
                count++;
            }
            if(id_2 == id_2){
                count--;
            }else{
                count++;
            }
            if(count < limit){
                count++;
                console.log("Id del segundo checkbox: ", id_2);
            }else{
                alert("Solo se puede escoger dos desagregaciones.")
                $(this).prop("checked", false);
            }
            
        });
    }
});