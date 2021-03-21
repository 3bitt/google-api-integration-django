const identifier_drop_zone = document.querySelector('.identifiers-drop')
const identifier_row = document.querySelector('.identifiers')
const add_identifier_btn = document.querySelector('.add-new-identifier')
const remove_identifier_btn = document.querySelector('.remove-last-identifier')
const clean_copy = identifier_row.cloneNode(deep = true)

const limit = 5

add_identifier_btn.addEventListener('click', function (e) {
    let current_identifiers_list = document.querySelectorAll('.identifiers')
    if (current_identifiers_list.length < limit - 1) {
        addHTMLnode();
    } else {
        addHTMLnode();
        add_identifier_btn.style.pointerEvents = "none";
    }
    remove_identifier_btn.removeAttribute('hidden')
})

remove_identifier_btn.addEventListener('click', function (e) {
    let current_identifiers_list = document.querySelectorAll('.identifiers')
    if (current_identifiers_list.length > 1) {
        current_identifiers_list[current_identifiers_list.length - 1].remove()
        add_identifier_btn.style.pointerEvents = "all";

        if (current_identifiers_list.length === 2) {
            remove_identifier_btn.setAttribute('hidden', true)
            add_identifier_btn.style.pointerEvents = "all";
        }
    }
    if (current_identifiers_list.length === limit) {
        add_identifier_btn.removeAttribute('hidden')
    }
})

function addHTMLnode() {
    const new_node = clean_copy.cloneNode(deep=true)
    identifier_drop_zone.appendChild(new_node)
}