$(document).ready(function() {
    let overlay = $('.logo__exit'),
    open_modal = $('.publication'),
    close = $('.logo__exit'),
    div = $('#openPhoto');
    
    open_modal.click( function(event){
        $(".open-photo__photo").attr("src", $(event.target).attr("src"));
        overlay.fadeIn(400, 
        function(){
            $(div) 
            .css('display', 'block')
            .animate({opacity: 1}, 200);
        });
    });
    
    close.click( function(){
        div 
        .animate({opacity: 0}, 200, 
        function(){
            $(this).css('display', 'none');
            overlay.fadeOut(400);
        });
    });
});