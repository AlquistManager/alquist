var endpoint;
var bot;
var state = 'init';
var context = {};
var payload = {};
var session = "";
var showHideTime = 500;
var scrollToBottomTime = 500;

//Function called right after the page is loaded
$(document).ready(function () {
    //input field size hack
    inputFieldSizeHack();
    //Get endpoint from URL address
    endpoint = getEndpoint();
    bot = getBot();
    $('#input_field').hide();
    $('#submit').hide();
    //Request response of init node
    init();
});

//Call init state
function init() {
    $.ajax({
        url: endpoint,
        type: 'post',
        processData: false,
        data: JSON.stringify({
            "text": '',
            "bot": bot,
            "state": state,
            "context": context,
            "session": session,
            "payload": payload
        }),
        contentType: "application/json; charset=utf-8",
        dataType: "json",

        success: function (data, textStatus, jQxhr) {
            // save state, context and session
            state = data["state"];
            context = data["context"];
            session = data["session"];
            payload = {};
            //show Alquist's response
            showSystemMessages(data["messages"], data["input"]);
        },
        error: function (jqXhr, textStatus, errorThrown) {
            console.log(errorThrown);
            //If Alquist doesn't response, wait and try it again
            setTimeout(init(), 3000);
        }
    });
}

//Click on submit button
$(document).on("submit", "#form", function (e) {
    //Prevent reload of page after submitting of form
    e.preventDefault();
    var text = $('#input_field').val();
    //send input to Alquist
    sendInput(text);
    //Erase input field
    $('#input_field').val("");
    //Show user's input immediately
    if (text != "") {
        showUserMessage(text);
    }
});

//Click on reset button
$(document).on("click", "#reset", function (e) {
    //Prevent reload of page after submitting of form
    e.preventDefault();
    //send input to Alquist
    sendInput("!reset");
    showUserMessage("Začít od začátku");
});

//Click on back button
$(document).on("click", "#back", function (e) {
    //Prevent reload of page after submitting of form
    e.preventDefault();
    //send input to Alquist
    sendInput("!undo");
    showUserMessage("Zpět");

});

//Click on back button
$("iframe").on("click", function (e) {
    e.preventDefault();
});

//send message to Alquist by REST
function sendInput(text) {
    // escape html tags
    text = text.replace(/</g, '&lt;').replace(/>/g, '&gt;');
    hideButtons();
    hideCheckboxes();
    $.ajax({
        url: endpoint,
        dataType: 'json',
        type: 'post',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({
            "text": text,
            "bot": bot,
            "state": state,
            "context": context,
            "session": session,
            "payload": payload
        }),
        processData: false,

        success: function (data, textStatus, jQxhr) {
            // save state, context and session
            state = data["state"];
            context = data["context"];
            session = data["session"];
            payload = {};
            //show Alquist's response
            showSystemMessages(data["messages"], data["input"]);
        },
        error: function (jqXhr, textStatus, errorThrown) {
            console.log(errorThrown);
        }
    });
}

//Shows responses of Alquist
function showSystemMessages(messages, input) {
    var buttons = [];
    var checkboxes = [];
    // absolute delay of showing the messages
    var cumulatedDelay = 0;
    for (var i = 0; i < messages.length; i++) {
        if (messages[i]['type'] == "text") {
            cumulatedDelay += messages[i]['delay'];
            showSystemMessageText(messages[i]['payload']['text'], cumulatedDelay);
        }
        else if (messages[i]['type'] == "button") {
            buttons.push({
                "text": messages[i]['payload']['label'], "next_state": messages[i]['payload']['next_state'],
                "type": messages[i]['payload']['type']
            });
        }
        else if (messages[i]['type'] == "checkbox") {
            checkboxes.push({
                "text": messages[i]['payload']['label'], "update_keys": messages[i]['payload']['update_keys'],
                "type": messages[i]['payload']['type']
            });
        }
        else if (messages[i]['type'] == "iframe") {
            cumulatedDelay += messages[i]['delay'];
            showIframe(messages[i]['payload']['url'], messages[i]['payload']['width'], messages[i]['payload']['height'], messages[i]['payload']['scrolling'], messages[i]['payload']['align'], cumulatedDelay);
        }
        else if (messages[i]['type'] == "carousel") {
            showCarousel(messages[i]['payload']['parts'], messages[i]['payload']['urls'], cumulatedDelay);
        }
    }
    // if there is some delay, than hide input
    if (cumulatedDelay > 0) {
        hideSubmitButon();
        hideInput();
    }
    // Show inputs after delay
    setTimeout(function () {
        showButtons(buttons);
        showCheckboxes(checkboxes);
        switch (input) {
            case "input":
                showInput();
                showSubmitButton(false);
                break;
            case "button":
                hideInput();
                showSubmitButton(true);
                break;
            case "none":
                hideSubmitButon();
                hideInput();
                break;
            case "both":
                showInput();
                showSubmitButton(false);
                break;
            default:
                showInput();
                showSubmitButton(false);
                break;
        }
    }, cumulatedDelay);
}

