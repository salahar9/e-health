
id  = (document.getElementById('doc_id'));
if (id != null){
    id=JSON.parse(id.textContent)
}
phar_id  = JSON.parse(document.getElementById('phar_id'));
if (phar_id != null){
    phar_id=JSON.parse(phar_id.textContent)
}
close=document.querySelector('.card .close')
if (close !=null){
    close.addEventListener("click",
        ()=>{
            document.getElementById("popup").classList.toggle("hide")
        }
        )
}

const chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/notif/'
            + id+"/"
            
        );
chatSocket.onmessage = function(e) {
            document.getElementById("popup").classList.toggle("hide")
            console.log(e.data + '\n');
            data  = JSON.parse(e.data).message
            document.getElementById("visite-img").src=data.img
            document.getElementById("visite-name").textContent=data.name
            document.getElementById("visite-email").textContent=data.email
            document.getElementById("visite-sexe").textContent=data.sexe
            document.getElementById("visite-nais").textContent=data.nais
            document.getElementById("visite-phone").textContent=data.phone
            document.getElementById("visite-username").textContent=data.username
            document.getElementById("visite-adress").textContent=data.adress
            document.getElementById("visite-ville").textContent=data.ville
            document.getElementById("visite-visite").href=data.visite
            document.getElementById("visite-profile").href=data.profile



            
        };
