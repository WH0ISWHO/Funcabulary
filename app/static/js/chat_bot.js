class ChatBot {
    constructor() {
        this.modal = document.getElementById("chat-modal");
        this.box = document.getElementById("chat-msg");
        this.user_inp = document.getElementById("user-inp");
        this.initEventListeners();
    }

    initEventListeners() {
        document.getElementById("chat-btn").addEventListener("click", () => this.open());
        document.getElementById("close-chat").addEventListener("click", () => this.close());
        document.getElementById("send-btn").addEventListener("click", () => this.sendMessage());
        this.user_inp.addEventListener("keypress", (e) => {
            if (e.key === "Enter") this.sendMessage();
        });
    }

    open() {
        this.modal.style.display = "block";
        this.box.innerHTML = `<div class="bot-msg-wrap"><div class="bot-msg">🤖 안녕하세요! 무엇을 도와드릴까요?</div></div>`;
    }

    close() {
        this.modal.style.display = "none";
    }

    sendMessage() {
        let userMsg = this.user_inp.value.trim();
        if (!userMsg) return;

        this.addMessage(userMsg, "user");
        
        fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ "Message": userMsg })
        })
        .then(response => response.json())
        .then(data => this.addMessage(data.response || "답변을 가져올 수 없습니다.", "bot"))
        .catch(error => {
            console.error("Error:", error);
            this.addMessage("🤖 오류가 발생했습니다.", "bot");
        })
        .finally(() => {
            this.user_inp.value = "";
            this.user_inp.focus();
        });
    }

    addMessage(text, sender) {
        let wrapDiv = document.createElement("div");
        wrapDiv.classList.add(sender === "user" ? "user-msg-wrap" : "bot-msg-wrap");
    
        let msgDiv = document.createElement("div");
        msgDiv.classList.add(sender === "user" ? "user-msg" : "bot-msg");
        msgDiv.innerHTML = sender === "user" ? `${text} 👤` : `🤖 ${text}`;
    
        wrapDiv.appendChild(msgDiv);
        this.box.appendChild(wrapDiv);
        this.box.scrollTop = this.box.scrollHeight;
    }
}

const chatBot = new ChatBot();


// document.querySelector("#chat-btn").addEventListener("click", function(){
//     document.getElementById("chat-modal").style.display = "block";
//     let chat_box = document.querySelector("#chat-msg");
//     chat_box.innerHTML = `<div class="bot-msg">🤖 안녕하세요! 무엇을 도와드릴까요?</div>`;
// });

// document.querySelector("#close-chat").addEventListener("click", () => document.getElementById("chat-modal").style.display = "none");

// document.querySelector("#send-btn").addEventListener("click", () => send_msg());

// document.querySelector("#user-inp").addEventListener("keypress", function(e){
//     if(e.key === "Enter") send_msg();
// });

// function send_msg(){
//     let user_msg = document.getElementById("user-inp").value;
//     if (user_msg.trim() === "") return;

//     let chat_box = document.getElementById("chat-msg");
//     chat_box.innerHTML += `<div class="user-msg">${user_msg} 👤</div>`;
//     chat_box.scrollTop = chat_box.scrollHeight;

//     fetch(`/api/chat`, {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json"
//         },
//         body: JSON.stringify({"Message": user_msg})
//     })
//     .then(response => response.json())
//     .then(data => {
//         let bot_msg = data.response || "답변을 가져올 수 없습니다.";
//         chat_box.innerHTML += `<div class="bot-msg">🤖 ${bot_msg}</div>`;
//         chat_box.scrollTop = chat_box.scrollHeight;
//     })
//     .catch(e => {
//         console.error("Error:", e);
//         chat_box.innerHTML += `<div class="bot-msg">🤖 오류가 발생했습니다.</div>`;
//     });

//     document.getElementById("user-inp").value = "";
//     document.getElementById("user-inp").focus();
// }