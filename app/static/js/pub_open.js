var overlay = $('.logo__exit'),
    open_modal = $('.publication'),
    close = $('.logo__exit'),
    div = $('#openPhoto'),
    buttonDelete = $('.logo__delete');

open_modal.click( function(event){
    event.preventDefault();
    open_modal = $('.publication');
    $(".open-photo__photo").attr("src", $(event.target).attr("src"));
    $(".open-photo__photo").attr("id", $(event.target).attr("id"));
    let pub_id = $(event.target).attr("id").replace("pub", "");
    let xhr = new XMLHttpRequest();
    xhr.open('GET', '/pub_info' + pub_id, true);
    xhr.send();
    xhr.onload = () => {
        let rqst = JSON.parse(xhr.response);
        document.getElementsByClassName('likes__count')[0].textContent = rqst.count_likes;
        document.getElementsByClassName('dislikes__count')[0].textContent = rqst.count_dislikes;
        let like = document.getElementsByClassName('logo__like')[0],
            dislike = document.getElementsByClassName('logo__dislike')[0];
        if (rqst.current_user_like) {
            like.src = "/static/icons/like1.png";
        } else {
            like.src = "/static/icons/like.png";
        }
        if (rqst.current_user_dislike) {
            dislike.src = "/static/icons/dislike1.png";
        } else {
            dislike.src = "/static/icons/dislike.png";
        }

        $("#pub_user_avatar").attr("src", rqst.user_avatar);
        $("#pub_user_login").html(rqst.user_login);
        $("#pub_user").attr("href", window.location.origin + "/profile_" + rqst.user_login);
        if (rqst.is_current_user){
            $(".logo__delete").css("display", "inline")
        } else {
            $(".logo__delete").css("display", "none")
        }

        // Прогружаем комментарии
        let commetnsElem = document.getElementsByClassName('comments')[0];
        rqst.comments.forEach(a => {
            commetnsElem.insertAdjacentHTML('beforeend',
                newComment(a['login'], a['avatar'], a['comment_text'], a['comment_time']));
        });

        // Проверка разрешения комментирования
        if (rqst.op_to_com || rqst.is_current_user){
            let commenting_elem = '' +
            '<div class="for_comment">' +
                '<input type="text" id="UserComment">' +
                '<button id="SendComment">Комментировать</button>' +
            '</div>';
            document.getElementsByClassName('comments')[0].insertAdjacentHTML('afterend', commenting_elem);
        }
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
    let i,
    comments = document.getElementsByClassName('comments-comment');
    for (i = comments.length - 1; i >= 0; i--) {
        comments[i].remove();
    }
    document.getElementsByClassName('for_comment')[0].remove();
});

buttonDelete.click(function(){
    let pub_id = $(".open-photo__photo").attr("id").replace("pub","");
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/pub_delete' + pub_id, true);
    xhr.send();
    close.click();
    let row = document.getElementById('pub' + pub_id).parentElement.parentElement.parentElement;
    let addElem = '<div class="col-xl-4" style="text-align: center;">' +
                '<a href="#" id="add"><img src="/static/icons/plus.png" class="photos__format" style="width: 150px;"></a>' +
                '</div>';
    if (row.children.length == 3 && row.children[2].children[0].id != "add"){
        document.getElementById('pub' + pub_id).parentElement.parentElement.remove();
        document.getElementById('add').remove();
        row.insertAdjacentHTML('beforeend', addElem);
    } else {
        document.getElementById('pub' + pub_id).parentElement.parentElement.remove();
    }
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

$("#SendComment").click(()=>{
    let pub_id = $(".open-photo__photo").attr("id").replace("pub","");
    let txt = $("#UserComment").val();
    console.log(txt);
    if(txt.replace(" ", "").length > 0){
        let xhr = new XMLHttpRequest();
        xhr.open('GET', '/Comment' + pub_id + "/" + txt, true);
        xhr.send();
        xhr.onload = () =>{
                let rqst = JSON.parse(xhr.response);
                $(".comments").append(newComment( rqst["Login"], rqst["Avatar"], txt, 0));
        }
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
};