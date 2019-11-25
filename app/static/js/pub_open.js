$(document).ready(function() {
    let overlay = $('.logo__exit'),
    open_modal = $('.publication'),
    close = $('.logo__exit'),
    div = $('#openPhoto');
    
    open_modal.click( function(event){
        $(".open-photo__photo").attr("src", $(event.target).attr("src"));
        $(".open-photo__photo").attr("id", $(event.target).attr("id"));
        let pub_id = $(event.target).attr("id").replace("pub", "");
        let promise = fetch('/pub_data'+pub_id)
        .then(promise => promise.json())
        .then((commit) => {
            let src = $(".logo__like").attr("src").replace("like1","like")
            if(commit["like"])
                $(".logo__like").attr("src", src.replace("like","like1"))
            else
                $(".logo__like").attr("src", src)
            src = $(".logo__dislike").attr("src").replace("dislike1","dislike") 
            if(commit["dislike"])
                $(".logo__dislike").attr("src", src.replace("dislike", "dislike1"))
            else 
                $(".logo__dislike").attr("src", src)
            $(".likes__count").text(commit["like_count"])
            $(".dislikes__count").text(commit["dislike_count"])

        })
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
    xhr.send();
    let src = $(event.target).attr("src")
    if(src.indexOf("like1") > 0){
        $(event.target).attr("src", src.replace("like1", "like"))
        $(".likes__count").text(parseInt($(".likes__count").text()) - 1)
    }
    else { 
        $(event.target).attr("src", src.replace("like", "like1"))
        $(".logo__dislike").attr("src", $(".logo__dislike").attr("src").replace("dislike1","dislike"))
        $(".likes__count").text(parseInt($(".likes__count").text()) + 1)
    }
        
})

$(".logo__dislike").click((event) =>{
    let pub_id = $(".open-photo__photo").attr("id").replace("pub","");
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/dislikes'+pub_id, true);
    xhr.send();
    let src = $(event.target).attr("src")
    if(src.indexOf("dislike1") > 0){
        $(event.target).attr("src", src.replace("dislike1", "dislike"))
        $(".dislikes__count").text(parseInt($(".dislikes__count").text()) - 1)
    }
    else {
        $(event.target).attr("src", src.replace("dislike", "dislike1"))
        $(".dislikes__count").text(parseInt($(".dislikes__count").text()) + 1)
        $(".logo__like").attr("src", $(".logo__like").attr("src").replace("like1","like"))
    }
})