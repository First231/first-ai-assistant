async function send(){

let message = document.getElementById("message").value

let res = await fetch("https://first-ai-assistant-ai-chatbot.onrender.com/chat", {
method:"POST",
headers:{
"Content-Type":"application/json"
},
body: JSON.stringify({
message: message
})
})

let data = await res.json()

let chat = document.getElementById("chat")

chat.innerHTML += "<p><b>You:</b> "+message+"</p>"
chat.innerHTML += "<p><b>AI:</b> "+data.response+"</p>"

document.getElementById("message").value = ""

}
