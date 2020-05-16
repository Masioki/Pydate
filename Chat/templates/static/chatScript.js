let username = null;
let openChats = {}

function displayChat() {
    document.getElementById("chat-window").style.display = "block";
    document.getElementById("chat-list-button").style.display = "none";
}

function hideChat() {
    document.getElementById("chat-window").style.display = "none";
    document.getElementById("chat-list-button").style.display = "block";
}

window.onload = function () {
    username = JSON.parse(document.getElementById('username').textContent);
}

window.onclose = function () {
    for (var id in openChats) {
        send("LEAVE", "", id);
    }
}

function send(command, content, chatID) {
    if (chatID in openChats) {
        let chatSocket = openChats[chatID];
        chatSocket.send(JSON.stringify({
            "type": command,
            "chat_id": chatID,
            "message": content
        }));
    }
}

function sendMessage(chatID) {
    if (chatID in openChats) {
        var popup = $(chatID);
        var content = popup.send("MESSAGE", content, chatID)
    }
}


function openChat(chatID) {
    if (!(chatID in openChats)) {
        let chatSocket = new WebSocket(
            "ws://"
            + window.location.host
            + '/ws/chat/'
            + chatID
            + '/'
        );
        chatSocket.onopen = function () {
            send("JOIN", "", chatID)
        }
        chatSocket.onmessage = function (mes) {
            addMessage(JSON.parse(mes.data))
        }
        openChats[chatID] = chatSocket;

        $.get({
            url: '/chat/messages/' + chatID,
            success: [function (data) {
                showNewChatPopup(chatID);
                for (var mes in data.messages) {
                    addMessage(mes, chatID);
                }
            }]
        });
    }
}

function showNewChatPopup(chatID) {
    var chatPopup = '<div id="' + chatID + '" class="msg_box">' +
        '<div class="close">x</div> ' +
        '<div class="msg_wrap"> <div class="msg_body"> <div class="msg_push"></div> </div>' +
        '<div class="msg_footer"><textarea class="msg_input" rows="4">dupa</textarea></div> </div>' +
        '</div>';
    $("body").append(chatPopup);
}

function addMessage(message, chatID) {

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

function closeChat(chatID) {
    if (chatID in openChats) {
        send("LEAVE", "", chatID);
        var element = document.getElementById(chatID);
        element.parentNode.removeChild(element);
    }
}