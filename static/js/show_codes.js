$('#standars').change(function(){
	var value_init = $(this).val();
	$('#tbody_estandares').children().remove();
	$('#search').remove();
	$('#search').hide();
	$('#table-footer').remove();
	$('#page-rows-form').remove();
	$.getJSON('/filter_code_standar/', {'standar_value' : value_init},
        function(data){
        	$.each(data, function(index, item){
        		$('#tbody_estandares').append('<tr><td>'+item.codigo+'</td><td>'+item.descripcion+'</td></tr>');
        	});
        	$('#label_text').hide();
        	$('#tabla_codigo_estandares').show();
			$('#tabla_codigo_estandares').bdt();
			$('#search').hide();
        });
});