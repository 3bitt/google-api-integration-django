const radio_buttons = document.querySelectorAll('.date-type-radios');
const year_input = document.getElementById('id_publish_date_0');
const month_input = document.getElementById('id_publish_date_1');
const day_input = document.getElementById('id_publish_date_2');

const date_type = JSON.parse(document.getElementById('datetype_from_template').textContent);

switch (date_type){
    case 'Y':
        day_input.setAttribute('hidden', true);
        month_input.setAttribute('hidden', true);
    case 'Y-m':
        day_input.setAttribute('hidden', true);
}

radio_buttons.forEach(button => button.addEventListener('click', function(e){
    toogle_fields(button)
}));

function toogle_fields(clicked_button){
    if (clicked_button.id == 'day'){
        [year_input, month_input, day_input].forEach(
            input => input.removeAttribute('hidden'));
    } 
    else if (clicked_button.id == 'month') {
        day_input.setAttribute('hidden', true);
        month_input.removeAttribute('hidden');
    }
    else {
        day_input.setAttribute('hidden', true);
        month_input.setAttribute('hidden', true);
    }
}