

const socket = new WebSocket('ws://' + window.location.host + '/websocket2');



function welcomeAlert(){
	alert("If you're seeing this, your server sent functions.js!");
}

function successAlert(){
	alert("If you're seeing this, you've made a new account!");
}



// Read the name/comment the user is sending to chat and send it to the server over the WebSocket as a JSON string
// Called whenever the user clicks the Send button or pressed enter
function cookieclick() {
  socket.send(JSON.stringify({'type': "1"}));
}

function catclick() {
  socket.send(JSON.stringify({'type': "2"}));
}


function dogclick() {
  socket.send(JSON.stringify({'type': "3"}));
}

// Called when the server sends a new message over the WebSocket and renders that message so the user can read it
function addMessage(message) {
   const chatMessage = JSON.parse(message.data);
   let chat = document.getElementById('chat');
   chat.innerHTML += "<b>" + chatMessage['username'] + "</b>: " + chatMessage["comment"] + "<br/>";
}


//Called when we parse the msg to see if a new user is added
function addUser(message) {
   let chat = document.getElementById('users');
   chat.innerHTML = "<b>" + "Online users:"+ message + "</b>";
}

function parsedata(message){
    const chatMessage = JSON.parse(message.data);
    console.log(chatMessage)

   let cats = parseInt(chatMessage['cats']);
   let dogs = parseInt(chatMessage['dogs']);
   let catcost = 20 + ((cats*15)*1.1);
   let dogcost = 100 + ((dogs*90)*1.05);

   let chat1 = document.getElementById('cookies');
   chat1.innerHTML = "<b>" + "Total cookies:" + chatMessage['cookies'] + "</b>";

   let chat2 = document.getElementById('cats');
   chat2.innerHTML = "<b>" + "Total cats:" + chatMessage['cats'] + "</b>" + "<b> Cost of a cat:" + catcost.toString() + "</br>" + "<b> Cats give an extra cookie per cat owned. </b>";

   let chat3 = document.getElementById('dogs');
   chat3.innerHTML = "<b>" + "Total dogs:" + chatMessage['dogs'] + "</b>" + "<b> Cost of a dog:" + dogcost.toString() + "</br>"+ "<b> Dogs give 5 extra cookies per dog owned. </b>";


}


// Call the addMessage function whenever data is received from the server over the WebSocket
socket.onmessage = parsedata; //modify to check if data is for user list or chat list

// Allow users to send messages by pressing enter instead of clicking the Send button
document.addEventListener("keypress", function (event) {
   if (event.code === "Enter") {
       sendMessage();
   }
});







