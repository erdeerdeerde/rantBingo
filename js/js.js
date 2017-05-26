

function submit(content) {
    content = JSON.stringify(content);
    return $.ajax({
      type: 'POST',
      url: "/submit",
      contentType: "application/json",
      processData: true,
      data: content,
      dataType: "json"
    });
}

function update_wordlist_textarea(wordlist_id) {
    content = { mode: 'get_wordlist', wordlist: wordlist_id };
    var xhr = submit(content);
    xhr.onload = function () {
        return_dict = JSON.parse(xhr.responseText);
        if (return_dict['mode'] === 'success') {
            return $('#words').val(return_dict['return_data']);
        } else if (return_dict['mode'] === 'redirect') {
            window.location.replace(return_dict['uri']);
        } else {
            alert(return_dict['message']);
        }
    };
}

function update_game_description(game_name) {
    content = { mode: 'get_game_description', game_name: game_name };
    var xhr = submit(content);
    xhr.onload = function () {
        $('#textbox_game_description').val(xhr.responseText);
    };
}

function click_create_game(game_name, words, player, check_duplicates) {
    if (game_name === '') {
        alert('title must not be empty');
        return
    }
    content = { mode: "create_game", title: game_name, wordlist: words, player: player, check_duplicates: check_duplicates };
    var xhr = submit(content);
    xhr.onload = function () {
        return_dict = JSON.parse(xhr.responseText);
        if (return_dict['mode'] === 'success') {
            click_join_game(game_name);
        } else {
            alert(return_dict['message']);
        }
    };
}

function click_join_game(game_name) {
    if (game_name == null) {
        console.log('game name is null');
        return
    }
    if($('#login').length > 0){
        content = { mode: "join_as_spectator", game: game_name };
    } else {
        content = { mode: "join_game", game: game_name };
    }
    var xhr = submit(content);
    xhr.onload = function () {
        return_dict = JSON.parse(xhr.responseText);
        if (return_dict['mode'] === 'redirect') {
            window.location.replace(return_dict['uri']);
        } else {
            alert(return_dict['message']);
        }
    };
}

function check_field(word_id, game, player) {
    content = { mode: "check_field", word_id: word_id, game: game, player: player };
    var xhr = submit(content);
    xhr.onload = function () {
        return_dict = JSON.parse(xhr.responseText);
        if (return_dict['mode'] === 'reload') {
            window.location.reload(true);
        } else {
            alert(return_dict['message']);
        }
    };
}

function click_login(player, secret) {
    content = { mode: "login", player: player, secret: secret };
    var xhr = submit(content);
    xhr.onload = function () {
        console.log(xhr.responseText);
        return_dict = JSON.parse(xhr.responseText);
        if (return_dict['mode'] === 'success') {
            alert(return_dict['message']);
            window.location.reload(true);
        } else {
            alert(return_dict['message']);
        }
    };
}

function click_register(player, secret) {
    content = { mode: "register", player: player, secret: secret };
    var xhr = submit(content);
    xhr.onload = function () {
        console.log(xhr.responseText);
        return_dict = JSON.parse(xhr.responseText);
        if (return_dict['mode'] === 'success') {
            alert(return_dict['message']);
            window.location.reload(true);
        } else {
            alert(return_dict['message']);
        }
    };
}

function initialize_landingpage() {
    if($('#login').length > 0){
        document.getElementById('create_game').classList.add('pure-button-disabled')
        document.getElementById('join').innerHTML = "Join as spectator"
    } else {
        document.getElementById('create_game').classList.remove('pure-button-disabled')
        document.getElementById('join').innerHTML = "Join";
    }
}
