function convertToHTML(text) {
  // Tách từng dòng trong văn bản
  const lines = text.split('\n');

  // Chuyển đổi mỗi dòng thành thẻ <div> và thêm vào mảng
  const htmlLines = lines.map(line => {
      // Thay thế ký tự ** thành thẻ <strong> để làm nổi bật
      let strongLine = line.replace(/\*\*(.*?)\*\*/g, '<strong class="font-bold">$1</strong>');
      // Thay thế ký tự * thành thẻ <em> để in nghiêng
      strongLine = strongLine.replace(/\*(.*?)\*/g, '<em class="italic">$1</em>');
      // Thay thế đoạn mã được bao quanh bởi ``` thành thẻ <pre><code>
      strongLine = strongLine.replace(/```(.*?)```/gs, '<pre class="bg-gray-200 p-4 rounded border border-gray-300"><code>$1</code></pre>');
      // Trả về mỗi dòng trong thẻ <div>
      return `<div>${strongLine}</div>`;
  });

  // Kết hợp tất cả các dòng lại thành một chuỗi HTML
  return htmlLines.join('');
}

function addMessageToChatContainer(message, isUserMessage = true) {
  const chatContainer = document.getElementById("chat-container");
  const messageHtml = `
   <div class="flex items-start gap-2 ${!isUserMessage ? "justify-start mr-20 ml-3" : "justify-end ml-20 mr-3"} my-3">
                            <div class="p-3 rounded-md bg-white ring-1 ring-gray-900/5">
                              ${message}
                            </div>
                          </div>
  `
  
  chatContainer.innerHTML += messageHtml
}

function addChatHistoryToHistoryContainer(label) {
  const historyHtml = `
    <li class="relative z-[15]">
                        <div class="no-draggable group relative rounded-lg active:opacity-90 hover:bg-black/5 fex-row">
                          <a class="flex items-center gap-2 p-2" data-discover="true" href="/changehistory/322">
                            <div class="relative grow overflow-hidden whitespace-nowrap" dir="auto">
                              ${label}
                              <div class="absolute bottom-0 top-0 to-transparent ltr:right-0 ltr:bg-gradient-to-l rtl:left-0 rtl:bg-gradient-to-r from-token-sidebar-surface-secondary w-10 from-60%"></div>
                            </div>
                          </a>
                          <div class="absolute right-0 bottom-0 top-0 items-center gap-1.5 pr-2 ltr:right-0 rtl:left-0 flex">
                            <button class="flex items-center justify-center text-token-text-secondary transition hover:text-token-text-primary radix-state-open:text-token-text-secondary" data-testid="history-item-0-option" type="button" id="radix-:r1b5:" aria-haspopup="menu" aria-expanded="false" data-state="closed">
                              <svg width="24" height="24" fill="#000000" width="64px" height="64px" viewBox="-3.2 -3.2 38.40 38.40" enable-background="new 0 0 32 32" id="Glyph" version="1.1" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" transform="matrix(1, 0, 0, 1, 0, 0)rotate(0)">
                                <path d="M16,13c-1.654,0-3,1.346-3,3s1.346,3,3,3s3-1.346,3-3S17.654,13,16,13z" id="XMLID_287_"></path>
                                <path d="M6,13c-1.654,0-3,1.346-3,3s1.346,3,3,3s3-1.346,3-3S7.654,13,6,13z" id="XMLID_289_"></path>
                                <path d="M26,13c-1.654,0-3,1.346-3,3s1.346,3,3,3s3-1.346,3-3S27.654,13,26,13z" id="XMLID_291_"></path>
                              </svg>
                            </button>
                          </div>
                        </div>
                      </li>
  `;
  const historyContainer = document.getElementById("history-container");
  historyContainer.insertAdjacentHTML("afterbegin", historyHtml)
}

function clearChatContainer() {
  const chatContainer = document.getElementById("chat-container");
  chatContainer.innerHTML = "";
}

document.getElementById("send-btn").addEventListener("click", function (event) {
  event.preventDefault();
  const message_input = document.getElementById("message-input");
  const message = message_input.value;
  if (message == "") {
    return
  }
  message_input.value = "";
  send_message(message);
});

document
  .getElementById("message-input")
  .addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      const message_input = document.getElementById("message-input");
      const message = message_input.value;
      if (message == "") {
        return
      }
      message_input.value = "";
      send_message(message);
    }
  });


document
  .getElementById("new-chat-btn")
  .addEventListener("click", function (event) {
    event.preventDefault();
    const chatContainer = document.getElementById("chat-container");
    if (!chatContainer.innerHTML == "") {
      send_new_chat();
    }
  })
// ===========================================

function send_new_chat() {
  client.sendMessage("new_chat", 0);
  clearChatContainer();
  addMessageToChatContainer("Hello, how can I help you?", false);
}

function send_message(message) {
  client.sendMessage("message", message);
  addMessageToChatContainer(message, true);
}

// =========================================
class NetworkClient {
    constructor(url) {
        this.url = url;
        this.ws = null;
        this.isConnected = false;
    }

    async connect() {
        try {
            const response = await fetch("/websocket/token");
            if (!response.ok) {
              throw new Error("Failed to fetch token");
            }
        
            const data = await response.json();
            if (data.onetimetoken) {
              sessionStorage.setItem("onetimetoken", data.onetimetoken);
            } else {
              throw new Error("No token received");
            }
        
            const onetimetoken = sessionStorage.getItem("onetimetoken");

            if (onetimetoken) {
                this.ws = new WebSocket(this.url + `?onetimetoken=${onetimetoken}`);
            }
            else {
                throw new Error("No token received");
            }

            this.ws.onopen = this.onOpen.bind(this);
            this.ws.onmessage = this.onMessage.bind(this);
            this.ws.onclose = this.onClose.bind(this);
            this.ws.onerror = this.onError.bind(this);
        }
        catch (error) {
            console.error("Error:", error.message);
            window.location.href = "http://localhost:8000/auth/login";
        }
    }

    sendMessage(type, message) {
        if (this.ws.readyState === WebSocket.OPEN) {
            const payload = JSON.stringify({ type: type, message: message });
            this.ws.send(payload);
        } else {
            console.error("WebSocket is not open. Ready state: " + this.ws.readyState);
        }
    }

    onOpen(event) {
        this.isConnected = true;
        console.log("Connected to WebSocket server");
    }

    onMessage(event) {
        const data = JSON.parse(event.data);
        console.log("Received message: ", data);

        switch (data.type) {
            case "message":
                console.log("Message from server:", data.message);
                addMessageToChatContainer(data.message, false);
                break;
            case "notification":
                alert("Notification from server:", data.message);
                break;
            default:
                console.warn("Unknown message type:", data.type);
                break;
        }
    }

    onClose(event) {
        this.isConnected = false;
        console.log("Disconnected from WebSocket server");
    }

    onError(error) {
        console.error("WebSocket error:", error);
    }
}

client = new NetworkClient("ws://localhost:8000/websocket/ws");

client.connect()

addMessageToChatContainer("Hello, how can I help you?", false);