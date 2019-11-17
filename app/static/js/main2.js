function add_pub(){
    let link_d = document.getElementById("link").value;
    let desc_d = document.getElementById("description").value;
    $.ajax("/add_publication", 
    {
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({link: link_d, description: desc_d})
    })
}

$(document).ready(function() {
    let overlay = $('#overlay'),
    open_modal = $('#add'),
    close = $('.modal_close, #overlay'),
    modal = $('.modal_div');

    open_modal.click( function(event){ 
        event.preventDefault();
        let div = $("#modal2")
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

