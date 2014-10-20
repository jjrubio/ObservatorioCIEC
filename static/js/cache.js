$("#generar_cache").click(function(){
    $("#generar_cache").hide();
    $("#msg_cache").show();
    $("#spin_cache").show();
    // $(".loading-progress").show();
    // $.getJSON('/numero_consultas/', {'represent': represent, 'yearStart': yearStart, 'trimStart': trimStart, 'yearEnd': yearEnd, 'trimEnd': trimEnd},
    // function(number){
    // timeData = 3500*14;
    // var progress = $(".loading-progress").progressTimer({
    //   timeLimit: timeData,
    //   baseStyle: 'progress-bar-warning',
    //   warningStyle: '',
    //   completeStyle: 'progress-bar-success',
    //   onFinish: function () {}
    // });
    // });
    $.get('/generar_cache/', {},function(data){
      progress.progressTimer('complete');
    });
});
