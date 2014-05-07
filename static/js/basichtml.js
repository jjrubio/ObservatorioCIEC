$(document).ready(function(){

    $( '#menu' ).multilevelpushmenu({
        containersToPush: [$( '#pushobj' )],
        menuWidth: '20%',
        backText: 'Atrás',

    });

    $( window ).resize(function() {
        $( '#menu' ).multilevelpushmenu( 'redraw' );
    });
});