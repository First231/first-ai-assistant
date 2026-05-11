async function send(){
    let message = document.getElementById("message").value;
    if(!message) return; // กันส่งค่าว่าง

    // 1. ต้องเติม /chat ต่อท้าย URL
    let res = await fetch("https://first-ai-assistant-ai-chatbot.onrender.com/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: message //
        })
    });

    let data = await res.json();
    let chat = document.getElementById("chat");

    chat.innerHTML += "<p><b>You:</b> "+message+"</p>";
    
    // 2. ตรวจสอบว่า Backend ส่งคำว่า response กลับมาจริง
    if(data.response) {
        chat.innerHTML += "<p><b>AI:</b> "+data.response+"</p>";
    } else {
        chat.innerHTML += "<p><b>AI:</b> (Error: ไม่ได้รับคำตอบจากระบบ)</p>";
    }

    document.getElementById("message").value = "";
    chat.scrollTop = chat.scrollHeight; // ให้เลื่อนลงล่างสุดอัตโนมัติ
}
