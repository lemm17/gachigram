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
            let newPub = '<div class="col-xl-4">' +
            '<a href="#"><img id="pub' + rqst.id + '" src="' + rqst.ref + '" class="photos__format align-middle" style="width: 150px;"></a></div>'
            document.getElementById('add').parentElement.insertAdjacentHTML('beforebegin', newPub);
        }
        $('.modal_close, #overlay').click();
    };
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

