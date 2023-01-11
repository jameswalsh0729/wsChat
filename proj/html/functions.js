

const socket = new WebSocket('ws://' + window.location.host + '/websocket');



function welcomeAlert(){
	alert("If you're seeing this, your server sent functions.js!");
}

function successAlert(){
	alert("If you're seeing this, you've made a new account!");
}

//const socket = new WebSocket('ws://' + window.location.host + '/websocket');

// Read the name/comment the user is sending to chat and send it to the server over the WebSocket as a JSON string
// Called whenever the user clicks the Send button or pressed enter
function sendMessage() {
   const chatBox = document.getElementById("chat-comment");
   const comment = chatBox.value;
   chatBox.value = "";
   chatBox.focus();
   if(comment !== "") {
       socket.send(JSON.stringify({'comment': comment}));
   }
}

// Called when the server sends a new message over the WebSocket and renders that message so the user can read it
function addMessage(message) {
   const chatMessage = JSON.parse(message.data);
   let chat = document.getElementById('chat');
   chat.innerHTML += "<img src= \"/../" + chatMessage['pfp'] +"\"width=\"50\" height=\"50\"/> <b>" + chatMessage['username'] + "</b>: " + chatMessage["comment"] + "<br/>";
}


//Called when we parse the msg to see if a new user is added
function addUser(message) {
   let chat = document.getElementById('users');
   chat.innerHTML = "<b>" + "Online users:"+ message + "</b>";
}

function parsedata(message){
    const chatMessage = JSON.parse(message.data);
    console.log(chatMessage)
    if( chatMessage['type'] == "1"){
        addMessage(message);
    }
    else if(chatMessage['type'] == "2"){
        addUser(chatMessage['data']);
    }

}


// Call the addMessage function whenever data is received from the server over the WebSocket
socket.onmessage = parsedata; //modify to check if data is for user list or chat list

// Allow users to send messages by pressing enter instead of clicking the Send button
document.addEventListener("keypress", function (event) {
   if (event.code === "Enter") {
       sendMessage();
   }
});







