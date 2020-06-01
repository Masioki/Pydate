let chatID = null;
let chatSocket = null;
let username = null;
let chatVisible = false;

function popupChat() {
    let display = "";
    if (chatVisible) {
        chatVisible = false;
        display = "none";
    } else {
        chatVisible = true;
        display = "block";
    }

    document.getElementById("chat").style.display = display;
}

window.onload = function () {
    username = JSON.parse(document.getElementById('username').textContent);
    chatID = JSON.parse(document.getElementById('chat_id').textContent);
    chatSocket = new WebSocket(
        "ws://"
        + window.location.host
        + '/ws/chat/'
        + chatID
        + '/'
    );
    chatSocket.onopen = function () {
        send("JOIN", "")
    }
    chatSocket.onmessage = function (mes) {
        addMessage(JSON.parse(mes.data))
    }

    /*
    let mes = JSON.parse(document.getElementById('messages').innerText);
    //alert(mes[0][0].data)
    for (let i in mes) {
        addMessage(JSON.parse(i.data))
    }*/
}

window.onclose = function () {
    send("LEAVE", "")
}

function sendMessage() {
    const message = $('#chat-message-input')[0].value
    send("MESSAGE", message)
}

function send(command, content) {
    chatSocket.send(JSON.stringify({
        "type": command,
        "chat_id": chatID,
        "message": content
    }));
}

function addMessage(message) {

    let control = null;
    if (message.username === username) {
        control = '<li style="width:100%">' +
            '<div class="msj macro">' +
            //'<div class="avatar"><img class="img-circle" style="width:100%;" src="' + me.avatar + '" /></div>' +
            '<div class="text text-l">' +
            '<p>' + message.message + '</p>' +
            '<p><small>' + message.date + '</small></p>' +
            '</div>' +
            '</div>' +
            '</li>';
    } else {
        control = '<li style="width:100%;">' +
            '<div class="msj-rta macro">' +
            '<div class="text text-r">' +
            '<p>' + message.message + '</p>' +
            '<p><small>' + message.date + '</small></p>' +
            '</div>' +
            //'<div class="avatar" style="padding:0 0 0 10px !important"><img class="img-circle" style="width:100%;" src="' + you.avatar + '" /></div>' +
            '</li>';
    }
    let ul = $("ul");
    ul.append(control).scrollTop(ul.prop('scrollHeight'));

    $("#chat-log").append(message.message)
}






