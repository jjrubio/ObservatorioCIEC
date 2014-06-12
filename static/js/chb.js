$(document).ready( function() {
    var limit = 2;
    var count = 0;
    $('input').on('change', filtro);
    function filtro(){
        var id_desagregacion = $(this).val();
        if (count < limit){
            $('#ckb').children().remove();
            $.getJSON('/list_denied/', {'id_desagregacion': id_desagregacion},
                function(data){
                    console.log(data);
                    $.each(data, function(index, item){
                        //console.log(id_desagregacion);
                        if(id_desagregacion == item.pk){
                            //console.log("Pinta el checkbox");
                            var div='<div class="checkbox">'+
                                '<label>'+
                                    '<input type="checkbox" value=\''+item.pk+'\' checked>'+item.fields.name+
                                '</label>'+
                            '</div>'
                            $('#ckb').append(div);
                            console.log(item.pk);
                        }else{
                            //console.log("Muestra los demas");
                            var div='<div class="checkbox">'+
                                '<label>'+
                                    '<input type="checkbox" value=\''+item.pk+'\'>'+item.fields.name+
                                '</label>'+
                            '</div>'
                            $('#ckb').append(div);
                            console.log(item.pk);
                        }
                    });
                });
            count++;
        }else{
            alert("Solo puede escoger dos desagregaciones.");
            $(this).prop("checked", "");
        }
    }
});