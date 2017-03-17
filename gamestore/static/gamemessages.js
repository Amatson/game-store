$(document).ready(function() {
    'use strict';
    $(window).on('message', function(event) {
        var msg = event.originalEvent.data;
        // Player submits a score
        if(msg.messageType == 'SCORE') {
            $('#score').val(msg.score);
            $('#score_form').submit();
        }
        // Player saves a game
        else if (msg.messageType == 'SAVE') {
            $('#state').val(JSON.stringify(msg.gameState));
            $('#save_form').submit();
        }
        // Player loads a game
        else if (msg.messageType == 'LOAD_REQUEST') {
            if ($('#load_data').val() == 'None') {
                $('#request_load').val('load_game');
                $('#request_load_form').submit();
            }
        }
        // Set window width and height
        else if (msg.messageType == 'SETTING') {
            document.getElementById('game_iframe').style.width = msg.options.width+'px';
            document.getElementById('game_iframe').style.height = msg.options.height+'px';
        }
    });
});

// Send the save state to the game or an error message if the game could not be loaded
$(document).ready(function() {
    // Prevent page refresh before loading the data with a 0,5 second timer
    setTimeout(function() {
        // Get data from gameplay.html
        var data = $('#load_data').val();
        // Send a postMessage to the game (LOAD or ERROR) if there has been a load request
        if (data != 'None') {
            parsed = JSON.parse(data);
            document.getElementById('game_iframe').contentWindow.postMessage(parsed, '*');
        }
    }, 500)
});
