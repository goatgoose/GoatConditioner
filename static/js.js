
var updateInterval;

document.getElementById("idealTemp").addEventListener("input", function(event) {
    var edited = $("#idealTemp");
    handleEdit(edited, function() {
        $.ajax({
            url: "/idealTemp",
            data: {idealTemp: edited.text()},
            dataType: 'json',
            type: 'post',
            success: function() {},
            failure: function() {}
        })
    });
});

document.getElementById("turnOnTemp").addEventListener("input", function(event) {
    var edited = $("#turnOnTemp");
    handleEdit(edited, function() {
        $.ajax({
            url: "/turnOnTemp",
            data: {turnOnTemp: edited.text()},
            dataType: 'json',
            type: 'post',
            success: function() {},
            failure: function() {}
        })
    });
});

document.getElementById("turnOffTemp").addEventListener("input", function(event) {
    var edited = $("#turnOffTemp");
    handleEdit(edited, function() {
        $.ajax({
            url: "/turnOffTemp",
            data: {turnOffTemp: edited.text()},
            dataType: 'json',
            type: 'post',
            success: function() {},
            failure: function() {}
        })
    });
});

$("#pause").on('click', function (event) {
    console.log("pause button click");
    var button = $("#pause");
    if (button.text() == "Pause") {
        button.text(function() { return "Resume"; });
        button.removeClass("btn-danger");
        button.addClass("btn-success");
        button.blur();

        $.ajax({
            url: "/pause",
            data: {},
            dataType: 'json',
            type: 'post',
            success: function() {},
            failure: function() {}
        })
    } else if (button.text() == "Resume") {
        button.text(function() { return "Pause"; });
        button.removeClass("btn-success");
        button.addClass("btn-danger");
        button.blur();

        $.ajax({
            url: "/resume",
            data: {},
            dataType: 'json',
            type: 'post',
            success: function() {},
            failure: function() {}
        })
    }
});

function handleEdit(element, onSubmit) {
    var content = element.html();
    console.log(content);
    if (content.includes("<br>")) {
        content = content.replace(/<br>/g, "");
        console.log(content);
        element.html(function() {
            return content;
        });
        element.blur();
        onSubmit();
    }
}

$(document).ready(function() {
    update();
    updateInterval = setInterval(update, 1000);
});

function update() {
    if (!$("*").is(":focus")) {
        $.ajax({
            url: "/update",
            data: {},
            dataType: 'json',
            type: 'get',
            success: function (response) {
                $("#conditionerStatus").text(function () {
                    return response.status + ".";
                });
                $("#currentTemp").html(function () {
                    return response.currentTemp + "&#176;";
                });
                $("#idealTemp").text(function () {
                    return response.idealTemp;
                });
                $("#turnOnTemp").text(function () {
                    return response.turnOnTemp;
                });
                $("#turnOffTemp").text(function () {
                    return response.turnOffTemp;
                });

                var currentTemp = $("#currentTemp");
                currentTemp.removeClass();
                if (response.currentTemp <= response.idealTemp + response.turnOnTemp) {
                    currentTemp.addClass("text-primary");
                } else if (response.currentTemp > response.idealTemp + response.turnOnTemp &&
                            response.currentTemp < response.idealTemp + response.turnOnTemp + 3) {
                    currentTemp.addClass("text-warning");
                } else {
                    currentTemp.addClass("text-danger");
                }
            },
            failure: function () {
            }
        });
    }
}


