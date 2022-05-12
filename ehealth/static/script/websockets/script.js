const d=document.getElementById('websocket')
const id  = JSON.parse(document.getElementById('doc_id').textContent);



const chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/notif/'
            + id
            + ':8001/'
        );
chatSocket.onmessage = function(e) {
       
            console.log(e.data + '\n');
        };
