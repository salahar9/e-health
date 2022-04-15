let add_med_btn = document.querySelector("#add_btn_med");
let add_trait_btn = document.querySelector("#add_btn_trait");

let med_form = document.querySelector("#med-form");
let trait_form = document.querySelector("#trait-form");

btns = [add_med_btn, add_trait_btn]

let i = 1;


// FUNCTIONS

const change_role = () => {
    document.querySelector(".drop-down-content").classList.toggle("show-drop-down")
}

const remove_row = (id) => {
    let row_id = `#row-${id.split('-')[1]}`
    let row = document.querySelector(row_id)
    row.remove()
}

const new_row = (type, num) => {
    i++;
    let row = document.createElement('div');
    if (type == 1) {
        row.innerHTML = `<div class="row" id=row-${++num}>
        <div class="col-4">
            <label for="exampleInputEmail1">Nom Medicament</label>
            <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter medicament">
        </div>
        <div class="col-2">
            <label for="exampleInputEmail1">Quantite par jour</label>
            <input type="number" class="form-control" id="exampleInputEmail1" value="1">

        </div>
        <div class="col-5">
            <label for="exampleInputEmail1">Description d utilisation</label>
            <textarea class="form-control" id="exampleFormControlTextarea1" rows="1"></textarea>

        </div>
        <div class="col-1 d-flex flex-column justify-content-center">
            <div class="remove-item" id="remove_btn-${num}" onclick="remove_row(this.id)">
                <i class="fa-solid fa-trash-can fa-xl"></i>
            </div>
        </div>
    </div>`

    } else if (type == 2) {
        row.innerHTML = `<div class="row" id="row-${++num}">
        <div class="col-4">
            <label for="exampleInputEmail1">Nom Traitement</label>
            <input type="email" class="form-control" placeholder="Enter traitement">
        </div>
        
        <div class="col-7">
            <label for="exampleInputEmail1">Description du Traitement</label>
            <textarea class="form-control" rows="1"></textarea>
        </div>

        <div class="col-1 d-flex flex-column justify-content-center">
            <div class="remove-item" id="remove_btn-${num}" onclick="remove_row(this.id)">
                <i class="fa-solid fa-trash-can fa-xl"></i>
            </div>
        </div>
    </div> `
    }
    return row
}




// EVENT LISTINERS
btns.forEach(btn => {

    try {
        btn.addEventListener('click', (btn) => {
            let id = btn['target']['id']
            if (id == 'add_btn_med') {
                med_form.appendChild(new_row(1, i))
            } else if (id == 'add_btn_trait') {
                trait_form.appendChild(new_row(2, i))
            }
        })
    } catch (error) {

    }

});


// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.role')) {
        try {
            document.querySelector(".drop-down-content").classList.remove("show-drop-down")
        } catch (error) {

        }
    }
}