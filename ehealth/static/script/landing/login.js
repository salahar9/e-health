// Login As
toggle_login_as_menu = (btn, type) => {
    if (type === 'drop-down') {
        btn.querySelector("span").classList.toggle("flip_180")
        document.querySelector("#login-as-menu").classList.toggle("hide")
    } else if (type === 'birthdate') {
        let calendar = document.querySelector(".landing .left main form .calendar.card")
        calendar.classList.toggle('hide')
    }
}

set_login_as_value = (value,d) => {
    document.querySelector(".landing .left main form .row.login-as h3.text-muted").innerHTML = value.innerHTML
    document.querySelector(".landing .left main form .row.login-as h3.text-muted").style.color = "#363949"
    document.querySelector("#login-as-menu").classList.add("hide")
    document.querySelector(".landing .left main form .row.login-as span").classList.toggle("flip_180")
    try {
        document.querySelector("input#login").value = d
    } catch (error) {}
    try {
        document.querySelector("input#sex").value = d
    } catch (error) {}
}


const validateEmail = (mail) => {
    let regex = new RegExp('[a-z0-9]+@[a-z]+\.[a-z]{2,3}');
    return regex.test(mail)
};

next_section = (btn) => {
    const section_2 = document.querySelector(".landing.register .left main form .section:last-child")
    const section_1 = document.querySelector(".landing.register .left main form .section:first-child")
    let can_next = true;
    if (btn === "next") {
        const all_inputs = section_1.querySelectorAll("input")
        console.log(validateEmail(all_inputs[1]));
        for (let i = 0; i < all_inputs.length; i++) {
            if (all_inputs[i].value.length === 0 || all_inputs[2].value != all_inputs[3].value || !validateEmail(all_inputs[1].value)) {
                can_next = false
                section_1.querySelector("#error_label").classList.remove("hide")
                section_1.querySelector("#error_label").style.color = 'red'
                if (all_inputs[i].value.length === 0) {
                    section_1.querySelector("#error_label").innerHTML = "Not all fileds are filled !"
                } else if (!validateEmail(all_inputs[1])) {
                    section_1.querySelector("#error_label").innerHTML = "Invalid email form !"
                } else {
                    section_1.querySelector("#error_label").innerHTML = "Passwords don't match"
                }
                break;
            }
        }
    } else if (btn === "back") {
        section_1.querySelector("#error_label").classList.add("hide")
    }

    if (can_next) {
        section_2.classList.toggle("hide")
        section_1.classList.toggle("hide")
    }
}



