

$(document).ready( function() {

    $('.indicator').click( function(){

        $.get('/detalle-indicador/'+$(this).attr('id')+'/', function(data) {

            $(".breadcrumb li:first-child i").attr('class', 'fa '+data.category_icon);
            $(".breadcrumb li:first-child span").text(" "+data.ind_category);

            $(".breadcrumb li:nth-last-child(2) i").attr('class', 'fa '+data.subcategory_icon);
            $(".breadcrumb li:nth-last-child(2) span").text(" "+data.ind_subcategory);

            $(".breadcrumb li:last-child i").attr('class', 'fa '+data.ind_icon);
            $(".breadcrumb li:last-child span").text(" "+data.ind_name);

            $(".panel-body p span").text(data.ind_definition);

            $(".panel-body div img").attr('src',MEDIA_URL +data.ind_formula);

            $(".panel-footer span").text(data.ind_unit);

        });

    });

});