// Show text message
function showSystemMessageText(text, delay) {
    var well = $('<table class="message"><tr><td><img src="img/Alquist.png" class="profile_picture_left"></td><td><div class="arrow-left"></div></td><td><div class="well well_system"><div class="clearfix"><span> ' + text + '</span></div></div></td><td class="empty_space"></td></tr></table>');
    setTimeout(function () {
        $("#communication_area").append(well.fadeIn("medium"));
        //scroll to bottom of page
        setTimeout(function () {
            $("html, body").animate({scrollTop: $(document).height()}, scrollToBottomTime);
        }, 1);
    }, delay);
}

//Shows message of user
function showUserMessage(text) {
    // escape html tags
    text = text.replace(/</g, '&lt;').replace(/>/g, '&gt;');
    //Show it on page
    var well = $('<table class="message message_user"><tr><td class="empty_space"></td><td><div class="well"><div class="clearfix"><span> ' + text + '</span></div></div></td><td><div class="arrow-right"></div></td><td><img src="img/User.png" class="profile_picture_right"></td></tr></table>');
    $("#communication_area").append(well);
    //scroll to bottom of page
    $("html, body").animate({scrollTop: $(document).height()}, scrollToBottomTime);
}

// Gets parameter by name
function getParameterByName(name, url) {
    var arr = url.split('#');
    var match = RegExp('[?&]' + name + '=([^&]*)')
        .exec(arr[0]);
    return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
}

//Get endpoint of Alquist from URL parameters
function getEndpoint() {
    //Get endpoint from URL
    var endpoint = getParameterByName("e", window.location.href);
    //Use default, if no endpoint is present
    if (endpoint == null) {
        endpoint = "http://localhost:5000/";
    }
    return endpoint;
}

//Get endpoint of Alquist from URL parameters
function getBot() {
    //Get endpoint from URL
    var bot = getParameterByName("bot", window.location.href);
    //Use default, if no endpoint is present
    if (bot == null) {
        bot = "";
    }
    return bot;
}

//show buttons
function showButtons(buttons) {
    //clear old buttons
    $('#buttons').empty();
    //create button
    for (var i = 0; i < buttons.length; i++) {
        var buttonElement = $('<button type="button" class="btn button-slave button">' + buttons[i].text + '</button>');
        if (buttons[i].type == "Main") {
            buttonElement.addClass("button-main");
            buttonElement.removeClass("button-slave");
        }
        $('#buttons').append(buttonElement);
        buttonElement.click(createButtonClickCallback(buttons[i].text, buttons[i].next_state));
    }
    // show button smoothly
    $('#buttons').show(showHideTime);
    //scroll to bottom of page
    $("html, body").animate({scrollTop: $(document).height()}, scrollToBottomTime);
}

//show buttons
function showCheckboxes(checkboxes) {
    //clear old checkboxes
    $('#checkboxes').empty();
    //create button
    for (var i = 0; i < checkboxes.length; i++) {
        var checkboxElement = $('<label class="checkboxes"><input type="checkbox" value="" class="checkbox-label">' + checkboxes[i].text + '</label>');
        $('#checkboxes').append(checkboxElement);
        checkboxElement.click(createCheckboxClickCallback(checkboxElement.find("input")[0], checkboxes[i].update_keys));
    }
    // show button smoothly
    $('#checkboxes').show(showHideTime);
    //scroll to bottom of page
    $("html, body").animate({scrollTop: $(document).height()}, scrollToBottomTime);
}

