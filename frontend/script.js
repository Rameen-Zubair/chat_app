const API_URL = "http://127.0.0.1:8000";  
let socket;

// ✅ Login function with better error handling
async function loginUser() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch(`${API_URL}/api/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        console.log("🔹 Login Response:", response.status, data);

        if (response.ok) {
            localStorage.setItem("token", data.access_token);  // ✅ Store JWT token
            alert("✅ Login successful! Redirecting...");

            // ✅ Redirect to chat page
            window.location.href = "http://127.0.0.1:8000/frontend/chat.html";  // Change "chat.html" to your actual chat page
        } else {
            throw new Error(data.detail || "Login failed");
        }
    } catch (error) {
        alert("❌ Error: " + error.message);
        console.error("❌ Login Error:", error);
    }
}


// ✅ Send message using WebSockets
function sendMessage() {
    const message = document.getElementById("message-input").value;
    if (!message.trim()) return;

    socket.send(message);
    document.getElementById("message-input").value = "";
}

// ✅ Connect WebSocket AFTER selecting a chat room
function connectWebSocket(roomId) {
    if (socket) {
        socket.close();
    }

    socket = new WebSocket(`ws://127.0.0.1:8000/ws/${roomId}`);

    socket.onopen = () => {
        console.log(`✅ WebSocket Connected to Room ${roomId}!`);
    };

    socket.onmessage = (event) => {
        console.log("📩 New Message Received:", event.data);
        document.getElementById("messages").innerHTML += `<p>${event.data}</p>`;
    };

    socket.onerror = (event) => {
        console.error(`❌ WebSocket Error in Room ${roomId}:`, event);
    };

    socket.onclose = () => {
        console.log(`⚠ WebSocket Disconnected from Room ${roomId}!`);
    };
}

// ✅ Load messages for a specific chat room using REST API
async function loadRoomMessages() {
    const token = localStorage.getItem("token");
    const roomId = document.getElementById("room-id-input").value;

    if (!roomId) {
        alert("Please enter a valid room number.");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/chatrooms/${roomId}/messages`, {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (!response.ok) throw new Error("No messages found for this room.");

        const messages = await response.json();
        const messageBox = document.getElementById("messages");
        messageBox.innerHTML = "";

        messages.forEach(msg => {
            const div = document.createElement("div");
            div.textContent = `User ${msg.user_id}: ${msg.content}`;
            messageBox.appendChild(div);
        });

        connectWebSocket(roomId);  // ✅ Connect WebSocket after loading messages
    } catch (error) {
        alert(error.message);
    }
}
