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

function add_pub(){
    let formData = new FormData(document.form_newPub);
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/add_publication', true);
    xhr.send(formData);
    xhr.onload = () => {
        let rqst = JSON.parse(xhr.response);
        if (rqst.error != undefined){
            let elemError = document.getElementById('addPub_error');
            elemError.textContent = rqst.error;
            elemError.style = "";
            setTimeout(function(){
                elemError.style = "display: none;"
            }, 5000);
        } else {
            let addElem = '<div class="col-xl-4" style="text-align: center;">' +
                    '<a href="#" id="add"><img src="/static/icons/plus.png" class="photos__format" style="width: 150px;"></a>' +
                    '</div>';
            let newPub = '<div class="col-xl-4">' +
                '<a href="#"><img id="pub' + rqst.id + '" src="' + rqst.ref + '" class="photos__format align-middle publication"></a></div>';
            let last = document.getElementsByClassName('align-items-center')[document.getElementsByClassName('align-items-center').length - 1];
            if (last.childElementCount == 3){
                document.getElementById('add').parentElement.insertAdjacentHTML('beforebegin', newPub);
                document.getElementById('add').parentElement.remove();
                last.insertAdjacentHTML('afterend', '<div class="row align-items-center">' + addElem + '</div>');
            } else {
                document.getElementById('add').parentElement.insertAdjacentHTML('beforebegin', newPub);
            }
        }
        $('.modal_close, #overlay').click();
        open_modal = $('.publication');
        overlay = $('.logo__exit'),
        add = $('#add');
        //---------------Жёсткий костыль---------------------
        add.click( function(event){
            let div = $("#modal2")
            $('#overlay').fadeIn(400,
            function(){
                $(div)
                .css('display', 'block')
                .animate({opacity: 1, top: '50%'}, 200);
            });
        });

        open_modal.click( function(event){
            event.preventDefault();
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
                if(rqst.is_current_user){
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
            }
            overlay.fadeIn(400,
            function(){
                div
                .css('display', 'block')
                .animate({opacity: 1}, 200);
            });
        });
        //---------------Жёсткий костыль---------------------
    };
}

$(document).ready(function() {
    let overlay = $('#overlay'),
    open_modal = $('.open_modal'),
    close = $('.modal_close, #overlay'),
    modal = $('.modal_div'),
    add = $('#add');
    
    open_modal.click( function(event){
        let div = $(this).attr('href');
        overlay.fadeIn(400,
        function(){
            $(div) 
            .css('display', 'block')
            .animate({opacity: 1, top: '50%'}, 200);
        });
    });

    add.click( function(event){
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

$("#MorePublicationPlease button").click(() =>{
    let xhr = new XMLHttpRequest();
    xhr.open('GET', '/MorePublication' + counter() * 10, true);
    xhr.send();
    xhr.onload = () =>{
        let rqst = JSON.parse(xhr.response),
        last_row = $(".row-lenta");
        last_row = last_row[last_row.length - 1];
        console.log(rqst);
        let new_pub;
        for(let key in rqst){
            new_pub = '<div class="row row-lenta">' +
            '<div class="col content-middle">' +
            '<a href="#"><img id="pub' + key + '" src="' + rqst[key]["Content"] + '" class="photos__format align-middle publication"></a>' +
            '<div id="AboutPub"><a href="/profile_' + rqst[key]["User_login"] + '" id="AboutPubLogin">' + rqst[key]["User_login"] + '</a></div>' +
            '</div></div>';
            $(new_pub).insertAfter(last_row);
        }




        //----------------------------- Ещё один жёсткий костыль -----------------------------
        open_modal = $('.publication');
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
                if(rqst.is_current_user){
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
            }
            overlay.fadeIn(400,
            function(){
                div
                .css('display', 'block')
                .animate({opacity: 1}, 200);
            });
        });
        //---------------Жёсткий костыль---------------------
    }
});

var counter = makeCounter();

function makeCounter() {
    var currentCount = 1;

    return function() {
        return currentCount++;
    };
}