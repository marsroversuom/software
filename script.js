const socket = new WebSocket('ws://10.20.1.1:8765'); // Replace with your Pi's IP address

socket.onopen = () => {
    console.log("Connected to the WebSocket server.");
};

socket.onclose = (event) => {
    console.log('Connection closed', event);
};

socket.onerror = (error) => {
    console.error('WebSocket error:', error);
};


let keys = {
    'w':false,
    'a':false,
    's':false,
    'd':false,
}

// Keyboard controls (W, A, S, D)
document.addEventListener('keydown', (event) => {
    if (socket.readyState === WebSocket.OPEN) {
        switch (event.key) {
            case 'w':  // Move forward
                keys.w = true
                break;
            case 'a':  // Turn left
                keys.a = true
                break;
            case 's':  // Stop
                keys.s = true
                break;
            case 'd':  // Turn right (optional)
                keys.d = true
                break;
            default:
                break;
        }
        if (keys.w){
            socket.send("1")
        } else {
            socket.send("0")
        }
        // socket.send(JSON.stringify(keys))
    }
});


document.addEventListener('keyup', (event) => {
    if (socket.readyState === WebSocket.OPEN) {
        switch (event.key) {
            case 'w':  // Move forward
                keys.w = false
                break;
            case 'a':  // Turn left
                keys.a = false
                break;
            case 's':  // Stop
                keys.s = false
                break;
            case 'd':  // Turn right (optional)
                keys.d = false
                break;
            default:
                break;
        }
        if (keys.w){
            socket.send("1")
        } else {
            socket.send("0")
        }
        // socket.send(JSON.stringify(keys))
    }
});