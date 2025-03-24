function refreshChat() {
  fetch('/get_messages')
    .then(response => response.json())
    .then(data => {
      const chatBox = document.getElementById('chat-box');
      chatBox.innerHTML = '';
      data.forEach(msg => {
        // Create a new paragraph for each message
        const p = document.createElement('p');
        p.innerHTML = `<strong>${msg.username}:</strong> ${msg.message} <em>${msg.timestamp}</em>`;
        chatBox.appendChild(p);
      });
    })
    .catch(error => console.error('Error fetching chat messages:', error));
}

// Automatically refresh the chat every 5 seconds
setInterval(refreshChat, 5000);
