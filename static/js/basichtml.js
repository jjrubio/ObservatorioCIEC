$(document).ready(function(){

    $( '#menu' ).multilevelpushmenu({
        containersToPush: [$( '#pushobj' )],
        menuWidth: '20%',
        backText: 'Atrás',
    });

    var $firstIndicator = $( '#menu' ).multilevelpushmenu( 'findmenusbytitle' , 'Toda la población' ).first();
     $( '#menu' ).multilevelpushmenu( 'expand' , $firstIndicator );

    $( window ).resize(function() {
        $( '#menu' ).multilevelpushmenu( 'redraw' );
    });
});