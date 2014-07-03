$(document).ready( function() {
    $('a').click(function(){
        var value_a = $(this).attr('value');
        console.log(value_a);
        //json, por el momento lo dejo asi solo por presentacion...
        $('#datos').children().remove();
        if(value_a == 1){
            var div = '<div class="panel-group" id="accordion">' +
                        '<div class="panel panel-default">' +
                            '<div class="panel-heading">' +
                                '<h4 class="panel-title">' +
                                    '<a data-toggle="collapse" data-parent="#accordion" href="#collapseOne">'+
                                        'PANEL PARA CV 1 - ESTUDIOS'+ '</a>' +
                                '</h4>' +
                            '</div>' +
                            '<div id="collapseOne" class="panel-collapse collapse">' +
                                '<div class="panel-body">' +
                                    'Nihil anim keffiyeh helvetica, craft beer labore wes anderson' +
                                    'cred nesciunt sapiente ea proident. Ad vegan excepteur butcher' +
                                    'vice lomo.' +
                                '</div>' +
                            '</div>' +
                        '</div>' +

                        '<div class="panel panel-default">' +
                            '<div class="panel-heading">' +
                                '<h4 class="panel-title">' +
                                    '<a data-toggle="collapse" data-parent="#accordion" href="#collapseTwo">' +
                                        'PANEL PARA CV 1 - HABILIDADES' + '</a>' +
                                '</h4>' +
                            '</div>' +
                            '<div id="collapseTwo" class="panel-collapse collapse">' +
                                '<div class="panel-body">' +
                                    'Nihil anim keffiyeh helvetica, craft beer labore wes anderson ' +
                                    'cred nesciunt sapiente ea proident. Ad vegan excepteur butcher' +
                                    'vice lomo.' +
                                '</div>'+
                            '</div>' +
                        '</div>' +

                        '<div class="panel panel-default">' +
                            '<div class="panel-heading">' +
                                '<h4 class="panel-title">' +
                                    '<a data-toggle="collapse" data-parent="#accordion" href="#collapseThree">' +
                                        'PANEL PARA CV 1 - EXPERIENCIA LABORAL' + '</a>' +
                                '</h4>' +
                            '</div>' +
                            '<div id="collapseThree" class="panel-collapse collapse">' +
                                '<div class="panel-body">' +
                                    'Nihil anim keffiyeh helvetica, craft beer labore wes anderson' +
                                    'cred nesciunt sapiente ea proident. Ad vegan excepteur butcher' +
                                    'vice lomo.' +
                                '</div>' +
                            '</div>' +
                        '</div>' +

                        '<div class="panel panel-default">' +
                            '<div class="panel-heading">' +
                                '<h4 class="panel-title">' +
                                    '<a data-toggle="collapse" data-parent="#accordion" href="#collapseFour">' +
                                        'PANEL PARA CV 1 - HOBBIES' + '</a>' +
                                '</h4>' +
                            '</div>' +
                            '<div id="collapseFour" class="panel-collapse collapse">' +
                                '<div class="panel-body">' +
                                    'Nihil anim keffiyeh helvetica, craft beer labore wes anderson' +
                                    'cred nesciunt sapiente ea proident. Ad vegan excepteur butcher' +
                                    'vice lomo.' +
                                '</div>' +
                            '</div>' +
                        '</div>' +

                        '<div class="panel panel-default">' +
                            '<div class="panel-heading">' +
                                '<h4 class="panel-title">' +
                                    '<a data-toggle="collapse" data-parent="#accordion" href="#collapseFive">' +
                                        'PANEL PARA CV 1 - REFERENCIAS LABORALES' + '</a>' +
                                '</h4>' +
                            '</div>' +
                            '<div id="collapseFive" class="panel-collapse collapse">' +
                                '<div class="panel-body">' +
                                    'Nihil anim keffiyeh helvetica, craft beer labore wes anderson' +
                                    'cred nesciunt sapiente ea proident. Ad vegan excepteur butcher' +
                                    'vice lomo.' +
                                '</div>' +
                            '</div>' +
                        '</div>' +

                        '<div class="panel panel-default">' +
                            '<div class="panel-heading">' +
                                '<h4 class="panel-title">' +
                                    '<a data-toggle="collapse" data-parent="#accordion" href="#collapseSix">' +
                                        'PANEL PARA CV 1 - REFERENCIAS PERSONALES' + '</a>' +
                                '</h4>' +
                            '</div>' +
                            '<div id="collapseSix" class="panel-collapse collapse">' +
                                '<div class="panel-body">' +
                                    'Nihil anim keffiyeh helvetica, craft beer labore wes anderson' +
                                    'cred nesciunt sapiente ea proident. Ad vegan excepteur butcher' +
                                    'vice lomo.' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>'

            $('#datos').append(div);

        }else if(value_a == 2){
            var div = '<div class="panel-group" id="accordion">' +
                        '<div class="panel panel-default">' +
                            '<div class="panel-heading">' +
                                '<h4 class="panel-title">' +
                                    '<a data-toggle="collapse" data-parent="#accordion" href="#collapseOne">'+
                                        'PANEL PARA CV 2 - ESTUDIOS'+ '</a>' +
                                '</h4>' +
                            '</div>' +
                            '<div id="collapseOne" class="panel-collapse collapse">' +
                                '<div class="panel-body">' +
                                    'Nihil anim keffiyeh helvetica, craft beer labore wes anderson' +
                                    'cred nesciunt sapiente ea proident. Ad vegan excepteur butcher' +
                                    'vice lomo.' +
                                '</div>' +
                            '</div>' +
                        '</div>' +

                        '<div class="panel panel-default">' +
                            '<div class="panel-heading">' +
                                '<h4 class="panel-title">' +
                                    '<a data-toggle="collapse" data-parent="#accordion" href="#collapseTwo">' +
                                        'PANEL PARA CV 2 - HABILIDADES' + '</a>' +
                                '</h4>' +
                            '</div>' +
                            '<div id="collapseTwo" class="panel-collapse collapse">' +
                                '<div class="panel-body">' +
                                    'Nihil anim keffiyeh helvetica, craft beer labore wes anderson ' +
                                    'cred nesciunt sapiente ea proident. Ad vegan excepteur butcher' +
                                    'vice lomo.' +
                                '</div>'+
                            '</div>' +
                        '</div>' +

                        '<div class="panel panel-default">' +
                            '<div class="panel-heading">' +
                                '<h4 class="panel-title">' +
                                    '<a data-toggle="collapse" data-parent="#accordion" href="#collapseThree">' +
                                        'PANEL PARA CV 2 - EXPERIENCIA LABORAL' + '</a>' +
                                '</h4>' +
                            '</div>' +
                            '<div id="collapseThree" class="panel-collapse collapse">' +
                                '<div class="panel-body">' +
                                    'Nihil anim keffiyeh helvetica, craft beer labore wes anderson' +
                                    'cred nesciunt sapiente ea proident. Ad vegan excepteur butcher' +
                                    'vice lomo.' +
                                '</div>' +
                            '</div>' +
                        '</div>' +

                        '<div class="panel panel-default">' +
                            '<div class="panel-heading">' +
                                '<h4 class="panel-title">' +
                                    '<a data-toggle="collapse" data-parent="#accordion" href="#collapseFour">' +
                                        'PANEL PARA CV 2 - HOBBIES' + '</a>' +
                                '</h4>' +
                            '</div>' +
                            '<div id="collapseFour" class="panel-collapse collapse">' +
                                '<div class="panel-body">' +
                                    'Nihil anim keffiyeh helvetica, craft beer labore wes anderson' +
                                    'cred nesciunt sapiente ea proident. Ad vegan excepteur butcher' +
                                    'vice lomo.' +
                                '</div>' +
                            '</div>' +
                        '</div>' +

                        '<div class="panel panel-default">' +
                            '<div class="panel-heading">' +
                                '<h4 class="panel-title">' +
                                    '<a data-toggle="collapse" data-parent="#accordion" href="#collapseFive">' +
                                        'PANEL PARA CV 2 - REFERENCIAS LABORALES' + '</a>' +
                                '</h4>' +
                            '</div>' +
                            '<div id="collapseFive" class="panel-collapse collapse">' +
                                '<div class="panel-body">' +
                                    'Nihil anim keffiyeh helvetica, craft beer labore wes anderson' +
                                    'cred nesciunt sapiente ea proident. Ad vegan excepteur butcher' +
                                    'vice lomo.' +
                                '</div>' +
                            '</div>' +
                        '</div>' +

                        '<div class="panel panel-default">' +
                            '<div class="panel-heading">' +
                                '<h4 class="panel-title">' +
                                    '<a data-toggle="collapse" data-parent="#accordion" href="#collapseSix">' +
                                        'PANEL PARA CV 2 - REFERENCIAS PERSONALES' + '</a>' +
                                '</h4>' +
                            '</div>' +
                            '<div id="collapseSix" class="panel-collapse collapse">' +
                                '<div class="panel-body">' +
                                    'Nihil anim keffiyeh helvetica, craft beer labore wes anderson' +
                                    'cred nesciunt sapiente ea proident. Ad vegan excepteur butcher' +
                                    'vice lomo.' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>'

            $('#datos').append(div);

        }else if(value_a == 3){
            var div = '<div class="panel-group" id="accordion">' +
                        '<div class="panel panel-default">' +
                            '<div class="panel-heading">' +
                                '<h4 class="panel-title">' +
                                    '<a data-toggle="collapse" data-parent="#accordion" href="#collapseOne">'+
                                        'PANEL PARA CV 3 - ESTUDIOS'+ '</a>' +
                                '</h4>' +
                            '</div>' +
                            '<div id="collapseOne" class="panel-collapse collapse">' +
                                '<div class="panel-body">' +
                                    'Nihil anim keffiyeh helvetica, craft beer labore wes anderson' +
                                    'cred nesciunt sapiente ea proident. Ad vegan excepteur butcher' +
                                    'vice lomo.' +
                                '</div>' +
                            '</div>' +
                        '</div>' +

                        '<div class="panel panel-default">' +
                            '<div class="panel-heading">' +
                                '<h4 class="panel-title">' +
                                    '<a data-toggle="collapse" data-parent="#accordion" href="#collapseTwo">' +
                                        'PANEL PARA CV 3 - HABILIDADES' + '</a>' +
                                '</h4>' +
                            '</div>' +
                            '<div id="collapseTwo" class="panel-collapse collapse">' +
                                '<div class="panel-body">' +
                                    'Nihil anim keffiyeh helvetica, craft beer labore wes anderson ' +
                                    'cred nesciunt sapiente ea proident. Ad vegan excepteur butcher' +
                                    'vice lomo.' +
                                '</div>'+
                            '</div>' +
                        '</div>' +

                        '<div class="panel panel-default">' +
                            '<div class="panel-heading">' +
                                '<h4 class="panel-title">' +
                                    '<a data-toggle="collapse" data-parent="#accordion" href="#collapseThree">' +
                                        'PANEL PARA CV 3 - EXPERIENCIA LABORAL' + '</a>' +
                                '</h4>' +
                            '</div>' +
                            '<div id="collapseThree" class="panel-collapse collapse">' +
                                '<div class="panel-body">' +
                                    'Nihil anim keffiyeh helvetica, craft beer labore wes anderson' +
                                    'cred nesciunt sapiente ea proident. Ad vegan excepteur butcher' +
                                    'vice lomo.' +
                                '</div>' +
                            '</div>' +
                        '</div>' +

                        '<div class="panel panel-default">' +
                            '<div class="panel-heading">' +
                                '<h4 class="panel-title">' +
                                    '<a data-toggle="collapse" data-parent="#accordion" href="#collapseFour">' +
                                        'PANEL PARA CV 3 - HOBBIES' + '</a>' +
                                '</h4>' +
                            '</div>' +
                            '<div id="collapseFour" class="panel-collapse collapse">' +
                                '<div class="panel-body">' +
                                    'Nihil anim keffiyeh helvetica, craft beer labore wes anderson' +
                                    'cred nesciunt sapiente ea proident. Ad vegan excepteur butcher' +
                                    'vice lomo.' +
                                '</div>' +
                            '</div>' +
                        '</div>' +

                        '<div class="panel panel-default">' +
                            '<div class="panel-heading">' +
                                '<h4 class="panel-title">' +
                                    '<a data-toggle="collapse" data-parent="#accordion" href="#collapseFive">' +
                                        'PANEL PARA CV 3 - REFERENCIAS LABORALES' + '</a>' +
                                '</h4>' +
                            '</div>' +
                            '<div id="collapseFive" class="panel-collapse collapse">' +
                                '<div class="panel-body">' +
                                    'Nihil anim keffiyeh helvetica, craft beer labore wes anderson' +
                                    'cred nesciunt sapiente ea proident. Ad vegan excepteur butcher' +
                                    'vice lomo.' +
                                '</div>' +
                            '</div>' +
                        '</div>' +

                        '<div class="panel panel-default">' +
                            '<div class="panel-heading">' +
                                '<h4 class="panel-title">' +
                                    '<a data-toggle="collapse" data-parent="#accordion" href="#collapseSix">' +
                                        'PANEL PARA CV 3 - REFERENCIAS PERSONALES' + '</a>' +
                                '</h4>' +
                            '</div>' +
                            '<div id="collapseSix" class="panel-collapse collapse">' +
                                '<div class="panel-body">' +
                                    'Nihil anim keffiyeh helvetica, craft beer labore wes anderson' +
                                    'cred nesciunt sapiente ea proident. Ad vegan excepteur butcher' +
                                    'vice lomo.' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>'

            $('#datos').append(div);

        }else if(value_a == 4){
            var div = '<div class="panel-group" id="accordion">' +
                        '<div class="panel panel-default">' +
                            '<div class="panel-heading">' +
                                '<h4 class="panel-title">' +
                                    '<a data-toggle="collapse" data-parent="#accordion" href="#collapseOne">'+
                                        'PANEL PARA CV 4 - ESTUDIOS'+ '</a>' +
                                '</h4>' +
                            '</div>' +
                            '<div id="collapseOne" class="panel-collapse collapse">' +
                                '<div class="panel-body">' +
                                    'Nihil anim keffiyeh helvetica, craft beer labore wes anderson' +
                                    'cred nesciunt sapiente ea proident. Ad vegan excepteur butcher' +
                                    'vice lomo.' +
                                '</div>' +
                            '</div>' +
                        '</div>' +

                        '<div class="panel panel-default">' +
                            '<div class="panel-heading">' +
                                '<h4 class="panel-title">' +
                                    '<a data-toggle="collapse" data-parent="#accordion" href="#collapseTwo">' +
                                        'PANEL PARA CV 4 - HABILIDADES' + '</a>' +
                                '</h4>' +
                            '</div>' +
                            '<div id="collapseTwo" class="panel-collapse collapse">' +
                                '<div class="panel-body">' +
                                    'Nihil anim keffiyeh helvetica, craft beer labore wes anderson ' +
                                    'cred nesciunt sapiente ea proident. Ad vegan excepteur butcher' +
                                    'vice lomo.' +
                                '</div>'+
                            '</div>' +
                        '</div>' +

                        '<div class="panel panel-default">' +
                            '<div class="panel-heading">' +
                                '<h4 class="panel-title">' +
                                    '<a data-toggle="collapse" data-parent="#accordion" href="#collapseThree">' +
                                        'PANEL PARA CV 4 - EXPERIENCIA LABORAL' + '</a>' +
                                '</h4>' +
                            '</div>' +
                            '<div id="collapseThree" class="panel-collapse collapse">' +
                                '<div class="panel-body">' +
                                    'Nihil anim keffiyeh helvetica, craft beer labore wes anderson' +
                                    'cred nesciunt sapiente ea proident. Ad vegan excepteur butcher' +
                                    'vice lomo.' +
                                '</div>' +
                            '</div>' +
                        '</div>' +

                        '<div class="panel panel-default">' +
                            '<div class="panel-heading">' +
                                '<h4 class="panel-title">' +
                                    '<a data-toggle="collapse" data-parent="#accordion" href="#collapseFour">' +
                                        'PANEL PARA CV 4 - HOBBIES' + '</a>' +
                                '</h4>' +
                            '</div>' +
                            '<div id="collapseFour" class="panel-collapse collapse">' +
                                '<div class="panel-body">' +
                                    'Nihil anim keffiyeh helvetica, craft beer labore wes anderson' +
                                    'cred nesciunt sapiente ea proident. Ad vegan excepteur butcher' +
                                    'vice lomo.' +
                                '</div>' +
                            '</div>' +
                        '</div>' +

                        '<div class="panel panel-default">' +
                            '<div class="panel-heading">' +
                                '<h4 class="panel-title">' +
                                    '<a data-toggle="collapse" data-parent="#accordion" href="#collapseFive">' +
                                        'PANEL PARA CV 4 - REFERENCIAS LABORALES' + '</a>' +
                                '</h4>' +
                            '</div>' +
                            '<div id="collapseFive" class="panel-collapse collapse">' +
                                '<div class="panel-body">' +
                                    'Nihil anim keffiyeh helvetica, craft beer labore wes anderson' +
                                    'cred nesciunt sapiente ea proident. Ad vegan excepteur butcher' +
                                    'vice lomo.' +
                                '</div>' +
                            '</div>' +
                        '</div>' +

                        '<div class="panel panel-default">' +
                            '<div class="panel-heading">' +
                                '<h4 class="panel-title">' +
                                    '<a data-toggle="collapse" data-parent="#accordion" href="#collapseSix">' +
                                        'PANEL PARA CV 4 - REFERENCIAS PERSONALES' + '</a>' +
                                '</h4>' +
                            '</div>' +
                            '<div id="collapseSix" class="panel-collapse collapse">' +
                                '<div class="panel-body">' +
                                    'Nihil anim keffiyeh helvetica, craft beer labore wes anderson' +
                                    'cred nesciunt sapiente ea proident. Ad vegan excepteur butcher' +
                                    'vice lomo.' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>'

            $('#datos').append(div);

        }
    });
});