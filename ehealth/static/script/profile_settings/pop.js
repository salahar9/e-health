const show_popup = (button) => {
    let type = button.getAttribute('type')
    let pop_up;
    if (type === "doctor") {
        pop_up = document.querySelector(".popup-holder.doctor")
    } else if (type === "pharmacy") {
        pop_up = document.querySelector(".popup-holder.pharmacy")
        console.log("doooone")
    }
    pop_up.classList.toggle('hide')
} 
console.log(document.querySelectorAll(".popup-holder .card .close-btn span"));

try {
    const all_clsoe_btns = Array.from(document.querySelectorAll(".popup-holder .card .close-btn span"))
    all_clsoe_btns.forEach(close => {
        close.addEventListener("click", () => {
            document.querySelectorAll(".popup-holder")[all_clsoe_btns.indexOf(close)].classList.add("hide")
        })
    })

    document.querySelector("#add-note").addEventListener("click", () => {
        document.querySelector(".popup-holder").classList.remove("hide")
    })



} catch (error) {

}