function showIframe(url, width, height, scrolling, align, delay) {
    var well = $('<table class="message"><tr><td><img src="img/Alquist.png" class="profile_picture_left"></td><td><div class="arrow-left"></div></td><td style="width: 100%"><div class="well well_system"><div class="clearfix"><table style="width:100%"><tr><td><b>Alquist:</b></td><td style="width: 100%; text-align: ' + align + ';"><iframe src=' + url + ' style="height: ' + height + 'px; width: ' + width + '%;"class="message_iframe" scrolling="' + scrolling + '"></iframe></td></tr></table></div></div></td><td class="empty_space" style="float: right;"></td></tr></table>');
    setTimeout(function () {
        $("#communication_area").append(well.fadeIn("medium"));
        //scroll to bottom of page
        setTimeout(function () {
            $("html, body").animate({scrollTop: $(document).height()}, scrollToBottomTime);
        }, 1);
    }, delay);
}

function showCarousel(parts, urls, delay) {
    //Show it on page
    setTimeout(function () {
        var carousell = $('<div class="multiple-items" style="height:600px"> </div>');
        var well = $('<div class="well" style="margin-bottom: 20px;"><div class="clearfix"></div></div>').append(carousell);
        $("#carousel").append(well);
        for (var i = 0; i < parts.length; i++) {
            carousell.append("<a style='height:600px' href='" + urls[i] + "'>" + parts[i] + "</a>");
        }
        //scroll to bottom of page
        $("html, body").animate({scrollTop: $(document).height()}, scrollToBottomTime);
        slick();
    }, delay);
}

// callback function for button click
function createButtonClickCallback(text, next_state) {
    return function () {
        state = next_state;
        sendInput("");
        showUserMessage(text);
        hideButtons();
    }
}

// callback function for checkbox click
function createCheckboxClickCallback(checkboxElement, update_keys) {
    return function () {
        if (checkboxElement.checked) {
            jQuery.extend(payload, update_keys);
        } else {
            for (var k in update_keys) {
                // skip loop if the property is from prototype
                if (!update_keys.hasOwnProperty(k)) continue;
                delete payload[k];
            }
        }
    }
}

//hide buttons smoothly
function hideButtons() {
    $('#buttons').hide(showHideTime);
}

//hide checkboxes smoothly
function hideCheckboxes() {
    $('#checkboxes').hide(showHideTime);
}

//show input form
function showInput() {
    $('#input_field').show(showHideTime);
    $('#submit').show(showHideTime);
    //scroll to bottom of page
    $("html, body").animate({scrollTop: $(document).height()}, scrollToBottomTime);
}

function showSubmitButton(rounded) {
    $('#submit').show(showHideTime);
    $('#submit_span').css("text-align", "right");
    if (rounded) {
        $('#submit').css("border-top-left-radius", "4px");
        $('#submit').css("border-bottom-left-radius", "4px");
    } else {
        $('#submit').css("border-top-left-radius", "0px");
        $('#submit').css("border-bottom-left-radius", "0px");
    }
    //scroll to bottom of page
    $("html, body").animate({scrollTop: $(document).height()}, scrollToBottomTime);
}

//hide input form
function hideInput() {
    $('#input_field').hide(showHideTime);
}

function hideSubmitButon() {
    $('#submit').hide(showHideTime);
}

//hack to have same size of input field and submit button
function inputFieldSizeHack() {
    var height = $('#submit_span').outerHeight();
    $('#submit').outerHeight(height);
    $('#input_field').outerHeight(height)
}

function slick() {
    $('.multiple-items').slick({
        slidesToShow: 3,
        slidesToScroll: 3,
        dots: true,
        arrows: false,
        infinite: false,
        responsive: [
            {
                breakpoint: 1200,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 2
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
            }]
    });
}