$(document).ready( function() {
    var limit = 2;
    var count = 0;
    $(":checkbox").click(function(){
        var id = $(this).attr('id');
        var isChecked = $(this).attr('checked');
        console.log("id es antes del getJSON:", id);
        $.getJSON('/list_denied/', {'id_desagregacion': id},
        function(data){
            console.log(data);
            $('#ckb').children().remove();
            $.each(data, function(index, item){
                if(id == item.pk){
                    var tmpHTML = "<div class=\'checkbox\'><label><input type=\'checkbox\' checked id="+item.pk+">"+item.fields.name+"</label></div>";
                    $('#ckb').append(tmpHTML);
                    console.log(item.pk);
                }else{
                    var tmpHTML = "<div class=\'checkbox\'><label><input type=\'checkbox\' id="+item.pk+">"+item.fields.name+"</label></div>";
                    $('#ckb').append(tmpHTML);
                    console.log(item.pk);
                }
            });
            count ++;
            console.log("Valor del contador:",count);
            validCheckbox();
        });
    });
    
    function validCheckbox(){
        $(":checkbox").click(function(){
            if(count < limit){
                var id = $(this).attr('id');
                var isChecked = $(this).attr('checked');
                count++;  
            }else{
                alert("Solo se puede escoger dos desagregaciones.")
                $(this).prop("checked", "");
            }
        });
    }
});