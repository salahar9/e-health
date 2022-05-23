id=document.getElementById('id').textContent
pid=document.getElementById('person_id').textContent

const chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/notif/chat/'
            + id+"/"
            
        );


fetch_messages = (i) => {
    container=document.querySelector(".conversation-body")
    container.innerHTML=''
    fetch("/chat/fetch/"+i)
    .then(response => response.json())
    .then(data => {

        for(i in data){
            if (data[i].sender_id==pid){
                element=document.createElement("div",{class:"chat-box outgoing"})
            }
            else{
                element=document.createElement("div",{class:"chat-box ingoing"})
   
            }
            element.innerHTML=' <div class="detail"><h3>'+data[i].body+'</h3><small class="text-muted">'+data[i].timestamp+' </small></div>'
            container.appendChild(element)
        }



        }
    )

}

chatSocket.onmessage = () => {

    fetch_messages(id)

}
send = ()=>{
    input=document.getElementById("input-bar")
    data=input.value
    fetch("/chat/sendmsg/", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
        body: JSON.stringify({
                sender: pid,
                to: id,
                message:data
        })})
    .then(response => console.log(response))
    
    //chatSocket.send("message")

}

back_to_recent = (id) => {
    id = id.split("-")[1]
    document.getElementById(`conv-${id}`).classList.add('hide')
    document.querySelector(".recent-messages").classList.remove("hide")
}

show_conv = (id) => {
    id = id.split("-")[1]
    document.querySelectorAll(".conversation.card").forEach(conv => {
        conv.classList.add('hide')
    })
    document.getElementById(`conv-${id}`).classList.remove('hide')
    if (window.innerWidth < 768) {
        document.querySelector(".recent-messages").classList.add("hide")
    }
}
const all_contacts = document.querySelectorAll(".chat-row")
search_bar = (value) => {
    const all_chats = document.querySelector(".recent-messages-body .all-chats")
    all_chats.innerHTML = ''
    all_contacts.forEach(contact => {
        let contact_name = contact.querySelector(".chat-details > h3").innerHTML.toLocaleLowerCase()
        if (contact_name.includes(value.toLocaleLowerCase())) {
            all_chats.appendChild(contact)
        }
    })
}