$(document).ready(function(){
})

function escribir(data){
    $('.interior').append('<div class="item insertado"><span>'+data+'</span></div>');
    $('.activo').addClass('inactivo').removeClass('activo');
    setTimeout(function() {
        $('.insertado').removeClass('insertado').addClass('activo');
        $('.inactivo').remove();
    }, 800);

}

function masgrande(){
    size = $('body').css('font-size');
    size = parseInt(size) + 1;
    $('body').css('font-size', size)
}

function menosgrande(){
    size = $('body').css('font-size');
    size = parseInt(size) - 1;
    $('body').css('font-size', size)
}

function fondo(archivo){
    $('body').css('background-image', 'url(../images/fondos/'+archivo+')');
    setTimeout(function() {
            $('header').css('opacity', 0);
        },
        2000
    );
    setTimeout(function() {
            anterior = $('body').css('background-image');
            $('header').css('background-image', anterior);
        },
        3500
    );
    setTimeout(function() {
            $('header').css('opacity', 100);
        },
        6000
    );
}