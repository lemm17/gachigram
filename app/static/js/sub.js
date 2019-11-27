let buttons = document.getElementsByClassName('btn-dark'), i;

for (i = 0; i < buttons.length; i++){
    buttons[i].onclick = (event) => {
        let user_id = event.target.id;
        let button = event.target;
        let xhr = new XMLHttpRequest();
        let isSub;
        if (button.classList.contains('btn-sub')){
            isSub = true;
            xhr.open('POST', '/sub' + user_id, true);
        } else {
            isSub = false;
            xhr.open('POST', '/unsub' + user_id, true);
        }
        xhr.send();
        button.disable = true;
        xhr.onload = () => {
            if (xhr.response.status = "ok"){
                if (isSub){
                    button.classList.remove('btn-sub');
                    button.classList.add('btn-unsub');
                    button.textContent = "Отписаться";
                } else {
                    button.classList.remove('btn-unsub');
                    button.classList.add('btn-sub');
                    button.textContent = "Подписаться";
                }
                button.disable = false;
            }
        }
    }
}