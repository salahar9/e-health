let calendar_childs = document.querySelectorAll(".landing .left main form .calendar.card *")
window.addEventListener("click", e => {
    let calendar = document.querySelector(".landing .left main form .calendar.card")
    
    let calendar_inpt = document.querySelector(".landing.register #login-as-input #birthdate_placeholder")

    if (e.target === calendar_inpt || e.target === calendar || (calendar_childs.includes(e.target))) {
        console.log(e.target);
    } else {        
        calendar.classList.add('hide')
    }
   
})