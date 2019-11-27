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
        xhr.open('GET', '/pub_info' + pub_id, true);
        xhr.send();
        xhr.onload = () => {
            let rqst = JSON.parse(xhr.response);
            console.log(rqst);
            document.getElementsByClassName('likes__count')[0].textContent = rqst.count_likes;
            document.getElementsByClassName('dislikes__count')[0].textContent = rqst.count_dislikes;
            if (rqst.current_user_like) {
                document.getElementsByClassName('logo__like')[0].src = "/static/icons/like1.png";
            }
            if (rqst.current_user_dislike) {
                document.getElementsByClassName('logo__dislike')[0].src = "/static/icons/dislike1.png";
            }

            // Прогружаем комментарии
            let commetnsElem = document.getElementsByClassName('comments')[0];
            rqst.comments.forEach(a => {
                commetnsElem.insertAdjacentHTML('beforeend',
                    newComment(a['login'], a['avatar'], a['comment_text'], a['comment_time']));
            });
        }
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
    xhr.open('POST', '/like' + pub_id, true);
    xhr.send();
    let like = document.getElementsByClassName('logo__like')[0],
        dislike = document.getElementsByClassName('logo__dislike')[0],
        lCount = document.getElementsByClassName('likes__count')[0],
        dCount = document.getElementsByClassName('dislikes__count')[0];
    if (like.src[like.src.length - 5] == '1') {
        like.src = "/static/icons/like.png";
        lCount.textContent = Number(lCount.textContent) - 1;
    } else if (dislike.src[dislike.src.length - 5] == '1'){
        like.src = "/static/icons/like1.png";
        lCount.textContent = Number(lCount.textContent) + 1;
        dislike.src = "/static/icons/dislike.png";
        dCount.textContent = Number(dCount.textContent) - 1;
    } else {
        like.src = "/static/icons/like1.png";
        lCount.textContent = Number(lCount.textContent) + 1;
    }
});

$(".logo__dislike").click(() =>{
    let pub_id = $(".open-photo__photo").attr("id").replace("pub","");
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/dislike' + pub_id, true);
    xhr.send();
    let like = document.getElementsByClassName('logo__like')[0],
        dislike = document.getElementsByClassName('logo__dislike')[0],
        lCount = document.getElementsByClassName('likes__count')[0],
        dCount = document.getElementsByClassName('dislikes__count')[0];
    if (dislike.src[dislike.src.length - 5] == '1') {
        dislike.src = "/static/icons/dislike.png";
        dCount.textContent = Number(dCount.textContent) - 1;
    } else if (like.src[like.src.length - 5] == '1'){
        dislike.src = "/static/icons/dislike1.png";
        dCount.textContent = Number(dCount.textContent) + 1;
        like.src = "/static/icons/like.png";
        lCount.textContent = Number(lCount.textContent) - 1;
    } else {
        dislike.src = "/static/icons/dislike1.png";
        dCount.textContent = Number(dCount.textContent) + 1;
    }
});

function newComment(login, avatar, text, time){
    return '<div class="comments-comment">' +
            '<a href="/profile_' + login + '">' +
                '<div class="comment-nickname">' +
                    '<img src="' + avatar + '" class="avatar__format">' +
                     '<span class="_bold _text-padding">' + login + '</span><br>' +
                '</div>' +
            '</a>' +
            '<div class="comments-text">' +
                text
            '</div>' +
        '</div>';
}