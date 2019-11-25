$(document).ready(function() {
    let overlay = $('.logo__exit'),
    open_modal = $('.publication'),
    close = $('.logo__exit'),
    div = $('#openPhoto');
    
    open_modal.click( function(event){
        $(".open-photo__photo").attr("src", $(event.target).attr("src"));
        $(".open-photo__photo").attr("id", $(event.target).attr("id"));
        let pub_id = $(event.target).attr("id").replace("pub", "");
        let xhr = new XMLHttpRequest();
        xhr.open('GET', '/has_like'+pub_id, true);
        xhr.send();
        overlay.fadeIn(400, 
        function(){
            div 
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

$(".logo__like").click(() =>{
    let pub_id = $(".open-photo__photo").attr("id").replace("pub","");
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/likes'+pub_id, true);
    xhr.send("");
})

$(".logo__dislike").click(() =>{
    let pub_id = $(".open-photo__photo").attr("id").replace("pub","");
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/dislikes'+pub_id, true);
    xhr.send("");
})