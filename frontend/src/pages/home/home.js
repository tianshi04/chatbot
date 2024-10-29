var ws;

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

// ===========================================

function send_new_chat() {
  client.sendMessage("new_chat", 0);
}

function send_message(message) {
  client.sendMessage("message", message);
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