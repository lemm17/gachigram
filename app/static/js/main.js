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
            document.getElementsByClassName('nums')[0].textContent = Number(document.getElementsByClassName('nums')[0].textContent) + 1;
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
        //---------------Жёсткий костыль---------------------
        $('#add').unbind('click');
        $('#add').click( function(event){
            open_add_window(event);
        });

        $('.publication').unbind('click');
        $('.publication').click(function(event){
            open_pub(event);
        });

        close_pub()
        //---------------Жёсткий костыль---------------------
    };
}

$(document).ready(function() {
    $('.open_modal').click(
        function(event){
            let div = $(this).attr('href');
            $('#overlay').fadeIn(400,
            function(){
                $(div).css('display', 'block').animate({opacity: 1, top: '50%'}, 200);
            });
        }
    );

    $('#add').unbind('click');
    $('#add').click( function(event){
        open_add_window(event);
    });
    
    $('.modal_close, #overlay').click(
        function(){
            $('.modal_div').animate({opacity: 0, top: '45%'}, 200,
                function(){
                    $(this).css('display', 'none');
                    $('#overlay').fadeOut(400);
                }
            );
        }
    );
});

$("#MorePublicationPlease button").click(() =>{
    let xhr = new XMLHttpRequest();
    xhr.open('GET', '/MorePublication' + counter() * 10, true);
    xhr.send();
    xhr.onload = () =>{
        let rqst = JSON.parse(xhr.response),
        last_row = $(".row-lenta");
        last_row = last_row[last_row.length - 1];
        let new_pub;
        for(let key in rqst){
            new_pub = '<div class="row row-lenta">' +
            '<div class="col content-middle">' +
            '<a href="#"><img id="pub' + key + '" src="' + rqst[key]["Content"] + '" class="photos__format align-middle publication"></a>' +
            '<div id="AboutPub"><a href="/profile_' + rqst[key]["User_login"] + '" id="AboutPubLogin">' + rqst[key]["User_login"] + '</a></div>' +
            '</div></div>';
            $(new_pub).insertAfter(last_row);
        }

        $('#add').unbind('click');
        $('#add').click( function(event){
            open_add_window(event);
        });

        $('.publication').unbind('click');
        $('.publication').click(function(event){
            open_pub(event);
        });
    }
});

var counter = makeCounter();

function makeCounter() {
    var currentCount = 1;

    return function() {
        return currentCount++;
    };
}

