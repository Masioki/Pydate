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
    if (Object.keys(openChats).length >= 3) {
        closeChat(Object.keys(openChats)[2]);
    }
    var chatPopup = '<div id="' + chatID + '" class="chat-popup">' +
        '            <div class="chat-popup-header">' +
        '                <div class="chat-popup-header-name">John</div>' +
        '                <div class="chat-popup-header-close">x</div>' +
        '            </div>' +
        '            <div class="chat-popup-body">' +
        '                <ul class="messages">' +
        '                </ul>' +
        '            </div>' +
        '            <div class="chat-popup-input">' +
        '                <input id="IN' + chatID + '" type="text" placeholder="Message...">' +
        '                <button>Send</button>' +
        '            </div>' +
        '        </div>'
    chatPopup = $(chatPopup);
    chatPopup.find("button").click(function () {
        let text = $("#IN" + chatID).val();
        if (text !== "") {
            alert(text);
            send("MESSAGE", text, chatID);
        }
    });
    chatPopup.find(".chat-popup-header-close").click(function () {
        closeChat(chatID);
    });
    chatPopup.find(".chat-popup-header").click(function () {
        minimize(chatID);
    })
    $("#popup-chat-list").append(chatPopup);
}

function addMessage(message, chatID) {
    let control = null;
    if (message.username.localeCompare(username)) {
        control = '<li class="message-right">' +
            message.message +
            '     </li>'
    } else {
        control = '<li class="message-left">' +
            message.message +
            '     </li>'
    }
    $("#" + chatID).find("ul").append($(control));
}

function closeChat(chatID) {
    if (chatID in openChats) {
        send("LEAVE", "", chatID);
        $("#" + chatID).remove();
        delete openChats[chatID];
    }
}

function minimize(chatID) {
    if (chatID in openChats) {
        let element = $("#" + chatID);
        if (element.find(".chat-popup-body").is(":visible")) {
            element.find(".chat-popup-body").hide();
            element.find(".chat-popup-input").hide();
        } else {
            element.find(".chat-popup-body").show();
            element.find(".chat-popup-input").show();
        }
    }
}