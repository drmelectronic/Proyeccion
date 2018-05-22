$(document).ready(function(){
})

function escribir(data){
    $('.inactivo').remove();
    $('.activo').addClass('inactivo').removeClass('activo');
    $('.interior').append('<div class="item insertado"><span>'+data+'</span></div>');
    setTimeout(function() {$('.insertado').removeClass('insertado').addClass('activo');}, 0.8);

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