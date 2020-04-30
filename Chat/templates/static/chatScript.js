let chatID = null;
let chatSocket = null;

window.onload = function () {
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
}

window.onclose = function () {
    send("LEAVE", "")
}

function sendMessage() {
    const message = $('#chat-message-input')[0].value
    send("MESSAGE", message)
}

function addMessage(message) {
    $("#chat-log").append(message.message)
}

function send(command, content) {
    chatSocket.send(JSON.stringify({
        "type": command,
        "chat_id": chatID,
        "message": content
    }));
}




