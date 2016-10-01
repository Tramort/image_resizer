var tasks = {};

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

    function refresh_table()
    {
        var table = $('#tasksTBody');
        var templ = $('#taskTmpl').html();
        table.html('');
        for (var id in tasks) {
            var html = Mustache.to_html(templ, tasks[id]);
            table.prepend(html);
        }
    }

    function add_task(task) {
        console.log(task);
        tasks[task.id] = task;

    }

    socket.onmessage = function (message) {
        console.log("socket.onmessage");
        var data = JSON.parse(message.data);
        add_task(data);
        refresh_table();
    }


    $.ajax({
        url: "/api/tasks/",
        success: function (data, textStatus) {
            console.log("Get tasks: " + textStatus)
            data.forEach(function (task) {
                add_task(task);
            });
            refresh_table();
        }
    });

    $('#img-upload-form').ajaxForm({
        clearForm: true ,
        beforeSubmit: function () {
            return $("#img-upload-form").validate();
        },
        success: function (res, status, xhr, form) {
            console.log(res);
        },
        error: function (data) {
            console.log(data.responseText);
            var r = jQuery.parseJSON(data.responseText);
            alert(r.image[0]);
        }
    });

    $(".fancybox").fancybox();
})
