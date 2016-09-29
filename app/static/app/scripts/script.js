
$(document).ready(function () {
    var socket = new WebSocket('ws://' + window.location.host + '/');
    
    socket.onopen = function () {
        console.log("Connection established.");
    };

    socket.onclose = function (event) {
        if (event.wasClean) {
            console.log('Connection closed successful');
        } else {
            console.log('Connection interrupted');
        }
        console.log('Error code: ' + event.code + ' reason: ' + event.reason);
    };

    socket.onmessage = function (message) {
        console.log("socket.onmessage");
        var data = JSON.parse(message.data);
        console.log(data);
        var table = $('#taskTable');
        var html = Mustache.to_html($('#taskTmpl').html(), data);
        console.log(html);
        table.prepend(html);
    }
})
