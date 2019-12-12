// var overlay = $('.temp'),
//     close = $('.logo__exit'),
//     modal = $('#notifOpen');

// $(".logo__notif").click((event) =>{
//     console.log("kek");
//     event.preventDefault();
//     let xhr = new XMLHttpRequest();
//     // xhr.open('GET', '/pub_info' + pub_id, true);
//     // xhr.send();
//     // xhr.onload = () => {
//     // }

//     overlay.fadeIn(400,
//     function(){
//         modal
//         .css('display', 'block')
//         .animate({opacity: 1}, 200);
//     });

//     close.click( function(){
//         modal 
//         .animate({opacity: 0, top: '45%'}, 200, 
//         function(){ 
//             $(this).css('display', 'none');
//             overlay.fadeOut(400);
//         });
//     });
// })

$(document).ready(function() {
    let overlay = $('#temp'),
    open_modal = $('.logo__notif'),
    close = $('#temp'),
    modal = $('#notifOpen');
    
    open_modal.click( function(event){
        let xhr = new XMLHttpRequest();
        $("#forAlerts").attr("data-content", "0");
        $("#forAlerts").text("0");
        let childrens = $("#notifOpen .container").children();
        for(let i = 0; i < childrens.length - 1; i++){
            // let not_id = $(childrens[i]).children().children().attr("id").replace("not", "");
            // xhr.open('GET', '/notif_read_' + not_id, true);
            // xhr.send();                
        }
        xhr.open('GET', '/notif_read_0', true);
        xhr.send();   
        overlay.fadeIn(400,
        function(){
            modal
            .css('display', 'block')
            .animate({opacity: 1}, 200);
        });
    });
    
    close.click( function(){
        modal 
        .animate({opacity: 0}, 200, 
        function(){ 
            $(this).css('display', 'none');
            overlay.fadeOut(400);
        });
    });
});