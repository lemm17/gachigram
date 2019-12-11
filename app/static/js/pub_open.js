var overlay = $('.logo__exit'),
    open_modal = $('.publication'),
    close = $('.logo__exit'),
    div = $('#openPhoto'),
    buttonDelete = $('.logo__delete');

$('.publication').click(function(event){
    open_pub(event);
});
$('.logo__exit').click(function(){
    close_pub();
});

$('.logo__delete').click(function(){
    let pub_id = $(".open-photo__photo").attr("id").replace("pub","");
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/pub_delete' + pub_id, true);
    xhr.send();

    document.getElementsByClassName('nums')[0].textContent = Number(document.getElementsByClassName('nums')[0].textContent) - 1;

    $('.logo__exit').click();
    let row = document.getElementById('pub' + pub_id).parentElement.parentElement.parentElement;
    let mainRow = row.parentElement;
    let ii;
    let nextElem;
    for (ii = 0; ii < mainRow.childElementCount; ii++){
        if (mainRow.children[ii] == row){
            break;
        }
    }
    if (ii != mainRow.childElementCount - 1){
        nextElem = mainRow.children[ii + 1].children[0];
    } else {
        nextElem = '<div class="col-xl-4" style="text-align: center;">' +
                '<a href="#" id="add"><img src="/static/icons/plus.png" class="photos__format" style="width: 150px;"></a>' +
                '</div>';
    }

    if (row.children.length == 3 && row.children[2].children[0].id != "add"){
        document.getElementById('pub' + pub_id).parentElement.parentElement.remove();
        nextElem.remove();
        row.insertAdjacentHTML('beforeend', '<div class="col-xl-4" style="text-align: center;">' + nextElem.innerHTML + '</div>');
    } else {
        document.getElementById('pub' + pub_id).parentElement.parentElement.remove();
    }
    // -------------------------------Снова костыль(((( ------------------------------------
    $('#add').unbind('click');
    $('#add').click( function(event){
        open_add_window(event);
    });
    $('.publication').unbind('click');
    $('.publication').click(function(event){
        open_pub(event);
    });
    // -------------------------------Снова костыль(((( ------------------------------------
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

function sendComment() {
    let pub_id = $(".open-photo__photo").attr("id").replace("pub","");
    let txt = $("#UserComment").val();
    if(txt.replace(" ", "").length > 0){
        let xhr = new XMLHttpRequest();
        xhr.open('GET', '/Comment' + pub_id + "/" + txt, true);
        xhr.send();
        xhr.onload = () =>{
            let rqst = JSON.parse(xhr.response);
            $(".comments").append(newComment( rqst["Login"], rqst["Avatar"], txt, Date.parse(new Date().toUTCString()), rqst["id"], true));
        }
    }
}

function newComment(login, avatar, text, time, id, op_to_delete){
    let dateNow = Date.parse(new Date().toUTCString());
    if (typeof(time) != "number") time = Date.parse(time);
    let diff = dateNow - time;
    let minutes = diff / (1000 * 60);
    let strTime;

    if (minutes <= 1){
        strTime = "Только что";
    } else if (minutes < 60) {
        strTime = Math.round(minutes) + " минут назад";
    } else if (minutes < 60 * 24){
        strTime = Math.round(minutes / 60) + " часов назад";
    } else {
        strTime = Math.round(minutes / (60 * 24)) + " дней назад";
    }
    let html = '<div class="comments-comment" id="';
                if (id == undefined) html += 'description">';
                else html += 'comment' + id + '">';
                html += '<div class="clearfix">' +
                    '<a href="/profile_' + login + '">' +
                        '<div class="comment-nickname">' +
                            '<img src="' + avatar + '" class="avatar__format">' +
                             '<span class="_bold _text-padding">' + login + '</span><br>' +
                        '</div>' +
                    '</a>';
                if (op_to_delete) {
                    html += '<img onclick="delete_comment(event)" class="comment-delete" src="/static/icons/exit.png">';
                }
                html += '</div>' +
                '<div class="comments-text">' +
                    text +
                '</div>' +
                '<div style="text-align: right;">' +
                    strTime +
                '</div>'
            '</div>';
    return html;
};

function delete_comment(event, id){
    let comment_elem = event.target.parentElement.parentElement;
    let comment_id = comment_elem.id.replace("comment", "");
    let xhr = new XMLHttpRequest();
    xhr.open('GET', '/comment_delete' + comment_id, true);
    xhr.send();
    xhr.onload = () => {
        let rqst = JSON.parse(xhr.response);
        if (rqst['msg'] == 'successfully'){
            comment_elem.remove();
        } else {
            console.log('Ошибка доступа');
        }
    }
}

function open_pub(event){
    event.preventDefault();
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
        if(rqst.is_current_user){
            $(".logo__delete").css("display", "inline")
        } else {
            $(".logo__delete").css("display", "none")
        }

        // Прогружаем комментарии
        let commetnsElem = document.getElementsByClassName('comments')[0];
        //Описание
        console.log(rqst['description']);
        if (rqst['description'] != ""){
            commetnsElem.insertAdjacentHTML('beforeend',
                newComment(rqst['user_login'], rqst['user_avatar'], rqst['description'], rqst['publication_date']));
        }

        if (rqst.comments.length != 0){
            rqst.comments.forEach(a => {
                commetnsElem.insertAdjacentHTML('beforeend',
                    newComment(a['login'], a['avatar'], a['comment_text'], a['comment_time'], a['comment_id'], a['op_to_delete']));
            });
        }

        if (rqst.op_to_com || rqst.is_current_user){
            let commenting_elem = '' +
            '<div class="for_comment">' +
                '<input type="text" id="UserComment">' +
                '<button id="SendComment" onclick="sendComment();" class="btn-dark">Комментировать</button>' +
            '</div>';
            document.getElementsByClassName('comments')[0].insertAdjacentHTML('afterend', commenting_elem);
        }
    }
    $('.logo__exit').fadeIn(400,
        function(){
            div
            .css('display', 'block')
            .animate({opacity: 1}, 200);
        }
    );
}

function close_pub(){
    $('#openPhoto')
    .animate({opacity: 0}, 200,
        function(){
            $(this).css('display', 'none');
            overlay.fadeOut(400);
        }
    );

    let i,
    comments = document.getElementsByClassName('comments-comment');

    for (i = comments.length - 1; i >= 0; i--) {
        comments[i].remove();
    }

    try {
        document.getElementsByClassName('for_comment')[0].remove();
    } catch {}
}

function open_add_window(event){
    let div = $("#modal2");
    $('#overlay').fadeIn(400,
        function(){
            console.log('Стараюсь всё сломать');
            $(div)
            .css('display', 'block')
            .animate({opacity: 1, top: '50%'}, 200);
        }
    );
}