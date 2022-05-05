const sideMenu = document.querySelector("aside")
const menuBtn = document.querySelector("#menu-btn")
const closeBtn = document.querySelector("#close-btn")
const themeToggler = document.querySelector("#theme-toggler")


// show sidebar
menuBtn.addEventListener('click', () => {
    sideMenu.style.display = 'block';
})

// close sidebar
closeBtn.addEventListener('click', () => {
    sideMenu.style.display = 'none';
})

// change theme
themeToggler.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme-variables')
    themeToggler.querySelector("span:first-child").classList.toggle('active')
    themeToggler.querySelector("span:last-child").classList.toggle('active')
})

// drop down menu
const dropMenu = (btn) => {
    btn.querySelector("span").classList.toggle("flip_180")

    let dropdown = document.querySelector("ul.drop-down-content")
    dropdown.classList.toggle("show-drop-down")

    
}

const decision=document.getElementsByClassName("decision")
for ( i = 0; i < decision.length; i++) {
    decision[i].addEventListener('click', ()=>
{
    parent=event.currentTarget.parentElement
    dec=event.currentTarget.getAttribute("decision")
    console.log(event.currentTarget)
    if (dec==1){
        parent.getElementsByTagName("input")[1].setAttribute("value",1)
    }
    else{
        parent.getElementsByTagName("input")[1].setAttribute("value",0)
    }
    fetch(parent.action, {method:'post', body: new FormData(parent)});
    parent.innerHTML="DOne"

}

    )
}