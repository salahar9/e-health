let first_checkbox = document.querySelector("#insurances thead > tr > th > span.checkbox:first-child")
let all_checkbox = Array.from(document.querySelectorAll("#insurances span.checkbox"))
all_checkbox.shift()
let selected_visites = document.querySelector("form input#selected_visites")
let SELECTED = new Set([])

const remove_value = (list, item) => {
    let index = list.indexOf(item);
    if (index !== -1) {
        list.splice(index, 1);
    }
    return list
}

const get_visite_id = (row) => {
    return row.getAttribute("visite_id")
}

const toggle_active = (row) => {
    if (row.classList.value === 'active')
        row.classList.remove("active")
    else {
        row.classList.add("active")
    }
}

const update_selected = (mode, id) => {
    if (mode === 'add') {
        SELECTED.add(id)
    }else if(mode === 'delete'){
        SELECTED.delete(id)
    }
    selected_visites.value = Array.from(SELECTED).join(',')
}

const toggle_checkbox = (checkbox) => {
    if (checkbox.innerHTML.trim() === "check_box_outline_blank") {
        checkbox.innerHTML = "check_box"
        if (checkbox != first_checkbox) {
            id = get_visite_id(checkbox.parentElement.parentElement)
            update_selected('add', id)
        }
    } else {
        checkbox.innerHTML = "check_box_outline_blank"
        if (checkbox != first_checkbox) {
            id = get_visite_id(checkbox.parentElement.parentElement)
            update_selected('delete', id)

        }
    }
}


const check_all = () => {
    all_checkbox.forEach(row_checkbox => {
        row_checkbox.innerHTML = "check_box"
        row_checkbox.parentElement.parentElement.classList.add("active")
        id = get_visite_id(row_checkbox.parentElement.parentElement)
        update_selected('add', id)

    });
}

const uncheck_all = () => {
    all_checkbox.forEach(row_checkbox => {
        row_checkbox.innerHTML = "check_box_outline_blank"
        row_checkbox.parentElement.parentElement.classList.remove("active")
        id = get_visite_id(row_checkbox.parentElement.parentElement)
        update_selected('delete', id)

    });
}


const toggle_first_check = () => {
    toggle_checkbox(first_checkbox)
    if (first_checkbox.innerHTML.trim() === "check_box_outline_blank") {
        uncheck_all()
    } else {
        check_all()
    }
    console.log(SELECTED);
}




first_checkbox.addEventListener("click", () => {
    toggle_first_check()
})



all_checkbox.forEach(row_checkbox => {
    row_checkbox.addEventListener("click", () => {
        toggle_checkbox(row_checkbox)
        toggle_active(row_checkbox.parentElement.parentElement)
        console.log(SELECTED);
        if (SELECTED.size === all_checkbox.length) {
            toggle_checkbox(first_checkbox)
        } else {
            first_checkbox.innerHTML = "check_box_outline_blank"
        }
    })
})
