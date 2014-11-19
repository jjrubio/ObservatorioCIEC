$("#generar_cache").click(function(){
    $("#generar_cache").hide();
    $("#msg_cache").show();
    $("#spin_cache").show();

    $('#msg_cache').text('La generación de cache está en proceso. Espere por favor ....');

    $.get('/generar_cache/', {},function(data){
      // progress.progressTimer('complete');
      $('#msg_cache').empty();
      $('#msg_cache').text('La generación de cache ha culminado. Gracias por su paciencia!');
      $('#spin_cache').hide();
    });
});
