function SendMessage() {
  const messageInput = document.getElementById("user-message");
  if (messageInput.value == "") {
    return
  }
  const chatBox = document.getElementById("chat-box");
  const userMessage = messageInput.value;
  // chatBox.innerHTML += `<div class="chat chat-end"><div class="py-3 px-5 rounded-full bg-mes_bg text-mes_te"> ${userMessage} </div></div>`;
  chatBox.innerHTML += `<div class="chat chat-end"><div class="py-3 px-5 rounded-lg bg-neutral ml-10"> ${userMessage} </div></div>`;
  messageInput.value = "";

  fetch("/api/message", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message: userMessage }),
  })
    .then((response) => response.json())
    .then((data) => {
      // Hiển thị phản hồi của server
      chatBox.innerHTML += `<div class="chat chat-start">
          <div class="py-3 px-5 rounded-lg bg-neutral mr-10"> ${data.response} </div></div>`;
      chatBox.scrollTop = chatBox.scrollHeight; // Tự động cuộn xuống cuối
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}



document.getElementById("send-btn").addEventListener("click", () => {
  SendMessage();
});

document.getElementById("user-message").addEventListener("keydown", (e) => {
  if (e.key == "Enter") {
    SendMessage();
  }
});

window.onload = function () {
  document.getElementById("user-message").focus()
}
