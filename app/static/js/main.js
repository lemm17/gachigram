function change_settings(e, setting){
    if (e.target.value == 'True'){
        e.target.value = 'False';
    } else {
         e.target.value = 'True';
    }

    if (setting == 'ea'){
        $.post('/settingea');
    } else {
        $.post('/settingotc');
    }
};

$(document).ready(function() {
    let overlay = $('#overlay'),
    open_modal = $('.open_modal'),
    close = $('.modal_close, #overlay'),
    modal = $('.modal_div');
    
    open_modal.click( function(event){ 
        event.preventDefault();
        let div = $(this).attr('href');
        overlay.fadeIn(400, 
        function(){
            $(div) 
            .css('display', 'block')
            .animate({opacity: 1, top: '50%'}, 200);
        });
    });
    
    close.click( function(){
        modal 
        .animate({opacity: 0, top: '45%'}, 200, 
        function(){ 
            $(this).css('display', 'none');
            overlay.fadeOut(400); 
        });
    });
});

